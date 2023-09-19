from abc import ABC
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


@dataclass
class MagneticBoundaryBaseClass(ABC):
    name: str
    boundary_format: int  # this is an identifier for the applied boundary
    A0: float = 0
    A1: float = 0
    A2: float = 0
    Phi: float = 0
    Mu: float = 0
    Sig: float = 0
    c0: float = 0
    c1: float = 0
    ia: float = 0
    oa: float = 0

    def __str__(self):
        cmd = Template(
            "mi_addboundprop($propname, $A0, $A1, $A2, $Phi, $Mu, $Sig, $c0, $c1, $BdryFormat, $ia, $oa)"
        )
        cmd = cmd.substitute(
            propname="'" + self.name + "'",
            A0=0,
            A1=0,
            A2=0,
            Phi=0,
            Mu=0,
            Sig=0,
            c0=0,
            c1=0,
            BdryFormat=6,
            ia=0,
            oa=self.angle,
        )


# Magnetic Boundary Conditions
class MagneticDirichlet(MagneticBoundaryBaseClass):

    def __init__(self, name, a_0=0.0, a_1=0.0, a_2=0.0, phi=0.0):
        self.name = name
        self.a_0 = a_0
        self.a_1 = a_1
        self.a_2 = a_2
        self.phi = phi
        self.boundary_format = 0


class MagneticMixed(MagneticBoundaryBaseClass):

    def __init__(self, name, c_0=0.0, c_1=0.0):
        self.name = name
        self.c_0 = c_0
        self.c_1 = c_1
        self.boundary_format = 2


class MagneticAnti(MagneticBoundaryBaseClass):

    def __init__(self, name):
        self.name = name
        self.boundary_format = 5


class MagneticPeriodic(MagneticBoundaryBaseClass):
    def __init__(self, name):
        self.name = name
        self.boundary_format = 4


class MagneticAntiPeriodicAirgap(MagneticBoundaryBaseClass):

    def __init__(self, name):
        self.name = name
        self.boundary_format = 7


@dataclass
class MagneticPeriodicAirgap(MagneticBoundaryBaseClass):

    def __init__(self, name):
        self.name = name
        self.boundary_format = 6
