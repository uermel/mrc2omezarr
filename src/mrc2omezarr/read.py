from typing import Tuple

import fsspec
import numpy as np
from mrcfile.mrcinterpreter import MrcInterpreter

from mrc2omezarr.header import MrcHeader
from mrc2omezarr.util import get_protocol


class Reader:
    def __init__(self, path: str, **kwargs):
        self.protocol, self.path = get_protocol(path)

        if "auto_mkdir" in kwargs:
            self.fs = fsspec.filesystem(self.protocol, **kwargs)
        else:
            self.fs = fsspec.filesystem(self.protocol, auto_mkdir=True, **kwargs)

    def read(self, permissive: bool = False) -> Tuple[np.ndarray, MrcHeader]:
        with self.fs.open(self.path, "rb") as f:
            mrc = MrcInterpreter(f, permissive=permissive)
            return mrc.data, MrcHeader.from_header(mrc.header)
