from typing import List, Tuple

import fsspec
import numpy as np
import ome_zarr.writer
import zarr
from pydantic_ome_ngff.v04 import MultiscaleMetadata

from mrc2omezarr.util import get_protocol


class Writer:
    def __init__(self, data: List[np.ndarray], meta: MultiscaleMetadata) -> None:
        self.data = data
        self.meta = meta

    def write(
        self,
        output_path: str,
        overwrite: bool = True,
        chunks: Tuple[int, int, int] = (256, 256, 256),
        **kwargs,
    ) -> None:
        protocol, path = get_protocol(output_path)

        if protocol in ["file", "local"]:
            am = kwargs.get("auto_mkdir", True)
            kwargs["auto_mkdir"] = am

        fs = fsspec.filesystem(protocol, **kwargs)

        loc = zarr.storage.FSStore(path, key_separator="/", mode="w", dimension_separator="/", fs=fs)
        root_group = zarr.group(loc, overwrite=overwrite)

        ome_zarr.writer.write_multiscale(
            self.data,
            group=root_group,
            axes=[a.model_dump() for a in self.meta.axes],
            coordinate_transformations=[
                list(mds.model_dump()["coordinateTransformations"]) for mds in self.meta.datasets
            ],
            storage_options=dict(chunks=chunks, overwrite=overwrite),
            compute=True,
            metadata=self.meta.metadata,
        )
