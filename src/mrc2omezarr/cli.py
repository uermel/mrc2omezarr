from typing import Tuple

import click

from mrc2omezarr.proc import convert_mrc_to_ngff
from mrc2omezarr.util import get_filesystem_args


@click.command(context_settings={"show_default": True})
@click.option(
    "--mrc-path",
    type=str,
    required=True,
    help="Path to the MRC file. Include the protocol if necessary. (e.g. s3://)",
)
@click.option(
    "--zarr-path",
    type=str,
    required=True,
    help="Path to the output Zarr file. Include the protocol if necessary. (e.g. s3://)",
)
@click.option(
    "--permissive/--no-permissive",
    default=False,
    help="Whether to read the MRC file in permissive mode.",
)
@click.option(
    "--overwrite/--no-overwrite",
    default=True,
    help="Whether to overwrite the output Zarr file.",
)
@click.option(
    "--scale-factors",
    type=str,
    default="1,2,4",
    help="Scale factors for multiscale pyramid. Comma-separated list of integers.",
)
@click.option(
    "--voxel-size",
    type=str,
    default=None,
    help="""Voxel size in Angstroms. Comma-separated list of floats or single float. """
    """If not provided, it will be read from the MRC header.""",
)
@click.option(
    "--is-image-stack/--no-is-image-stack",
    default=None,
    help="Whether the data is an image stack (determined from MRC-header by default).",
)
@click.option(
    "--chunk-size",
    type=int,
    default=256,
    help="Chunk size for the Zarr file.",
)
@click.option(
    "--filesystem-args",
    type=str,
    default=None,
    help="Path to a JSON file containing additional arguments to pass to the fsspec-filesystem.",
)
@click.option(
    "--pyramid-method",
    type=str,
    default="local_mean",
    help="Method to downscale the data. Options: local_mean, downsample.",
)
@click.pass_context
def convert(
    ctx,
    mrc_path,
    zarr_path,
    permissive,
    overwrite,
    scale_factors,
    voxel_size,
    is_image_stack,
    chunk_size,
    filesystem_args,
    pyramid_method,
):
    scale_factors: Tuple[int, ...] = tuple([int(x) for x in scale_factors.split(",")])

    if voxel_size is not None:
        voxel_size = [int(x) for x in voxel_size.split(",")]

    if filesystem_args is not None:
        filesystem_args = get_filesystem_args(filesystem_args)

    convert_mrc_to_ngff(
        mrc_path,
        zarr_path,
        permissive,
        overwrite,
        scale_factors,
        voxel_size,
        is_image_stack,
        (chunk_size, chunk_size, chunk_size),
        filesystem_args,
        pyramid_method,
    )


if __name__ == "__main__":
    convert()
