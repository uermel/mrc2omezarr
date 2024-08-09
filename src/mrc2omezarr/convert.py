from typing import Dict, List, Literal, Optional, Tuple, Union

import numpy as np
from pydantic_ome_ngff.v04 import Axis
from pydantic_ome_ngff.v04.multiscale import Dataset, MultiscaleMetadata
from pydantic_ome_ngff.v04.transform import VectorScale
from skimage.transform import downscale_local_mean, rescale

from mrc2omezarr.header import MrcHeader


def convert(
    data: np.ndarray,
    header: MrcHeader,
    scale_factors: List[Dict[str, int]],
    voxel_size: Optional[Union[float, Tuple[float, float, float]]] = None,
    pyramid_method: Union[Literal["local_mean"], Literal["downsample"]] = "local_mean",
):
    if voxel_size is None:
        voxel_size = header.voxel_size

    if isinstance(voxel_size, float):
        voxel_size = (voxel_size, voxel_size, voxel_size)

    data_pyramid = []
    meta = []

    for idx, sf in enumerate(scale_factors):
        scale = VectorScale(scale=[sf["z"] * voxel_size[0], sf["y"] * voxel_size[1], sf["x"] * voxel_size[2]])
        ms = Dataset(path=f"{idx}", coordinateTransformations=[scale])
        meta.append(ms)
        if pyramid_method == "local_mean":
            data_pyramid.append(downscale_local_mean(data, (sf["z"], sf["y"], sf["x"])))
        elif pyramid_method == "downsample":
            data_pyramid.append(
                rescale(
                    data,
                    (1 / sf["z"], 1 / sf["y"], 1 / sf["x"]),
                    anti_aliasing=False,
                    preserve_range=True,
                    order=0,
                ),
            )

    meta_pyramid = MultiscaleMetadata(
        name="/",
        axes=[
            Axis(name="z", type="space", unit="angstrom"),
            Axis(name="y", type="space", unit="angstrom"),
            Axis(name="x", type="space", unit="angstrom"),
        ],
        metadata={"source_mrc_header": header.model_dump()},
        datasets=tuple(meta),
    )

    return data_pyramid, meta_pyramid


def convert_array(
    data: np.ndarray,
    scale_factors: Tuple[int],
    voxel_size: Union[float, Tuple[float, float, float]],
    pyramid_method: Union[Literal["local_mean"], Literal["downsample"]] = "local_mean",
    is_image_stack: bool = False,
):
    scale_maps = []
    for sf in scale_factors:
        scale_maps.append(
            {
                "x": sf,
                "y": sf,
                "z": 1 if is_image_stack else sf,
            },
        )

    scale_factors = scale_maps

    if isinstance(voxel_size, float):
        voxel_size = (voxel_size, voxel_size, voxel_size)

    data_pyramid = []
    meta = []

    for idx, sf in enumerate(scale_factors):
        scale = VectorScale(scale=[sf["z"] * voxel_size[0], sf["y"] * voxel_size[1], sf["x"] * voxel_size[2]])
        ms = Dataset(path=f"{idx}", coordinateTransformations=[scale])
        meta.append(ms)
        if pyramid_method == "local_mean":
            data_pyramid.append(downscale_local_mean(data, (sf["z"], sf["y"], sf["x"])))
        elif pyramid_method == "downsample":
            data_pyramid.append(
                rescale(
                    data,
                    (1 / sf["z"], 1 / sf["y"], 1 / sf["x"]),
                    anti_aliasing=False,
                    preserve_range=True,
                    order=0,
                ),
            )

    meta_pyramid = MultiscaleMetadata(
        name="/",
        axes=[
            Axis(name="z", type="space", unit="angstrom"),
            Axis(name="y", type="space", unit="angstrom"),
            Axis(name="x", type="space", unit="angstrom"),
        ],
        datasets=tuple(meta),
        metadata={},
    )

    return data_pyramid, meta_pyramid
