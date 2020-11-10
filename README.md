# Web Scraping con Python

## Introducción

Web scraping es en pocas palabras extracción de información
de la web de manera automática, que más adelante podemos procesar.
Existen cientos de aplicaciones que utilizan web scrapers.

Un ejemplo sencillo es esta aplicación web “Linux Compatibility Checker”,
que analiza el sitio de Steam para buscar tu perfil, tus juegos,
y su compatibilidad con Linux consultando el sitio web WineHQ.

En este curso les enseñaré técnicas para obtener información
de sitios web con diferentes estructuras. Crearemos un web
scraper que analizará varias páginas dentro de un mismo sitio
web, para exportar la información a Excel, una base de datos
o un archivo JSON.

Antes de empezar me gustaría aclarar el tema de la legalidad
de los web-scrapers.

En pocas palabras, si son legales, siempre y cuando no abuses
de ellos. Vamos a ver un ejemplo sencillo.

Puedo utilizar un web scraper para que me avise cuando un
producto de edición limitada salga a la venta, para yo mismo
ir al sitio web y comprar dicho producto. Sin embargo, utilizar
este web-scraper para también comprar estos productos en grandes
cantidades si es ilegal, porque estoy afectando directamente a
los demás usuarios.
No tengas miedo a hacer web scraping, sólo usa tu sentido común
para no ser abusivo con usuarios “regulares”.

## Cómo hacer un web scraper

### La metodología

Los web-scraper generalmente siguen la siguiente metodología:

1. Obtener HTML de un sitio web.
2. Parsear ese HTML para obtener información.
3. Almacenar la información.
4. Opcionalmente, dirigirse a otra pagina para repetir el proceso.

Vamos a ver cómo realizar cada uno de estos pasos, uno a uno.

### Obtener HTML de un sitio web

Para empezar, vamos a ver un ejemplo sencillo de cómo obtener
HTML de una página web.
Voy a crear el primer script de este curso.

```python
# page1.py
from urllib.request import urlopen
html = urlopen('http://pythonscraping.com/pages/page1.html')
print(html.read())
```

Como podemos ver, esto nos permite obtener directamente
el HTML de un sitio web, que tambien podemos visitar con
nuestro navegador web.

### Parsear HTML

Ahora vamos con el segundo paso, que es Parsear este HTML.
Para ello utilizaremos una popular librería llamada BeautifulSoup;
la cual se encargará de darnos una interfaz sencilla para manipular el HTML.

Dejaré en los comentarios la página con la documentación
oficial, si es que quieren aprender a utilizarla con mayor
profundidad.

Vamos a instalar BeautifulSoup utilizando PIP.

```shell
pip install beautifulsoup4
```

Ahora crearemos nuestro segundo script.

```python
# soup.py
from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen('http://www.pythonscraping.com/pages/page1.html')
bs = BeautifulSoup(html.read(), 'html.parser')
print(bs.h1)
```

Esto nos permite obtener el primer tag `h1` encontrado
en la página.
También podemos pasar directamente el objecto de archivo
regresado por `urlopen`, así que esto también es válido:

```python
bs = BeautifulSoup(html, 'html.parser')
```

_Ver la estructura en la página web_
Como vemos, `h1` está dos niveles adentro del objeto BeautifulSoup,
porque está adentro de `body`, que está dentro de HTML. Sin embargo,
lo que estamos haciendo es obtener la primera ocurrencia de un `h1`
en todo el archivo. Si queremos ser más específicos, cualquiera
de estas llamadas funciona igual:

- `bs.html.body.h1`
- `bs.body.h1`
- `bs.html.h1`

Con esta información podemos crear los web-scraper que queramos
si aplicamos nuestra lógica, pero BeautifulSoup nos ofrece más
herramientas para facilitarnos el trabajo. Sin embargo, antes de
comenzar a estudiarlas, vamos a analizar algunos posibles errores
que pueden suceder y cómo evitarlos, porque no hay nada peor que
crear un web-scraper y dejarlo correr durante unas horas, sólo para
regresar y darte cuenta de que se detuvo a los 5 minutos porque
hubo un error.

Para empezar, la primera línea de código que nos puede generar
un problema es esta:

```python
html = urlopen('http://www.pythonscraping.com/pages/page1.html'))
```

Aquí pueden salir mal dos cosas:

- La página no se encuentra en el servidor (o hubo un error al obtenerla)
- No se pudo encontrar el servidor

En el primer caso se nos regresará un error HTTP 404 _Página no
encontrada_, HTTP 500, _Error Interno de Servidor_, u otro código
HTTP. En todos estos casos, la función urlopen arroja la excepción
HTTPError. La podemos manejar de la siguiente manera:

```python
from urllib.request import urlopen
from urllib.error import HTTPError

try:
    html = urlopen('http://www.pythonscraping.com/pages/page1.html')
except HTTPError as e:
    print(e)
else:
    # Si haces un return adentro del except, no necesitas este else
```

Aquí, si ocurre una excepción HTTPError en el bloque try, se
ejecutará el codigo de except, y no se ejecutará el código en else.

En el segundo caso, si no se puede encontrar al servidor, ya sea
porque cambió de dirección, lo escribimos mal, o simplemente no
está disponible, urlopen arrojará una excepción URLError. Esto
indica que no se alcanzó ningun servidor, y como el servidor es
el que se encarga de darte una respuesta HTTP, la excepción
HTTPError no lo puede manejar, y es cuando URLError lo debe de
capturar. Podemos usar este código para capturarlo:

```python
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError

try:
    html = urlopen('http://www.pythonscraping.com/pages/page1.html')
except HTTPError as e:
    print(e)
except URLError as e:
    print('The server could not be found!')
else:
    print('It worked')
    # Si haces un return adentro del except, no necesitas este else
```

Ahora, si la página se descarga correctamente del servidor,
aún hay un problema. Cuando intentamos acceder a un tag
utilizando BeautifulSoup, y éste no existe, se nos regresa
un objeto `None`.

```python
print(bs.nonExistentTag)
```

El problema es que si intentamos acceder a una propiedad
de un objeto `None`, se nos arrojará una excepción
`AttributeError`:

```python
print(bs.nonExistentTag.someTag)

# AttributeError: 'NoneType' object has no attribute 'someTag'
```

Esta es la solución más sencilla para esto:

```python
try:
    badContent = bs.nonExistingTag.anotherTag
except AttributeError as e:
    print('Tag was not found')
else:
    if badContent == None:
        print('Tag was not found')
    else:
        print(badContent)
```

Todo este chequeo de errores puede parecer bastante
laborioso al principio, pero es posible organizar mejor
nuestro código para hacerlo más fácil de escribir y de
leer. Por ejemplo, este es nuestro primer scraper escrito
de una manera ligeramente diferente:

```python
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

def getTitle(url):
    try:
        html = urlopen(url)
    except: HTTPError as e:
        return None
    try:
        bs = BeautifulSoup(html.read(), 'html.parser')
        title = bs.body.h1
    except Attribute Error as e:
        return None
    return title

title = getTitle('http://www.pythonscraping.com/pages/page1.html')
if title = None:
    print('Title could not be found')
else:
    print(title)
```

Esto es suficiente para obtener una información sencilla,
pero al momento de escribir scrapers más completos hay que
pensar en el patrón completo que sigue nuestro código para
manejar errores, y hacerlo más legible.

Tener funciones genéricas que incluyan manejo de
excepciones hace que sea más fácil y confiable
desarrollar web-scrapers.

#### Selectores

Prácticamente todos los sitios web que visitamos
utilizan CSS, y éste sigue algun tipo de lógica
que podemos aprovechar para obtener los elementos
que deseamos.

Vamos a tomar como ejemplo esta página:

<http://www.pythonscraping.com/pages/warandpeace.html>

En esta página, las líneas dichas por los personajes
están en rojo, mientras que los nombres de los
personajes están en verde. Esto se consigue gracias
a la clase de los elementos `span`.

Vamos a tomar la página como un objeto `BeautifulSoup`.

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://www.pythonscraping.com/pages/page1.html')
bs = BeautifulSoup(html.read(), 'html.parser')
```

Podemos utilizar la función `find_all` para extraer
una lista de los nombres y pronombres en la pagina si
obtenemos los elementos dentro de `<span class="green"></span>`

```python
nameList = bs.find_all('span', {'class': 'green'})
for name in nameList:
    print(name.get_text())
```

Si lo corremos, nos muestra todos los pronombres
en orden. `get_text()` obtiene el contenido visible
de un tag.

##### find() y find_all()

Estas dos funciones son muy simlares, estas son
sus definiciones:

```python
find_all(tag, attributes, recursive, text, limit, keywords)
find(tag, attributes, recursive, text, keywords)`
```

En realidad, la mayor parte de las veces solo
vas a necesitar utilizar `tag` y `attributes`.

Vamos a analizarlos con mayor detalle.

En el parámetro `tag` podemos pasar un string con
el nombre de un tag, o una lista de strings con
nombres de tags.

```python
.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
```

El parámetro `attributes` toma un diccionario
de atributos, y hace match con las tags que
tengan los mismos atributos. Por ejemplo, esta
función regresa los span con clase `green` o
`red`:

```python
.find_all('span', {'class':{'green', 'red'}})
```

Estos son los dos parámetros que vamos a usar
en la mayoría de los casos. Si utilizo otro
parámetro en la elaboración del proyecto,
lo explicaré en su momento.
