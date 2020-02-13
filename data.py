import pickle

import pandas as pd

n_projects_min = 10
n_shared_projects_edge = 1

df = pd.read_csv("data/movie_actors.csv")
df = df.drop("index", axis=1)
print(df.shape[0])

df['count'] = df['nconst'].map(df['nconst'].value_counts())
df = df[df['count'] >= n_projects_min]
print(df.shape[0])

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

print(len(edge_list))

with open("data/imdb.p", "wb") as f:
    pickle.dump(edge_list, f)
