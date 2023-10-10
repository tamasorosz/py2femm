from dataclasses import dataclass
from enum import Enum
from string import Template

from src.general import Material, Boundary


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
    mu_x: float = 1.0
    mu_y: float = 1.0
    H_c: float = 0.0
    J: float = 0.0
    Cduct: float = 0.0
    Lam_d: float = 0.0
    Phi_hmax: float = 0.0
    lam_fill: float = 0.0
    LamType: LamType = LamType.NOT_LAMINATED
    Phi_hx: float = 0.0
    Phi_hy: float = 0.0
    NStrands: int = 0.0
    WireD: float = 0.0

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
            LamType=self.LamType.value,
            Phi_hx=self.Phi_hx,
            Phi_hy=self.Phi_hy,
            NStrands=self.NStrands,
            WireD=self.WireD,
        )
        return cmd


@dataclass(kw_only=True)
class MagneticBoundaryBaseClass(Boundary):
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
            "mi_addboundprop($propname, $A0, $A1, $A2, $Phi, $Mu, $Sig, $c0, $c1, $boundary_format, $ia, $oa)"
        )
        cmd = cmd.substitute(
            propname="'" + self.name + "'",
            A0=self.A0,
            A1=self.A1,
            A2=self.A2,
            Phi=self.Phi,
            Mu=self.Mu,
            Sig=self.Sig,
            c0=self.c0,
            c1=self.c1,
            boundary_format=self.boundary_format,
            ia=self.ia,
            oa=self.oa,
        )
        return cmd


# Magnetic Boundary Conditions
class MagneticDirichlet(MagneticBoundaryBaseClass):

    def __init__(self, name: str, a_0: float, a_1: float, a_2: float, phi: float):
        self.name = name
        self.A0 = a_0
        self.A1 = a_1
        self.A2 = a_2
        self.Phi = phi
        self.boundary_format = 0


class MagneticMixed(MagneticBoundaryBaseClass):

    def __init__(self, name, c_0=0.0, c_1=0.0):
        self.name = name
        self.c0 = c_0
        self.c1 = c_1
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
