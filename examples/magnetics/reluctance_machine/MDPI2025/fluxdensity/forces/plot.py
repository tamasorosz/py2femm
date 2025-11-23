import matplotlib.pyplot as plt
import pandas as pd

dfA = pd.read_csv('forces_caseA')
dfB = pd.read_csv('forces_caseB')

posA = [x+y for x, y in zip(dfA.iloc[:, 1], dfA.iloc[:, 3])]
negA = [x+y for x, y in zip(dfA.iloc[:, 2], dfA.iloc[:, 4])]

posB = [x+y for x, y in zip(dfB.iloc[:, 1], dfB.iloc[:, 3])]
negB = [x+y for x, y in zip(dfB.iloc[:, 2], dfB.iloc[:, 4])]

diffA = [n-p for n,p in zip(negA,posA)]
diffB = [n-p for n,p in zip(negB,posB)]


plt.plot(diffA)
plt.plot(diffB)
plt.show()