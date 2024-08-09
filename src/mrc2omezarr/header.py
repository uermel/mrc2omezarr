from typing import List, Tuple

import numpy as np
from pydantic import BaseModel


class CellA(BaseModel):
    x: float
    y: float
    z: float

    @classmethod
    def from_header(cls, header: np.recarray):
        return cls(**{n: header[n] for n in header.dtype.names})


class CellB(BaseModel):
    alpha: float
    beta: float
    gamma: float

    @classmethod
    def from_header(cls, header: np.recarray):
        return cls(**{n: header[n] for n in header.dtype.names})


class Origin(BaseModel):
    x: float
    y: float
    z: float

    @classmethod
    def from_header(cls, header: np.recarray):
        return cls(**{n: header[n] for n in header.dtype.names})


class MrcHeader(BaseModel):
    nx: int
    ny: int
    nz: int

    mode: int

    nxstart: int
    nystart: int
    nzstart: int

    mx: int
    my: int
    mz: int

    cella: CellA
    cellb: CellB

    mapc: int
    mapr: int
    maps: int

    dmin: float
    dmax: float
    dmean: float

    ispg: int
    nsymbt: int

    extra1: str
    exttyp: str
    nversion: int
    extra2: str

    origin: Origin

    map: str
    machst: str

    rms: float

    nlabl: int
    label: List[str]

    @classmethod
    def from_header(cls, header: np.recarray):
        header_dict = {n: header[n] for n in header.dtype.names}

        header_dict["cella"] = CellA.from_header(header["cella"])
        header_dict["cellb"] = CellB.from_header(header["cellb"])

        header_dict["extra1"] = str(header_dict["extra1"].tobytes())
        header_dict["exttyp"] = header["exttyp"].tobytes().decode()
        header_dict["extra2"] = str(header_dict["extra2"].tobytes())

        header_dict["origin"] = Origin.from_header(header["origin"])

        header_dict["map"] = header["map"].tobytes().decode()
        header_dict["machst"] = str(header["machst"].tobytes())
        header_dict["label"] = [lab.decode() for lab in header["label"]]

        return cls(**header_dict)

    @property
    def voxel_size(self) -> Tuple[float, float, float]:
        x = self.cella.x / self.mx
        y = self.cella.y / self.my
        z = self.cella.z / self.mz
        return x, y, z

    @property
    def is_image_stack(self) -> bool:
        return self.nz == 1
