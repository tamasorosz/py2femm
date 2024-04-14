from dataclasses import dataclass, field
from enum import Enum
from string import Template
from typing import List
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
    Sigma: float = 0.0
    Lam_d: float = 0.0
    Phi_hmax: float = 0.0
    lam_fill: float = 0.0
    LamType: LamType = LamType.NOT_LAMINATED
    Phi_hx: float = 0.0
    Phi_hy: float = 0.0
    NStrands: int = 0.0
    WireD: float = 0.0
    h: list = None
    b: list = None

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
            Cduct=self.Sigma,
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
class BHCurve:
    M: str = 'name'
    B: List[float] = field(default_factory=lambda: [1.0])
    H: List[float] = field(default_factory=lambda: [1.0])

    def __str__(self):
        cmds = []
        for b, h in zip(self.B, self.H):
            cmd = Template("mi_addbhpoint($materialname, $Bcurve, $Hcurve)")
            formatted_cmd = cmd.substitute(materialname=f"'{self.M}'", Bcurve=b, Hcurve=h)
            cmds.append(formatted_cmd)
        return "\n".join(cmds)

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


class MagneticVolumeIntegral(Enum):
    """ integral type values for evaluating the electrostatics results"""

    AJ = 0
    A = 1
    Energy = 2
    HysteresysLoss = 3
    ResistiveLoss = 4
    CrossSection = 5
    TotalLosses = 6
    TotalCurrent = 7
    IntegralBx = 8
    IntegralBy = 9
    Volume = 10
    Fx = 11  # x part of the steady-state lorentz force
    Fy = 12  # y part of the steady-state lorentz force
    Fxx = 13  # x part of the 2 x lorentz force
    Fyy = 14  # y part of the 2 x lorentz force
    Torque = 15  # steady state torque
    DTorque = 16  # 2 x component of the steady state torque
    CoEnergy = 17
    wFx = 18
    wFy = 19
    wFxx = 20
    wFyy = 21
    wTorque = 22
    wDTorque = 23
    inertia_m = 24
    wxFstress = 25
    wyFstress = 26
    wStTorque = 27
    FxL = 28  # x stress tensor torque
    FyL = 29  # y stress tensor torque
    LorentzT = 30
