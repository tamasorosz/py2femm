import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
matplotlib.use("QtAgg")

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Generate X and Y values
X_vals = np.linspace(15, 25, 11)  # Range 15 to 25
Y_vals = np.linspace(60, 140, 91)  # Range 60 to 140

# Create meshgrid for 3D plotting
X, Y = np.meshgrid(X_vals, Y_vals)

# Compute Z values
Z = np.zeros_like(X)
W = np.zeros_like(X)

for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        midpoint = np.cos(np.radians(X[i, j] / 2)) * 22
        distance = 2 * np.sin(np.radians(X[i, j] / 2)) * 22
        R = distance / (2 * np.tan(np.radians(Y[i, j]  / 2)))
        centerpoint = midpoint + R
        radius = np.sqrt(22 ** 2 + centerpoint ** 2 - (2 * 22 * centerpoint * np.cos(np.radians(X[i, j] / 2))))
        selection_point = centerpoint - radius
        Z[i, j] = 22 - selection_point  # Final Z value
        A = 1 / np.tan(np.radians(X[i, j] / 2))
        B = 1 / np.tan(np.radians(Y[i, j] / 2))
        W[i, j] = 22 * (1 - np.sin(np.radians(X[i, j] / 2)) * (A+B-np.sqrt(1+B**2)))

# Create 3D figure
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='k', alpha=0.7)
ax.plot_surface(X, Y, W, cmap='viridis', edgecolor='k', alpha=0.7)

# Set labels with fontsize 18
ax.set_xlabel("X0 [deg]", fontsize=18, labelpad=12)
ax.set_ylabel("X1 [deg]", fontsize=18, labelpad=14)
ax.set_zlabel("X5 [mm]", fontsize=18, labelpad=10)

# Set tick parameters with fontsize 18
ax.tick_params(axis='both', which='major', labelsize=18)

# plt.savefig('3Dplot.png', dpi=300)
plt.show()

