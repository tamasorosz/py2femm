import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pymcdm.methods import TOPSIS, MABAC, COMET, SPOTIS
from pymcdm import weights as w
from pymcdm.helpers import rankdata, rrankdata
from pymcdm.methods.comet_tools import MethodExpert
from pymcdm import visuals

# df_base = pd.read_csv('results/nsga2_case3_p25o25g40_pareto.csv')
#
# df_alts = df_base.iloc[:, -4:]
#
# df_alts.iloc[:, 0] *= -1
#
# alts = df_alts.to_numpy()
#
# weights = w.entropy_weights(alts)
# types = np.array([1, -1, -1, -1])
#
# cvalues = COMET.make_cvalues(alts)
#
# expert_function = MethodExpert(TOPSIS(), weights, types)
#
# bounds = SPOTIS.make_bounds(alts)
#
# methods = [
#     TOPSIS(),
#     MABAC(),
#     COMET(cvalues, expert_function),
#     SPOTIS(bounds)
# ]
#
# method_names = ['TOPSIS', 'MABAC', 'COMET', 'SPOTIS']
#
# prefs = []
# ranks = []
#
# for method in methods:
#     pref = method(alts, weights, types)
#     rank = method.rank(pref)
#
#     prefs.append(pref)
#     ranks.append(rank)
#
# a = [f'$A_{{{i+1}}}$' for i in range(len(prefs[0]))]
# df = pd.DataFrame(zip(*ranks), columns=method_names, index=a).round(3)
# colors = ["#B90276", '#50237F', '#005691', "#008ECF", '#00A8B0', '#78BE20', "#006249", '#525F6B', '#000']
#
# fig, ax = plt.subplots(dpi=150, tight_layout=True)
# visuals.ranking_flows(ranks, colors=colors, labels=method_names, ax=ax, better_grid=True)
# plt.ylabel('Position in the ranking [u.]', fontsize=14)
# ax.set_xticklabels(method_names, rotation=0, fontsize=14)
# ax.set_yticklabels(np.linspace(1,24,24, dtype=int), rotation=0, fontsize=14)
#
# plt.savefig('figures/flow_ranking', bbox_inches='tight')
# plt.show()

15,18,14,8

categories = ['AVG', 'RIP', 'COG', 'THD']

data1 = [1759.97,35.9,13.94,118.45]
data2 = [1376.92,40.2,20.12,33.72]
data3 = [1371.99,11.4,19.95,41.11]


# Custom colors
colors = ["#B90276", '#50237F', '#005691', "#008ECF", '#00A8B0', '#78BE20', "#006249", '#525F6B', '#000']

# Bar width
bar_width = 0.2

# Positions of the bars on the x-axis
r1 = np.arange(len(categories))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]

fig, ax1 = plt.subplots(figsize=(8, 6))

# Bars for the 'AVG' category on the primary y-axis
ax1.bar(r1[0], data1[0], color=colors[0], width=bar_width, edgecolor='grey', label='Equal priority')
ax1.bar(r2[0], data2[0], color=colors[1], width=bar_width, edgecolor='grey', label='THD priority')
ax1.bar(r3[0], data3[0], color=colors[2], width=bar_width, edgecolor='grey', label='Ripple priority')

# Labels and title for the primary y-axis
ax1.set_xlabel('Categories', fontsize=16)
ax1.set_ylabel('Tavg [mNm]', fontsize=16)
ax1.set_xticks([r + bar_width for r in range(len(categories))])
ax1.set_xticklabels(categories, fontsize=16)

# Create a secondary y-axis
ax2 = ax1.twinx()

# Bars for the 'RIP', 'COG', 'THD' categories on the secondary y-axis
ax2.bar(r1[1:], data1[1:], color=colors[0], width=bar_width, edgecolor='grey')
ax2.bar(r2[1:], data2[1:], color=colors[1], width=bar_width, edgecolor='grey')
ax2.bar(r3[1:], data3[1:], color=colors[2], width=bar_width, edgecolor='grey')

# Labels and title for the secondary y-axis
ax2.set_ylabel('RIP [%] / COG [mNm] / THD [%]', fontsize=16)

# Combine legends from both axes
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(handles1 + handles2, labels1 + labels2, loc='upper center', fontsize=16)
plt.axvline(x=(r1[0] + r1[1])/1.4, color='black', linestyle='--')
ax1.tick_params(axis='both', labelsize=16)
ax2.tick_params(axis='y', labelsize=16)
plt.savefig('figures/priorities', bbox_inches='tight')
plt.show()