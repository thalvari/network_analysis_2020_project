from collections import Counter

import networkx as nx
import pandas as pd
from IPython.core.display import display, HTML


def display_side_by_side(dfs:list, captions:list):
    """Display tables side by side to save vertical space
    Input:
        dfs: list of pandas.DataFrame
        captions: list of table captions
    """
    output = ""
    combined = dict(zip(captions, dfs))
    for caption, df in combined.items():
        output += df.style.set_table_attributes("style='display:inline'").set_caption(caption)._repr_html_()
        output += "\xa0\xa0\xa0"
    display(HTML(output))


def print_leaderboards(G, clusters, by="betweenness"):
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

    # Add betweeness
    betweeness = nx.betweenness_centrality(G)
    df_betweeness = pd.DataFrame(betweeness.items(), columns=['nconst', 'betweenness'])
    df_actor_info = df_actor_info.merge(df_betweeness, how='inner')
    # print(df_actor_info.shape)

    # Import Actor names data
    df_names = pd.read_csv("data/actor_names.csv", sep=",").reset_index()
    df_names = df_names.drop("index", axis=1)
    # print(df_names.shape)

    # Merge names to actor info dataframe. Columns: nconst, cluster, degree, primaryName
    df_actor_info = df_actor_info.merge(df_names, how='inner')
    # print(df_actor_info.shape)

    # Sort results
    df_actor_info = df_actor_info.sort_values(by=by, ascending=False)

    # Print every cluster top5 actors
    df_list = []
    caption_list = []
    for i in range(len(counter) - 1):
        # print("")
        caption_list.append(f"Cluster index: {i}")
        cluster_top_actors = df_actor_info.loc[df_actor_info['cluster'] == i]
        # print("Cluster shape:", cluster_top_actors.shape)
        df_list.append(cluster_top_actors.reset_index().drop(["cluster", "index", "nconst"], axis=1).head())

    display_side_by_side(df_list, caption_list)
