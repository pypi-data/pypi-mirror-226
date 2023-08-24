from typing import Callable, List, Optional
from indra.pytorch.buffered_loader import BufferedLoader
from indra.pytorch.util import (
    transform_collate_batch,
)

from indra.pytorch.common import collate_fn as default_collate
from deeplake.integrations.pytorch.common import convert_sample_to_data
from deeplake.core.serialize import bytes_to_text

from PIL import Image, ImageFile

import io


class ZeroWorkerIterator:
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
        transform_fn: Optional[Callable] = None,
        collate_fn: Optional[Callable] = default_collate,
    ):
        self.dataloader = dataloader
        self.htype_dict = htype_dict
        self.ndim_dict = ndim_dict
        self.tensor_info_dict = tensor_info_dict
        self.pil_compressed_tensors = pil_compressed_tensors
        self.raw_tensors = raw_tensors
        self.json_tensors = json_tensors
        self.list_tensors = list_tensors
        self.upcast = upcast
        self.transform_fn = transform_fn
        self.collate_fn = collate_fn
        self.current_pos = None
        self.raw_tensor_set = (
            set(self.raw_tensors) - set(self.json_tensors) - set(self.list_tensors)
        )  # tensors to be returned as bytes

    def __iter__(self):
        if isinstance(self.dataloader, BufferedLoader):
            self.dataloader.dataloader().reset()
        else:
            self.dataloader.reset()

        self.current_pos = iter(self.dataloader)
        return self

    def __next__(self):
        return self.get_data()

    # TODO add all exception types which are not the StopIteration handling
    def get_data(self):
        batch = next(self.current_pos)
        for sample in batch:
            for tensor in self.pil_compressed_tensors:
                if isinstance(sample[tensor], (list, tuple)):
                    sample[tensor] = list(
                        Image.open(io.BytesIO(t)) for t in sample[tensor]
                    )
                else:
                    sample[tensor] = Image.open(io.BytesIO(sample[tensor]))
            for tensor in self.json_tensors:
                sample[tensor] = bytes_to_text(sample[tensor], "json")
            for tensor in self.list_tensors:
                sample[tensor] = bytes_to_text(sample[tensor], "list")
            if self.htype_dict:
                convert_sample_to_data(
                    sample, self.htype_dict, self.ndim_dict, self.tensor_info_dict
                )
        return transform_collate_batch(
            batch, self.transform_fn, self.collate_fn, self.upcast, self.raw_tensor_set
        )

    def close(self):
        pass
