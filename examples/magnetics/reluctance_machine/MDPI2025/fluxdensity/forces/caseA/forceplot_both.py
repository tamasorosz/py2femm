import csv

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Read CSV files
dfArl = pd.read_csv("caseAr_left.csv")
dfAtl = pd.read_csv("caseAt_left.csv")

# Read CSV files
dfArr = pd.read_csv("caseAr_right.csv")
dfAtr = pd.read_csv("caseAt_right.csv")

# Define colors
colors = ["#B90276", "#50237F", "#00A8B0", "#006249", "#525F6B",
          "#FF5733", "#2E86C1", "#28B463", "#F1C40F", "#8E44AD"]

plt.figure(figsize=(8, 6))

x = np.linspace(0, 90, 5998)

# for i in range(len(dfArl.columns)):
for i in range(6,7):
    yArl = dfArl.iloc[:, i].tolist()
    yArr = [e for e in dfArr.iloc[:, i].tolist()]
    yAr = yArl + yArr

    yAtl = dfAtl.iloc[:, i].tolist()
    yAtr = [e for e in dfAtr.iloc[:, i].tolist()]
    yAt = yAtl + yAtr

    with open("../tangential_max/outputA.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([-Ar*At/(4*np.pi*1e-7)/1e6 for Ar, At in zip(yAr, yAt)])

    # Plot cases
    plt.plot(x, [-Ar*At/(4*np.pi*1e-7)/1e6 for Ar, At in zip(yAr, yAt)], color=colors[2], linewidth=2, label="case A", alpha=1)
# plt.plot(x, [-Br*Bt/(4*np.pi*1e-7)/1e6 for Br, Bt in zip(yBr, yBt)], color=colors[5], linewidth=2, label="case B", alpha=0.5)

# Labels and title
plt.xlabel("Rotor position [deg]", fontsize=18)
plt.ylabel("Tangential stress [N/mm\u00B2]", fontsize=18)

# plt.plot([15.2, 15.2], [-0.05, 0.05], color='gray', linestyle='--', linewidth=3)
# plt.text(5, -0.2, 'T1', fontsize=40, color='gray', va='bottom')
# plt.text(30, -0.2, 'T2', fontsize=40, color='gray', va='bottom')

# Legend
# plt.legend(fontsize=18)

# Grid
plt.grid(True, linestyle="--", alpha=0.6)

plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

plt.tight_layout()
# plt.savefig('shearstress_caseA_both.png', dpi=300)
plt.show()