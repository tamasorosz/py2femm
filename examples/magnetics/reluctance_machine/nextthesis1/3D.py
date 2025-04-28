import numpy as np
import pandas as pd

import matplotlib
import seaborn as sns

matplotlib.use('Qt5Agg')

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)  # Use full width of the terminal
pd.set_option('display.expand_frame_repr', False)  # Avoid wrapping into multiple lines

colors = ["#B90276", "#50237F", "#00A8B0", "#006249", "#525F6B",
          "#FF5733", "#2E86C1", "#28B463", "#F1C40F", "#8E44AD"]

with open('all_res_avg_case3_20250215.csv', 'r') as f:
    df_A1 = pd.read_csv(f)

with open('all_res_cog_case3_20250215.csv', 'r') as f:
    df_temp = pd.read_csv(f)
df_A1["COG"] = df_temp.iloc[:,-1]
df_A1["MOD"] = 'A1'
df_A1["COL"] = colors[2]

df_A1 = df_A1.drop_duplicates()

with open('all_res_avg_case4_20250221.csv', 'r') as f:
    df_A2 = pd.read_csv(f)

with open('all_res_cog_case4_20250221.csv', 'r') as f:
    df_temp = pd.read_csv(f)
df_A2["COG"] = df_temp.iloc[:,-1]
df_A2["MOD"] = 'A2'
df_A2["COL"] = colors[3]

df_A2 = df_A2.drop_duplicates()

with open('all_res_avg_case6_20250229.csv', 'r') as f:
    df_B1 = pd.read_csv(f)

with open('all_res_cog_case6_20250229.csv', 'r') as f:
    df_temp = pd.read_csv(f)

with open('all_res_avg_case6_20250125.csv', 'r') as f:
    df_Bt1 = pd.read_csv(f)

with open('all_res_cog_case6_20250125.csv', 'r') as f:
    df_Bt2 = pd.read_csv(f)

df_B1['COG'] = df_temp['COG']
df_Bt1['COG'] = df_Bt2['COG']
df_Bt1['X10'] = df_Bt2['X10'] / 2
df_Bt1['X11'] = df_Bt2['X11'] / 2

df_B1 = pd.concat([df_B1, df_Bt1])
df_B1["MOD"] = 'B1'
df_B1["COL"] = colors[4]

df_B1 = df_B1.drop_duplicates()

with open('all_res_avg_case7_20250120.csv', 'r') as f:
    df_B2 = pd.read_csv(f)

with open('all_res_cog_case7_20250120.csv', 'r') as f:
    df_temp = pd.read_csv(f)
df_B2["COG"] = df_temp.iloc[:,-1]
df_B2["MOD"] = 'B2'
df_B2["COL"] = colors[5]

df_B2 = df_B2.drop_duplicates()

with open('all_res_avg_case1_20250205.csv', 'r') as f:
    df_C1 = pd.read_csv(f)

with open('all_res_cog_case1_20250205.csv', 'r') as f:
    df_temp = pd.read_csv(f)
df_C1["COG"] = df_temp["COG"]
df_C1["MOD"] = 'C1'
df_C1["COL"] = colors[0]

with open('all_res_avg_case2_20250210.csv', 'r') as f:
    df_C2 = pd.read_csv(f)

with open('all_res_cog_case2_20250210.csv', 'r') as f:
    df_temp = pd.read_csv(f)
df_C2["COG"] = df_temp["COG"]
df_C2["MOD"] = 'C2'
df_C2["COL"] = colors[1]

df_C2 = df_C2.drop_duplicates(ignore_index=True)

df_all = pd.concat([df_C1.iloc[:,-5:],  df_C2.iloc[:,-5:], df_A1.iloc[:,-5:], df_A2.iloc[:,-5:], df_B1.iloc[:,-5:], df_B2.iloc[:,-5:]], ignore_index=True)

df_all = df_all[df_all['RIP'] < 30]
df_all = df_all[df_all['AVG'] < -1000]

a = 1

# Apply a fancy seaborn style
sns.set_style("whitegrid")

# Create 3D figure
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

x_plane = np.array([1400, 2200])  # X values
y_plane = np.array([20, 20])  # Fixed Y value (horizontal)
z_plane = np.array([13, 23])  # Z values range from 13 to 23

# Mesh grid for plotting the surface
X, Z = np.meshgrid(x_plane, z_plane)
Y = np.full_like(X, 20)  # Y value is fixed to 20

ax.plot_surface(X, Y, Z, color='b', alpha=0.2)

x_plane = np.array([1400, 1400])  # X values
y_plane = np.array([9, 20])  # Fixed Y value (horizontal)
z_plane = np.array([13, 23])  # Z values range from 13 to 23

# Mesh grid for plotting the surface
Y, Z = np.meshgrid(y_plane, z_plane)
X = np.full_like(X, 1400)  # Y value is fixed to 20

ax.plot_surface(X, Y, Z, color='b', alpha=0.2)

# Scatter plot with enhanced visualization
scatter = ax.scatter(
    df_all.loc[df_all['MOD'] == 'C1', 'AVG'] * -1,
    df_all.loc[df_all['MOD'] == 'C1', 'RIP'],
    df_all.loc[df_all['MOD'] == 'C1', 'COG'],
    c=df_all.loc[df_all['MOD'] == 'C1', 'COL'],
    marker='o',
    edgecolors='black',
    alpha=a,
    s=30,
    label = 'Case C1'
)

scatter = ax.scatter(
    df_all.loc[df_all['MOD'] == 'C2', 'AVG'] * -1,
    df_all.loc[df_all['MOD'] == 'C2', 'RIP'],
    df_all.loc[df_all['MOD'] == 'C2', 'COG'],
    c=df_all.loc[df_all['MOD'] == 'C2', 'COL'],
    marker='o',
    edgecolors='black',
    alpha=a,
    s=30,
    label = 'Case C2'
)

scatter = ax.scatter(
    df_all.loc[df_all['MOD'] == 'A1', 'AVG'] * -1,
    df_all.loc[df_all['MOD'] == 'A1', 'RIP'],
    df_all.loc[df_all['MOD'] == 'A1', 'COG'],
    c=df_all.loc[df_all['MOD'] == 'A1', 'COL'],
    marker='o',
    edgecolors='black',
    alpha=a,
    s=30,
    label = 'Case A1'
)

scatter = ax.scatter(
    df_all.loc[df_all['MOD'] == 'A2', 'AVG'] * -1,
    df_all.loc[df_all['MOD'] == 'A2', 'RIP'],
    df_all.loc[df_all['MOD'] == 'A2', 'COG'],
    c=df_all.loc[df_all['MOD'] == 'A2', 'COL'],
    marker='o',
    edgecolors='black',
    alpha=a,
    s=30,
    label = 'Case A2'
)

scatter = ax.scatter(
    df_all.loc[df_all['MOD'] == 'B1', 'AVG'] * -1,
    df_all.loc[df_all['MOD'] == 'B1', 'RIP'],
    df_all.loc[df_all['MOD'] == 'B1', 'COG'],
    c=df_all.loc[df_all['MOD'] == 'B1', 'COL'],
    marker='o',
    edgecolors='black',
    alpha=0.1,
    s=30,
    label = 'Case B1'
)

scatter = ax.scatter(
    df_all.loc[df_all['MOD'] == 'B2', 'AVG'] * -1,
    df_all.loc[df_all['MOD'] == 'B2', 'RIP'],
    df_all.loc[df_all['MOD'] == 'B2', 'COG'],
    c=df_all.loc[df_all['MOD'] == 'B2', 'COL'],
    marker='o',
    edgecolors='black',
    alpha=a,
    s=30,
    label = 'Case B2'
)


# Labels with better styling
ax.set_xlabel("Average torque [mNm]", fontsize=16, labelpad=10)
ax.set_ylabel("Torque ripple [%]", fontsize=16, labelpad=10)
ax.set_zlabel("Cogging torque [mNm]", fontsize=16, labelpad=10)
ax.tick_params(axis='both', which='major', labelsize=14)
ax.tick_params(axis='z', which='major', labelsize=14)
ax.set_xticks(np.arange(1000, 2201, 200))
ax.set_yticks(np.arange(10, 31, 5))
ax.set_zticks(np.arange(13, 23, 2))
# Rotate the 3D view for better visualization
ax.view_init(elev=20, azim=-140)  # Adjust elevation and azimuth
plt.legend(fontsize=14, loc="upper center", frameon=True, ncol=3, bbox_to_anchor=(0.5, 1))
plt.savefig('comp_3D_all_2.png')

# ax.view_init(elev=90, azim=180, )  # Adjust elevation and azimuth
# ax.set_zticks([])
# ax.set_zlabel('')
# plt.legend(fontsize=14, loc="upper center", frameon=True, ncol=3, bbox_to_anchor=(0.5, 1))
# plt.savefig('comp_3D_avg_rip.png')

# ax.view_init(elev=0, azim=0, )  # Adjust elevation and azimuth
# ax.set_xticks([])
# ax.set_xlabel('')
# plt.legend(fontsize=14, loc="upper center", frameon=True, ncol=3, bbox_to_anchor=(0.5, 0.9))
# plt.savefig('comp_3D_rip_cog.png')

# ax.view_init(elev=0, azim=270, )  # Adjust elevation and azimuth
# ax.set_yticks([])
# ax.set_ylabel('')
# plt.legend(fontsize=14, loc="upper center", frameon=True, ncol=3, bbox_to_anchor=(0.5, 0.9))
# plt.savefig('comp_3D_avg_cog.png')


# Improve grid aesthetics
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.grid(True, linestyle="--", alpha=0.5)
# plt.legend(fontsize=14, loc="upper center", frameon=True, ncol=3)

# Show the plot
plt.show()