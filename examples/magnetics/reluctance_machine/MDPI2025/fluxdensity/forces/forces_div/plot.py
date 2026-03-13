import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

dfA = pd.read_csv('forces_caseA')
dfB = pd.read_csv('forces_caseB')

colors = ["#B90276", "#50237F", "#00A8B0", "#006249", "#525F6B",
          "#FF5733", "#2E86C1", "#28B463", "#F1C40F", "#8E44AD"]

plt.figure(figsize=(8, 6))

posA = [x+y for x, y in zip(dfA.iloc[:, 1], dfA.iloc[:, 3])]
negA = [x+y for x, y in zip(dfA.iloc[:, 2], dfA.iloc[:, 4])]

posB = [x+y for x, y in zip(dfB.iloc[:, 1], dfB.iloc[:, 3])]
negB = [x+y for x, y in zip(dfB.iloc[:, 2], dfB.iloc[:, 4])]

diffA = [n-p for n,p in zip(negA,posA)]
diffB = [n-p for n,p in zip(negB,posB)]

plt.fill_between(
    range(len(posA)), diffA, diffB,
    facecolor="none",
    edgecolor="gray",
    hatch="|",        # vertical stripes
    linewidth=0.0     # make stripes thicker
)

plt.plot(diffA, color=colors[3], linewidth=2, label="case A")
plt.plot(diffB, color=colors[5], linewidth=2, label="case B", linestyle='--')

tick_positions = np.linspace(0, 15, 16)
label_values = np.linspace(0, 7.5, 4)
label_positions = np.linspace(tick_positions[0], tick_positions[-1], len(label_values))
plt.xticks(label_positions, [f'{val:.1f}' for val in label_values], fontsize=18)

plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=18)
plt.ylim(-0.5, 5.5)
plt.yticks(np.arange(0, 6, 1), fontsize=18)

plt.xlabel("Rotor position [deg]", fontsize=18)
plt.ylabel("Tangential force [N]", fontsize=18)

plt.savefig('forces_div.png', dpi=300)
plt.show()
