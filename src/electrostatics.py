from dataclasses import dataclass
from string import Template

from src.general import Material


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

# Electrostatic Boundary Conditions
@dataclass
class ElectrostaticFixedVoltage:
    name: str
    Vs: float


@dataclass
class ElectrostaticMixed:
    name: str
    c0: float
    c1: float


@dataclass
class ElectrostaticSurfaceCharge:
    name: str
    qs: float


@dataclass
class ElectrostaticPeriodic:
    name: str


@dataclass
class ElectrostaticAntiPeriodic:
    name: str
