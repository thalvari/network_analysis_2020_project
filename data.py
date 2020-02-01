import pickle

import pandas as pd

df = pd.read_csv("actors.csv")
df['count'] = df['nconst'].map(df['nconst'].value_counts())
df = df[df['count'] >= 20]
data = df.values
print(len(data))

# print(df.sort_values('count', ascending=False))

title_dict = dict()
for x in data:
    if x[0] not in title_dict:
        title_dict[x[0]] = list()
    title_dict[x[0]].append(x[1])

# edge_set = set()
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
        if edge_dict[(a, b)] == 20:
            edge_list.append((a, b))
        # if (y, x[1]) not in edge_set:
        #     edge_set.add((x[1], y))

with open("imdb.p", "wb") as f:
    # pickle.dump(list(edge_set), f)
    pickle.dump(edge_list, f)

# print(len(list(edge_set)))
print(len(edge_list))
