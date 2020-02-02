import pickle

import pandas as pd

n_projects_min = 50
n_shared_projects_edge = 10

df = pd.read_csv("data/actors.csv")
df['count'] = df['nconst'].map(df['nconst'].value_counts())
df = df[df['count'] >= n_projects_min]
data = df.values
print(len(data))

title_dict = dict()
for x in data:
    if x[0] not in title_dict:
        title_dict[x[0]] = list()
    title_dict[x[0]].append(x[1])

edge_dict = dict()
edge_list = []
for x in data:
    for y in title_dict[x[0]]:
        if y < x[1]:
            a = y
            b = x[1]
        else:
            a = x[1]
            b = y
        if (a, b) not in edge_dict:
            edge_dict[(a, b)] = 1
        else:
            edge_dict[(a, b)] += 1
        if edge_dict[(a, b)] == n_shared_projects_edge:
            edge_list.append((a, b))

with open("data/imdb.p", "wb") as f:
    pickle.dump(edge_list, f)

print(len(edge_list))
