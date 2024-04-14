from typing import Any, Dict, Literal, Optional, Tuple, Union

from mrc2omezarr.convert import convert
from mrc2omezarr.read import Reader
from mrc2omezarr.write import Writer


def convert_mrc_to_ngff(
    mrc_path: str,
    zarr_path: str,
    permissive: bool = False,
    overwrite: bool = True,
    scale_factors: Tuple[int, ...] = (1, 2, 4),
    voxel_size: Optional[Union[float, Tuple[float, float, float]]] = None,
    is_image_stack: Optional[bool] = None,
    chunk_size: Optional[Tuple[int, int, int]] = (256, 256, 256),
    filesystem_args: Optional[Dict[str, Any]] = None,
    pyramid_method: Union[Literal["local_mean"], Literal["downsample"]] = "local_mean",
) -> None:
    if filesystem_args is None:
        filesystem_args = {}

    reader = Reader(mrc_path)
    data, header = reader.read(permissive=permissive)

    if voxel_size is None:
        voxel_size = header.voxel_size

    if isinstance(voxel_size, float):
        voxel_size = (voxel_size, voxel_size, voxel_size)

    if is_image_stack is None:
        is_image_stack = header.is_image_stack

    # If the data is an image stack, we don't want to scale the z-axis
    # TODO: Image stacks should be saved as image stacks in the first place, not using this workaround
    scale_maps = []
    for sf in scale_factors:
        scale_maps.append(
            {
                "x": sf,
                "y": sf,
                "z": 1 if is_image_stack else sf,
            },
        )

    data_pyramid, meta_pyramid = convert(data, header, scale_maps, voxel_size=voxel_size, pyramid_method=pyramid_method)

    writer = Writer(data_pyramid, meta_pyramid)
    writer.write(zarr_path, overwrite=overwrite, chunks=chunk_size, **filesystem_args)
