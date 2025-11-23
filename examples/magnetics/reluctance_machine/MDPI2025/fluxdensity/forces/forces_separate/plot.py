import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

dfA = pd.read_csv('forces_caseA')

colors = ["#B90276", "#50237F", "#00A8B0", "#006249", "#525F6B",
          "#FF5733", "#2E86C1", "#28B463", "#F1C40F", "#8E44AD"]

plt.figure(figsize=(8, 6))

plt.plot(dfA.iloc[:, 1], color=colors[0], linewidth=2, label="T4")
plt.plot(dfA.iloc[:, 2], color=colors[1], linewidth=2, label="T3", linestyle='--')
plt.plot(dfA.iloc[:, 3], color=colors[2], linewidth=2, label="T2")
plt.plot(dfA.iloc[:, 4], color=colors[5], linewidth=2, label="T1", linestyle='--')

tick_positions = np.linspace(0, 15, 16)
label_values = np.linspace(0, 7.5, 4)
label_positions = np.linspace(tick_positions[0], tick_positions[-1], len(label_values))
plt.xticks(label_positions, [f'{val:.1f}' for val in label_values], fontsize=18)

plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=18, loc='lower left')
plt.ylim(-0.5, 12.5)
plt.yticks(np.arange(0, 13, 2), fontsize=18)

plt.xlabel("Rotor position [deg]", fontsize=18)
plt.ylabel("Tangential force [N]", fontsize=18)

plt.savefig('forces_separate_A.png', dpi=300)
plt.show()
