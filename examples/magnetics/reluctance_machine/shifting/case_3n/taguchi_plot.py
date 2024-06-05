import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

current_dir = os.getcwd()

# ----------------------------------------------------------------
#  Plot average torque and torque ripple parameter sensitivity for
#  an average on current of [5, 10, 15, 20, 25, 30, 50, 100]

df_avg = pd.read_csv(current_dir + '/results/' + 'taguchi_avg.csv')
df_rip = pd.read_csv(current_dir + '/results/' + 'taguchi_rip.csv')
df_cog = pd.read_csv(current_dir + '/results/' + 'taguchi_cog.csv')
df_thd = pd.read_csv(current_dir + '/results/' + 'taguchi_thd.csv')

y_avg = list(df_avg.iloc[5])
y_rip = list(df_rip.iloc[5])
y_cog = list(df_cog.iloc[5])
y_thd = list(df_thd.iloc[5])

data = [y_avg, y_rip, y_cog, y_thd]

labels = ['AVG', 'RIP', 'COG', 'THD']
n_sets = len(data)
x = np.arange(len(data[0]))
width = 0.20
colors = ["#B90276", '#50237F', '#005691', "#008ECF", '#00A8B0', '#78BE20', "#006249", '#525F6B', '#000']

fig, ax = plt.subplots(figsize=(10, 8))
for i in range(n_sets):
    ax.bar(x + i * width, data[i], width, label=labels[i], color=colors[i])

fs = 20

ax.set_xlabel('Parameters', fontsize=fs)
ax.set_ylabel('\u0394S/N [db]', fontsize=fs)
ax.set_xticks(x + width * (n_sets - 1) / 2)
ax.set_xticklabels(['X1', 'X2', 'X3', 'X4'])
ax.tick_params(axis='both', which='major', labelsize=fs)
ax.grid(True, which='both', linestyle='--', linewidth=0.5)
ax.legend(fontsize=fs)
plt.show()



