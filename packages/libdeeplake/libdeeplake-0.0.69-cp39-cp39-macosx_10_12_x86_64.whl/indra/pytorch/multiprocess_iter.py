from itertools import repeat
from typing import Callable, List, Optional
from indra.pytorch.buffered_loader import BufferedLoader
from indra.pytorch.util import (
    process_initializer,
    transform_collate_batch,
)
from indra.pytorch.common import collate_fn as default_collate
from deeplake.integrations.pytorch.common import convert_sample_to_data
from deeplake.core.serialize import bytes_to_text
from multiprocessing import Pool, Manager, Queue
import warnings
import os
from PIL import Image
import dill as pickle
import io


class StopChildProcess:
    pass


class MultiprocessIterator:
    def __init__(
        self,
        dataloader,
        htype_dict: Optional[dict] = None,
        ndim_dict: Optional[dict] = None,
        tensor_info_dict: Optional[dict] = None,
        pil_compressed_tensors: Optional[List[str]] = None,
        raw_tensors: Optional[List[str]] = None,
        json_tensors: Optional[List[str]] = None,
        list_tensors: Optional[List[str]] = None,
        upcast: bool = True,
        prefetch_factor: int = 10,
        transform_fn: Optional[Callable] = None,
        collate_fn: Optional[Callable] = default_collate,
        worker_init_fn: Optional[Callable] = None,
        num_workers: int = 0,
        persistent_workers: bool = False,
    ):
        self.dataloader = dataloader
        self.htype_dict = htype_dict
        self.ndim_dict = ndim_dict
        self.tensor_info_dict = tensor_info_dict
        self.pil_compressed_tensors = pil_compressed_tensors
        self.raw_tensors = raw_tensors
        self.prefetch_factor = prefetch_factor
        self.json_tensors = json_tensors
        self.list_tensors = list_tensors
        self.upcast = upcast
        self.transform_fn = transform_fn
        self.collate_fn = collate_fn
        self.worker_init_fn = worker_init_fn or None
        self.num_workers = num_workers
        self.persistent_workers = persistent_workers or False
        self.num_prefetch_tasks = self.prefetch_factor * self.num_workers
        self.length = len(dataloader)
        self.current_pos = 0
        self.iter_pos = 0
        self.workers_initialised = False

        self.pool = None
        self.manager = None

        import atexit

        atexit.register(MultiprocessIterator._clean_up_worker, self)

    def __iter__(self):
        if self.current_pos != 0:
            if isinstance(self.dataloader, BufferedLoader):
                self.dataloader.dataloader().reset()
            else:
                self.dataloader.reset()

        if self.persistent_workers and self.pool is not None:
            self.clear_queues()

        self.current_pos = 0
        self.iter_pos = 0
        self.iter_dl = iter(self.dataloader)
        if self.pool is not None:
            if not self.persistent_workers:
                self.close()
                self.start_processes()
            self.run_workers()
            self.fill_prefetch_jobs()

        return self

    def clear_queues(self):
        for item in self.data_in_queues:
            while not item.empty():
                item.get_nowait()

        for item in self.data_out_queues:
            while not item.empty():
                item.get_nowait()

    def fetch_next_job(self):
        try:
            wid = self.current_pos % self.num_workers
            batch = next(self.iter_dl)

            if self.pil_compressed_tensors:
                all_bts, batch = combine_compressed_bytes(
                    batch,
                    self.pil_compressed_tensors,
                    self.json_tensors,
                    self.list_tensors,
                )
            else:
                all_bts = None
            batch = (all_bts, batch)
            self.data_in_queues[wid].put(batch)
            self.current_pos += 1
        except:
            for j in range(self.num_workers):
                self.data_in_queues[j].put(StopIteration())

    def fill_prefetch_jobs(self):
        while self.current_pos <= self.num_prefetch_tasks:
            self.fetch_next_job()

    def __next__(self):
        if self.pool is None:
            self.start_processes()
            self.run_workers()
            self.fill_prefetch_jobs()
        elif (
            self.pool is not None
            and self.persistent_workers
            and not self.workers_initialised
        ):
            self.run_workers()
            self.fill_prefetch_jobs()
        return self.get_data()

    def start_processes(self):
        if self.pool is not None:
            return
        child_env = os.environ.copy()

        # This code is referred from https://github.com/pytorch/pytorch/blob/master/torch/distributed/run.py
        if self.num_workers >= 1 and "OMP_NUM_THREADS" not in os.environ:
            omp_num_threads = 1
            warnings.warn(
                f"Setting OMP_NUM_THREADS environment variable for each process "
                f"to be {omp_num_threads} in default, to avoid your system being "
                f"overloaded, please further tune the variable for optimal "
                f"performance in your application as needed."
            )
            child_env["OMP_NUM_THREADS"] = str(omp_num_threads)
            os.environ["OMP_NUM_THREADS"] = str(omp_num_threads)

        if self.num_workers >= 1 and "MKL_NUM_THREADS" not in os.environ:
            mkl_num_threads = 1
            warnings.warn(
                f"Setting MKL_NUM_THREADS environment variable for each process "
                f"to be {mkl_num_threads} in default, to avoid your system being "
                f"overloaded, please further tune the variable for optimal "
                f"performance in your application as needed."
            )

            child_env["MKL_NUM_THREADS"] = str(mkl_num_threads)
            os.environ["MKL_NUM_THREADS"] = str(mkl_num_threads)

        id_queue = Queue(maxsize=self.num_workers)
        for i in range(self.num_workers):
            id_queue.put(i)

        self.pool = Pool(
            processes=self.num_workers,
            initializer=process_initializer,
            initargs=(child_env, self.worker_init_fn, id_queue),
        )

        if self.manager is None:
            self.manager = Manager()

        self.data_in_queues = [self.manager.Queue() for _ in range(self.num_workers)]
        self.data_out_queues = [self.manager.Queue() for _ in range(self.num_workers)]

    def run_workers(self):
        transform_fn = (
            None if self.transform_fn is None else pickle.dumps(self.transform_fn)
        )
        collate_fn = None if self.collate_fn is None else pickle.dumps(self.collate_fn)
        inp = list(
            zip(
                self.data_in_queues,
                self.data_out_queues,
                repeat(transform_fn),
                repeat(collate_fn),
                repeat(self.upcast),
                repeat(self.pil_compressed_tensors),
                repeat(self.json_tensors),
                repeat(self.list_tensors),
                repeat(self.raw_tensors),
                repeat(self.htype_dict),
                repeat(self.ndim_dict),
                repeat(self.tensor_info_dict),
            )
        )
        self.workers_initialised = True
        self.pool.map_async(early_transform_collate, inp)

    def get_data(self):
        out = None

        wid = self.iter_pos % self.num_workers
        if self.current_pos >= self.num_prefetch_tasks:
            out = self.data_out_queues[wid].get()
            if isinstance(out, StopIteration):
                # get StopIteration from other workers too, to empty the queues
                for j in range(self.num_workers):
                    if j != wid:
                        self.data_out_queues[j].get()
                if not self.persistent_workers:
                    self.close()
                self.workers_initialised = False
                raise StopIteration
            if isinstance(out, Exception):
                raise out
        if self.current_pos < self.length:
            self.fetch_next_job()
        elif self.current_pos == self.length:
            try:
                batch = next(self.iter_dl)
            except StopIteration:
                # send StopIteration (stop signal) to all workers
                for j in range(self.num_workers):
                    self.data_in_queues[j].put(StopIteration())
        self.iter_pos += 1
        return out

    def close(self):
        if self.pool is not None:
            self.pool.close()
            self.pool.join()
            self.pool = None

    def free_resources(self):
        if self.pool is not None:
            for idx in range(self.num_workers):
                self.data_in_queues[idx].put(StopChildProcess())
        self.close()
        if self.manager is not None:
            self.manager.shutdown()
            self.manager = None

    def __del__(self):
        self.free_resources()

    @staticmethod
    def _clean_up_worker(obj):
        obj.free_resources()


def early_transform_collate(inp):
    (
        data_in_queue,
        data_out_queue,
        transform_fn,
        collate_fn,
        upcast,
        pil_compressed_tensors,
        json_tensors,
        list_tensors,
        raw_tensors,
        htype_dict,
        ndim_dict,
        tensor_info_dict,
    ) = inp
    raw_tensor_set = set(raw_tensors) - set(json_tensors) - set(list_tensors)
    transform_fn = None if transform_fn is None else pickle.loads(transform_fn)
    collate_fn = None if collate_fn is None else pickle.loads(collate_fn)
    while 1:
        try:
            batch = data_in_queue.get()
            if isinstance(batch, StopIteration):
                data_out_queue.put(batch)
                break
            elif isinstance(batch, StopChildProcess):
                break
            else:
                if batch is None:
                    data_out_queue.put(None)
                    continue
                all_bts, batch = batch
                if all_bts is not None:
                    batch = bytes_to_batch(
                        batch,
                        pil_compressed_tensors,
                        json_tensors,
                        list_tensors,
                        all_bts,
                    )
                if htype_dict:
                    for sample in batch:
                        convert_sample_to_data(
                            sample, htype_dict, ndim_dict, tensor_info_dict
                        )
                out = transform_collate_batch(
                    batch, transform_fn, collate_fn, upcast, raw_tensor_set
                )
                data_out_queue.put(out)
        except Exception as e:
            data_out_queue.put(e)
            break


def combine_compressed_bytes(batch, pil_compressed_tensors, json_tensors, list_tensors):
    all_byte_tensors = set(pil_compressed_tensors + json_tensors + list_tensors)
    sb, eb, all_bts = 0, 0, []
    for sample in batch:
        for tensor in all_byte_tensors:
            if isinstance(sample[tensor], bytes):
                sample_bts = sample.pop(tensor)
                all_bts.append(sample_bts)
                eb += len(sample_bts)
                sample[tensor] = (sb, eb)
                sb = eb
            elif isinstance(sample[tensor], list):
                sb_eb_list = []
                for item in sample[tensor]:
                    sample_bts = item
                    all_bts.append(sample_bts)
                    eb += len(sample_bts)
                    sb_eb_list.append((sb, eb))
                    sb = eb
                sample[tensor] = sb_eb_list

    # combine all_bts into one bytearray
    all_bts = bytearray(b"".join(all_bts))
    return all_bts, batch


def bytes_to_batch(batch, pil_compressed_tensors, json_tensors, list_tensors, all_bts):
    data_bytes = memoryview(all_bts)
    all_byte_tensors = set(pil_compressed_tensors + json_tensors + list_tensors)
    pil_compressed_tensors = set(pil_compressed_tensors)
    json_tensors = set(json_tensors)
    list_tensors = set(list_tensors)
    for sample in batch:
        for tensor in all_byte_tensors:
            if tensor in pil_compressed_tensors:
                decompress_fn = lambda x: Image.open(io.BytesIO(x))
            elif tensor in json_tensors:
                decompress_fn = lambda x: bytes_to_text(x, "json")
            elif tensor in list_tensors:
                decompress_fn = lambda x: bytes_to_text(x, "list")

            if isinstance(sample[tensor], tuple):
                sb, eb = sample[tensor]
                sample[tensor] = decompress_fn(data_bytes[sb:eb])
            elif isinstance(sample[tensor], list):
                sb_eb_list = sample[tensor]
                sample[tensor] = [
                    decompress_fn(data_bytes[sb:eb]) for sb, eb in sb_eb_list
                ]
            else:
                # will only happen for Image tensors that are tiled
                sample[tensor] = Image.fromarray(sample[tensor])
    return batch
