from .scrapers import myanimelist as mal

animes_table = mal.getAnimesTable()
print(animes_table)