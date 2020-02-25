import pickle

import imdb
import pandas as pd

with open("data/actors.pkl", "rb") as f:
    df = pd.DataFrame(sorted(pickle.load(f))[:10], columns=["nconst"])

print(df)


def get_country(nconst):
    ia = imdb.IMDb()
    person = ia.get_person(nconst[2:])
    country = person.data["birth info"]["birth place"].split(",")[-1].strip()
    return country


df["birth_country"] = df["nconst"].apply(get_country)
print(df)
