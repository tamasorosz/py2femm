import numpy as np
import pandas as pd
from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import silhouette_score
from joblib import Parallel, delayed
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, MaxAbsScaler, Normalizer, \
    PowerTransformer, QuantileTransformer
from tqdm import tqdm
from joblib import parallel_backend

# Load your DataFrame
df = pd.read_csv('../refined/case1_all.csv')
del df['ANG']
df = df.iloc[:, :-3]

scaler = StandardScaler()
scaler.fit(df)
X = scaler.transform(df)

k_values = range(2,3)

def evaluate_k(k):
    kmeans = MiniBatchKMeans(n_clusters=k, batch_size=2048, random_state=42)
    labels = kmeans.fit_predict(X)
    s_score = silhouette_score(X, labels)
    inertia = kmeans.inertia_
    return k, s_score, inertia, kmeans.cluster_centers_

# Parallel evaluation across k values
with parallel_backend("loky"):
    results = Parallel(n_jobs=8)(
        delayed(evaluate_k)(k) for k in tqdm(k_values)
    )

# Unpack results
ks, silhouettes, inertias, centroids_list = zip(*results)

# Plot
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(ks, inertias, '-o')
plt.title('Elbow Method')
plt.xlabel('k')
plt.ylabel('Inertia')

plt.subplot(1, 2, 2)
plt.plot(ks, silhouettes, '-o')
plt.title('Silhouette Score')
plt.xlabel('k')
plt.ylabel('Score')

plt.tight_layout()
plt.show()

# Find best silhouette score
best_idx = np.argmax(silhouettes)
best_k = ks[best_idx]
best_silhouette = silhouettes[best_idx]
best_centroids = centroids_list[best_idx]

print(f"\n✅ Best silhouette score: {best_silhouette:.4f} at k = {best_k}")
print(f"\n✅ Corresponding centroids:\n{best_centroids}")

# Find the closest design (row) to each centroid to use as initial medoids
from sklearn.metrics import pairwise_distances_argmin_min

closest_indices, distances = pairwise_distances_argmin_min(best_centroids, X)

print(f"\n✅ Closest designs (indices) for initial medoids:")
for idx, dist in zip(closest_indices, distances):
    print(f"Medoid index: {idx}, Distance to centroid: {dist:.4f}")

# Optionally, extract these initial medoid designs:
initial_medoids_designs = df.iloc[closest_indices]
initial_medoids_designs['IND'] = closest_indices
initial_medoids_designs.to_csv('initial_medoids_designs.csv', index=False)