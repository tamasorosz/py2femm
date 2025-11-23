import numpy as np
import matplotlib.pyplot as plt

colors = ["#B90276", "#50237F", "#00A8B0", "#006249", "#525F6B",
          "#FF5733", "#2E86C1", "#28B463", "#F1C40F", "#8E44AD"]

# Create the x-axis (load angle)
x = np.linspace(0, 2 * np.pi, 500)

# Define three example waveforms (representing torque components)
T_PM = 2.0 * np.sin(x)            # PM torque component
T_REL = 1.0 * np.sin(2 * x) # Reluctance torque component
T_SUM = T_PM + T_REL                  # Resultant torque

# Create the plot
plt.figure(figsize=(8, 6))
plt.plot(x, T_PM, linestyle='--', color=colors[0], linewidth=2.5, label=r'T$_\mathrm{PM}$')
plt.plot(x, T_REL, linestyle='--', color=colors[1], linewidth=2.5, label=r'T$_\mathrm{REL}$')
plt.plot(x, T_SUM, linestyle='-', color=colors[2], linewidth=3, label=r'T$_\mathrm{SUM}$')

# Labels and formatting
plt.xlabel(r'Load angle [rad]', fontsize=18)
plt.ylabel(r'Torque [Nm]', fontsize=18)
plt.xticks(
    [0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi],
    ["0", "π/2", "π", "3π/2", "2π"],
    fontsize=18
)
plt.yticks(fontsize=18)
plt.legend(fontsize=18, loc='best', framealpha=0.9)
plt.grid(True, linestyle=':', linewidth=0.7)

plt.tight_layout()
plt.savefig('thesis3_sinewaves_pmsm', dpi=600)
plt.show()

import numpy as np
import matplotlib.pyplot as plt

colors = ["#B90276", "#50237F", "#00A8B0", "#006249", "#525F6B",
          "#FF5733", "#2E86C1", "#28B463", "#F1C40F", "#8E44AD"]

# Create the x-axis (load angle)
x = np.linspace(0, 2 * np.pi, 500)

# Define three example waveforms (representing torque components)
T_PM = 1.0 * np.sin(x)            # PM torque component
T_REL = 2.0 * np.sin(2 * x) # Reluctance torque component
T_SUM = T_PM + T_REL                  # Resultant torque

# Create the plot
plt.figure(figsize=(8, 6))
plt.plot(x, T_PM, linestyle='--', color=colors[0], linewidth=2.5, label=r'T$_\mathrm{PM}$')
plt.plot(x, T_REL, linestyle='--', color=colors[1], linewidth=2.5, label=r'T$_\mathrm{REL}$')
plt.plot(x, T_SUM, linestyle='-', color=colors[2], linewidth=3, label=r'T$_\mathrm{SUM}$')

# Labels and formatting
plt.xlabel(r'Load angle [rad]', fontsize=18)
plt.ylabel(r'Torque [Nm]', fontsize=18)
plt.xticks(
    [0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi],
    ["0", "π/2", "π", "3π/2", "2π"],
    fontsize=18
)
plt.yticks(fontsize=18)
plt.legend(fontsize=18, loc='best', framealpha=0.9)
plt.grid(True, linestyle=':', linewidth=0.7)

plt.tight_layout()
plt.savefig('thesis3_sinewaves_fipmasynrm', dpi=600)
plt.show()

