import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse

df_base = pd.read_csv('../../cogmob24/nsga2_const_p50o25g100.csv')

df_x = df_base.iloc[:, 0:5]
df_x = np.round(df_x, 1)

df_y = df_base.iloc[:, -2:]
df_y.iloc[:, 0] *= -1
df_y.iloc[:, 1] *= 100
df_y = np.round(df_y, 1)

colors = ["#B90276", '#50237F', '#005691', "#008ECF", '#00A8B0', '#78BE20', "#006249", '#525F6B', '#000']

# pareto ---------------------------------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 8))
ax.scatter(df_y.iloc[:, 1], df_y.iloc[:, 0], label='Non-dominated designs', color=colors[1], linewidth=5, linestyle='-')
ax.grid(True, which='both', linestyle='--', linewidth=0.5)
ax.set_xlabel('Torque ripple [%]', fontsize=20)
ax.set_ylabel('Average torque [mNm]', fontsize=20)
ax.tick_params(axis='both', which='major', labelsize=20)
ax.legend(fontsize=20, loc='upper left')

ax = plt.gca()
ellipse = Ellipse((38, 1150), 10, 500, edgecolor=colors[0], facecolor='none', linewidth=3)
ax.add_patch(ellipse)

ax = plt.gca()
ellipse = Ellipse((55, 1701), 1, 30, edgecolor=colors[2], facecolor=colors[2], linewidth=3)
ax.add_patch(ellipse)

ax = plt.gca()
ellipse = Ellipse((41.4, 1428), 1, 30, edgecolor=colors[2], facecolor=colors[2], linewidth=3)
ax.add_patch(ellipse)

ax = plt.gca()
ellipse = Ellipse((47.2, 1565), 1, 30, edgecolor=colors[2], facecolor=colors[2], linewidth=3)
ax.add_patch(ellipse)

ax = plt.gca()
ellipse = Ellipse((57.3, 1724), 1, 30, edgecolor=colors[2], facecolor=colors[2], linewidth=3)
ax.add_patch(ellipse)

plt.annotate('Entropy weighted', xy=(47.2, 1565), xytext=(35, 1625),
             arrowprops=dict(facecolor=colors[3], shrink=0.05),
             fontsize=20, color='black', ha='center')

plt.annotate('Entropy weighted', xy=(41.4, 1428), xytext=(35, 1625),
             arrowprops=dict(facecolor=colors[3], shrink=0.05),
             fontsize=20, color='black', ha='center')

plt.annotate('Variance weighted', xy=(55, 1701), xytext=(55, 1400),
             arrowprops=dict(facecolor=colors[3], shrink=0.05),
             fontsize=20, color='black', ha='center')

plt.annotate('Variance weighted', xy=(57.3, 1724), xytext=(55, 1400),
             arrowprops=dict(facecolor=colors[3], shrink=0.05),
             fontsize=20, color='black', ha='center')



plt.savefig('figures/cogmob_pareto', bbox_inches='tight')
plt.show()

# df_base = pd.read_csv('results/cogmob_dynamic.csv')
# df_base.iloc[:, :] *= -1
#
# f = pd.DataFrame(np.round(df_base, 1))
#
# colors = ["#B90276", '#50237F', '#005691', "#008ECF", '#00A8B0', '#78BE20', "#006249", '#525F6B', '#000']
#
# # avg ---------------------------------------------------------------------------------------------------------
# fig, ax = plt.subplots(figsize=(10, 8))
# ax.plot(f.iloc[:, 0], label='Variance weighted (V)', color=colors[0], linewidth=5, linestyle='-')
# ax.plot(f.iloc[:, 1], label='Entropy weighted (E)', color=colors[1], linewidth=5, linestyle='-')
# ax.grid(True, which='both', linestyle='--', linewidth=0.5)
# ax.set_xlabel('Rotor position [deg]', fontsize=20)
# ax.set_ylabel('Average torque [mNm]', fontsize=20)
# ax.tick_params(axis='both', which='major', labelsize=20)
#
#
# ax.axhline(y=np.mean(f.iloc[:, 0]), color=colors[0], linestyle='--', linewidth=2,
#                label='avg(V): ' + f'{1701.3}' + ' mNm')
# ax.axhline(y=np.mean(f.iloc[:, 1]), color=colors[1], linestyle='--', linewidth=2,
#                label='avg(E): ' + f'{1565.1}' + ' mNm')
#
# ripV = (np.max(f.iloc[:, 0])-np.min(f.iloc[:, 0]))/np.mean(f.iloc[:, 0])
# ripE = (np.max(f.iloc[:, 1])-np.min(f.iloc[:, 1]))/np.mean(f.iloc[:, 1])
# ripV = np.round(ripV, 1)*100
# ripE = np.round(ripE, 1)*100
# ax.plot([], color=colors[0], linestyle='None', label='rip(V): ' + f'{55.0}' + ' %')
# ax.plot([], color=colors[1], linestyle='None', label='rip(E): ' + f'{47.2}' + ' %')
#
# plt.subplots_adjust(bottom=0.25)
#
# plt.yticks(np.linspace(1250, 2250, 6), np.linspace(1200, 2200, 6, dtype=int))
#
# ax.legend(fontsize=16,loc='upper center', ncol=3, bbox_to_anchor=(0.47, -0.125))
# plt.savefig('figures/cogmob_avg', bbox_inches='tight')
# plt.show()