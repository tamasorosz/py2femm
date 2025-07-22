Xmin = 15
Xmax = 25
X = 25

X_std = (X - Xmin) / (Xmax - Xmin)
print(X_std)

X_scaled = X_std * (Xmax - Xmin) + Xmin
print(X_scaled)