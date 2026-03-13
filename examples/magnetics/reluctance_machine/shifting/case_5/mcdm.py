import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pymcdm.methods import TOPSIS, MABAC, COMET, SPOTIS
from pymcdm import weights as w
from pymcdm.helpers import rankdata, rrankdata
from pymcdm.methods.comet_tools import MethodExpert
from pymcdm import visuals

df_base = pd.read_csv('results/optimisation/nsga2_X7_p50o25g100_top10.csv')

df_alts = df_base.iloc[:, -2:]

df_alts.iloc[:, 0] *= -1

alts = df_alts.to_numpy()

weights = w.entropy_weights(alts)
types = np.array([1, -1])

cvalues = COMET.make_cvalues(alts)

expert_function = MethodExpert(TOPSIS(), weights, types)

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
    pref = method(alts, weights, types)
    rank = method.rank(pref)

    prefs.append(pref)
    ranks.append(rank)

a = [f'$A_{{{i+1}}}$' for i in range(len(prefs[0]))]
df = pd.DataFrame(zip(*ranks), columns=method_names, index=a).round(3)
colors = ["#B90276", '#50237F', '#005691', "#008ECF", '#00A8B0', '#78BE20', "#006249", '#525F6B', '#000']

fig, ax = plt.subplots(dpi=150, tight_layout=True)
visuals.ranking_flows(ranks, colors=colors, labels=method_names, ax=ax, better_grid=True)
plt.ylabel('Position in the ranking [u.]', fontsize=14)
ax.set_xticklabels(method_names, rotation=0, fontsize=14)
ax.set_yticklabels(list(range(1, 10)), rotation=0, fontsize=14)

plt.savefig('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\optimisation\case_2/figures/flow_ranking_span5', bbox_inches='tight')
plt.show()