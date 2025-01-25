import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pymcdm.methods import TOPSIS, MABAC, COMET, SPOTIS
from pymcdm import weights as w
from pymcdm.helpers import rankdata, rrankdata
from pymcdm.methods.comet_tools import MethodExpert
from pymcdm import visuals

df_base = pd.read_csv('results/nsga2_const_p50o25g100_best10e.csv')

df_alts = df_base.iloc[:, -2:]

df_alts.iloc[:, 0] *= -1

alts = df_alts.to_numpy()

# weights = w.variance_weights(alts)
# weights = w.entropy_weights(alts)
weights = np.array([0.50941744, 0.49058256]) #entropy
# weights = np.array([0.6233861, 0.3766139]) #variance

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
# visuals.ranking_flows(ranks, colors=colors, labels=method_names,
#                       ax=ax, better_grid=True)
visuals.ranking_flows(ranks, alt_indices=[47, 23, 20, 49, 45, 11, 2, 39, 22, 30], colors=colors, labels=method_names,
                      ax=ax, better_grid=True) # entropy
# visuals.ranking_flows(ranks, alt_indices=[4, 18, 31, 22, 9, 29, 14, 15, 33, 7], colors=colors, labels=method_names,
#                       ax=ax, better_grid=True) # variance
plt.ylabel('Position in the ranking [u.]', fontsize=20)
ax.set_xticklabels(method_names, rotation=0, fontsize=20)
ax.set_yticklabels(np.linspace(1, 10, 10, dtype=int), rotation=0, fontsize=20)

plt.savefig('figures/cogmob_ranking_entropy.png', bbox_inches='tight')
plt.show()

# Variance32: 24.797122859527548,138.9738621432909,1.0095929038723075,1.775489368729279,1.5004808591769936,-1701.3458101454326,0.5496674866053894
# Variance08: 24.848132419294817,138.31942333884666,1.025565071663171,1.5981073830927328,1.5046990490148267,-1724.5354328899282,0.57309259073097
# Entropy23: 24.849263868143975,91.53190820462422,1.0095428903429515,2.169255217879338,1.5069937965181435,-1428.173703895285,0.4147652563673747
# Entropy48: 24.421842197721,119.78309037203509,1.0692574232769567,2.1351434846855457,1.506946791778798,-1565.0915571790938,0.4720301913271463

# Variance32: 24.8,139.0, 1.0, 1.8, 1.5, 1701.3,55.0
# Entropy48: 24.4, 119.8, 1.1, 2.1, 1.5, 1565.1, 47.2
