import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# === Load data ===
df1 = pd.read_excel('fipmasynrm1.xlsx')
df2 = pd.read_excel('fipmasynrm2.xlsx')

# === Define helper ===
def rotate_right(arr, k=1):
    k %= len(arr)
    return arr[-k:] + arr[:-k]

# === Load and process other data 2D ===
df_raw = rotate_right(pd.read_csv('2D.csv').values.flatten().tolist(), -45)
rotated_2D = rotate_right(df_raw, 192)
_2D = rotate_right([(a + b) - 0.021 for a, b in zip(df_raw, rotated_2D)] * 6, -10)

# === Plot settings ===
colors = ["#B90276", "#50237F", "#00A8B0", "#006249", "#525F6B",
          "#FF5733", "#2E86C1", "#28B463", "#F1C40F", "#8E44AD"]

plt.figure(figsize=(8, 6))
plt.rcParams.update({'font.size': 18})

# Plot original data and combined harmonic
plt.plot([i * 90/len(_2D) for i in range(len(_2D))],rotate_right(df1['Forward'].tolist()[0:1530],8), color=colors[0], label='Measurement', linewidth=1)
plt.plot([i * 90/len(_2D) for i in range(len(_2D))],_2D, color=colors[2], label='Simulation 2D', linewidth=3, linestyle='--')

# === Final styling ===
plt.xlabel("Rotor position [deg]", fontsize=18)
plt.xticks(np.arange(0, 91, 10))
plt.ylabel("Amplitude [Nm]", fontsize=18)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(fontsize=16, ncol=2)
plt.tight_layout()
plt.savefig('measurement_cogging_comparison_2D.png', dpi=300)
plt.show()

print('2D:', max(df_raw)-min(df_raw))

# # === Load and process other data 3D ===
# df_raw = rotate_right([i / 100000 * 2.2222 for i in pd.read_csv('3D.csv').values.flatten().tolist()], -110)
# rotated_3D = rotate_right(df_raw, 192)
# _3D = rotate_right([(a + b) - 0.021 for a, b in zip(df_raw, rotated_3D)] * 6, -10)
#
# # === Plot settings ===
# colors = ["#B90276", "#50237F", "#00A8B0", "#006249", "#525F6B",
#           "#FF5733", "#2E86C1", "#28B463", "#F1C40F", "#8E44AD"]
#
# plt.figure(figsize=(8, 6))
# plt.rcParams.update({'font.size': 18})
#
# # Plot original data and combined harmonic
# plt.plot([i * 90/len(_3D) for i in range(len(_3D))], rotate_right(df1['Forward'].tolist()[0:1530],8), color=colors[0], label='Measurement', linewidth=1)
# plt.plot([i * 90/len(_3D) for i in range(len(_3D))],_3D, color=colors[3], label='Simulation 3D', linewidth=2, linestyle='-')
#
# # === Final styling ===
# plt.xlabel("Rotor position [deg]", fontsize=18)
# plt.xticks(np.arange(0, 91, 10))
# plt.ylabel("Amplitude [Nm]", fontsize=18)
# plt.grid(True, linestyle='--', alpha=0.5)
# plt.legend(fontsize=16, ncol=2, loc='upper right')
# plt.tight_layout()
# plt.savefig('measurement_cogging_comparison_3D.png', dpi=300)
# plt.show()
#
# print('3D:', max(df_raw)-min(df_raw))