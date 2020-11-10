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

def getAnimesTable():
    bs = getSoup('https://myanimelist.net/topanime.php?limit=0')
    print(bs.find('table', {'class': 'top-ranking-table'}))
