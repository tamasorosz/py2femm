from src.femm_problem import FemmProblem
from examples.SynRM.geom_from_dxf import geom_from_dxf
from src.general import LengthUnit
import os
from src.executor import Executor


problem = FemmProblem(out_file="../Test.csv")
problem.magnetic_problem(0, LengthUnit.MILLIMETERS, "axi")
geometry = geom_from_dxf("SzESynRM_full_model.dxf",precision=4)
problem.create_geometry(geometry)
problem.write("test.lua")

femm = Executor()
current_dir = os.getcwd()
lua_file = current_dir + "/test.lua"
femm.run(lua_file)

A = 0;
