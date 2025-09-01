import pandas as pd

df_all = pd.read_csv('../refined/case2_all.csv')

# Normalisation of the base data
del df_all['ANG']
df_torq = df_all.iloc[:, -3:]

scale_avg = 0.03178129894772644
scale_rip = 0.027410906420647047
scale_cog = 0.05406433759944656
print('AVG:',a_avg:=df_torq['AVG'].min(), b_avg:=df_torq['AVG'].max(), scale_avg*(b_avg-a_avg))
print('RIP:',a_rip:=df_torq['RIP'].min(), b_rip:=df_torq['RIP'].max(), scale_rip*(b_rip-a_rip))
print('COG:',a_cog:=df_torq['COG'].min(), b_cog:=df_torq['COG'].max(), scale_cog*(b_cog-a_cog))
