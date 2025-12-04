import csv
import matplotlib.pyplot as plt
import os

filename = '2D_FEMM_Steel_18mm_full_exc015_static.csv'

def rotate(arr, k=0):
    k %= len(arr)
    return arr[-k:] + arr[:-k]

# Verify file exists
if os.path.exists(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)

        data = []
        for row in reader:
            if row:
                try:
                    data.append(float(row[0]))
                except ValueError:
                    continue

        data = rotate(data[0:], -40)
        skew = rotate(data[0:], 64)
        sum = [i + j for i, j in zip(data, skew)]


        plt.figure(figsize=(8, 6))
        plt.plot(sum)
        plt.title(f"Data from {filename}")
        plt.xlabel("Sample Index")
        plt.ylabel("Value")
        plt.grid(True)
        plt.show()
else:
    print(f"File {filename} not found.")