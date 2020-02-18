from collections import Counter

import networkx as nx
import pandas as pd


def print_leaderboards(G, clusters):
    counter = Counter(clusters)
    node_list = list(G.nodes())

    # Get degree function
    deg = nx.degree(G)

    def getdegree(node):
        degree = deg(node)
        return degree

    # Create dataframe nconst, cluster
    d = {'nconst': node_list, 'cluster': clusters}
    df_actor_info = pd.DataFrame(d)
    # print(df_actor_info.shape)

    # Add degree to dataframe
    df_actor_info['degree'] = df_actor_info['nconst'].apply(getdegree)
    # print(df_actor_info.shape)

    # Import Actor names data
    df_names = pd.read_csv("data/actor_names.csv", sep=",").reset_index()
    df_names = df_names.drop("index", axis=1)
    # print(df_names.shape)

    # Merge names to actor info dataframe. Columns: nconst, cluster, degree, primaryName
    df_actor_info = df_actor_info.merge(df_names, how='inner')
    # print(df_actor_info.shape)

    # Sort results
    df_actor_info = df_actor_info.sort_values(by=['cluster', 'degree'], ascending=False)

    # Print every cluster top5 actors
    for i in range(len(counter) - 1):
        print("")
        print("Cluster index:", i)
        cluster_top_actors = df_actor_info.loc[df_actor_info['cluster'] == i]
        print("Cluster shape:", cluster_top_actors.shape)
        print(cluster_top_actors.head())
