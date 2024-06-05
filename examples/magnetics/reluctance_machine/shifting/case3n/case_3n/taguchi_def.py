from abc import ABC
from dataclasses import dataclass

import pandas as pd


# L25 orthogonal matrix with 6 factors at 5 levels
def l25():
    data = [[1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2],
            [1, 3, 3, 3, 3, 3],
            [1, 4, 4, 4, 4, 4],
            [1, 5, 5, 5, 5, 5],
            [2, 1, 2, 3, 4, 5],
            [2, 2, 3, 4, 5, 1],
            [2, 3, 4, 5, 1, 2],
            [2, 4, 5, 1, 2, 3],
            [2, 5, 1, 2, 3, 4],
            [3, 1, 3, 5, 2, 4],
            [3, 2, 4, 1, 3, 5],
            [3, 3, 5, 2, 4, 1],
            [3, 4, 1, 3, 5, 2],
            [3, 5, 2, 4, 1, 3],
            [4, 1, 4, 2, 5, 3],
            [4, 2, 5, 3, 1, 4],
            [4, 3, 1, 4, 2, 5],
            [4, 4, 2, 5, 3, 1],
            [4, 5, 3, 1, 4, 2],
            [5, 1, 5, 4, 3, 2],
            [5, 2, 1, 5, 4, 3],
            [5, 3, 2, 1, 5, 4],
            [5, 4, 3, 2, 1, 5],
            [5, 5, 4, 3, 2, 1]]

    df = pd.DataFrame(data, columns=['X1', 'X2', 'X3', 'X4', 'X5', 'X6'])
    df = df.drop(labels=['X5', 'X6'], axis=1)

    return df


@dataclass
class FactorL25(ABC):
    name: str
    level: list


# See /supplementary/parameters.xlsx/1.case
ang_m = 15
ang_mp = 18
deg_m = 14/2
deg_mp = 8/2

delta1 = 0.1
delta2 = 0.1
delta3 = 0.1
delta4 = 0.1

X1 = FactorL25("X1", [ang_m-2*delta1, ang_m-delta1, ang_m, ang_m+delta1, ang_m+2*delta1])  # ang_m
X2 = FactorL25("X2", [ang_mp-2*delta2, ang_mp-delta2, ang_mp, ang_mp+delta2, ang_mp+2*delta2])  # ang_mp
X3 = FactorL25("X3", [deg_m-2*delta3, deg_m-delta3, deg_m, deg_m+delta3, deg_m+2*delta3])  # deg_m
X4 = FactorL25("X4", [deg_mp-2*delta4, deg_mp-delta4, deg_mp, deg_mp+delta4, deg_mp+2*delta4])  # deg_mp

df = pd.DataFrame([[float(0.00)] * 4] * 25, columns=["X1", "X2", "X3", "X4"])

factors = [X1, X2, X3, X4]
for i, j in zip(factors, range(len(factors))):
    for k in range(df.shape[0]):
        df.iloc[k, j] = float(i.level[l25().iloc[k, j] - 1])