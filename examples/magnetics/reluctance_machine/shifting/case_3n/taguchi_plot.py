import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

current_dir = os.getcwd()

# ----------------------------------------------------------------
#  Plot average torque and torque ripple parameter sensitivity for
#  an average on current of [5, 10, 15, 20, 25, 30, 50, 100]

df_avg = pd.read_csv(current_dir + '/results/' + 'taguchi_avg_os.csv')
df_rip = pd.read_csv(current_dir + '/results/' + 'taguchi_rip_os.csv')
df_cog = pd.read_csv(current_dir + '/results/' + 'taguchi_cog_os.csv')
df_thd = pd.read_csv(current_dir + '/results/' + 'taguchi_thd_os.csv')

y_avg = list(df_avg.iloc[5])
y_rip = list(df_rip.iloc[5])
y_cog = list(df_cog.iloc[5])
y_thd = list(df_thd.iloc[5])

data = [y_avg, y_rip, y_cog, y_thd]

labels = ['\u0394Tavg: 45.3 mNm (2.5 %)', '\u0394Trip: 2.1 % (5.7 %)', '\u0394Tcog: 1.5 mNm (10.6 %)', '\u0394Tthd: 2.6 % (2.2 %)']
n_sets = len(data)
x = np.arange(len(data[0]))
width = 0.20
colors = ["#B90276", '#50237F', '#00A8B0', "#006249", '#525F6B', '#000']

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
plt.savefig('figures/sensitivity', bbox_inches='tight')
plt.show()

df_res = pd.read_csv(current_dir + '/results/' + 'taguchi_res_os.csv')
avg = max(df_res.iloc[:, 4]) - min(df_res.iloc[:, 4])
rip = max(df_res.iloc[:, 6]) - min(df_res.iloc[:, 6])
cog = max(df_res.iloc[:, 8]) - min(df_res.iloc[:, 8])
thd = max(df_res.iloc[:, 10]) - min(df_res.iloc[:, 10])
print(avg, rip, cog, thd)