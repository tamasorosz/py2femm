import matplotlib.pyplot as plt
import pandas as pd

# Read CSV files
dfA = pd.read_csv("caseA.csv")
dfB = pd.read_csv("caseB.csv")

xA, yA = dfA.iloc[:, 0], dfA.iloc[:, 1]
xB, yB = dfB.iloc[:, 0], dfB.iloc[:, 1]

# Define colors
colors = ["#B90276", "#50237F", "#00A8B0", "#006249", "#525F6B",
          "#FF5733", "#2E86C1", "#28B463", "#F1C40F", "#8E44AD"]

plt.figure(figsize=(8, 6))

# Plot cases
plt.plot(xA, yA, color=colors[0], linewidth=2, label="case A", alpha=1)
plt.plot(xB, yB, color=colors[1], linewidth=2, label="case B", alpha=0.5)

# Labels and title
plt.xlabel("Relative rotor position [mm]", fontsize=18)
plt.ylabel("Flux density [T]", fontsize=18)

# Example horizontal lines
lines = [
    (0, 5.5, 0.25),
    (0, 5.5, 0.5),
    (0, 6.4, 0.65),
    (0, 6.4, 0.89)
]

for x_start, x_end, y_val in lines:
    plt.plot([x_start, x_end], [y_val, y_val], color='gray', linestyle='--', linewidth=1.5)
    # Place text slightly above the line
    plt.text(x_start+ 0.1, y_val, f'{y_val} T', fontsize=12, color='gray', va='bottom')

# Legend
plt.legend(fontsize=18)

# Grid
plt.grid(True, linestyle="--", alpha=0.6)

plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

plt.tight_layout()
plt.savefig('absoluteflux.png', dpi=300)
plt.show()