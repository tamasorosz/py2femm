import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pandas.core.interchange.dataframe_protocol import DataFrame
import seaborn as sns

with open ('all_res_avg_case0_20250202.csv', 'r') as f:
    df_202 = pd.read_csv(f)

with open('all_res_avg_case0_20250306.csv', 'r') as f:
    df_306 = pd.read_csv(f)

with open('all_res_avg_case0_20250310.csv', 'r') as f:
    df_310 = pd.read_csv(f)

with open('all_res_avg_case0_20250314.csv', 'r') as f:
    df_314 = pd.read_csv(f)
    df_314['AVG'] = df_314['AVG'] * -1

with open('all_res_avg_case0_20250316.csv', 'r') as f:
    df_316 = pd.read_csv(f)

with open('all_res_avg_case0_20250326.csv', 'r') as f:
    df_326 = pd.read_csv(f)
    df_326['AVG'] = df_326['AVG'] * -1

with open('all_res_avg_case0_20250330.csv', 'r') as f:
    df_330 = pd.read_csv(f)
    df_330['AVG'] = df_330['AVG'] * -1

# HEATMAP M330
# ---------------------------------------------------------------------------------------------------------------------
# Compute correlation matrix
corr = df_330.corr()

# Select the subset (last 2 rows, first 6 columns)
subset = corr.iloc[-2:, :6]

# Set figure size and style
plt.figure(figsize=(8, 4))
sns.set_style("whitegrid")

# Create heatmap with enhancements
ax = sns.heatmap(
    subset, annot=True, cmap="coolwarm", fmt=".2f",
    linewidths=2, linecolor='white',  # Thick gridlines
    annot_kws={"size": 18, "weight": "bold", "color": "white"},  # Bigger, bold annotations
    cbar_kws={'shrink': 0.98, 'aspect': 10}  # Adjust color bar size
)

# Customize colorbar font size
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=18)  # Set font size for colorbar

# Center x-tick labels
ax.set_xticks(np.arange(len(subset.columns)) + 0.5)
ax.set_xticklabels(subset.columns, fontsize=18, ha="center")

# Center y-tick labels (optional, but keeps everything aligned)
ax.set_yticks(np.arange(len(subset.index)) + 0.5)
ax.set_yticklabels(subset.index, fontsize=18, rotation=0)

# Display plot
plt.savefig('heatmap_M330.png', dpi=300)
plt.show()
# ---------------------------------------------------------------------------------------------------------------------

# HEATMAP M314
# ---------------------------------------------------------------------------------------------------------------------
# Compute correlation matrix
corr = df_326.corr()

# Select the subset (last 2 rows, first 6 columns)
subset = corr.iloc[-2:, :6]

# Set figure size and style
plt.figure(figsize=(8, 4))
sns.set_style("whitegrid")

# Create heatmap with enhancements
ax = sns.heatmap(
    subset, annot=True, cmap="coolwarm", fmt=".2f",
    linewidths=2, linecolor='white',  # Thick gridlines
    annot_kws={"size": 18, "weight": "bold", "color": "white"},  # Bigger, bold annotations
    cbar_kws={'shrink': 0.98, 'aspect': 10}  # Adjust color bar size
)

# Customize colorbar font size
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=18)  # Set font size for colorbar

# Center x-tick labels
ax.set_xticks(np.arange(len(subset.columns)) + 0.5)
ax.set_xticklabels(subset.columns, fontsize=18, ha="center")

# Center y-tick labels (optional, but keeps everything aligned)
ax.set_yticks(np.arange(len(subset.index)) + 0.5)
ax.set_yticklabels(subset.index, fontsize=18, rotation=0)

# Display plot
plt.savefig('heatmap_M326.png', dpi=300)
plt.show()
# ---------------------------------------------------------------------------------------------------------------------