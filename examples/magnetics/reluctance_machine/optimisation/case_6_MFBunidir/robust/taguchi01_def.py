import math
import os
from abc import ABC
from dataclasses import dataclass

import numpy as np
import pandas as pd


# L25 orthogonal matrix with 6 factors at 5 levels
@dataclass
class FactorL25(ABC):
    name: str
    level: list


file_path = os.getcwd() + f'/taguchi_L25.csv'
cols = ["X1", "X2", "X3", "X4", "X5", "X6"]
data = pd.read_csv(file_path, usecols=cols)

X1 = FactorL25("X1", list(np.linspace(10-0.15, 10+0.15, 5)))  # ang_m
X2 = FactorL25("X2", list(np.linspace(11-0.15, 11+0.15, 5)))  # ang_mp
X3 = FactorL25("X3", list(np.linspace(16-0.15, 16+0.15, 5)))  # deg_m
X4 = FactorL25("X4", list(np.linspace(14-0.15, 14+0.15, 5)))  # deg_mp
X5 = FactorL25("X5", list(np.linspace(0, 0, 5)))  # deg_mp
X6 = FactorL25("X6", list(np.linspace(0, 0, 5)))  # deg_mp

df = pd.DataFrame([[float(0.00)] * len(cols)] * 25, columns=cols)
df1 = pd.DataFrame([[float(0.00)] * len(cols)] * 25, columns=cols)
df2 = pd.DataFrame([[float(0.00)] * len(cols)] * 25, columns=cols)

factors = [X1, X2, X3, X4, X5, X6]
for i, j in enumerate(factors):
    for k in range(data.shape[0]):
        if i < len(factors):
            df1.iloc[k, i] = float(j.level[int(data.iloc[k, i] - 1)])