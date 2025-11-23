import numpy as np
import pandas as pd

def rotate_right(arr, k=1):
    k %= len(arr)
    return arr[-k:] + arr[:-k]

df1 = pd.read_csv('res4.csv').values
df2 = rotate_right(list(pd.read_csv('res4.csv').values), 192)
arr = [i+j for i,j in zip(df1,df2)]*32

chunk_size = 256

min_list = []
max_list = []
for i in range(0, len(arr), chunk_size):
    chunk = arr[i:i + chunk_size]
    if chunk:  # make sure it’s not empty
        min_val = min(chunk)
        max_val = max(chunk)
        min_list.append(min_val)
        max_list.append(max_val)
print(np.average(max_list)-np.average(min_list))

df1 = pd.read_excel('fipmasynrm1.xlsx')
arr = df1['Forward'].tolist()

chunk_size = 256

min_list = []
max_list = []
for i in range(0, len(arr), chunk_size):
    chunk = arr[i:i + chunk_size]
    if chunk:  # make sure it’s not empty
        min_val = min(chunk)
        max_val = max(chunk)
        min_list.append(min_val)
        max_list.append(max_val)
print(np.average(max_list)-np.average(min_list))

df2 = pd.read_excel('fipmasynrm2.xlsx')

rows = []

for i, j in zip(df2['Spectrum'], df2['Forward']):
    if i % 2 != 0:
        rows.append({
                'Spectrum': i,
                'Harmonic': [j * np.sin(np.radians(k) * i) for k in df1['Position'].astype(float)]
            })
    if i % 2 == 0:
        rows.append({
            'Spectrum': i,
            'Harmonic': [j * np.cos(np.radians(k) * i) for k in df1['Position'].astype(float)]
        })

df_fourier = pd.DataFrame(rows)

# Convert all list elements in 'Harmonic' to numpy arrays (for fast elementwise sum)
arrays = df_fourier['Harmonic'].apply(np.array)

# Stack into a 2D array, then sum along axis=0
sum_list = np.sum(np.stack(arrays), axis=0)

arr = sum_list.tolist()

chunk_size = 256

min_list = []
max_list = []
for i in range(0, len(arr), chunk_size):
    chunk = arr[i:i + chunk_size]
    if chunk:  # make sure it’s not empty
        min_val = min(chunk)
        max_val = max(chunk)
        min_list.append(min_val)
        max_list.append(max_val)
print(np.average(max_list)-np.average(min_list))