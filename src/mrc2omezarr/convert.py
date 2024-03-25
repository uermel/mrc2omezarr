from typing import Dict, List, Optional, Tuple, Union

import numpy as np
from pydantic_ome_ngff.v04 import Axis, Multiscale
from pydantic_ome_ngff.v04.coordinateTransformations import VectorScaleTransform
from pydantic_ome_ngff.v04.multiscales import MultiscaleDataset
from skimage.transform import downscale_local_mean

from mrc2omezarr.header import MrcHeader


def convert(
    data: np.ndarray,
    header: MrcHeader,
    scale_factors: List[Dict[str, int]],
    voxel_size: Optional[Union[float, Tuple[float, float, float]]] = None,
):
    meta_pyramid = Multiscale(
        name="/",
        axes=[
            Axis(name="z", type="space", unit="angstrom"),
            Axis(name="y", type="space", unit="angstrom"),
            Axis(name="x", type="space", unit="angstrom"),
        ],
        datasets=[],
        metadata={"source_mrc_header": header.dict()},
    )

    if voxel_size is None:
        voxel_size = header.voxel_size

    if isinstance(voxel_size, float):
        voxel_size = (voxel_size, voxel_size, voxel_size)

    data_pyramid = []

    for idx, sf in enumerate(scale_factors):
        scale = VectorScaleTransform(scale=[sf["z"] * voxel_size[0], sf["y"] * voxel_size[1], sf["x"] * voxel_size[2]])
        ms = MultiscaleDataset(path=f"{idx}", coordinateTransformations=[scale])
        meta_pyramid.datasets.append(ms)
        data_pyramid.append(downscale_local_mean(data, (sf["z"], sf["y"], sf["x"])))

    return data_pyramid, meta_pyramid
