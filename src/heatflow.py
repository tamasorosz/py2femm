from dataclasses import dataclass
from string import Template
from src.general import Material, Boundary


@dataclass(kw_only=True)
class HeatFlowMaterial(Material):
    kx: float
    ky: float
    qv: float
    kt: float

    def __str__(self):
        cmd = Template("hi_addmaterial($materialname, $kx, $ky, $qv, $kt)")
        cmd = cmd.substitute(
            materialname=f'"{self.material_name}"',
            kx=self.kx,
            ky=self.ky,
            qv=self.qv,
            kt=self.kt,
        )
        return cmd


@dataclass(kw_only=True)
class HeatFlowBaseClass(Boundary):
    type: int
    Tset: float = 0
    qs: float = 0
    Tinf: float = 0
    h: float = 0
    beta: float = 0

    def __str__(self):
        cmd = Template("hi_addboundprop($propname, $BdryFormat, $Tset, $qs, $Tinf, $h, $beta)")
        cmd = cmd.substitute(
            propname=f'"{self.name}"',
            BdryFormat=self.type,
            Tset=self.Tset,
            qs=self.qs,
            Tinf=self.Tinf,
            h=self.h,
            beta=self.beta,
        )
        return cmd


# HeatFlow Boundary Conditions
class HeatFlowFixedTemperature(HeatFlowBaseClass):
    def __init__(self, name: str, Tset: float):
        self.name = name
        self.Tset = Tset
        self.type = 0


class HeatFlowHeatFlux(HeatFlowBaseClass):
    def __init__(self, name: str, qs: float):
        self.name = name
        self.qs = qs
        self.type = 1


class HeatFlowConvection(HeatFlowBaseClass):
    def __init__(self, name: str, Tinf: float, h: float):
        self.name = name
        self.h = h
        self.Tinf = Tinf
        self.type = 2


class HeatFlowRadiation(HeatFlowBaseClass):
    def __init__(self, name: str, Tinf: float, beta: float):
        self.name = name
        self.beta = beta
        self.Tinf = Tinf
        self.type = 3


class HeatFlowPeriodic(HeatFlowBaseClass):
    def __init__(self, name: str):
        self.name = name
        self.type = 4


class HeatFlowAntiPeriodic(HeatFlowBaseClass):
    def __init__(self, name: str):
        self.name = name
        self.type = 5
