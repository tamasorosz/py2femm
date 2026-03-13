# Tangential force %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
resA_T4 = []
resA_T3 = []

# Inputs
r = 22.25/1000      # radius [m]
l = 40/1000       # stack length [m]

dfArl = pd.read_csv('caseBr_left.csv')
dfAtl = pd.read_csv('caseBt_left.csv')

for i in range(len(dfArl.columns)):
    # Example: tangential stress list (in Pa)
    pt = [Ar*At for Ar, At in zip(dfArl.iloc[:,i], dfAtl.iloc[:,i])]

    pt_t4 = pt[:1054]
    pt_t3 = pt[1054:]

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
    Ft_t4 = -1 * r * l / (4*np.pi*1e-7) * np.trapz(pt_t4, theta_t4)
    Ft_t3 = r * l / (4*np.pi*1e-7) * np.trapz(pt_t3, theta_t3)

    resA_T4.append(Ft_t4)
    resA_T3.append(Ft_t3)

resA_T2 = []
resA_T1 = []

# Inputs
r = 22.25/1000      # radius [m]
l = 40/1000       # stack length [m]

dfArr = pd.read_csv('caseBr_right.csv')
dfAtr = pd.read_csv('caseBt_right.csv')

for i in range(len(dfArr.columns)):
    # Example: tangential stress list (in Pa)
    pt = [Ar*At for Ar, At in zip(dfArr.iloc[:,i], dfAtr.iloc[:,i])]

    pt_t2 = pt[:1950]
    pt_t1 = pt[1950:]

    # Number of samples
    Nt2 = len(pt_t2)
    Nt1 = len(pt_t1)

    # Create angular positions
    theta_t2 = np.linspace(0, np.radians(28.71), Nt2, endpoint=False)
    theta_t1 = np.linspace(0, np.radians(14.86), Nt1, endpoint=False)

    # Convert pt list to numpy array
    pt_t2 = np.array(pt_t2)
    pt_t1 = np.array(pt_t1)

    # Numerical integration using trapezoidal rule
    Ft_t2 = -1 * r * l / (4*np.pi*1e-7) * np.trapz(pt_t2, theta_t2)
    Ft_t1 = r * l / (4*np.pi*1e-7) * np.trapz(pt_t1, theta_t1)

    resA_T2.append(Ft_t2)
    resA_T1.append(Ft_t1)

plt.plot(resA_T4)
plt.plot(resA_T3)
plt.plot(resA_T2)
plt.plot(resA_T1)
plt.show()

plt.plot(pos:=[a+b for a, b in zip(resA_T4,resA_T2)])
plt.plot(neg:=[a+b for a, b in zip(resA_T3,resA_T1)])
plt.show()

plt.plot([n-p for n,p in zip(neg,pos)])
plt.show()

df_save = pd.DataFrame({
    'T4': resA_T4,
    'T3': resA_T3,
    'T2': resA_T2,
    'T1': resA_T1
})

df_save.to_csv('forces_caseB')


