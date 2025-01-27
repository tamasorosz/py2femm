import machine_model
from src.executor import Executor

variables = machine_model.VariableParameters(folder="test",
                                             filename="test",
                                             current_density=0,
                                             current_angle=0,
                                             rotor_position=0,
                                             rotor_diameter=40,
                                             shaft_diameter=10,
                                             magnet_width=30,
                                             magnet_height=5,
                                             pole_pairs=4,
                                             stack_lenght=1)

model = machine_model.model_creation(variables)

femm = Executor()
femm.run(variables.output_file + ".lua")