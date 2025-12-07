def rotate_right(arr, k=1):
    k %= len(arr)
    return arr[-k:] + arr[:-k]
#
# arr = [1, 2, 3, 4, 5]
# arr = rotate_right(arr, 3)  # rotate 2 steps
# print(arr)  # Output: [4, 5, 1, 2, 3]
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# res4 = pd.read_csv('res4.csv').values.flatten().tolist()
# df_2D = pd.read_csv('2D.csv').values.flatten().tolist()[0:257]
# plt.plot(res4, label='res4')
# plt.plot(df_2D, label = '2D')
# plt.legend()
# plt.show()
#
df_2D = rotate_right(pd.read_csv('2D.csv').values.flatten().tolist(), -45)
df_3D = rotate_right([i / 100000 * 2.2222 for i in pd.read_csv('3D.csv').values.flatten().tolist()], -110)
plt.plot(df_2D, label='2D')
plt.plot(df_3D, label='3D')
plt.legend()
plt.show()

df_raw = pd.read_csv('2D.csv').values.flatten().tolist()
rotated_2D = rotate_right(df_raw, 192)
_2D = rotate_right([(a + b) - 0.02 for a, b in zip(df_raw, rotated_2D)] * 4, -56)

df1 = pd.read_excel('fipmasynrm1.xlsx')
_M = rotate_right(df1['Forward'].tolist()[0:1024],8)

rotated_3D = rotate_right(df_3D, 192)
_3D = rotate_right([(a + b) - 0.02 for a, b in zip(df_3D, rotated_3D)] * 4, -5)

plt.plot(_M)
plt.plot(_2D)
plt.show()

