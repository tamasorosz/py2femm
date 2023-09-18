from dataclasses import dataclass
from enum import Enum


# Enums
class LamType(Enum):
    NOT_LAMINATED = 0
    LAMINATED_X_OR_R = 1
    LAMINATED_Y_OR_Z = 2
    MAGNET_WIRE = 3
    PLAIN_STRANDED_WIRE = 4
    LITZ_WIRE = 5
    SQUARE_WIRE = 6


@dataclass
class MagneticMaterial:
    material_name: str
    mu_x: float
    mu_y: float
    H_c: float
    J: float
    Cduct: float
    Lam_d: float
    Phi_hmax: float
    lam_fill: float
    LamType: LamType
    Phi_hx: float
    Phi_hy: float
    NStrands: int
    WireD: float


# Magnetic Boundary Conditions
@dataclass
class MagneticDirichlet:
    name: str
    a_0: float
    a_1: float
    a_2: float
    phi: float


@dataclass
class MagneticMixed:
    name: str
    c0: float
    c1: float


@dataclass
class MagneticAnti:
    name: str


@dataclass
class MagneticPeriodic:
    name: str


@dataclass
class MagneticAntiPeriodicAirgap:
    name: str
    angle: float


@dataclass
class MagneticPeriodicAirgap:
    name: str
    angle: float
