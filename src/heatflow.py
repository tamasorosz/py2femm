from dataclasses import dataclass


@dataclass
class HeatFlowMaterial:
    material_name: str
    kx: float
    ky: float
    qv: float
    kt: float


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
