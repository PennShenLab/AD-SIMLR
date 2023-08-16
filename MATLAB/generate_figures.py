# Import necessary libraries
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Define different methods and corresponding titles
methods = ["SC", "SC_diff", "SIMLR", "SIMLR_diff"]
title = ["Traditional Spectral Clustering", "Spectral Clustering + Network Diffusion", "SIMLR w/o Network Diffusion", "SIMLR + Network Diffusion"]

# Define file paths for latent embeddings, similarity matrices, and labels
latent_files = [f"/content/drive/MyDrive/Shen Lab/TADPOLE/data_final/latent_{m}.txt" for m in methods]
latent_embed = [np.loadtxt(fn, delimiter=",") for fn in latent_files]

S_matrix_files = [f"/content/drive/MyDrive/Shen Lab/TADPOLE/data_final/simMat_{m}.txt" for m in methods]
S_matrices = [np.loadtxt(fn, delimiter=",") for fn in S_matrix_files]

labels_files = [f"/content/drive/MyDrive/Shen Lab/TADPOLE/data_final/clusters_labels_{m}.txt" for m in methods]
labels = [np.loadtxt(fn, delimiter=",") for fn in labels_files]
kmeans_labels = np.loadtxt("/content/drive/MyDrive/Shen Lab/TADPOLE/data_final/clusters_labels_kmeans.txt", delimiter=",")
labels.append(kmeans_labels)

tsne_vis_files = [f"/content/drive/MyDrive/Shen Lab/TADPOLE/data_final/tsne_visualization_{m}.txt" for m in methods]
tsne_vis = [np.loadtxt(fn, delimiter=",") for fn in tsne_vis_files]
kmeans_vis = np.loadtxt("/content/drive/MyDrive/Shen Lab/TADPOLE/data_final/tsne_visualization_kmeans.txt", delimiter=",")
tsne_vis.append(kmeans_vis)

# Define a function to display a similarity matrix
def showSimMat(S_mat, labels):
    idx = np.argsort(labels) # sort indices according to labels [1,2,3, ...]
    _, indices = np.unique(labels[idx], return_index=True)
    S_ordered = S_mat[idx][:, idx]

    # Display the heatmap
    sns.heatmap(S_ordered, vmin=0, vmax=0.01, cmap='Oranges', xticklabels=False, yticklabels=False)
    plt.show()

# Display similarity matrices for each method
for i in range(len(methods)):
    showSimMat(S_matrices[i], labels[i])

# 2D visualization using t-SNE
for i in range(len(tsne_vis)):
    plt.figure(figsize=(6, 4.5))
    plt.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    plt.scatter(tsne_vis[i][:, 0], tsne_vis[i][:, 1], c=labels[3], cmap="Set3", s=10)
    plt.show()
