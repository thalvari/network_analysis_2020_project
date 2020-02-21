import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

from matplotlib.cm import get_cmap
from matplotlib.patches import Patch

colors = plt.cm.tab20.colors + tuple(plt.cm.tab20b.colors[i] for i in [0, 1, 4, 5, 8, 9, 12, 13, 16, 17])
print(len(colors))

# print(len(colors))
# G = nx.empty_graph(len(colors))
# patch_list = [Patch(color=colors[i], label=i) for i in range(len(colors))]
# pos_sp = nx.spring_layout(G, seed=42)
# nx.draw_networkx_nodes(G, pos=pos_sp, node_color=colors)
# plt.legend(handles=patch_list, loc="center left", bbox_to_anchor=(1, 0.5), ncol=2, fancybox=True)
# plt.tight_layout()
# plt.show()
