import math
import random

import numpy as np
from matplotlib import pyplot as plt

from examples.magnetics.reluctance_machine.optimisation.case_0_noPM import calc_max_torque_angle
from examples.magnetics.reluctance_machine.optimisation.case_0_noPM import machine_model_synrm
from src.geometry import Node

if __name__ == "__main__":
    X0 = 25
    X1 = 10
    X2 = 4
    X3 = 0.01
    X4 = 4
    X5 = 1

    # COSTRAINT VARIABLES
    midpoint = np.cos(np.radians(X0 / 2)) * 22  # OK 21.4758
    distance = 2 * np.sin(np.radians(X0 / 2)) * 22  # OK 9.52334
    R = (distance / (2 * np.tan(np.radians(X1 * 10 / 2))))
    centerpoint = midpoint + R
    radius = np.sqrt(22 ** 2 + centerpoint ** 2 - (2 * 22 * centerpoint * np.cos(np.radians(X0 / 2))))
    selection_point = centerpoint - radius

    if X5 / 2 > 22 - selection_point:
        X5 = (22 - selection_point) * 2

    # Compute x1, y1, x2, y2 based on the provided equations
    a = radius + X2 + X4
    b = 22 - X5 / 2
    c = centerpoint
    x1 = (b ** 2 + c ** 2 - a ** 2) / (2 * c)
    y1 = np.sqrt(b ** 2 - x1 ** 2)
    x_rot1 = x1 * math.cos(np.radians(45)) - y1 * math.sin(np.radians(45))
    y_rot1 = x1 * math.sin(np.radians(45)) + y1 * math.cos(np.radians(45))

    a = radius + X2
    b = 22 - X5 / 2
    c = centerpoint
    x2 = (b ** 2 + c ** 2 - a ** 2) / (2 * c)
    y2 = np.sqrt(b ** 2 - x2 ** 2)
    x_rot2 = x2 * math.cos(np.radians(45)) - y2 * math.sin(np.radians(45))
    y_rot2 = x2 * math.sin(np.radians(45)) + y2 * math.cos(np.radians(45))

    # Calculate the slope (m1) and y-intercept (b1) for the first line
    m1 = (y_rot2 - y_rot1) / (x_rot2 - x_rot1)
    b1 = y_rot1 - m1 * x_rot1

    # Solve for intersection with y = x line
    x_intersect_r = -b1 / (m1 - 1)
    y_intersect_r = x_intersect_r  # Since y = x

    x_intersect_l = - b1 / (m1 - np.tan(np.radians(67.5)))
    y_intersect_l = m1 * x_intersect_l + b1

    # Calculate the distance between the intersection point and (x1, y1)
    constraint_distance = np.sqrt((x_intersect_r - x_rot1) ** 2 + (y_intersect_r - y_rot1) ** 2)
    constraining_distance = np.sqrt((x_intersect_l - x_rot1) ** 2 + (y_intersect_l - y_rot1) ** 2)

    print(constraining_distance)

    if random.choice([True, False]):
        if x_rot1 - x_intersect_l > 0:
            if constraining_distance < 0.25:
                g = X4 - (0.25 - constraining_distance)
                X4 = g
                if g < 0.5:
                    X4 = 0.5
                    X2 = X2 - (0.5 - g)
                    if X2 < 0.5:
                        X2 = 0.5
        else:
            g = X4 - (constraining_distance + 0.5)
            X4 = g
            if g < 0.5:
                X4 = 0.5
                X2 = X2 + g - 0.25
                if X2 < 0.5:
                    X2 = 0.5
    else:
        if x_rot1 - x_intersect_l > 0:
            if constraining_distance < 0.25:
                g = X2 - (0.25 - constraining_distance)
                X2 = g
                if g < 0.5:
                    X2 = 0.5
                    X4 = X4 - (0.5 - g)
                    if X4 < 0.5:
                        X4 = 0.5
        else:
            g = X2 - (constraining_distance + 0.5)
            X2 = g
            if g < 0.5:
                X2 = 0.5
                X4 = X4 + g - 0.25
                if X4 < 0.5:
                    X4 = 0.5


    print(X0, X1, X2, X3, X4, X5)


    calc_max_torque_angle.max_torque_angle(30, X0, X1, X2, X3, X4, X5)
