import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv('C:/Users/sevir/PycharmProjects/py2femm/examples/magnetics/reluctance_machine/MDPI2025/refined/case1_all.csv')

del df['ANG']

print(((0.417 + 0.05) * (25-15) + 15) - (0.417 * (25-15) + 15))
print(((0.417 + 0.05) * (140-75.2) + 75.2) - (0.417 * (140-75.2) + 75.2))
print(((0.417 + 0.05) * (3.75-0.5) + 0.5) - (0.417 * (3.75-0.5) + 0.5))
print(((0.417 + 0.05) * (1-0) + 0) - (0.417 * (1-0) + 0))
print(((0.417 + 0.05) * (4.15-0.5) + 0.5) - (0.417 * (4.15-0.5) + 0.5))
print(((0.417 + 0.05) * (2.82-2.01) + 2.01) - (0.417 * (2.82-2.01) + 2.01))
print(((0.417 + 0.05) * (1.99-1.51) + 1.51) - (0.417 * (1.99-1.51) + 1.51))
print(((0.417 + 0.05) * (15-10) + 10) - (0.417 * (15-10) + 10))
print(((0.417 + 0.05) * (18-11.05) + 11.05) - (0.417 * (18-11.05) + 11.05))
print(((0.417 + 0.05) * (7.81-0) + 7.81) - (0.417 * (7.81-0) + 7.81))
print(((0.417 + 0.05) * (4.9-0) + 4.9) - (0.417 * (4.9-0) + 4.9))


# Initialize empty lists
a, b, c, d, e, f, g, h, Y, X = [], [], [], [], [], [], [], [], [], []

for i in range(1, 10000):
    a_val = random.uniform(0, 0.05)
    b_val = random.uniform(0, 0.05)
    c_val = random.uniform(0, 0.05)
    d_val = random.uniform(0, 0.05)
    e_val = random.uniform(0, 0.05)
    f_val = random.uniform(0, 0.05)
    g_val = random.uniform(0, 0.05)
    h_val = random.uniform(0, 0.05)

    # Append values
    a.append(a_val)
    b.append(b_val)
    c.append(c_val)
    d.append(d_val)
    e.append(e_val)
    f.append(f_val)
    g.append(g_val)
    h.append(h_val)

    # Calculate Euclidean norm for this row
    norm = np.sqrt(a_val**2 + b_val**2 + c_val**2 + d_val**2 + e_val**2 + f_val**2 + g_val**2 + h_val**2)
    Y.append(norm)

    # Append index
    X.append(i)

# Create DataFrame
df = pd.DataFrame({
    'a': a,
    'b': b,
    'c': c,
    'd': d,
    'e': e,
    'f': f,
    'g': g,
    'h': h,
    'Y': Y
})

filtered_df = df[(df['Y'] < 0.05) & (df['Y'] > 0.049)]
print(np.round(list(filtered_df.iloc[0]), 3))
print(sum(np.round(list(filtered_df.iloc[0]), 3)))

plt.scatter(X,Y)
plt.axhline(y=0.05, color='red', linestyle='--', linewidth=2)
plt.plot()
plt.show()

print(filtered_df.iloc[0,-1])
print(((0.417 + filtered_df.iloc[0,0]) * (25-15) + 15) - (0.417 * (25-15) + 15))
print(((0.417 + filtered_df.iloc[0,1]) * (140-75.2) + 75.2) - (0.417 * (140-75.2) + 75.2))
print(((0.417 + filtered_df.iloc[0,2]) * (3.75-0.5) + 0.5) - (0.417 * (3.75-0.5) + 0.5))
print(((0.417 + filtered_df.iloc[0,3]) * (1-0) + 0) - (0.417 * (1-0) + 0))
print(((0.417 + filtered_df.iloc[0,4]) * (4.15-0.5) + 0.5) - (0.417 * (4.15-0.5) + 0.5))
print(((0.417 + filtered_df.iloc[0,5]) * (2.82-2.01) + 2.01) - (0.417 * (2.82-2.01) + 2.01))
print(((0.417 + filtered_df.iloc[0,6]) * (1.99-1.51) + 1.51) - (0.417 * (1.99-1.51) + 1.51))
print(((0.417 + filtered_df.iloc[0,7]) * (15-10) + 10) - (0.417 * (15-10) + 10))

# from scipy.spatial.distance import pdist, squareform
#
# # Assuming df is numeric
# distance_matrix = squareform(pdist(df, metric='euclidean'))
# distance_df = pd.DataFrame(distance_matrix, index=df.index, columns=df.index)
# print(distance_df)
#
# nonzero_df = distance_df.replace(0, np.nan)
#
# print(nonzero_df.min().min())
#
# positions = np.where(nonzero_df < 1)
# result = list(zip(nonzero_df.index[positions[0]], nonzero_df.columns[positions[1]]))
#
# print(result)
# print(df.loc[3831])
# print(df.loc[13569])

