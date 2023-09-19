from dataclasses import dataclass
from string import Template


@dataclass(kw_only=True)
class CurrentFlowMaterial:
    material_name: str
    ox: float
    oy: float
    ex: float
    ey: float
    ltx: float
    lty: float

    def __str__(self):
        cmd = Template("ci_addmaterial($materialname, $ox, $oy, $ex, $ey, $ltx, $lty)")
        cmd = cmd.substitute(
            materialname=f'"{self.material_name}"',
            ox=self.ox,
            oy=self.oy,
            ex=self.ex,
            ey=self.ey,
            ltx=self.ltx,
            lty=self.lty,
        )
        return cmd


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
