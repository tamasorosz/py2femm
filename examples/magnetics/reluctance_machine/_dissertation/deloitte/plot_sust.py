import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

colors = ["#B90276", "#50237F", "#00A8B0", "#006249", "#525F6B",
          "#FF5733", "#2E86C1", "#28B463", "#F1C40F", "#8E44AD"]

data_range = {
    "China": [38, 42, 19],
    "Germany": [54, 40, 44],
    "India": [35, 43, 36],
    "Japan": [40, 48, 50],
    "Rep. of Korea": [26, 48, 38],
    "Southeast Asia": [43, 45, 43],
    "UK": [52, None, None],
    "USA": [49, 50, 52],
    "Year": [2025, 2024, 2023]
}

data_cost = {
    "China": [22, 40, 29],
    "Germany": [45, 55, 57],
    "India": [32, 39, 32],
    "Japan": [40, 41, 43],
    "Rep. of Korea": [24, 36, 36],
    "Southeast Asia": [37, 43, 43],
    "UK": [49, None, None],
    "USA": [44, 49, 48],
    "Year": [2025, 2024, 2023]
}

data_sust = {
    "China": [24, 21, 29],
    "Germany": [22, 23, 32],
    "India": [30, 30, 36],
    "Japan": [11, 13, 24],
    "Rep. of Korea": [10, 13, 24],
    "Southeast Asia": [23, 22, 33],
    "UK": [21, None, None],
    "USA": [20, 20, 30],
    "Year": [2025, 2024, 2023]
}
# Create DataFrame
df_range = pd.DataFrame(data_range)
df_cost = pd.DataFrame(data_cost)
df_sust = pd.DataFrame(data_sust)

countries = ["China", "Germany", "India", "USA"]

# Convert to 2D array and reverse rows so 2023 is first
values = np.array([data_sust[c] for c in countries]).T[::-1]

n_groups = len(countries)
n_bars = values.shape[0]
bar_width = 0.2
x = np.arange(n_groups)

# Create plot with specified size
fig, ax = plt.subplots(figsize=(8, 6))
a = 20

# Place grid behind bars
ax.set_axisbelow(True)
ax.grid(True, linestyle='--', alpha=0.7)

# Plot bars with zorder > 0 to ensure they are on top of grid
for i in range(n_bars):
    ax.bar(x + i*bar_width, values[i], width=bar_width, color=colors[i+2],
           label=f'Year {2023+i}', zorder=2)

# Set ticks, labels, title with font size a
ax.set_xticks(x + bar_width)
ax.set_xticklabels(countries, fontsize=a)
ax.set_ylabel("Percentage of participants [%]", fontsize=a)
ax.tick_params(axis='y', labelsize=a)
ax.set_yticks(np.arange(0, 46, 5), minor=True)

# Legend with larger font
ax.legend(fontsize=18)

plt.savefig('deloitte_sustainability.png', dpi=300)
plt.show()