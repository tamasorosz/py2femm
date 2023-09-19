from dataclasses import dataclass
from enum import Enum
from string import Template

from src.general import Material


# Enums
class LamType(Enum):
    NOT_LAMINATED = 0
    LAMINATED_X_OR_R = 1
    LAMINATED_Y_OR_Z = 2
    MAGNET_WIRE = 3
    PLAIN_STRANDED_WIRE = 4
    LITZ_WIRE = 5
    SQUARE_WIRE = 6


@dataclass(kw_only=True)
class MagneticMaterial(Material):
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

    def __str__(self):
        cmd = Template(
            "mi_addmaterial($materialname, $mux, $muy, $Hc, $J, $Cduct, $Lamd, $Phi_hmax, $lamfill, "
            "$LamType, $Phi_hx, $Phi_hy, $NStrands, $WireD)"
        )

        cmd = cmd.substitute(
            materialname=f"'{self.material_name}'",
            mux=self.mu_x,
            muy=self.mu_y,
            Hc=self.H_c,
            J=self.J,
            Cduct=self.Cduct,
            Lamd=self.Lam_d,
            Phi_hmax=self.Phi_hmax,
            lamfill=self.lam_fill,
            LamType=self.LamType,
            Phi_hx=self.Phi_hx,
            Phi_hy=self.Phi_hy,
            NStrands=self.NStrands,
            WireD=self.WireD,
        )
        return cmd


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
