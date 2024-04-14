# mrc2omezarr

Command line tool for conversion from MRC to multiscale OME-Zarr format.

Default settings produce Zarr-files similar to those on the CZI cryoET data portal:

- Files contain one image
- Scales: 1x, 2x, 4x (original resolution)
- Scale transformations transform to angstrom coordinates
- Chunk size: 256, 256, 256

The original MRC-header is retained as a dictionary in the root .zattrs file.

Input as well as output can be local or remote. For remote files include the protocol in the filename, e.g. `s3://bucket/path/to/file.mrc`.

## Install

```bash
git clone https://github.com/uermel/mrc2omezarr.git
cd mrc2omezarr
pip install .
```

## Usage

```bash
Usage: mrc2omezarr [OPTIONS]

Options:
  --mrc-path TEXT                 Path to the MRC file. Include the protocol
                                  if necessary. (e.g. s3://)  [required]
  --zarr-path TEXT                Path to the output Zarr file. Include the
                                  protocol if necessary. (e.g. s3://)
                                  [required]
  --permissive / --no-permissive  Whether to read the MRC file in permissive
                                  mode.  [default: no-permissive]
  --overwrite / --no-overwrite    Whether to overwrite the output Zarr file.
                                  [default: overwrite]
  --scale-factors TEXT            Scale factors for multiscale pyramid. Comma-
                                  separated list of integers.  [default:
                                  1,2,4]
  --voxel-size TEXT               Voxel size in Angstroms. Comma-separated
                                  list of floats or single float. If not
                                  provided, it will be read from the MRC
                                  header.
  --is-image-stack / --no-is-image-stack
                                  Whether the data is an image stack
                                  (determined from MRC-header by default).
  --chunk-size INTEGER            Chunk size for the Zarr file.  [default:
                                  256]
  --filesystem-args TEXT          Path to a JSON file containing additional
                                  arguments to pass to the fsspec-filesystem.
  --help                          Show this message and exit.

```
