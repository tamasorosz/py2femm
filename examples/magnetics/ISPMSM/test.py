from matplotlib import pyplot as plt

import machine_model as model
import calculate_max_torque_angle as angle
import calculate_average_torque_and_ripple as average

if __name__ == '__main__':

    variables = model.VariableParameters(folder_name="ang",
                                         file_name="ang",
                                         current_density=30,
                                         current_angle=0,
                                         initial_rotor_position=0,
                                         rotor_diameter=44,
                                         shaft_diameter=10,
                                         magnet_width=45,
                                         magnet_height=5,
                                         pole_pairs=4,
                                         stack_lenght=40,
                                         winding_scheme='ABCABCABCABC',
                                         shortening=0,
                                         rotor_position=0
                                         )

    x, y = angle.max_torque_angle(variables, resolution=46, start_position=0, end_position=90, rounding=None,
                                  delete_after=False)

    print(x)
    print(y)

    plt.plot(y)
    plt.show()
    #
    # variables.update_folder_name("test")
    # variables.update_file_name("test")
    #
    # x, y, z = average.average_torque_and_ripple(variables, resolution_angle=9, start_position_angle=0,
    #                                             end_position_angle=8, resolution_average_ripple=9,
    #                                             start_position_average_ripple=0, end_position_average_ripple=8,
    #                                             rounding=2, initial_rotor_position=-15, delete_after=False)
    #
    # print(x)
    # print(y)
    # print(z)
    #
    # plt.plot(z)
    # plt.show()