import pickle

import networkx as nx
import pandas as pd

n_projects_min = 1
n_shared_projects_edge = 1

df = pd.read_csv("data/movie_actors.csv")
df = df.drop("index", axis=1)

df['count'] = df['nconst'].map(df['nconst'].value_counts())
df = df[df['count'] >= n_projects_min]

data = df.values
title_dict = dict()
for x in data:
    if x[0] not in title_dict:
        title_dict[x[0]] = list()
    title_dict[x[0]].append(x[1])

coappearances_dict = dict()
edge_list = []
for x in data:
    for y in title_dict[x[0]]:
        if y < x[1]:
            a = y
            b = x[1]
        else:
            a = x[1]
            b = y
        if (a, b) not in coappearances_dict:
            coappearances_dict[(a, b)] = 1
        else:
            coappearances_dict[(a, b)] += 1
        if coappearances_dict[(a, b)] == n_shared_projects_edge:
            edge_list.append((a, b))

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
