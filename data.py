import pickle

import pandas as pd

df = pd.read_csv("actors.csv")
df['count'] = df['nconst'].map(df['nconst'].value_counts())
df.sort_values('count', ascending=False, inplace=True)
data = df.values[:10000000]
print(len(df.values))
print(data)

title_dict = dict()
for x in data:
    if x[0] not in title_dict:
        title_dict[x[0]] = list()
    title_dict[x[0]].append(x[1])

edge_set = set()
for x in data:
    for y in title_dict[x[0]]:
        if (y, x[1]) not in edge_set:
            edge_set.add((x[1], y))

with open("imdb.p", "wb") as f:
    pickle.dump(list(edge_set), f)

print(len(list(edge_set)))
