import numpy as np
import pandas as pd

df_base = pd.read_csv('all_res_avg_case6_20250404_all_variable.csv')
del df_base['ANG']
del df_base['RIP']
# print(df_base)

df_minmax = pd.DataFrame({'X1': [15, 25],
                          'X2': [60, 140],
                          'X3': [0.5, 4],
                          'X4': [0.01, 1],
                          'X5': [0.5, 4],
                          'X6': [2, 3],
                          'X7': [1.5, 2],
                          'X8': [10, 15],
                          'X9': [10, 18],
                          'X10': [0, 16],
                          'X11': [0, 16],})
# print(df_minmax)

min_vals = df_minmax.iloc[0]
max_vals = df_minmax.iloc[1]

# Min-max normalization
df_normalized = ((df_base.iloc[:,:-1] - min_vals) / (max_vals - min_vals)).round(3)
df_normalized['AVG'] = df_base.iloc[:,-1]

# print(df_normalized)

for x in range(10000,10200):
    indexes = []
    deviat = []

    df_sub = df_normalized.iloc[:x,:].copy()
    # print(df_sub)
    #
    df_unit = df_normalized.iloc[x,:].copy()
    # print(df_unit)

    correlations = list(abs((df_normalized.iloc[:, :-1].corrwith(df_normalized.iloc[:, -1])).round(3)))
    # print(correlations)

    for i in range(len(df_sub)):
        subs = list(abs((df_unit-df_sub.iloc[i,:]).round(3)))
        deviat.append(subs[-1])
        # print(subs)

        ind = np.round(np.dot(subs[:-1], correlations),3)
        # print(ind)
        # print('---------------------')
        # indexes.append(sum(subs[:-1]))
        indexes.append(ind)
    df_sub.loc[:, 'DEV'] = deviat
    df_sub.loc[:, 'IND'] = indexes
    # print( df_sub)


    print(f'{x}:', float(df_sub[df_sub['IND'] == df_sub['IND'].min()]['DEV'].iloc[0]), float(df_sub[df_sub['IND'] == df_sub['IND'].min()]['IND'].iloc[0]))
    print('---------------------')
