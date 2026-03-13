import os

import pandas as pd

import taguchi_def

df = taguchi_def.l25()

X = {}
for i in range(1, 5):  # number of variables
    X[i] = {}
    for j in range(1, 6):  # number of levels
        X[i][j] = list(df.index[df.iloc[:, i-1] == j])

df = pd.DataFrame(X)
column_key_map = {i: 'X' + str(i) for i in range(1, 5)}
L25 = df.rename(columns=column_key_map)

current_dir = os.getcwd()
tag = pd.read_csv(current_dir + '/results/' + f'taguchi_res_os.csv')

SNavg_results = []

x = 4
y = 5

for i in range(x):
    for j in range(y):
        SNavg_temp1 = [tag.iloc[L25.iloc[j, i][k], 7] for k in range(len(L25.iloc[j, i]))]
        count_of_zeros = SNavg_temp1.count(0)
        SNavg_temp2 = sum(SNavg_temp1) / (len(SNavg_temp1) - count_of_zeros)
        SNavg_results.append(SNavg_temp2)

result_array = [[SNavg_results[j + i*3] for i in range(x)] for j in range(y)]
df = pd.DataFrame(result_array, columns=['X' + str(i) for i in range(1, 5)])

difference = df.max() - df.min()
new_row_df = pd.DataFrame([difference.values], columns=difference.index)
df = pd.concat([df, new_row_df], ignore_index=True)
df = df.rename(index={0: 'L1', 1: 'L2', 2: 'L3', 3: 'L4', 4: 'L5', 5: 'R'})

print(df)

current_dir = os.getcwd()
file_path = current_dir + '/results/' + f'taguchi_rip_os.csv'
df.to_csv(file_path, encoding='utf-8', index=False)