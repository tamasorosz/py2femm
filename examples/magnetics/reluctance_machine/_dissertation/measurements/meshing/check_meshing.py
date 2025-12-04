import csv
import matplotlib.pyplot as plt
import os

f0 = '2D_FEMM_Steel_18mm_full_base.csv'
f1 = '2D_FEMM_Steel_18mm_full_exc000_gl000_mag10_mesh025.csv'
f2 = '2D_FEMM_Steel_18mm_full_exc000_gl000_mag10_mesh010.csv'

filename = [f0, f1,f2]

def rotate(arr, k=0):
    k %= len(arr)
    return arr[-k:] + arr[:-k]

# Verify file exists
for filename in filename:
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

            i = 0
            j = 86
            k = 85
            cog = []
            while j < 2040:
                ymin = min(sum[i:j])
                ymax = max(sum[i:j])
                cog.append(ymax - ymin)
                i += k
                j += k
            print("Periodic:", max(cog))

            # print("Full:", max(sum)-min(sum))


    else:
        print(f"File {filename} not found.")