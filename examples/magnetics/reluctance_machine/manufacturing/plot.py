import pandas as pd

import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)  # Use full width of the terminal
pd.set_option('display.expand_frame_repr', False)  # Avoid wrapping into multiple lines

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

df = pd.concat([df_B1, df_Bt1])
# df = df_B1
print(len(df))

df = df.drop_duplicates(ignore_index=True)

print(len(df))

#
# Create 3D figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Scatter plot
ax.scatter(df['AVG'], df['RIP'], df['COG'], c=df['COG'], cmap='viridis', marker='o')

# Labels
ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
ax.set_zlabel("Z Axis")
ax.set_title("3D Scatter Plot")

# plt.show()

# print(df[(df['COG'] < 13.7)])
print(df[(df['RIP'] < 12) & (df['AVG'] < -1400)])


# for i in range(0, 9):
#     plt.scatter(df_A.iloc[:, i], df_A['COG'])
#     plt.show()