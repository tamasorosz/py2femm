import csv
import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import uniform_filter1d
import pandas as pd

cw = 'cw.csv'
ccw = 'ccw.csv'

def rotate(arr, k=0):
    k %= len(arr)
    return arr[-k:] + arr[:-k]

filename = [cw, ccw]
l_cw = []
l_ccw = []
for f in filename:
    if os.path.exists(f):
        with open(f, 'r') as file:
            reader = csv.reader(file)



            for row in reader:
                if row:
                    try:
                        if f == 'cw.csv':
                            l_cw.append(float(row[0]))
                        else:
                            l_ccw.append(float(row[0]))
                    except ValueError:
                        continue

# 1. Check for perfect alignment --> okay
plt.plot(l_cw[0:2048], label='cw')
plt.plot(l_ccw[0:2048], label='ccw')
plt.legend()
plt.show()

l_cw = rotate(l_cw, 0)

# 2. CW/CWW correction to cancel friction offset --> okay
corr = [(i+j)/2 for i,j in zip(l_cw, l_ccw)]
plt.plot(corr, label='corr')
plt.show()

# 3. Mean subtraction to cancel sensor offset --> okay
corr_mean = [i-np.mean(corr) for i in corr]
plt.plot(corr_mean, label='corr_mean')
plt.show()

# 4. Apply moving average to filter the measurement --> okay
corr_filtered = uniform_filter1d(corr_mean, size=8, mode='wrap')
plt.plot(corr_filtered[0:180], label='corr_filtered')
plt.show()

# 5. Shaft misalignment correction --> Sine wave aligned
o = -0.0005  # Vertical offset
a = 0.0020  # Amplitude
sine = rotate([o + a * np.sin(np.deg2rad(i)) for i in np.linspace(0,1440,8192)], -1138)
plt.plot(corr_filtered, label='corr_filtered')
plt.plot(sine, label='sine')
plt.show()

# 6. Shaft misalignment correction -->
corr_aligned = [i-j for i,j in zip(corr_filtered, sine)][0:2048]
plt.plot(corr_aligned, label='corr_aligned')
plt.show()

print(max(corr_aligned[0:86])-min(corr_aligned[0:86]))

df = pd.DataFrame(corr_aligned).to_csv('measurement_filtered.csv')
