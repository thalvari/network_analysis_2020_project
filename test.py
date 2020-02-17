import pickle
import warnings
warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from collections import Counter
from hdbscan import HDBSCAN
from matplotlib.axes._axes import _log
from matplotlib.cm import get_cmap
from sklearn.manifold import spectral_embedding
from umap import UMAP

_log.setLevel('ERROR')

seed = 42
np.random.seed(seed)

with open("data/imdb.pkl", "rb") as f:
    G = nx.Graph()
    G.add_edges_from(pickle.load(f))

G.remove_nodes_from(set(nx.nodes(G)) - max(nx.connected_components(G), key=len))

print(f"nodes: {len(nx.nodes(G))}")
print(f"edges: {len(nx.edges(G))}")

adj_matrix = nx.to_numpy_array(G)
node_list = list(G.nodes())

embedding = spectral_embedding(adj_matrix, n_components=50, drop_first=False, random_state=np.random.RandomState(seed))
embedding = UMAP(
    n_components=2, n_neighbors=30, min_dist=0.0, random_state=np.random.RandomState(seed)
).fit_transform(embedding)

# modify min_samples, min_cluster_size to add/remove clusters
clusters = HDBSCAN(min_samples=50, min_cluster_size=50, core_dist_n_jobs=-1).fit_predict(embedding)

counter = Counter(clusters)
print(f"clusters: {len(counter) - 1}")
print(f"cluster sizes: {sorted(counter.items(), key=lambda x: x[1], reverse=True)}")
print(f"noise level: {np.round(counter[-1] / len(clusters), 3)}")

# add code here

print(node_list[:5])
print(clusters[:5])

# only visualization after this


def draw_network(G, pos, node_colors, pdf_name, edge_width=.1, font_size=1):
    nx.draw_networkx_nodes(G, pos=pos, node_size=1, node_color=node_colors)
    nx.draw_networkx_edges(G, pos=pos, width=edge_width)
    # nx.draw_networkx_labels(G, pos=pos, font_size=font_size)
    plt.savefig(f"results/{pdf_name}.pdf")
    plt.show()


cmap = get_cmap("tab20").colors
cmap = [cmap[i] for i in range(len(cmap)) if i % 2 == 0] + [cmap[i] for i in range(len(cmap)) if i % 2 == 1]
node_colors = [cmap[cluster] for cluster in clusters]
pos_su = {node_list[i]: embedding[i] for i in range(len(node_list))}

draw_network(G, pos=pos_su, node_colors=node_colors, pdf_name="test")
