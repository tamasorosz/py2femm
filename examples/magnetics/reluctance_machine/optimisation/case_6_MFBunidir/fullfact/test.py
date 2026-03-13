import os

import pandas as pd

from itertools import product

# Generate full factorial permutations for X1 to X6 with values [1, 2, 3, 4, 5]
values = [1, 2, 3, 4, 5]
permutations = list(product(values, repeat=4))

# Create a dictionary for X1 to X6
full_factorial_dict = {
    "X1": [row[0] for row in permutations],
    "X2": [row[1] for row in permutations],
    "X3": [row[2] for row in permutations],
    "X4": [row[3] for row in permutations],
}

# Convert to DataFrame
data = pd.DataFrame(full_factorial_dict)

file_path = os.getcwd() + f'/fullfact.csv'
df = pd.DataFrame(data)
csv_path = file_path
df.to_csv(csv_path, index=False)
