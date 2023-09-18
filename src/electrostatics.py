from dataclasses import dataclass


@dataclass
class ElectrostaticMaterial:
    material_name: str
    ex: float  # Relative permittivity in the x- or r-direction.
    ey: float  # Relative permittivity in the y- or z-direction.
    qv: float  # Volume charge density in units of C / m3


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
