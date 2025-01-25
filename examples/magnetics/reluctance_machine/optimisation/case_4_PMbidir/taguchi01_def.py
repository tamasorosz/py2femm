import math
import os
from abc import ABC
from dataclasses import dataclass

import numpy as np
import pandas as pd


# L27 orthogonal matrix with 6 factors at 5 levels
@dataclass
class FactorL27(ABC):
    name: str
    level: list


file_path = os.getcwd() + '/results/' + f'taguchi_L27.csv'
cols = ["X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8", "X9"]
data = pd.read_csv(file_path, usecols=cols)

X1 = FactorL27("X1", list(np.linspace(15, 25, 3)))  # ang_co
X2 = FactorL27("X2", list(np.linspace(10, 15, 3)))  # deg_co
X3 = FactorL27("X3", list(np.linspace(1, 4, 3)))  # bd
X4 = FactorL27("X4", list(np.linspace(0.5, 1, 3)))  # bw
X5 = FactorL27("X5", list(np.linspace(1, 4, 3)))  # bh
X6 = FactorL27("X6", list(np.linspace(1, 2, 3)))  # bgp
X7 = FactorL27("X7", list(np.linspace(1, 1.5, 3)))  # mh
X8 = FactorL27("X8", list(np.linspace(10, 15, 3)))  # ang_m
X9 = FactorL27("X9", list(np.linspace(0, 16, 3)))  # deg_m

df = pd.DataFrame([[float(0.00)] * 9] * 27, columns=cols)
df1 = pd.DataFrame([[float(0.00)] * 9] * 27, columns=cols)
df2 = pd.DataFrame([[float(0.00)] * 9] * 27, columns=cols)

factors = [X1, X2, X3, X4, X5, X6, X7, X8, X9]
for i, j in enumerate(factors):
    for k in range(df.shape[0]):
        if i < 9:
            df.iloc[k, i] = float(j.level[int(data.iloc[k, i] - 1)])

for i in range(len(df)):
    x = list(df.iloc[i])

    g = (math.tan(math.radians(x[0] / 2)) * (22 - (x[5] * 0.5 + 1.5)) + x[2] + x[4]) - 8
    if g > 0:
        temp_x3 = np.round((8 - (math.tan(math.radians(x[0] / 2)) * (22 - (x[5] * 0.5 + 1.5))) - x[2]), 1)
        if temp_x3 < 1:
            x[4] = 1
            x[2] = np.round(x[2] - (1 - temp_x3), 1)
            if x[2] < 1:
                x[2] = 1
        else:
            x[4] = temp_x3

    if x[7] + x[8] / 2 + x[0] > 43:
        x[8] = 2 * (43 - x[7] - x[0])

    df1.iloc[i] = x

