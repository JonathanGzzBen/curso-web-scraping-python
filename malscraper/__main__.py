from .scrapers import myanimelist as mal

animes_first_50_skip_2 = mal.get50Animes(2)
anime = animes_first_50_skip_2[0]

print(mal.get_anime_data(anime["url"]))
