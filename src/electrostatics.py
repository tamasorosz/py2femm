from abc import ABC
from dataclasses import dataclass
from string import Template

from src.general import Material, Boundary


@dataclass(kw_only=True)
class ElectrostaticMaterial(Material):
    ex: float  # Relative permittivity in the x- or r-direction.
    ey: float  # Relative permittivity in the y- or z-direction.
    qv: float  # Volume charge density in units of C / m3

    def __str__(self):
        cmd = Template("ei_addmaterial($materialname, $ex, $ey, $qv)")
        cmd = cmd.substitute(
            materialname=f'"{self.material_name}"',
            ex=self.ex,
            ey=self.ey,
            qv=self.qv,
        )
        return cmd


@dataclass(kw_only=True)
class ElectrostaticBoundaryBase(Boundary):
    Vs: float = 0.0
    c0: float = 0.0
    c1: float = 0.0
    qs: float = 0.0

    def __str__(self):
        return f'ei_addboundprop("{self.name}", {self.Vs}, {self.qs}, {self.c0}, {self.c1}, {self.type})'


class ElectrostaticFixedVoltage(ElectrostaticBoundaryBase):

    def __init__(self, name: str, Vs: float):
        self.name = name
        self.Vs = Vs
        self.type = 0


class ElectrostaticMixed(ElectrostaticBoundaryBase):

    def __init__(self, name: str, c0: float, c1: float):
        self.name = name
        self.c0 = c0
        self.c1 = c1
        self.type = 1


class ElectrostaticSurfaceCharge(ElectrostaticBoundaryBase):
    def __init__(self, name: str, qs: float):
        self.name = name
        self.q = qs
        self.type = 2


@dataclass
class ElectrostaticPeriodic(ElectrostaticBoundaryBase):
    def __init__(self, name: str):
        self.name = name
        self.type = 3

@dataclass
class ElectrostaticAntiPeriodic(ElectrostaticBoundaryBase):
    def __init__(self, name: str):
        self.name = name
        self.type = 4
