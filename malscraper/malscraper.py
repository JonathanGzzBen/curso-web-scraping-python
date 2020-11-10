from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('https://myanimelist.net/topanime.php?limit=0')
bs = BeautifulSoup(html.read(), 'html.parser')
print(bs.find('table', {'class': 'top-ranking-table'}))
