import itertools
import pickle

import networkx as nx
import pandas as pd

n_projects_min = 10
n_shared_projects_edge = 1

df = pd.read_csv("data/movie_actors.csv")
df = df.drop("index", axis=1)

df['count'] = df['nconst'].map(df['nconst'].value_counts())
df = df[df['count'] >= n_projects_min]

data = df.values
title_dict = dict()
for x in data:
    if x[0] not in title_dict:
        title_dict[x[0]] = set()
    title_dict[x[0]].add(x[1])

edge_set = set()
edge_dict = dict()
for x in title_dict.values():
    for e in itertools.combinations(x, 2):
        if e in edge_dict:
            pass
        elif (e[1], e[0]) in edge_dict:
            e = (e[1], e[0])
        else:
            edge_dict[e] = 0
        edge_dict[e] += 1
        if edge_dict[e] == n_shared_projects_edge:
            edge_set.add(e)
edge_list = list(edge_set)

with open("data/imdb.p", "wb") as f:
    pickle.dump(edge_list, f)

nodes = set()
for e in edge_list:
    nodes.add(e[0])
    nodes.add(e[1])
print(f"nodes: {len(nodes)}")
print(f"edges: {len(edge_list)}")

G = nx.Graph()
G.add_edges_from(edge_list)

largest_cc = G.subgraph(max(nx.connected_components(G), key=len))
print(f"largest cc nodes: {len(nx.nodes(largest_cc))}")
print(f"largest cc edges: {len(nx.edges(largest_cc))}")
