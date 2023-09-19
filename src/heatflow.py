from dataclasses import dataclass
from string import Template


@dataclass(kw_only=True)
class HeatFlowMaterial:
    material_name: str
    kx: float
    ky: float
    qv: float
    kt: float

    def __str__(self):
        cmd = Template("hi_addmaterial($materialname, $kx, $ky, $qv, $kt)")
        cmd = cmd.substitute(
            selfname=f'"{self.material_name}"',
            kx=self.kx,
            ky=self.ky,
            qv=self.qv,
            kt=self.kt,
        )
        return cmd


# HeatFlow Boundary Conditions
@dataclass
class HeatFlowFixedTemperature:
    name: str
    Tset: float


@dataclass
class HeatFlowHeatFlux:
    name: str
    qs: float


@dataclass
class HeatFlowConvection:
    name: str
    h: float
    Tinf: float


@dataclass
class HeatFlowRadiation:
    name: str
    beta: float
    Tinf: float


@dataclass
class HeatFlowPeriodic:
    name: str


@dataclass
class HeatFlowAntiPeriodic:
    name: str
