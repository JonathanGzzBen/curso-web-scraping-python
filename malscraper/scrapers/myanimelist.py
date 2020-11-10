from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

def getSoup(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bs = BeautifulSoup(html.read(), 'html.parser')
        return bs
    except AttributeError as e:
        return None

def get50Animes(offset = 0):
    bs = getSoup(f'https://myanimelist.net/topanime.php?limit={offset}')
    animes_table = bs.find('table', {'class': 'top-ranking-table'})
    animes_containers = animes_table.find_all('tr', {'class': 'ranking-list'})
    animes_data = []
    for anime_container in animes_containers:
        anime_rank = anime_container.find('span', {'class': 'top-anime-rank-text'}).get_text()
        anime_link = anime_container.find('h3', {'class': 'anime_ranking_h3'}).a
        anime_title = anime_link.get_text()
        anime_url = anime_link["href"]
        anime_url = anime_url[0: anime_url.rindex("/")]
        anime_score = anime_container.find('td', {'class': 'score'}).div.span.get_text()
        animes_data.append(
            {
                'rank': anime_rank,
                'title': anime_title,
                'score': anime_score,
                'url': anime_url
            }
        )

    return animes_data

def get_anime_data(anime_url):
    bs = getSoup(anime_url)
    general_information_container = bs.find('td', {'class': 'borderClass'})
    anime_image_url = general_information_container.find('img')["src"]
    return {
        'image_url': anime_image_url
    }
        


