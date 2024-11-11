import csv
import math
import os
import re

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import calc_max_torque_angle
import calc_cogging
import calc_torque_avg_rip

if __name__ == "__main__":
    # xl = np.array([15, 9, 1, 1, 1, 10]),
    # xu = np.array([25, 14, 4, 4, 2, 15]),

    y = calc_cogging.cogging(0, 15.0,  10.0,  1.0,  0.50,  4.0,  1.0,  2.0,  15.0,  16.0)
