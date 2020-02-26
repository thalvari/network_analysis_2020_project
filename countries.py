import imdb


def get_country(nconst):
    try:
        ia = imdb.IMDb()
        person = ia.get_person(nconst[2:])
        birth_place = ""
        country = ""
        if "birth info" in person.data:
            birth_place = person.data["birth info"]["birth place"]
            country = birth_place.split(",")[-1].strip()
            country = country.split("[now ")[-1].strip()
            if country[:3] == "in ":
                country = country[3:].strip()
            country = "".join([ch for ch in country if ch.isalpha() or ch in {" ", "-"}])
        print(nconst + "|" + country + "|" + birth_place)
    except:
        country = ""
        print(nconst + "|ERROR")
    return country


def get_countries(df):
    df["birth_country"] = df["nconst"].apply(get_country)
    return df
