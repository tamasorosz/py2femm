import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pandas.core.interchange.dataframe_protocol import DataFrame

with open ('all_res_avg_case0_20250202.csv', 'r') as f:
    df1 = pd.read_csv(f)
    df1 = df1[df1.iloc[:, -1] <= 70]

    df7 = df1.head(0).copy()

    for i in range(850, 1200):
        df_temp = df1[(df1.iloc[:, -2] * -1 <= i) & (df1.iloc[:, -2] * -1 > i - 50)]
        min_value = df_temp.iloc[:, -1].min()
        min_row = df_temp[df_temp.iloc[:, -1] == min_value]
        if min_value < 100:
            df7 = pd.concat([df7, min_row], ignore_index=True)
    df7 = df7.drop_duplicates(ignore_index=True)

    for i in range(1250, 1390):
        df_temp = df1[(df1.iloc[:, -2] * -1 <= i) & (df1.iloc[:, -2] * -1 > i - 50)]
        min_value = df_temp.iloc[:, -1].min()
        min_row = df_temp[df_temp.iloc[:, -1] == min_value]
        if min_value < 100:
            df7 = pd.concat([df7, min_row], ignore_index=True)
    df7 = df7.drop_duplicates(ignore_index=True)

    for i in range(1550, 2000):
        df_temp = df1[(df1.iloc[:, -2] * -1 <= i) & (df1.iloc[:, -2] * -1 > i - 50)]
        min_value = df_temp.iloc[:, -1].min()
        min_row = df_temp[df_temp.iloc[:, -1] == min_value]
        if min_value < 100:
            df7 = pd.concat([df7, min_row], ignore_index=True)
    df7 = df7.drop_duplicates(ignore_index=True)

with open ('nsga2_case0_p100o100g200_var6_20250202.csv', 'r') as f:
    df2 = pd.read_csv(f)
#
with open ('nsga2_const_p50o25g100.csv', 'r') as f:
    df3 = pd.read_csv(f)

with open('all_res_avg_case1_20250205.csv', 'r') as f:
    df4 = pd.read_csv(f)

with open('all_res_avg_case0_20250306.csv', 'r') as f:
    dfA = pd.read_csv(f)

print(len(dfA))
dfA = dfA.drop_duplicates(ignore_index=True)
print(len(dfA))

df6 = df4.head(0).copy()

with open('nsga2_case0_p100o100g200_var6_20250306.csv', 'r') as f:
    df_306p = pd.read_csv(f)

with open('all_res_avg_case0_20250310.csv', 'r') as f:
    df_310 = pd.read_csv(f)

with open('nsga2_case0_p100o100g200_var6_20250310.csv', 'r') as f:
    df_310p = pd.read_csv(f)

print(len(df_310))
df_310 = df_310.drop_duplicates(ignore_index=True)
print(len(df_310))

with open('all_res_avg_case0_20250314.csv', 'r') as f:
    df_314 = pd.read_csv(f)

with open('nsga2_case0_p100o100g200_var6_20250314.csv', 'r') as f:
    df_314p = pd.read_csv(f)

with open('all_res_avg_case0_20250316.csv', 'r') as f:
    df_316 = pd.read_csv(f)

with open('nsga2_case0_p100o100g200_var6_20250316.csv', 'r') as f:
    df_316p = pd.read_csv(f)

with open('all_res_avg_case0_20250326.csv', 'r') as f:
    df_326 = pd.read_csv(f)

with open('nsga2_case0_p100o100g200_var6_20250326.csv', 'r') as f:
    df_326p = pd.read_csv(f)

# for i in range(500, 2000):
#     df_temp = df4[(df4.iloc[:, -2] * -1 <= i) & (df4.iloc[:, -2] * -1 > i - 100)]
#     min_value = df_temp.iloc[:, -1].min()
#     min_row = df_temp[df_temp.iloc[:, -1] == min_value]
#     df6 = pd.concat([df6, min_row], ignore_index=True)
# df6 = df6.drop_duplicates(ignore_index=True)

# with open ('all_res_avg_case2_20250210.csv', 'r') as f:
#     df8 = pd.read_csv(f)
#     df8 = df8[df8.iloc[:, -1] <= 100]
#
# df9 = df8.head(0).copy()
#
# for i in range(500, 2000):
#     df_temp = df8[(df8.iloc[:, -2] * -1 <= i) & (df8.iloc[:, -2] * -1 > i - 50)]
#     min_value = df_temp.iloc[:, -1].min()
#     min_row = df_temp[df_temp.iloc[:, -1] == min_value]
#     df9 = pd.concat([df9, min_row], ignore_index=True)
# df9 = df9.drop_duplicates(ignore_index=True)



# plt.scatter(df1.iloc[:, -2] * -1, df1.iloc[:, -1])
# plt.scatter(df2.iloc[:,-2] * -1, df2.iloc[:,-1])
# plt.scatter(df3.iloc[:,-2] * -1, df3.iloc[:,-1] *100)
# plt.scatter(df4.iloc[:,-2] * -1, df4.iloc[:,-1])
# plt.scatter(df5.iloc[:,-3] * -1, df5.iloc[:,-2])
# plt.scatter(df6.iloc[:, -2] * -1, df6.iloc[:, -1])
# plt.scatter(df7.iloc[:, -2] * -1, df7.iloc[:, -1])
# # plt.scatter(df8.iloc[:, -2] * -1, df8.iloc[:, -1])
# plt.scatter(df9.iloc[:,-2] * -1, df9.iloc[:,-1])
# plt.scatter(dfA.iloc[:, -2] * -1, dfA.iloc[:, -1])
plt.scatter(df_306p.iloc[:, -2] * -1, df_306p.iloc[:, -1])
plt.scatter(df_310p.iloc[:, -2] * -1, df_310p.iloc[:, -1])
# plt.scatter(df_314.iloc[:, -2] * -1, df_314.iloc[:, -1])
plt.scatter(df_314p.iloc[:, -2] * -1, df_314p.iloc[:, -1])
# plt.scatter(df_326.iloc[:, -2] * -1, df_326.iloc[:, -1])
# plt.scatter(df_316.iloc[:, -2] * -1, df_316.iloc[:, -1])
plt.scatter(df_316p.iloc[:, -2] * -1, df_316p.iloc[:, -1])
# plt.scatter(df_314.iloc[:, -2] * -1, df_314.iloc[:, -1])
plt.scatter(df3.iloc[:,-2] * -1, df3.iloc[:,-1] *100)
plt.scatter(df_326p.iloc[:, -2] * -1, df_326p.iloc[:, -1])

plt.show()

# plt.plot(df_310.iloc[:,-3])
# plt.show()

print(np.linspace(42, 47, 6))