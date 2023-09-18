from dataclasses import dataclass


@dataclass
class CurrentFlowMaterial:
    material_name: str
    ox: float
    oy: float
    ex: float
    ey: float
    ltx: float
    lty: float


# Current Flow Boundary Conditions
@dataclass
class CurrentFlowFixedVoltage:
    name: str
    Vs: float


@dataclass
class CurrentFlowMixed:
    name: str
    c0: float
    c1: float


@dataclass
class CurrentFlowSurfaceCurrent:
    name: str
    qs: float


@dataclass
class CurrentFlowPeriodic:
    name: str


@dataclass
class CurrentFlowAntiPeriodic:
    name: str
