from dataclasses import dataclass
from string import Template
from src.general import Material, Boundary


@dataclass(kw_only=True)
class CurrentFlowMaterial(Material):
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


@dataclass(kw_only=True)
class CurrentFlowBaseClass(Boundary):
    type: int
    Vs: float = 0
    c0: float = 0
    c1: float = 0
    qs: float = 0

    def __str__(self):
        return f'ci_addboundprop("{self.name}", {self.Vs}, {self.qs}, {self.c0}, {self.c1}, {self.type})'


# Current Flow Boundary Conditions
class CurrentFlowFixedVoltage(CurrentFlowBaseClass):
    def __init__(self, name: str, Vs: float):
        self.name = name
        self.Vs = Vs
        self.type = 0


class CurrentFlowMixed(CurrentFlowBaseClass):

    def __init__(self, name: str, c0: float, c1: float):
        self.name = name
        self.c0 = c0
        self.c1 = c1
        self.type = 2


class CurrentFlowSurfaceCurrent(CurrentFlowBaseClass):
    def __init__(self, name: str, qs: float):
        self.name = name
        self.qs = qs
        self.type = 2



class CurrentFlowPeriodic(CurrentFlowBaseClass):
    def __init__(self, name: str):
        self.name = name
        self.type = 3



class CurrentFlowAntiPeriodic(CurrentFlowBaseClass):
    def __init__(self, name: str):
        self.name = name
        self.type = 4