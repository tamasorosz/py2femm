import machine_model as model
from src.executor import Executor

if __name__ == '__main__':
    variables = model.VariableParameters(folder_name='test',
                 file_name='test',
                 current=0,
                 number_of_coil_turns=0,
                 initial_current_angle=0,
                 current_angle=0,
                 initial_rotor_position=0,
                 rotor_position=0,
                 shaft_diameter=10,
                 rotor_diameter=44,
                 cut_off_barrier_angle=90,
                 cut_off_barrier_curve_degree=100,
                 barrier_distance=0,
                 barrier_width=0,
                 barrier_height=0,
                 barrier_gap=0,
                 magnet_height=0,
                 magnet_width=0,
                 magnet_pocket_width=0,
                 magnet_shift=0,
                 magnet_pocket_shift=0,
                 pole_pairs=1,
                 stack_length=1,
                 winding_scheme='A|b|C|a|B|c|A|b|C|a|B|c|',
                 shortening=0)

    model.model_creation(variables=variables)