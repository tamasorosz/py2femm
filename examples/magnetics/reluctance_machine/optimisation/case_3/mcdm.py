import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pymcdm.methods import TOPSIS, MABAC, COMET, SPOTIS
from pymcdm import weights as w
from pymcdm.helpers import rankdata, rrankdata
from pymcdm.methods.comet_tools import MethodExpert
from pymcdm import visuals

df_base = pd.read_csv('results/nsga2_case3_p50o50g100_obj7_20240711.csv')

df_base = df_base[df_base['AVG'] <= -1500]
df_base = df_base.reset_index(drop=True)
print(df_base)

df_alts = df_base.iloc[:, -4:]
df_alts.iloc[:, 0] *= -1


alts = df_alts.to_numpy()

df = pd.DataFrame({'TOPSIS': [], 'MABAC': [], 'COMET': [], 'SPOTIS': []})

types = np.array([1, -1, -1, -1])
weights = np.array([w.equal_weights(alts),
                    w.angle_weights(alts),
                    w.cilos_weights(alts, types),
                    w.critic_weights(alts),
                    w.entropy_weights(alts),
                    w.gini_weights(alts),
                    w.idocriw_weights(alts, types),
                    w.merec_weights(alts, types),
                    w.standard_deviation_weights(alts),
                    w.variance_weights(alts)])

for i in range(len(weights)):
    cvalues = COMET.make_cvalues(alts)
    expert_function = MethodExpert(TOPSIS(), weights[i], types)
    bounds = SPOTIS.make_bounds(alts)

    methods = [
        TOPSIS(),
        MABAC(),
        COMET(cvalues, expert_function),
        SPOTIS(bounds)
    ]

    method_names = ['TOPSIS', 'MABAC', 'COMET', 'SPOTIS']

    prefs = []
    ranks = []

    for method in methods:
        pref = method(alts, weights[i], types)
        rank = method.rank(pref)

        prefs.append(pref)
        ranks.append(rank)

    new_row = {"TOPSIS": ranks[0], "MABAC": ranks[1], "COMET": ranks[2], "SPOTIS": ranks[3]}
    df = df._append(new_row, ignore_index=True)

# print(df)

current_file_path = os.path.abspath(__file__)
folder_path = os.path.dirname(current_file_path)

for i in range(len(df.index)):
    for j in range(len(df.columns)):
        df_rank = df.iloc[i, j].tolist()
        df.iloc[i, j] = df_rank.index(1)

row_names = {0: 'equal',
             1: 'angle',
             2: 'cilos',
             3: 'critic',
             4: 'entropy',
             5: 'gini',
             6: 'idocriw',
             7: 'merec',
             8: 'stdev',
             9: 'variance'}

df = df.rename(index=row_names)

weights = np.round(weights, 2)
weights = weights.tolist()
df['weights'] = weights

print(df)
df_base.to_json(os.path.join(folder_path, 'results/case2_mcdm_base.json'), orient='split', compression='infer')
df.to_json(os.path.join(folder_path, 'results/case2_mcdm_4goals.json'), orient='split', compression='infer')