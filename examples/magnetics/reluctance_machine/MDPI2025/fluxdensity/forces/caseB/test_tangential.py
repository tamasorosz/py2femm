import pandas as pd
from matplotlib import pyplot as plt

dfAtl = pd.read_csv("caseBt_left.csv")
dfAtr = pd.read_csv("caseBt_right.csv")

for i in range(len(dfAtl.columns)):
    yAtl = dfAtl.iloc[:, i].tolist()
    yAtr = [-e for e in dfAtr.iloc[:, i].tolist()]

    plt.plot(yAtl+yAtr)

plt.show()