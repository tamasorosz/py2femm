from matplotlib import pyplot as plt

import machine_model as model
import calculate_max_torque_angle as angle
import calculate_average_torque_and_ripple as average

if __name__ == '__main__':

    variables = model.VariableParameters(folder_name="ang",
                                         file_name="ang",
                                         current_density=30,
                                         initial_current_angle=-120,
                                         initial_rotor_position=0,
                                         rotor_diameter=44.5,
                                         shaft_diameter=10,
                                         magnet_width=40,
                                         magnet_height=2,
                                         pole_pairs=4,
                                         stack_lenght=40,
                                         winding_scheme='ABCABCABCABC',
                                         )

    # x, y = angle.max_torque_angle(variables, resolution=8, start_position=19, end_position=26, rounding=None,
    #                               delete_after=False,)
    #
    # print(x)
    # print(y)
    #
    # plt.plot(y)
    # plt.show()

    variables.update_folder_name("test")
    variables.update_file_name("test")

    x, y, z = average.average_torque_and_ripple(variables, initial_rotor_position=21, resolution_average_ripple=16,
                                                start_position_average_ripple=0, end_position_average_ripple=15,
                                                rounding=2, delete_after=False)

    print(x)
    print(y)
    print(z)

    plt.plot(z)
    plt.show()