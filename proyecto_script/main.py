from bs4 import BeautifulSoup as bs
import requests as rq
import re 
from functions import *
import pandas as pd

#obteniendo las páginas
main_url = 'http://books.toscrape.com/index.html'

page = rq.get(main_url)

soup = bs(page.text, 'html.parser')

main_books_urls = [x.div.a.get('href') for x in soup.findAll("article", class_ = 'product_pod')] #obteniendo las urls de los libros 

categorias_url = [main_url.replace('index.html','') + x.get('href') for x in soup.find_all('a', href = re.compile('catalogue/category/books'))] #obtenemos las url de las categorías de los libros

paginas_url = [main_url]

soup = obtenerYConvertirURL(paginas_url[0])#utilizamos nuestra página para leer las demás páginas. 
#a continuacion vamos a revisar si contiene algún botón que nos lleve a la otra página

while len(soup.findAll('a', href = re.compile('page'))) == 2 or len(paginas_url) == 1:
    new_url = "/".join(paginas_url[-1].split('/')[:-1]) + "/" + soup.findAll('a', href = re.compile('page'))[-1].get('href')
    paginas_url.append(new_url)
    soup = obtenerYConvertirURL(new_url)

libros_url = obtenerTodosLibros(paginas_url)

dict_ = obtenerDatosLibros(libros_url)

df = crearDataFrame(dict_)

crearCsv(df)

print('Proceso Finalizado')
#creamos requerimientos  con pip freeze > requirements.txt
