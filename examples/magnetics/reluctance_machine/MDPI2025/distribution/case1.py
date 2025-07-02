import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler

colors = ["#B90276", "#50237F", "#00A8B0", "#006249", "#525F6B",
          "#FF5733", "#2E86C1", "#28B463", "#F1C40F", "#8E44AD"]

with open('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025/refined\case1_all.csv', 'r') as f:
    df = pd.read_csv(f)

del df['ANG']

# FEATURES%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
scaler = MinMaxScaler()
scaled_array = scaler.fit_transform(df.iloc[:, :-3])
X = pd.DataFrame(scaled_array, columns=df.columns[:8])

# Create 2x4 subplots
fig, axes = plt.subplots(2, 4, figsize=(16, 6))
axes = axes.flatten()

# Plot each histogram
for i, col in enumerate(X.columns):
    axes[i].hist(X[col], bins=50, color=colors[3], edgecolor='black')
    axes[i].set_title(f"A{i+1}", fontsize=14)
    axes[i].set_axisbelow(True)
    axes[i].grid(True)
    # Set tick label font sizes
    axes[i].tick_params(axis='both', labelsize=12)

# axes[i].set_xlabel("Value", fontsize=18)
axes[0].set_ylabel("Frequency", fontsize=14)
axes[4].set_ylabel("Frequency", fontsize=14)
axes[4].set_xlabel("Normalised value", fontsize=14)
axes[5].set_xlabel("Normalised value", fontsize=14)
axes[6].set_xlabel("Normalised value", fontsize=14)
axes[7].set_xlabel("Normalised value", fontsize=14)


plt.tight_layout()
# plt.savefig('distribution_case1_params.png', dpi=300)
# plt.show()