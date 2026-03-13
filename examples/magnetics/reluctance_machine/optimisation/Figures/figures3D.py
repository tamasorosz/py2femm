import pandas as pd
from matplotlib import pyplot as plt

star_point = (1.46340, 18.81, 20.74)

# Define color palette
colors = ["#B90276", '#50237F', '#005691', "#008ECF", '#00A8B0', '#78BE20', "#006249", '#525F6B', '#000']

# Load data
df1 = pd.read_csv('nsga2_case3_p50o50g100_obj7_20240807.csv')
df2 = pd.read_csv('nsga2_case4_p50o50g100_obj7_20240806.csv')
df4 = pd.read_csv('nsga2_case6_p50o50g100_obj9_20240811.csv')
df3 = pd.read_csv('nsga2_case7_p50o50g150_obj9_20240818.csv')

# Adjust data
for d in [df1, df2, df3, df4]:
    d['AVG'] *= -0.001  # Convert torque values to positive

df3 = df3[df3["X6"] != df4["X7"]].copy()
df4 = df4[df4["X6"] != df4["X7"]].copy()

# Create a 3D scatter plot
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d', facecolor='#f5f5f5')

# Plot each dataset with customized markers and colors
ax.scatter(df1['AVG'], df1['RIP'], df1['COG'], c=colors[5], marker='o', s=80, label='Case A1', alpha=0.8)
ax.scatter(df2['AVG'], df2['RIP'], df2['COG'], c=colors[3], marker='o', s=80, label='Case A2', alpha=0.8)
ax.scatter(df3['AVG'], df3['RIP'], df3['COG'], c=colors[1], marker='o', s=80, label='Case B1', alpha=0.8)
ax.scatter(df4['AVG'], df4['RIP'], df4['COG'], c=colors[0], marker='o', s=80, label='Case B2', alpha=0.8)

# Add grid, labels, and title
ax.set_xlabel('Average Torque [Nm]', fontsize=16, labelpad=10)
ax.set_ylabel('Torque Ripple [%]', fontsize=16, labelpad=10)
ax.set_zlabel('Cogging Torque [mNm]', fontsize=16, labelpad=10)

# Customize legend
legend = ax.legend(loc='upper right', fontsize=14)

# Fine-tune aesthetics
ax.grid(color='#dcdcdc', linestyle='--', linewidth=0.5)
ax.xaxis.label.set_color('#333333')
ax.yaxis.label.set_color('#333333')
ax.zaxis.label.set_color('#333333')
ax.tick_params(axis='both', which='major', labelsize=16, colors='#333333')
ax.tick_params(axis='both', which='minor', labelsize=14, colors='#333333')

ax.scatter(star_point[0], star_point[1], star_point[2], c=colors[-1], marker='*', s=500, label='Optimum')

plt.tight_layout()
ax.view_init(elev=5, azim=320)
plt.savefig('obj_3d.png', format='png', dpi=300)
plt.show()

# -----------------------------------------------------------------------------------------------------
import pandas as pd
from matplotlib import pyplot as plt

# Define color palette
colors = ["#B90276", '#50237F', '#005691', "#008ECF", '#00A8B0', '#78BE20', "#006249", '#525F6B', '#000']

# Load data
df1 = pd.read_csv('nsga2_case3_p50o50g100_obj7_20240807.csv')
df2 = pd.read_csv('nsga2_case4_p50o50g100_obj7_20240806.csv')
df4 = pd.read_csv('nsga2_case6_p50o50g100_obj9_20240811.csv')
df3 = pd.read_csv('nsga2_case7_p50o50g150_obj9_20240818.csv')

# Adjust data
for d in [df1, df2, df3, df4]:
    d['AVG'] *= -0.001  # Convert torque values to positive

df3 = df3[df3["X6"] != df4["X7"]].copy()
df4 = df4[df4["X6"] != df4["X7"]].copy()

# Prepare datasets
datasets = [
    (df1, colors[5], 'Case A1'),
    (df2, colors[3], 'Case A2'),
    (df3, colors[1], 'Case B1'),
    (df4, colors[0], 'Case B2')
]

ft = 12  # Font size for labels and ticks
ss1 = 50
ss = 300

# XY Projection
plt.figure(figsize=(5, 4))
for data, color, label in datasets:
    plt.scatter(data['AVG'], data['RIP'], color=color, label=label, alpha=0.8, s=ss1)

plt.scatter(star_point[0], star_point[1], c=colors[-1], marker='*', s=ss, label='Optimum')

plt.xlabel("Average Torque [Nm]", fontsize=ft)
plt.ylabel("Torque Ripple [%]", fontsize=ft)
plt.xticks(fontsize=ft)
plt.yticks(fontsize=ft)
plt.legend(loc='best', fontsize=ft)
plt.grid(color='#dcdcdc', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.savefig('obj_avg_rip.png', format='png', dpi=300)
plt.show()

# XZ Projection
plt.figure(figsize=(5, 4))
for data, color, label in datasets:
    plt.scatter(data['AVG'], data['COG'], color=color, label=label, alpha=0.8, s=ss1)

plt.scatter(star_point[0], star_point[2], c=colors[-1], marker='*', s=ss, label='Optimum')

plt.xlabel("Average Torque [Nm]", fontsize=ft)
plt.ylabel("Cogging Torque [mNm]", fontsize=ft)
plt.xticks(fontsize=ft)
plt.yticks(fontsize=ft)
plt.legend(loc='best', fontsize=ft)
plt.grid(color='#dcdcdc', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.savefig('obj_avg_cog.png', format='png', dpi=300)
plt.show()

# YZ Projection
plt.figure(figsize=(5, 4))
for data, color, label in datasets:
    plt.scatter(data['RIP'], data['COG'], color=color, label=label, alpha=0.8, s=ss1)

plt.scatter(star_point[1], star_point[2], c=colors[-1], marker='*', s=ss, label='Optimum')

plt.xlabel("Torque Ripple [%]", fontsize=ft)
plt.ylabel("Cogging Torque [mNm]", fontsize=ft)
plt.xticks(fontsize=ft)
plt.yticks(fontsize=ft)
plt.legend(loc='best', fontsize=ft)
plt.grid(color='#dcdcdc', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.savefig('obj_rip_cog.png', format='png', dpi=300)
plt.show()
