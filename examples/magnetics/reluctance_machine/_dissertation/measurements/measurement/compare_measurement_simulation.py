import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

mes = pd.read_csv('../measurement/measurement_filtered.csv')
sim = pd.read_csv('2D_FEMM_Steel_18mm_full_base.csv')

def rotate(arr, k=0):
    k %= len(arr)
    return arr[-k:] + arr[:-k]

base = list(sim["torque"])
skew1 = rotate(list(sim["torque"]), -64)

simulation_data = rotate([(i+j)/1000 for i,j in zip(base, skew1)], -13)

# plt.plot([i * 1 for i in np.linspace(0,2047, 2048)], mes.iloc[:, 1][0:2048], label='Measurement')
# plt.plot(np.linspace(0,2047,2048),simulation_data, label='Simulation')
# plt.legend()
# plt.show()

# === Plot settings ===
colors = ["#B90276", "#50237F", "#00A8B0", "#006249", "#525F6B",
          "#FF5733", "#2E86C1", "#28B463", "#F1C40F", "#8E44AD"]

plt.figure(figsize=(8, 6))
plt.rcParams.update({'font.size': 18})

plt.plot([i * 1 for i in np.linspace(0,45, 256)], mes.iloc[:, 1][0:256]*1000, label='Measurement', color=colors[0], linestyle='-', linewidth=2)
plt.plot(np.linspace(0,45,256),[i*1000 for i in simulation_data[0:256]], label='Simulation', color=colors[2], linestyle='--', linewidth=3)

# === Final styling ===
plt.xlabel("Rotor Position [deg]", fontsize=18)
plt.xticks(np.arange(0, 46, 5))
plt.ylabel("Cogging Torque [mNm]", fontsize=18)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(fontsize=16, ncol=2)
plt.tight_layout()
plt.savefig('measurement_cogging_comparison_2D.png', dpi=300)
plt.show()

print(max(simulation_data[0:86])-min(simulation_data[0:86]))
print(max(mes.iloc[:, 1][0:86])-min(mes.iloc[:, 1][0:86]))

# plt.plot([i*1 for i in np.linspace(0,2047, 2048)], mes.iloc[:, 1][0:2048], label='Measurement')
# plt.plot(np.linspace(0,2047,683),simulation_data[0:683], label='Simulation*3')
# plt.show()
#
# simulation_data = rotate([(i+j)/1000 for i,j in zip(base, skew)], -45)
#
# plt.plot([i*1.045 for i in np.linspace(0,6143, 6148)], mes.iloc[:, 1][0:6148], label='Measurement')
# plt.plot(np.linspace(0,6413,2048),simulation_data, label='Simulation*3')
# plt.show()
#
# plt.plot([i*1 for i in np.linspace(0,2047, 2048)], mes.iloc[:, 1][0:2048], label='Measurement')
# plt.plot(np.linspace(0,2047,683),simulation_data[0:683], label='Simulation*3')
# plt.show()