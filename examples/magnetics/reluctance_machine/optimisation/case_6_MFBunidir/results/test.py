import pandas as pd

df = pd.read_csv('all_res_avg_case6_20250404_all_variable.csv')
#
# print(df[df['RIP'] < 4])

cog = pd.read_csv('all_res_cog_case6_20250404_all_variable.csv')

# print(df[df['COG'] < 13.2])

df['COG'] = cog['COG']

print(df[df['COG'] < 13.2])