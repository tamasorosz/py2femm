# Tangential force %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

resA_T4 = []
resA_T3 = []

# Inputs
r = 22.25/1000      # radius [m]
l = 40/1000       # stack length [m]

dfArl = pd.read_csv('caseAr_left.csv')
dfAtl = pd.read_csv('caseAt_left.csv')

for i in range(len(dfArl.columns)):
    # Example: tangential stress list (in Pa)
    pt = [Ar*At for Ar, At in zip(dfArl.iloc[:,i], dfAtl.iloc[:,i])]

    pt_t4 = pt[:1066]
    pt_t3 = pt[1066:]

    # Number of samples
    Nt4 = len(pt_t4)
    Nt3 = len(pt_t3)

    # Create angular positions
    theta_t4 = np.linspace(0, np.radians(14.86), Nt4, endpoint=False)
    theta_t3 = np.linspace(0, np.radians(28.71), Nt3, endpoint=False)

    # Convert pt list to numpy array
    pt_t4 = np.array(pt_t4)
    pt_t3 = np.array(pt_t3)

    # Numerical integration using trapezoidal rule
    Ft_t4 = -1 * r * l / (4*np.pi*1e-7) * np.trapezoid(pt_t4, theta_t4)
    Ft_t3 = r * l / (4*np.pi*1e-7) * np.trapezoid(pt_t3, theta_t3)

    resA_T4.append(Ft_t4)
    resA_T3.append(Ft_t3)

dAT1 = np.gradient(resA_T4, np.linspace(0, 7.5, 16))
dAT2 = np.gradient(resA_T3, np.linspace(0, 7.5, 16))
plt.plot(resA_T4)
plt.plot(resA_T3)
plt.show()
plt.plot(dAT1)
plt.plot(dAT2)
plt.show()