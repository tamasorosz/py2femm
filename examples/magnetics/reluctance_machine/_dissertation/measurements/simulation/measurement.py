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

# === Load and process other data ===
df_raw = pd.read_csv('res4.csv').values.flatten().tolist()
rotated = rotate_right(df_raw, 192)
y = [(a + b - 0.02) for a, b in zip(df_raw, rotated)] * 4

# === Plot settings ===
colors = ["#B90276", "#50237F", "#00A8B0", "#006249", "#525F6B",
          "#FF5733", "#2E86C1", "#28B463", "#F1C40F", "#8E44AD"]

plt.figure(figsize=(8, 6))
plt.rcParams.update({'font.size': 18})

# Plot original data and combined harmonic
plt.plot(rotate_right(df1['Forward'].tolist()[0:1024],8), color=colors[0], label='Measurement', linewidth=1)
plt.plot(y, color=colors[2], label='Simulation', linewidth=3, linestyle='--')

# === Final styling ===
plt.xlabel("Sample Index", fontsize=18)
plt.ylabel("Amplitude [Nm]", fontsize=18)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(fontsize=16, ncol=2)
plt.tight_layout()
plt.savefig('measurement_cogging_comparison.png', dpi=300)
plt.show()