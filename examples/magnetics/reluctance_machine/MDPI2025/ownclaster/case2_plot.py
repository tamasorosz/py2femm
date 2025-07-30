import pandas as pd
from matplotlib import pyplot as plt

clusters = pd.read_csv('case2_s001_e1_p19_average.csv')

# Create figure and first axis
fig, ax1 = plt.subplots(figsize=(10, 6))

# Unpack clusters into separate lists for plotting
thresholds = clusters['threshold'].tolist()
num_clusters = clusters['clusters'].tolist()
max_avg = clusters['distance_avg'].tolist()
max_rip = clusters['distance_rip'].tolist()
max_cog = clusters['distance_cog'].tolist()

# Plot number of clusters (left y-axis)
ax1.set_xlabel('Threshold')
ax1.set_ylabel('Number of Remaining Designs (Clusters)', color='tab:blue')
ax1.plot(thresholds, num_clusters, 'o-', label='Remaining Designs', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Create second y-axis
ax2 = ax1.twinx()

# Plot torque differences (right y-axis)
ax2.set_ylabel('Torque Differences (normalized)', color='tab:red')
ax2.plot(thresholds, max_avg, 's-', label='AVG Torque Δ', color='tab:red')
ax2.plot(thresholds, max_rip, '^-', label='Ripple Torque Δ', color='tab:orange')
ax2.plot(thresholds, max_cog, 'd-', label='Cogging Torque Δ', color='tab:green')
ax2.tick_params(axis='y', labelcolor='tab:red')

# Combine legends from both axes
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

plt.grid(True)
plt.title('Clustering Threshold vs. Torque Characteristics')
plt.tight_layout()
plt.show()