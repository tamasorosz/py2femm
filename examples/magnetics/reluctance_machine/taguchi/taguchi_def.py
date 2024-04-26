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

    return df


@dataclass
class FactorL25(ABC):
    name: str
    level: list


# See /supplementary/parameters.xlsx/1.case
X1 = FactorL25("X1", [16, 16.5, 17, 17.5, 18])  # ang_co
X2 = FactorL25("X2", [120, 130, 140, 150, 160])  # deg_co
X3 = FactorL25("X3", [1, 1.25, 1.5, 1.75, 2.0])  # bd
X4 = FactorL25("X4", [0.6, 0.7, 0.8, 0.9, 1.0])  # bw
X5 = FactorL25("X5", [2, 2.25, 2.5, 2.75, 3])  # bh
X6 = FactorL25("X6", [1.5, 1.75, 2, 2.25, 2.5])  # bg

df = pd.DataFrame([[float(0.00)] * 6] * 25, columns=["X1", "X2", "X3", "X4", "X5", "X6"])

factors = [X1, X2, X3, X4, X5, X6]
for i, j in zip(factors, range(len(factors))):
    for k in range(df.shape[0]):
        df.iloc[k, j] = float(i.level[l25().iloc[k, j] - 1])