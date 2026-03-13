# import math
# import os
#
# import pandas as pd
# from matplotlib import pyplot as plt
#
# import machine_model_synrm
# import calc_max_torque_angle
# import calc_torque_avg_rip
#
import math

import matplotlib.pyplot as plt
import numpy as np

from examples.magnetics.reluctance_machine.optimisation.case_0_noPM import calc_max_torque_angle

if __name__ == "__main__":

    #     # df_base = pd.read_csv('results/nsga2_case1_p50o50g100_obj5_20240704.csv')
    #
        # f = calc_max_torque_angle.max_torque_angle(30, 24.8, 18, 1.0, 0.5, 1.8, 1)
    #     # g = calc_max_torque_angle.max_torque_angle(30, 24.4, 119.8, 1.1, 0.5, 2.1, 1.5)
    #
    #     # f = calc_torque_avg_rip.torque_avg_rip(30, 24.8, 139.0, 1.0, 0.5, 1.8, 1.5)
    #     g = calc_torque_avg_rip.torque_avg_rip(110, 24.8, 13.9, 1.0, 2, 1.8, 1)
    #
    #     # df = pd.DataFrame({'V': f[2], 'E': g[2]})
    #     # current_file_path = os.path.abspath(__file__)
    #     # folder_path = os.path.dirname(current_file_path)
    #     # file_path = os.path.join(folder_path, f'results/cogmob_dynamic.csv')
    #     # df.to_csv(file_path, encoding='utf-8', index=False)
    #     #
    #     plt.plot(g[3])
    #     plt.show()
    # import numpy as np
    #
    # random_number = np.round(np.random.random(), 2)
    # print(random_number)



    # # CONSTRAINT_0: Does not let the Cc to be lower than the diameter.
    # x = (b ** 2 + c ** 2 - a ** 2) / (2 * C)




    #
    # x = 20
    # y = (math.degrees(2 * math.atan2(math.sin(math.radians(x / 2)), 1 - math.cos(math.radians(x / 2))))) / 10
    # print(y)
    # #
    # #CONSTRAINT_1: Ensures that the X5 doesnt go lower than the cut-off arc selection point.
    # MD = math.cos(math.radians(x0/2))*22
    # R = math.sin(math.radians(x0/2))*22/math.tan(math.radians(x1/2))
    # CP = MD-R
    # y = 2*(22-CP)
    #
    # import numpy as np
    # import matplotlib.pyplot as plt
    # from mpl_toolkits.mplot3d import Axes3D
    # import math
    #
    # # Define a range for x0 and x1
    # x0 = np.linspace(15, 25, 100)  # Adjusted range to avoid extreme values
    # x1 = np.linspace(10, 18, 100)
    # X0, X1 = np.meshgrid(x0, x1)
    #
    # # Compute MD, R, CP, and y
    # MD = np.cos(np.radians(X0 / 2)) * 22
    # R = np.sin(np.radians(X0 / 2)) * 22 / np.tan(np.radians(X1 * 10 / 2))
    # CP = MD - R
    #
    # y = 2 * (22 - CP)
    #
    # # Plot the surface
    # fig = plt.figure(figsize=(8, 6))
    # ax = fig.add_subplot(111, projection='3d')
    #
    # ax.plot_surface(X0, X1, y, cmap='viridis', alpha=0.7)
    #
    # # Labels and title
    # ax.set_xlabel('X0')
    # ax.set_ylabel('X1')
    # ax.set_zlabel('y')
    # ax.set_title('3D Plot of y based on X0 and X1')

    # plt.show()

    # #CONSTRAINT_3: ENSURES THE GAP BETWEEN TWO ADJACENT POLES
    # MD = np.cos(np.radians(X0 / 2)) * 22
    # R = np.sin(np.radians(X0 / 2)) * 22 / np.tan(np.radians(X1 * 10 / 2))
    # CP = MD - R
    # Z = (2*np.sin(np.radians(22.5/2))*(22-X5/2))-B/2
    # b = CP + X2 + X4
    # CC = MD + R
    # d = CC-(22-X5/2)
    # alpha = np.arccos((np.power(22-X5/2,2)+np.power(b,2)-np.power(CC,2)) / ((22-X5/2) * b))
    # a = np.sqrt(np.power(b,2)+np.power(d,2)-2*b*d*np.cos(alpha))

    i = 19
    j = 111
    d = 44

    midpoint = np.cos(np.radians(i / 2)) * 22
    distance = 2 * np.sin(np.radians(i / 2)) * 22
    R = (distance / (2 * np.tan(np.radians(j / 2))))
    centerpoint = midpoint + R
    radius = np.sqrt(22 ** 2 + centerpoint ** 2 - (2 * 22 * centerpoint * np.cos(np.radians(i / 2))))
    selection_point = centerpoint - radius
    # radius2 = np.sqrt(R ** 2 + (distance/2) ** 2)
    #
    x0 = np.radians(i)  # Convert x0 to radians
    x1 = np.radians(j)  # Convert x1 to radians
    #
    # sin_x0_2 = math.sin(x0 / 2)
    # tan_x1_2 = math.tan(x1 / 2)
    #
    # radius3 = sin_x0_2 * 44 / 2 * np.sqrt(1 / tan_x1_2**2 + 1)
    #
    # print(radius1, radius2, radius3)

    sin_x0_2 = math.sin(x0 / 2)
    tan_x0_2 = math.tan(x0 / 2)
    tan_x1_2 = math.tan(x1 / 2)

    # Calculate the full expression
    s = (d / 2) * sin_x0_2 * (
            (1 / tan_x0_2) + (1 / tan_x1_2) - math.sqrt(1 + (1 / tan_x1_2 ** 2))
    )

    print(selection_point, s)