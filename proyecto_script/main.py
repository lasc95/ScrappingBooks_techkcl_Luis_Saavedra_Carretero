from bs4 import BeautifulSoup as bs
import requests as rq
import re 
from functions import *
import pandas as pd

#obteniendo la página principal
main_url = 'http://books.toscrape.com/index.html'

page = rq.get(main_url)

soup = bs(page.text, 'html.parser')

categorias_url = [main_url.replace('index.html','') + x.get('href') for x in soup.find_all('a', href = re.compile('catalogue/category/books'))] #obtenemos las url de las categorías de los libros

paginas_url = [main_url] #esta variable contendrá todas las páginas del sitio para rescatar los libros

soup = obtenerYConvertirURL(paginas_url[0])#utilizamos nuestra página para leer las demás páginas. 

#creamos este while para modificar las páginas, ya que pueden haber más. En este caso revisamos si contiene botones con bs4
while len(soup.findAll('a', href = re.compile('page'))) == 2 or len(paginas_url) == 1:
    new_url = "/".join(paginas_url[-1].split('/')[:-1]) + "/" + soup.findAll('a', href = re.compile('page'))[-1].get('href')#obtenemos la nueva url.
    paginas_url.append(new_url)#agregamos las nuevas páginas (ejemplo página1 pagina2 pagina3) a nuestra coleccion de urls
    soup = obtenerYConvertirURL(new_url)#convertimos la url con bs4

libros_url = obtenerTodosLibros(paginas_url)#obtenemos los libros de todas las páginas del sitio (que son 50)

dict_ = obtenerDatosLibros(libros_url)#obtenemos toda la info de los libros según lo requerido

df = crearDataFrame(dict_)#creamos un dataFrame con pandas con la información deseada

crearCsv(df)#exportamos nuestra data en un csv según lo solicitado

print('Proceso Finalizado')
#creamos requerimientos  con pip freeze > requirements.txt
