import numpy as np
import pandas as pd
from IPython.core.pylabtools import figsize
from matplotlib import pyplot as plt
from sklearn.feature_selection import f_classif
from sklearn.preprocessing import StandardScaler, MinMaxScaler

with open('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025/refined\case2_all.csv', 'r') as f:
    df = pd.read_csv(f)

del df['ANG']

print(df)

scaler = MinMaxScaler()
scaled_array = scaler.fit_transform(df.iloc[:, :-3])
X = pd.DataFrame(scaled_array, columns=df.columns[:9])
AVG = df.iloc[:, -3]
RIP = df.iloc[:, -2]
COG = df.iloc[:, -1]

f_avg, p_avg = f_classif(X.values, AVG.values)
f_rip, p_rip = f_classif(X.values, RIP.values)
f_cog, p_cog = f_classif(X.values, COG.values)

colors = ["#B90276", "#50237F", "#00A8B0", "#006249", "#525F6B",
          "#FF5733", "#2E86C1", "#28B463", "#F1C40F", "#8E44AD"]

# AVERAGE TORQUE%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
feature_names = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9']
f_scores = f_avg
p_values = p_avg

plt.figure(figsize=(10, 6))
bars = plt.barh(feature_names, f_scores, color=colors[0])
plt.xlabel('F-score', fontsize=18)
plt.ylabel('Features', fontsize=18)
plt.xticks(ticks=np.arange(0,10), fontsize=18)
plt.yticks(fontsize=18)
plt.grid(True)
plt.gca().set_axisbelow(True)

# Add p-values as text next to each bar
for i, (bar, pval) in enumerate(zip(bars, p_values)):
    plt.text(
        bar.get_width() + 0.2,              # X position (just beyond bar)
        bar.get_y() + bar.get_height() / 2, # Y position (center of bar)
        f'p={pval:.3g}',                    # Format p-value
        va='center', fontsize=18, color='black',
        bbox = dict(facecolor='white', alpha=1, edgecolor='none', boxstyle='round,pad=0.2')
    )

plt.gca().invert_yaxis()  # Highest score at top
plt.tight_layout()
plt.savefig('sensitivity_case2_avg.png', dpi=300)
plt.show()



# TORQUE RIPPLE%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
f_scores = f_rip
p_values = p_rip

plt.figure(figsize=(10, 6))
bars = plt.barh(feature_names, f_scores, color=colors[1])
plt.xlabel('F-score', fontsize=18)
plt.ylabel('Features', fontsize=18)
plt.xticks(ticks=np.arange(0,10), fontsize=18)
plt.yticks(fontsize=18)
plt.grid(True)
plt.gca().set_axisbelow(True)

# Add p-values as text next to each bar
for i, (bar, pval) in enumerate(zip(bars, p_values)):
    plt.text(
        bar.get_width() + 0.2,              # X position (just beyond bar)
        bar.get_y() + bar.get_height() / 2, # Y position (center of bar)
        f'p={pval:.3g}',                    # Format p-value
        va='center', fontsize=18, color='black',
        bbox = dict(facecolor='white', alpha=1, edgecolor='none', boxstyle='round,pad=0.2')
    )

plt.gca().invert_yaxis()  # Highest score at top
plt.tight_layout()
plt.savefig('sensitivity_case2_rip.png', dpi=300)
plt.show()



# COGGING TORQUE%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
f_scores = f_cog
p_values = p_cog

plt.figure(figsize=(10, 6))
bars = plt.barh(feature_names, f_scores, color=colors[2])
plt.xlabel('F-score', fontsize=18)
plt.ylabel('Features', fontsize=18)
plt.xticks(ticks=np.arange(0,150,20), fontsize=18)
plt.yticks(fontsize=18)
plt.grid(True)
plt.gca().set_axisbelow(True)

# Add p-values as text next to each bar
for i, (bar, pval) in enumerate(zip(bars, p_values)):
    plt.text(
        bar.get_width() + 2,              # X position (just beyond bar)
        bar.get_y() + bar.get_height() / 2, # Y position (center of bar)
        f'p={pval:.3g}',                    # Format p-value
        va='center', fontsize=18, color='black',
        bbox = dict(facecolor='white', alpha=1, edgecolor='none', boxstyle='round,pad=0.2')
    )

plt.gca().invert_yaxis()  # Highest score at top
plt.tight_layout()
plt.savefig('sensitivity_case2_cog.png', dpi=300)
plt.show()

