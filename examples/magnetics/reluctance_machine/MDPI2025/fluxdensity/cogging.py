import numpy as np
import pandas as pd

import numpy as np

# Cogging torque %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Inputs
r = 22.25/1000      # radius [m]
l = 40/1000       # stack length [m]

yBr = pd.read_csv('caseBr_all.csv').iloc[:, 0]
yBt = pd.read_csv('caseBt_all.csv').iloc[:, 0]

# Example: tangential stress list (in Pa)
pt = [-Br*Bt for Br, Bt in zip(yBr, yBt)]

# Number of samples
N = len(pt)

# Create angular positions
theta = np.linspace(0, 2*np.pi, N, endpoint=False)

# Convert pt list to numpy array
pt = np.array(pt)

# Numerical integration using trapezoidal rule
Ft = r**2 * l / (4*np.pi*1e-7) * np.trapezoid(pt, theta) * 1000

print(f"Cogging torque Ft = {Ft:.6f} mNm")

# # Tangential force %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import numpy as np

# Inputs
r = 22.25/1000      # radius [m]
l = 40/1000       # stack length [m]

yBr = pd.read_csv('caseBr.csv').iloc[:, 1]
yBt = pd.read_csv('caseBt.csv').iloc[:, 1]

# Example: tangential stress list (in Pa)
pt = [-Br*Bt for Br, Bt in zip(yBr, yBt)]

pt_t1 = pt[:524]
pt_t2 = pt[524:]

# Number of samples
Nt1 = len(pt_t1)
Nt2 = len(pt_t2)

# Create angular positions
theta_t1 = np.linspace(0, np.radians(14.86), Nt1, endpoint=False)
theta_t2 = np.linspace(0, np.radians(28.71), Nt2, endpoint=False)

# Convert pt list to numpy array
pt_t1 = np.array(pt_t1)
pt_t2 = np.array(pt_t2)

# Numerical integration using trapezoidal rule
Ft_t1 = r * l / (4*np.pi*1e-7) * np.trapezoid(pt_t1, theta_t1)
Ft_t2 = r * l / (4*np.pi*1e-7) * np.trapezoid(pt_t2, theta_t2)

print(f"Tangential force Ft_t1 = {Ft_t1:.6f} N")
print(f"Tangential force Ft_t2 = {Ft_t2:.6f} N")

# Tangential force %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import numpy as np

# Inputs
r = 22.25/1000      # radius [m]
l = 40/1000       # stack length [m]

yAr = pd.read_csv('caseAr.csv').iloc[:, 1]
yAt = pd.read_csv('caseAt.csv').iloc[:, 1]

# Example: tangential stress list (in Pa)
pt = [-Ar*At for Ar, At in zip(yAr, yAt)]

pt_t1 = pt[:524]
pt_t2 = pt[524:]

# Number of samples
Nt1 = len(pt_t1)
Nt2 = len(pt_t2)

# Create angular positions
theta_t1 = np.linspace(0, np.radians(14.86), Nt1, endpoint=False)
theta_t2 = np.linspace(0, np.radians(28.71), Nt2, endpoint=False)

# Convert pt list to numpy array
pt_t1 = np.array(pt_t1)
pt_t2 = np.array(pt_t2)

# Numerical integration using trapezoidal rule
Ft_t1 = r * l / (4*np.pi*1e-7) * np.trapezoid(pt_t1, theta_t1)
Ft_t2 = r * l / (4*np.pi*1e-7) * np.trapezoid(pt_t2, theta_t2)

print(f"Tangential force Ft_t1 = {Ft_t1:.6f} N")
print(f"Tangential force Ft_t2 = {Ft_t2:.6f} N")