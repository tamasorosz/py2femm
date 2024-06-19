import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pymcdm.methods import TOPSIS, MABAC, COMET, SPOTIS
from pymcdm import weights as w
from pymcdm.helpers import rankdata, rrankdata
from pymcdm.methods.comet_tools import MethodExpert
from pymcdm import visuals

df_base = pd.read_csv('results/nsga2_const_p50o25g100_best10.csv')

df_alts = df_base.iloc[:, -2:]

df_alts.iloc[:, 0] *= -1

alts = df_alts.to_numpy()

weights = w.variance_weights(alts)
# weights = w.entropy_weights(alts)

print(weights)

types = np.array([1, -1])

cvalues = COMET.make_cvalues(alts)

expert_function = MethodExpert(TOPSIS(), weights, types)

bounds = SPOTIS.make_bounds(alts)

methods = [
    TOPSIS(),
    MABAC(),
]

method_names = ['TOPSIS', 'SPOTIS']

prefs = []
ranks = []

for method in methods:
    pref = method(alts, weights, types)
    rank = method.rank(pref)

    prefs.append(pref)
    ranks.append(rank)

a = [f'$A_{{{i + 1}}}$' for i in range(len(prefs[0]))]
df = pd.DataFrame(zip(*ranks), columns=method_names, index=a).round(3)
colors = ["#B90276", '#50237F', '#005691', "#008ECF", '#00A8B0', '#78BE20', "#006249", '#525F6B', '#000']

fig, ax = plt.subplots(figsize=(10, 8))
visuals.ranking_flows(ranks, alt_indices=[5, 16, 32, 23, 10, 30, 15, 16, 34, 8], colors=colors, labels=method_names,
                      ax=ax, better_grid=True)
plt.ylabel('Position in the ranking [u.]', fontsize=20)
ax.set_xticklabels(method_names, rotation=0, fontsize=20)
ax.set_yticklabels(np.linspace(1, 10, 10, dtype=int), rotation=0, fontsize=20)

plt.savefig('figures/cogmob_ranking_variance.png', bbox_inches='tight')
plt.show()

# Variance: 24.8,139.0, 1.0, 1.8, 1.5, 1701.3,55.0
# Entropy: 24.4, 119.8, 1.1, 2.1, 1.5, 1565.1, 47.2
