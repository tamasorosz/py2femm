# def rotate_right(arr, k=1):
#     k %= len(arr)
#     return arr[-k:] + arr[:-k]
#
# arr = [1, 2, 3, 4, 5]
# arr = rotate_right(arr, 3)  # rotate 2 steps
# print(arr)  # Output: [4, 5, 1, 2, 3]
import matplotlib.pyplot as plt
import pandas as pd

df_raw = pd.read_csv('res4.csv').values.flatten().tolist()
plt.plot(df_raw)
plt.show()