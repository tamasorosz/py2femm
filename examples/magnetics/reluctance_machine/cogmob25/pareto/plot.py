import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pandas.core.interchange.dataframe_protocol import DataFrame

with open ('nsga2_case0_p100o100g200_var6_20250202.csv', 'r') as f:
    df_202p = pd.read_csv(f)

with open('nsga2_case0_p100o100g200_var6_20250306.csv', 'r') as f:
    df_306p = pd.read_csv(f)

with open('nsga2_case0_p100o100g200_var6_20250310.csv', 'r') as f:
    df_310p = pd.read_csv(f)

with open('nsga2_case0_p100o100g200_var6_20250314.csv', 'r') as f:
    df_314p = pd.read_csv(f)

with open('nsga2_case0_p100o100g200_var6_20250316.csv', 'r') as f:
    df_316p = pd.read_csv(f)

with open('nsga2_case0_p100o100g200_var6_20250326.csv', 'r') as f:
    df_326p = pd.read_csv(f)

with open('nsga2_case0_p100o100g200_var6_20250330.csv', 'r') as f:
    df_330p = pd.read_csv(f)

with open('nsga2_const_p50o25g100.csv', 'r') as f:
    df_base = pd.read_csv(f)


# Define colors and labels
colors = ["#B90276", "#50237F", "#00A8B0", "#006249", "#525F6B",
          "#FF5733", "#2E86C1", "#28B463", "#F1C40F", "#8E44AD"]

labels = ["M202", "M306", "M314", "M316", "M326", "M330", "Base"]

# Create figure
plt.figure(figsize=(8, 6))

# Scatter plots with colors and labels

plt.scatter(df_314p.iloc[:, -2] * -1, df_314p.iloc[:, -1], color=colors[0], label="M314", s=150, edgecolors="black", alpha=0.8)
plt.scatter(df_316p.iloc[:, -2] * -1, df_316p.iloc[:, -1], color=colors[1], label="M316", s=80, edgecolors="black", alpha=0.8)
plt.scatter(df_326p.iloc[:, -2] * -1, df_326p.iloc[:, -1], color=colors[2], label="M326", s=80, edgecolors="black", alpha=0.8)
plt.scatter(df_330p.iloc[:, -2] * -1, df_330p.iloc[:, -1], color=colors[3], label="M330", s=80, edgecolors="black", alpha=0.8)

# Labels and title
plt.xlabel("Average torque [mNm]", fontsize=18)
plt.ylabel("Torque ripple [%]", fontsize=18)

# Set tick font sizes
plt.xticks(fontsize=18)  # X-axis ticks
plt.yticks(fontsize=18)  # Y-axis ticks

# Legend
plt.legend(fontsize=18, loc="best", frameon=True, edgecolor="black")

# Show plot
plt.savefig('pareto_front.png', dpi=300)
plt.show()