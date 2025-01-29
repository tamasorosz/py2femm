import machine_model as model
import calculate_max_torque_angle as angle
from src.executor import Executor

if __name__ == '__main__':

    variables = model.VariableParameters(folder="ang",
                                         filename="ang",
                                         current_density=100,
                                         current_angle=0,
                                         initial_rotor_position=0,
                                         rotor_diameter=40,
                                         shaft_diameter=10,
                                         magnet_width=30,
                                         magnet_height=5,
                                         pole_pairs=4,
                                         stack_lenght=1,
                                         winding_scheme='AA|bb|CC|aa|BB|cc|AA|bb|CC|aa|BB|cc|',
                                         shortening=1,
                                         rotor_position=0
                                         )

    x, y = angle.max_torque_angle(variables, resolution=11, start_position=0, end_position=10, rounding=3,
                                  delete_after=True)
    print(x)
    print(y)