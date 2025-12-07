import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

sim = pd.read_csv('2D_FEMM_Steel_18mm_full_base.csv')

def rotate(arr, k=0):
    k %= len(arr)
    return arr[-k:] + arr[:-k]

for k in [-65, -64, -63]:
    base = list(sim["torque"])
    skew1 = rotate(list(sim["torque"]), k)

    simulation_data = rotate([(i+j)/1000 for i,j in zip(base, skew1)], 0)

    l = 0
    m = 86
    n = 85
    cog = []
    while m < 2040:
        ymin = min(simulation_data[l:m])
        ymax = max(simulation_data[l:m])
        cog.append(ymax - ymin)
        l += n
        m += n
    print("Periodic:", max(cog)*1000)