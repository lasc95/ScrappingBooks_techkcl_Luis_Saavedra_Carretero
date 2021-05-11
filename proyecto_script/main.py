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


soup = getAndParseURL(paginas_url[0])#utilizamos nuestra página para leer las demás páginas. 
#a continuacion vamos a revisar si contiene algún botón que nos lleve a la otra página
while len(soup.findAll('a', href = re.compile('page'))) == 2 or len(paginas_url) == 1:
    new_url = "/".join(paginas_url[-1].split('/')[:-1]) + "/" + soup.findAll('a', href = re.compile('page'))[-1].get('href')
    paginas_url.append(new_url)
    soup = getAndParseURL(new_url)

libros_url = []

for page in paginas_url:
    libros_url.extend(obtenerLibroUrls(page)) #extendemos desde un iterable como es la obtencion de las urls de los libros



dict_ = obtenerDatosLibros(libros_url)

df = pd.DataFrame({'Title': dict_['names'], 'Price': dict_['price_with_tax'], 'Stock': dict_['stock'], "Category": dict_['categories'], 
                             "Cover": dict_['img_urls'], "UPC": dict_['upc'], "Product Type": dict_['type_of'], "Price (excl. tax)": dict_['price_without_tax'],
                             "Price (incl. tax)" : dict_['price_with_tax'], "Tax" : dict_['tax'], "Availability" : dict_['avl'], "Number of reviews" : dict_['no_reviews'] 
                            })

#arreglamos la columna categorías del dataframe
l = []
for i in df['Category']:
    l.append(i.split('_')[0])
df['Category'] = l

#exportamos a un csv
df.to_csv('encargo_scrapping_books_Luis_Saavedra_Carretero.csv', index = False)

#creamos requerimientos  con pip freeze > requirements.txt
