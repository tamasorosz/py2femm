import pandas as pd
from matplotlib import pyplot as plt

def rotate_right(arr, k=1):
    k %= len(arr)
    return arr[-k:] + arr[:-k]

df1 = pd.read_csv('res4.csv').values
df2 = rotate_right(list(pd.read_csv('res4.csv').values), 32)
plt.plot([i+j for i,j in zip(df1,df2)]*32)
plt.show()