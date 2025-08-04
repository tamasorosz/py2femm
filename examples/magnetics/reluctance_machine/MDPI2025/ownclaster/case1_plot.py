import pandas as pd
from matplotlib import pyplot as plt

# clusters = pd.read_csv('case1_m2_s001_e2_average_doublecluster_random.csv')
# clusters = pd.read_csv('case1_m2_s001_e2_average_doublecluster_forward.csv')
clusters = pd.read_csv('case1_m2_s001_e2_average_doublecluster_backward.csv')

# Create figure and first axis
fig, ax1 = plt.subplots(figsize=(10, 6))

# Unpack clusters into separate lists for plotting
thresholds = clusters['threshold'].tolist()
num_clusters = clusters['clusters'].tolist()
average_avg = clusters['distance_avg_average'].tolist()
average_rip = clusters['distance_rip_average'].tolist()
average_cog = clusters['distance_cog_average'].tolist()
max_avg = clusters['distance_avg_max'].tolist()
max_rip = clusters['distance_rip_max'].tolist()
max_cog = clusters['distance_cog_max'].tolist()

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

# Add vertical line at threshold = 1.5
ax1.axvline(x=0.15, color='gray', linestyle='--', linewidth=1.5)
ax1.axhline(y=1552, color='gray', linestyle='--', linewidth=1.5)

plt.grid(True)
plt.title('Clustering Threshold vs. Torque Characteristics')
plt.tight_layout()
plt.show()