import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

current_dir = os.getcwd()

# ----------------------------------------------------------------
#  Plot average torque and torque ripple parameter sensitivity for
#  an average on current of [5, 10, 15, 20, 25, 30, 50, 100]

df_avg = [pd.read_csv(current_dir + '/results/' + f'res_avg_taguchi_{j}A.csv') for j in [5, 10, 15, 20, 25, 50, 75, 100]]
df_rip = [pd.read_csv(current_dir + '/results/' + f'res_rip_taguchi_{j}A.csv') for j in [5, 10, 15, 20, 25, 50, 75, 100]]

df_avg = pd.concat(df_avg, ignore_index=False).groupby(level=0).agg(list)
df_rip = pd.concat(df_rip, ignore_index=False).groupby(level=0).agg(list)

df_avg = df_avg.apply(lambda col: col.apply(lambda x: np.mean(x)))
df_rip = df_rip.apply(lambda col: col.apply(lambda x: np.mean(x)))

df_avg = df_avg.T.sort_values(df_avg.index[-1], ascending=False).T
df_rip = df_rip.T.sort_values(df_avg.index[-1], ascending=False).T
print(df_avg)
print(df_rip)

ind = np.arange(12)
width = 0.3

y1_values = list(df_avg.iloc[3])
y2_values = list(df_rip.iloc[3])

for i in range(len(y1_values)):
    plt.bar(df_avg.iloc[3].index[i], y1_values[i], width, label='AVG', color='blue')
    plt.bar(ind[i] + width, y2_values[i], width, label='RIP', color='green')

plt.xlabel('Parameters')
plt.ylabel('S/N')
plt.title('Parameter sensitivity on average torque and torque ripple')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(['AVG', 'RIP'])
plt.tight_layout()
plt.show()

# ----------------------------------------------------------------
#  Plot average torque and torque ripple parameter sensitivity for
#  on current of [5, 10, 15, 20, 25, 30, 50, 100]

df_avg = [pd.read_csv(current_dir + '/results/' + f'res_avg_taguchi_{j}A.csv') for j in [5, 10, 15, 20, 25, 50, 75, 100]]
df_rip = [pd.read_csv(current_dir + '/results/' + f'res_rip_taguchi_{j}A.csv') for j in [5, 10, 15, 20, 25, 50, 75, 100]]

df_avg = pd.concat(df_avg, ignore_index=False).groupby(level=0).agg(list)
df_rip = pd.concat(df_rip, ignore_index=False).groupby(level=0).agg(list)
for i in range(8):
    plt.plot(df_avg.iloc[3, i], label=f'{df_avg.columns[i]}')
plt.xlabel('Excitation current [A]')
plt.ylabel('S/N [db]')
plt.title('Parameter sensitivity on average torque')
plt.xticks([0, 1, 2, 3, 4, 5, 6, 7], ['5', '10', '15', '20', '25', '50', '75', '100'], rotation=45)
plt.grid(True)
plt.legend(loc='upper left', ncol=4)
plt.tight_layout()
plt.show()

for i in range(8):
    plt.plot(df_rip.iloc[3, i], label=f'{df_rip.columns[i]}')
plt.xlabel('Excitation current [A]')
plt.ylabel('S/N [db]')
plt.title('Parameter sensitivity on torque ripple')
plt.xticks([0, 1, 2, 3, 4, 5, 6, 7], ['5', '10', '15', '20', '25', '30', '50', '100'], rotation=45)
plt.grid(True)
plt.legend(loc='upper left', ncol=4)
plt.tight_layout()
plt.show()