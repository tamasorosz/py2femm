import pandas as pd
from matplotlib import pyplot as plt

clusters = pd.read_csv('case1_m2_s001_e1_average_max_doublecluster_backward_all_noiloc_low_v2.csv')

colors = ["#B90276", "#50237F", "#00A8B0", "#006249", "#525F6B",
          "#FF5733", "#2E86C1", "#28B463", "#F1C40F", "#8E44AD"]

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
ax1.set_xlabel('Threshold', fontsize=16)
ax1.set_ylabel('Number of Medoid Designs [-]', fontsize=16)
ax1.plot(thresholds, num_clusters, 'o-', label='Medoids', color=colors[0])

# Increase tick font size
ax1.tick_params(axis='both', which='major', labelsize=16)

# Create second y-axis
ax2 = ax1.twinx()

# Plot torque differences (right y-axis)
ax2.set_ylabel('Torque Differences (normalised)', fontsize=16)
ax2.plot(thresholds, average_avg, 'd-', label='AVG (MEAN)', color=colors[1])
ax2.plot(thresholds, average_rip, 'd-', label='RIP (MEAN)', color=colors[2])
ax2.plot(thresholds, average_cog, 'd-', label='COG (MEAN)', color=colors[5])

ax2.plot(thresholds, max_avg, 's-', label='AVG (MAX)', color=colors[1])
ax2.plot(thresholds, max_rip, 's-', label='RIP (MAX)', color=colors[2])
ax2.plot(thresholds, max_cog, 's-', label='COG (MAX)', color=colors[5])

# Increase tick font size
ax2.tick_params(axis='both', which='major', labelsize=16)

# Combine legends from both axes
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=14)

# Add vertical and horizontal reference lines
ax1.axvline(x=0.07, color='gray', linestyle='--', linewidth=1.5)
ax1.axhline(y=7029, color='gray', linestyle='--', linewidth=1.5)

# Add labels to the lines
ax1.text(0.07, ax1.get_ylim()[1]*0.975, '0.07',
         rotation=90, color='gray', fontsize=14, va='top', ha='right')

ax1.text(ax1.get_xlim()[1]*0.075, 7029, '7029',
         color='gray', fontsize=14, va='bottom', ha='right')

plt.grid(True)
plt.tight_layout()
plt.savefig('case1_clusters_v2.png', dpi=300)
plt.show()
