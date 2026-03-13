import pandas as pd
import matplotlib.pyplot as plt

# === Load data ===
clusters = pd.read_csv('case1_m2_s001_e1_average_max_doublecluster_backward_all_noiloc_low_v2.csv')

colors = ["#B90276", "#50237F", "#00A8B0", "#006249", "#525F6B",
          "#FF5733", "#2E86C1", "#28B463", "#F1C40F", "#8E44AD"]

# === Main plot ===
fig, ax1 = plt.subplots(figsize=(10, 6))

thresholds = clusters['threshold']
num_clusters = clusters['clusters']
average_avg = clusters['distance_avg_average']
average_rip = clusters['distance_rip_average']
average_cog = clusters['distance_cog_average']
max_avg = clusters['distance_avg_max']
max_rip = clusters['distance_rip_max']
max_cog = clusters['distance_cog_max']

# Left axis
ax1.set_xlabel('Threshold', fontsize=18)
ax1.set_ylabel('Number of Medoid Designs [-]', fontsize=18)
ax1.plot(thresholds, num_clusters, 'o-', label='Medoids', color=colors[0])
ax1.tick_params(axis='both', labelsize=16)

# Right axis
ax2 = ax1.twinx()
ax2.set_ylabel('Torque Differences (normalised)', fontsize=18)
ax2.plot(thresholds, average_avg, 'd-', label='AVG (MEAN)', color=colors[1])
ax2.plot(thresholds, average_rip, 'd-', label='RIP (MEAN)', color=colors[2])
ax2.plot(thresholds, average_cog, 'd-', label='COG (MEAN)', color=colors[5])
ax2.plot(thresholds, max_avg, 's-', label='AVG (MAX)', color=colors[1])
ax2.plot(thresholds, max_rip, 's-', label='RIP (MAX)', color=colors[2])
ax2.plot(thresholds, max_cog, 's-', label='COG (MAX)', color=colors[5])
ax2.tick_params(axis='both', labelsize=16)

# Reference lines
ax1.axvline(x=0.07, color='gray', linestyle='--', linewidth=1.5)
ax1.axhline(y=7029, color='gray', linestyle='--', linewidth=1.5)
ax1.text(0.07, ax1.get_ylim()[1]*0.975, '0.07',
         rotation=90, color='gray', fontsize=18, va='top', ha='right')
ax1.text(ax1.get_xlim()[1]*0.075, 7029, '7029',
         color='gray', fontsize=18, va='bottom', ha='right')

# Collect legend items
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
all_lines = lines1 + lines2
all_labels = labels1 + labels2

plt.grid(True)
plt.tight_layout()
plt.savefig('thesis4_metrics_main.png', dpi=300, bbox_inches='tight')

# === Separate legend figure ===
fig_legend = plt.figure(figsize=(10, 2))
fig_legend.legend(all_lines, all_labels, loc='center', ncol=4, fontsize=17, frameon=False)
fig_legend.tight_layout()
fig_legend.savefig('thesis4_metrics_legend.png', dpi=300, bbox_inches='tight')

plt.show()
