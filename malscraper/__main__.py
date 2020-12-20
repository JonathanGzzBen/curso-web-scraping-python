from .scrapers import myanimelist as mal

animes_first_50 = mal.get50Animes()

for anime in animes_first_50:
    print(mal.get_anime_data(anime["url"]))
