import pandas as pd

df_torque = pd.read_csv('../refined/case3_all.csv')
df_cluster = pd.read_csv('case3_m2_s001_e1_average_max_doublecluster_backward_all_noiloc_low.csv')

del df_torque['ANG']

# AVERAGE --------------------------------------------------------------------------------------------------------------
df_avg = abs(df_torque.iloc[:, -3])
df_diff_mean_avg = df_cluster.iloc[:, 2]
df_diff_max_avg = df_cluster.iloc[:, 5]
avg_min = df_avg.min()
avg_max = df_avg.max()

torque_diff_average_mean = (avg_max - avg_min) * df_diff_mean_avg
torque_diff_average_max = (avg_max - avg_min) * df_diff_max_avg

# RIPPLE --------------------------------------------------------------------------------------------------------------
df_rip = abs(df_torque.iloc[:, -2])
df_diff_mean_rip = df_cluster.iloc[:, 3]
df_diff_max_rip = df_cluster.iloc[:, 6]
rip_min = df_rip.min()
rip_max = df_rip.max()

torque_diff_ripple_mean = (rip_max - rip_min) * df_diff_mean_rip
torque_diff_ripple_max = (rip_max - rip_min) * df_diff_max_rip

# COGGING --------------------------------------------------------------------------------------------------------------
df_cog = abs(df_torque.iloc[:, -1])
df_diff_mean_cog = df_cluster.iloc[:, 4]
df_diff_max_cog = df_cluster.iloc[:, 7]
cog_min = df_cog.min()
cog_max = df_cog.max()

torque_diff_cogging_mean = (cog_max - cog_min) * df_diff_mean_cog
torque_diff_cogging_max = (cog_max - cog_min) * df_diff_max_cog

df_res = pd.DataFrame({'AVG_MEAN': round(torque_diff_average_mean, 3),
                       'AVG_MAX': round(torque_diff_average_max, 3),
                       'RIP_MEAN': round(torque_diff_ripple_mean, 3),
                       'RIP_MAX': round(torque_diff_ripple_max, 3),
                       'COG_MEAN': round(torque_diff_cogging_mean, 3),
                       'COG_MAX': round(torque_diff_cogging_max, 3),
                       'CLUSTERS': df_cluster.iloc[:, 1],
                       'THRESHOLD': df_cluster.iloc[:, 0]})
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df_res)

print(avg_min, avg_max)
print(rip_min, rip_max)
print(cog_min, cog_max)
print