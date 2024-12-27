import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from pymcdm.methods import TOPSIS, MABAC, COMET, SPOTIS
from pymcdm import weights as w
from pymcdm.helpers import rankdata, rrankdata
from pymcdm.methods.comet_tools import MethodExpert
from pymcdm import visuals

df1 = pd.read_csv('nsga2_case3_p50o50g100_obj7_20240807.csv')
df2 = pd.read_csv('nsga2_case4_p50o50g100_obj7_20240806.csv')
df4 = pd.read_csv('nsga2_case6_p50o50g100_obj9_20240811.csv')
df3 = pd.read_csv('nsga2_case7_p50o50g150_obj9_20240818.csv')

for d in [df1, df2, df4, df3]:
    d['AVG'] *= -1  # Convert torque values to positive

del df1['THD']
df1.insert(7, 'X8', 'NaN')
df1.insert(8, 'X9', 'NaN')
df1['CAS'] = [f'A1_{i}' for i in range(1, len(df1)+1)]

df2.insert(7, 'X8', 'NaN')
df2.insert(8, 'X9', 'NaN')
df2['CAS'] = [f'A2_{i}' for i in range(1, len(df2)+1)]

df3 = df3[df3["X6"] != df3["X7"]].copy()
df3['CAS'] = [f'B1_{i}' for i in range(1, len(df3)+1)]

df4 = df4[df4["X6"] != df4["X7"]].copy()
df4['CAS'] = [f'B2_{i}' for i in range(1, len(df4)+1)]

df = pd.concat([df1, df2, df3, df4], ignore_index=True)


# df = df[df['AVG'] >= 1400].reset_index(drop=True)
# df = df[df['AVG'] <= 1700].reset_index(drop=True)

# df = df[df['RIP'] <= 20].reset_index(drop=True)


# df = df[df['COG'] <= 15].reset_index(drop=True)
# df = df[df['COG'] <= 20].reset_index(drop=True)
df.index = df.index + 1

pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)  # Adjust width to avoid line breaks
pd.set_option('display.max_colwidth', None)  # Adjust max column width if needed
print(df)
types = np.array([1, -1])  # Specifies the purpose of the objective function as it is cost or profit
alts = df.iloc[:, -4:-2].to_numpy()
# print(alts)
weights = w.entropy_weights(alts)
# weights = w.variance_weights(alts)
# weights = w.equal_weights(alts)
# weights = w.critic_weights(alts)
# weights = w.angle_weights(alts)
# weights = w.cilos_weights(alts, types)
# weights = w.gini_weights(alts)
# weights = w.idocriw_weights(alts, types)
# weights = w.merec_weights(alts, types)
# weights = w.standard_deviation_weights(alts)
# weights = np.array([0.1, 0.8, 0.2])
print(weights)

bounds = SPOTIS.make_bounds(alts)

methods = [
    TOPSIS(),
    SPOTIS(bounds)
]

method_names = ['TOPSIS', 'SPOTIS']

prefs = []
ranks = []

for method in methods:
    pref = method(alts, weights, types)
    rank = method.rank(pref)

    ranks.append(rank)

colors = ["#B90276", '#50237F', '#005691', "#008ECF", '#00A8B0', '#78BE20', "#006249", '#525F6B', '#000']

ranks.append(np.array([colors[5]]*df[df['CAS'].str.startswith('A1_')].shape[0] +
                      [colors[3]]*df[df['CAS'].str.startswith('A2_')].shape[0] +
                      [colors[1]]*df[df['CAS'].str.startswith('B1_')].shape[0] +
                      [colors[0]]*df[df['CAS'].str.startswith('B2_')].shape[0]))

ft = 12

fig, ax = plt.subplots(figsize=(5, 4), dpi=150, tight_layout=True)

x_values = np.linspace(1, 179, 180)  # Create x values
y_values = x_values  # y = x line
ax.plot(x_values, y_values, color='black', linestyle='--', label='y = x', zorder=1)  # Plot y = x line

for i in range(len(ranks[0])):
    ax.scatter(ranks[0][i], ranks[1][i], c=ranks[2][i], zorder=2)
plt.xlabel("TOPSIS", fontsize=ft)
plt.ylabel("SPOTIS", fontsize=ft)
plt.xticks(fontsize=ft)
plt.yticks(fontsize=ft)
# Custom legend
custom_legend = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor=colors[5], markersize=10, label='Case A1'),  # Dot for Case A1
    Line2D([0], [0], marker='o', color='w', markerfacecolor=colors[3], markersize=10, label='Case A2'),  # Dot for Case A2
    Line2D([0], [0], marker='o', color='w', markerfacecolor=colors[1], markersize=10, label='Case B1'),  # Dot for Case B1
    Line2D([0], [0], marker='o', color='w', markerfacecolor=colors[0], markersize=10, label='Case B2'),  # Dot for Case B2
]
ax.scatter(1, 4, c=colors[-1], marker='*', s=300, label='Optimum')

# Add the legend to the plot
plt.legend(handles=custom_legend, loc='best', fontsize=ft)
plt.grid(color='#dcdcdc', linestyle='--', linewidth=0.5)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_xticks(np.arange(0, 10, 1))  # X-axis ticks from 0 to 10
ax.set_yticks(np.arange(0, 10, 1))  # Y-axis ticks from 0 to 10

offsetx = -0.5
offsety = -0.75
for i, (r1i, r2i) in enumerate(zip(ranks[0], ranks[1])):
    ax.text(r1i + offsetx, r2i + offsety, f'{df.iloc[i, -1]}',
            bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.01'))
plt.savefig('mcdm_all.png', format='png', dpi=300)
plt.show()

fig, ax = plt.subplots(figsize=(5, 4), dpi=150, tight_layout=True)

x_values = np.linspace(1, 179, 180)  # Create x values
y_values = x_values  # y = x line
ax.plot(x_values, y_values, color='black', linestyle='--', label='y = x', zorder=2)  # Plot y = x line

for i in range(len(ranks[0])):
    ax.scatter(ranks[0][i], ranks[1][i], c=ranks[2][i], zorder=3)
plt.xlabel("TOPSIS", fontsize=ft)
plt.ylabel("SPOTIS", fontsize=ft)
plt.xticks(fontsize=ft)
plt.yticks(fontsize=ft)
# Custom legend
custom_legend = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor=colors[5], markersize=10, label='Case A1'),  # Dot for Case A1
    Line2D([0], [0], marker='o', color='w', markerfacecolor=colors[3], markersize=10, label='Case A2'),  # Dot for Case A2
    Line2D([0], [0], marker='o', color='w', markerfacecolor=colors[1], markersize=10, label='Case B1'),  # Dot for Case B1
    Line2D([0], [0], marker='o', color='w', markerfacecolor=colors[0], markersize=10, label='Case B2'),  # Dot for Case B2
]
ax.scatter(1, 4, c=colors[-1], marker='*', s=300, label='Optimum', zorder=1)
# Add the legend to the plot
plt.legend(handles=custom_legend, loc='best', fontsize=ft)
plt.grid(color='#dcdcdc', linestyle='--', linewidth=0.5)
plt.savefig('mcdm_best.png', format='png', dpi=300)
plt.show()