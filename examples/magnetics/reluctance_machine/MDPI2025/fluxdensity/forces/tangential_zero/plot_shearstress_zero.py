import csv

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

with open('outputA.csv', 'r') as f:
    reader = list(csv.reader(f))
    dfA = [float(row) for row in reader[0]]

with open('outputB.csv', 'r') as f:
    reader = list(csv.reader(f))
    dfB = [float(row) for row in reader[0]]

colors = ["#B90276", "#50237F", "#00A8B0", "#006249", "#525F6B",
          "#FF5733", "#2E86C1", "#28B463", "#F1C40F", "#8E44AD"]

plt.figure(figsize=(8, 6))

# Plot cases
plt.plot(dfA, color=colors[0], linewidth=2, label="case A", alpha=1)
plt.plot(dfB, color=colors[1], linewidth=2, label="case B", alpha=0.5)

# Labels and title
plt.xlabel("Position on rotor circumference [deg]", fontsize=18)
plt.ylabel("Tangential stress [N/mm\u00B2]", fontsize=18)

plt.hlines(0, 0, len(dfA), color='gray', linestyle='--', linewidth=1.5)

# Legend
plt.legend(fontsize=18)

# Grid
plt.grid(True, linestyle="--", alpha=0.6)

# Suppose your x-axis is based on len(dfA)
n = len(dfA)

# Define tick labels you want
tick_labels = [0, 15, 30, 45, 60, 75, 90]

# Map them to positions (index range 0 → n-1)
tick_positions = np.linspace(0, n-1, len(tick_labels))

# Apply to plot
plt.xticks(tick_positions, tick_labels, fontsize=18)

# Draw vertical lines at 15° and 75°
x15 = np.interp(15, tick_labels, tick_positions)
x45 = np.interp(45, tick_labels, tick_positions)
x75 = np.interp(75, tick_labels, tick_positions)

plt.axvline(x=x15, color='grey', linestyle='--', linewidth=2)
plt.axvline(x=x45, color='grey', linestyle='--', linewidth=2)
plt.axvline(x=x75, color='grey', linestyle='--', linewidth=2)

# Add text between lines
plt.text(x15/2, plt.ylim()[1]*-0.75, 'T4', ha='center', fontsize=24)
plt.text((x15+x45)/2, plt.ylim()[1]*-0.75, 'T3', ha='center', fontsize=24)
plt.text((x45+x75)/2, plt.ylim()[1]*-0.75, 'T2', ha='center', fontsize=24)
plt.text((x75 + (n-1))/2, plt.ylim()[1]*-0.75, 'T1', ha='center', fontsize=24)

plt.yticks(fontsize=18)

plt.tight_layout()
plt.savefig('tangentialstress_zero.png', dpi=300)
plt.show()