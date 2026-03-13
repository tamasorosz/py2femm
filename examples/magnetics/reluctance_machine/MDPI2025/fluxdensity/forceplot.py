import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Read CSV files
dfAr = pd.read_csv("caseAr.csv")
dfBr = pd.read_csv("caseBr.csv")

xAr, yAr = dfAr.iloc[:, 0], dfAr.iloc[:, 1]
xBr, yBr = dfBr.iloc[:, 0], dfBr.iloc[:, 1]

# Read CSV files
dfAt = pd.read_csv("caseAt.csv")
dfBt = pd.read_csv("caseBt.csv")

xAt, yAt = dfAt.iloc[:, 0], dfAt.iloc[:, 1]
xBt, yBt = dfBt.iloc[:, 0], dfBt.iloc[:, 1]

# Define colors
colors = ["#B90276", "#50237F", "#00A8B0", "#006249", "#525F6B",
          "#FF5733", "#2E86C1", "#28B463", "#F1C40F", "#8E44AD"]

plt.figure(figsize=(8, 6))

x = np.linspace(0, 44, len(xAt))

# Plot cases
plt.plot(x, [-Ar*At/(4*np.pi*1e-7)/1e6 for Ar, At in zip(yAr, yAt)], color=colors[2], linewidth=2, label="case A", alpha=1)
plt.plot(x, [-Br*Bt/(4*np.pi*1e-7)/1e6 for Br, Bt in zip(yBr, yBt)], color=colors[5], linewidth=2, label="case B", alpha=0.5)

# Labels and title
plt.xlabel("Rotor position [deg]", fontsize=18)
plt.ylabel("Tangential stress [N/mm\u00B2]", fontsize=18)

plt.plot([15.2, 15.2], [-0.31, 0.10], color='gray', linestyle='--', linewidth=1.5)
plt.text(5, -0.2, 'T1', fontsize=40, color='gray', va='bottom')
plt.text(30, -0.2, 'T2', fontsize=40, color='gray', va='bottom')

# Legend
plt.legend(fontsize=18)

# Grid
plt.grid(True, linestyle="--", alpha=0.6)

plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

plt.tight_layout()
plt.savefig('sheerstress.png', dpi=300)
plt.show()