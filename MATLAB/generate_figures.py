# Import necessary libraries
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import argparse

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="generating figures script")
    parser.add_argument("--dir", type=str, default="results", help="Directory containing the data")
    args = parser.parse_args()
    
    # Define different methods and corresponding titles
    methods = ["SC", "SC_diff", "SIMLR", "SIMLR_diff"]
    title = ["Traditional Spectral Clustering", "Spectral Clustering + Network Diffusion", "SIMLR w/o Network Diffusion", "SIMLR + Network Diffusion"]

    # import pdb; pdb.set_trace()
    # Define file paths for latent embeddings, similarity matrices, and labels
    latent_files = [f"{args.dir}/latent_{m}.txt" for m in methods]
    latent_embed = [np.loadtxt(fn, delimiter=",") for fn in latent_files]

    S_matrix_files = [f"{args.dir}/simMat_{m}.txt" for m in methods]
    S_matrices = [np.loadtxt(fn, delimiter=",") for fn in S_matrix_files]

    labels_files = [f"{args.dir}/clusters_labels_{m}.txt" for m in methods]
    labels = [np.loadtxt(fn, delimiter=",") for fn in labels_files]
    kmeans_labels = np.loadtxt(f"{args.dir}/clusters_labels_kmeans.txt", delimiter=",")
    labels.append(kmeans_labels)

    tsne_vis_files = [f"{args.dir}/tsne_visualization_{m}.txt" for m in methods]
    tsne_vis = [np.loadtxt(fn, delimiter=",") for fn in tsne_vis_files]
    kmeans_vis = np.loadtxt(f"{args.dir}/tsne_visualization_kmeans.txt", delimiter=",")
    tsne_vis.append(kmeans_vis)

    # Define a function to display a similarity matrix
    def showSimMat(S_mat, labels, fig_title):
        idx = np.argsort(labels) # sort indices according to labels [1,2,3, ...]
        _, indices = np.unique(labels[idx], return_index=True)
        S_ordered = S_mat[idx][:, idx]

        # Display the heatmap
        sns.heatmap(S_ordered, vmin=0, vmax=min(0.01,np.max(S_ordered)), cmap='Oranges', xticklabels=False, yticklabels=False)
        plt.savefig(f"{args.dir}/simMat_{fig_title}.png", dpi=300, bbox_inches='tight')
        plt.show()

    # Display similarity matrices for each method
    for i in range(len(methods)):
        showSimMat(S_matrices[i], labels[i], methods[i])

    # 2D visualization using t-SNE
    for i in range(len(tsne_vis)):
        plt.figure(figsize=(6, 4.5))
        plt.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        plt.scatter(tsne_vis[i][:, 0], tsne_vis[i][:, 1], c=labels[i], cmap="Set3", s=10)
        if i < len(tsne_vis) - 1:
            plt.savefig(f"{args.dir}/tsne_{methods[i]}.png", dpi=300, bbox_inches='tight')
        else: 
            plt.savefig(f"{args.dir}/tsne_kmeans.png", dpi=300, bbox_inches='tight')
        plt.show()
        
if __name__ == "__main__":
    main()
    print("Done!")
