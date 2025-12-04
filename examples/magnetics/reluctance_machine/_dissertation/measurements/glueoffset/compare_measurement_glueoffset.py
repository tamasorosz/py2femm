import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

mes = pd.read_csv('../measurement/measurement_filtered.csv')
sim = pd.read_csv('2D_FEMM_Steel_18mm_full_exc000_gl020.csv')

def rotate(arr, k=0):
    k %= len(arr)
    return arr[-k:] + arr[:-k]

base = list(sim["torque"])
skew = rotate(list(sim["torque"]), 64)

simulation_data = rotate([(i+j)/1000 * 3 for i,j in zip(base, skew)], -45)

plt.plot([i*1.045 for i in np.linspace(0,6143, 6148)], mes.iloc[:, 1][0:6148], label='Measurement')
plt.plot(np.linspace(0,6413,2048),simulation_data, label='Simulation*3')
plt.show()

plt.plot([i*1 for i in np.linspace(0,2047, 2048)], mes.iloc[:, 1][0:2048], label='Measurement')
plt.plot(np.linspace(0,2047,683),simulation_data[0:683], label='Simulation*3')
plt.show()

simulation_data = rotate([(i+j)/1000 for i,j in zip(base, skew)], -45)

plt.plot([i*1.045 for i in np.linspace(0,6143, 6148)], mes.iloc[:, 1][0:6148], label='Measurement')
plt.plot(np.linspace(0,6413,2048),simulation_data, label='Simulation*3')
plt.show()

plt.plot([i*1 for i in np.linspace(0,2047, 2048)], mes.iloc[:, 1][0:2048], label='Measurement')
plt.plot(np.linspace(0,2047,683),simulation_data[0:683], label='Simulation*3')
plt.show()