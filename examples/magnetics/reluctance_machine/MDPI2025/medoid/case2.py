import numpy as np
import pandas as pd
from pyclustering.cluster.kmedoids import kmedoids as KMedoids
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
from multiprocessing import Pool

def compute_silhouette_for_k(args):
    k, D, n_samples = args
    # Initialize medoids randomly for each k
    initial_medoids = np.random.choice(n_samples, k, replace=False).tolist()
    kmedoids_instance = KMedoids(data=D, initial_index_medoids=initial_medoids, data_type='distance_matrix')
    kmedoids_instance.process()
    clusters = kmedoids_instance.get_clusters()
    medoids = kmedoids_instance.get_medoids()

    # Assign labels based on clusters
    labels = np.empty(n_samples, dtype=int)
    for cluster_id, cluster_indices in enumerate(clusters):
        labels[cluster_indices] = cluster_id

    # Compute silhouette score
    score = silhouette_score(D, labels, metric='precomputed')
    print(f"k={k}, silhouette score={score:.4f}")
    return k, score, medoids

if __name__ == "__main__":
    # ---------------- Simulated Data ----------------
    D = pd.read_parquet(
        '../eculidean/distance_df_case2_case2.parquet')
    # chunk_size = 2000

    # D = D.iloc[:chunk_size, :chunk_size]
    D = D.values

    # Range of k values to test
    k_values = list(range(2, len(D)))
    args_list = [(k, D, len(D)) for k in k_values]

    # ---------------- Parallel Execution ----------------
    with Pool(32) as pool:
        results = pool.map(compute_silhouette_for_k, args_list)

    # Sort and extract results
    results.sort(key=lambda x: x[0])
    ks, sil_scores, medoids = zip(*results)

    # ---------------- Plot ----------------
    plt.figure(figsize=(8, 5))
    plt.plot(ks, sil_scores, marker='o')
    plt.title("Silhouette Score vs. Number of Clusters (k)")
    plt.xlabel("Number of clusters (k)")
    plt.ylabel("Silhouette score")
    plt.grid(True)
    plt.show()

    # ---------------- Best k ----------------
    best_idx = np.argmax(sil_scores)
    best_k = ks[best_idx]
    print(f"\nBest k based on silhouette score: {best_k} (score = {sil_scores[best_idx]:.4f}), medoids = {medoids[best_idx]}")