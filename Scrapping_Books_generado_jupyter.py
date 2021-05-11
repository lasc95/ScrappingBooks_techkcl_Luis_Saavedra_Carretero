#!/usr/bin/env python
# coding: utf-8

# # Scrapping Luis Saavedra Carretero
# Este proyecto tiene como finalidad la extracción de data requerida desde la página http://books.toscrape.com/ En la cual se nos solicitó extraer:
# * 1) el título de los libros
# * 2) Precio
# * 3) Stock 
# * 4) Categoría
# * 5) Carátula del libro (url)
# * 6) Descripción del libro (
#     UPC
#     Product Type
#     Price (excl. tax)
#     Price (incl. tax)
#     Tax
#     Availability
#     Number of reviews
# )
# <br> <br>
# Por lo que lo haremos con las siguientes librerías: BeautifulSoup4, requests y regex. <br> <br> <br>
# Una vez extraída la data, debemos almacenar todos estos datos en un archivo csv; para ello, usaremos la librería pandas para crear un dataFrame y así guardarlo en formato csv

# In[11]:


conda install -c conda-forge pipreqs


# Importamos librerías que vamos a utilizar a lo largo de este proyecto

# In[12]:


import pandas as pd 
from bs4 import BeautifulSoup as bs 
import requests as rq 
import re


# ## 1) Obtener contenido de la página principal
# En esta sección lo que haremos, será crear la variable que contendrá la página principal, donde se encuentran todas las categorías, libros, etc. 

# In[3]:


#recorrer y obtener títulos de libros
main_url = 'http://books.toscrape.com/index.html' #página principal
page = rq.get(main_url) #obtenemos el requests de la página
soup = bs(page.text, 'html.parser') #usamos beautiful soup para leer nuestro html


# ## 1.1) Creando función getAndParseURL() para obtener todas las páginas en formato óptimo para BeautifulSoup
# Como podemos percatarnos, tendremos que navegar por muchas páginas durante este proyecto para obtener todos los libros, así que crearemos una función que nos permitirá obtener cualquier página del sitio y leerlo mediante BeautifulSoup.

# In[8]:


#creamos función para obtener cualquier página
def getAndParseURL(url):
    """
    Función que tiene como objetivo obtener/parsear cualquier 
    página, mediante su url
    """
    result = rq.get(url)
    soup = bs(result.text, 'html.parser')
    return(soup)


# ## 2) Obtener los libros de una determinada url (sección de prueba)
# Una vez ya adentrado en nuestra página, debemos obtener la información de cada libro en la página que sea. En este caso, vemos que el libro se encuentra dentro de un "article" (de html) y con la clase "product_pod".
# Haremos la prueba de obtener solamente el primer producto que encuentre con las características/atributos mencionados anteriormente

# In[21]:


soup.find("article", class_ = "product_pod")


# #### Ahora podemos obtener la url del libro para así acceder y tomar sus atributos. 
# En este caso haremos una prueba con el primer producto. Ahora vamos a utilizar una función para obtener todas las urls de los libros

# In[26]:


soup.find("article", class_ = "product_pod").div.a.get('href')


# Lo que haremos será almacenar en una lista todos los href, para ello utilizaremos lo que se conoce como "List Comprehension"

# In[30]:


main_books_urls = [x.div.a.get('href') for x in soup.findAll("article", class_ = 'product_pod')]
main_books_urls[:10] #consultaremos los primeros 10 urls


# #### Ahora crearemos una función para obtener la información de cualquier libro desde cualquier página (ya que no solo trabajaremos con la página principal)

# In[39]:


def obtenerLibroUrls(url):
    """
    Función para obtener libros desde cualquier página 
    (de bookstoscrape).
    """
    soup = getAndParseURL(url)
    return(["/".join(url.split("/")[:-1]) + "/" + x.div.a.get('href') for x in soup.findAll("article", class_ = "product_pod")])


# ## 3) Obteniendo las urls de cada categoría
# Obtendremos las categorías de los libros (url). En esta ocasión, utilizaremos una herramienta que nos será de mucha utilidad, **Regex**, el cual buscaremos un patrón dentro del href que direcciona a las categorías, que en este caso es: **catalogue/category/books/nombre_categoría**

# In[54]:


#obtenemos categorías
categorias_url = [main_url.replace('index.html','') + x.get('href') for x in soup.find_all('a', href = re.compile('catalogue/category/books'))]
categorias_url[:5]#consultamos


# Nos percatamos que poseemos las urls de todas las categorías, es cosa de copiar una y la pegamos en nuestro navegador para ver que funciona. En el primer elemento, vemos que es el index.html de todos los libros, así que vamos a eliminarlo

# In[55]:


categorias_url = categorias_url[1:]
#quitamos http://books.toscrape.com/catalogue/category/books_1/index.html


# In[56]:


len(categorias_url) #podemos contar las categorías y obtenemos 50 urls


# ## 4) Obteniendo el número de páginas 
# Nos hemos percatado que no solo existe una página, sino pueden existir varias (además pueden agregarse durante el tiempo), así que vamos obtener el número de las páginas con la siguiente serie de pasos

# In[5]:


paginas_url = [main_url] #creamos una variable donde tendremos nuestras url de las paginas (todas***)


# In[6]:


paginas_url #consultamos su contenido


# In[75]:


soup = getAndParseURL(paginas_url[0])#utilizamos nuestra página para leer las demás páginas. 
#a continuacion vamos a revisar si contiene algún botón que nos lleve a la otra página
while len(soup.findAll('a', href = re.compile('page'))) == 2 or len(paginas_url) == 1:
    new_url = "/".join(paginas_url[-1].split('/')[:-1]) + "/" + soup.findAll('a', href = re.compile('page'))[-1].get('href')
    paginas_url.append(new_url)
    soup = getAndParseURL(new_url)


# In[78]:


len(paginas_url) #vemos cuantas páginas en total hemos coleccionado


# In[81]:


paginas_url[-1]#obtenemos la última y la consultamos


# ## 5) Obtener la url de todos los libros en cualquier página.
# Aquí utilizaremos la funcion de obtenerlibrourls, la cual obtiene los libros según una url entregada. En este caso tenemos 50 urls, y obtendremos todos los libros de esas urls

# In[83]:


libros_url = []

for page in paginas_url:
    libros_url.extend(obtenerLibroUrls(page)) #extendemos desde un iterable como es la obtencion de las urls de los libros


# In[86]:


libros_url[:10] #consultamos los primeros 10 libros y los podemos copiar en nuestro navegador para comprobar


# In[87]:


len(libros_url)#tenemos un total de 1000 libros


# ## 6) Obteniendo los datos solicitados de los libros
# Ya estando con todas las urls de los libros, vamos a proceder a obtener la información de ellos. como todos las páginas poseen la misma estructura, será más amable la obtención de los datos

# In[185]:


names = []
prices = []
stock = []
img_urls = []
categories = [] 
ratings = []
upc = []
type_of = []
price_without_tax = []
price_with_tax = []
tax = []
no_reviews = []
avl = []
#vamos a obtener toda la data de los libros
for url in libros_url:
    soup = getAndParseURL(url)
    #el nombre del producto
    names.append(soup.find('div', class_ = re.compile('product_main')).h1.text)
    #el precio del producto
    #prices.append(soup.find('p', class_ = 'prices_color').text[2:])
    #stock del producto
    stock.append(re.sub('[^0-9]', '', soup.find('p', class_ = 'instock availability').text))
    #img_urls
    img_urls.append(url.replace('index.html', '') + soup.find('img').get('src'))
    #categoría
    categories.append(soup.find('a', href = re.compile('../category/books/')).get('href').split('/')[3])
    #ratings 
    ratings.append(soup.find('p', class_ = re.compile('star-rating')).get('class')[1])
    #upc
    upc.append(soup.find('table').find('tr').find('td').text)
    #tipo del producto
    type_of.append(soup.find("th", text="Product Type").find_next_sibling("td").text)
    #precio sin impuesto
    price_without_tax.append(soup.find("th", text="Price (excl. tax)").find_next_sibling("td").text[1:])
    #precio con impuesto
    price_with_tax.append(soup.find("th", text="Price (incl. tax)").find_next_sibling("td").text[1:])
    #impuesto
    tax.append(soup.find("th", text="Tax").find_next_sibling("td").text[1:])
    #reviews
    no_reviews.append(soup.find("th", text="Number of reviews").find_next_sibling("td").text)
    #disponibles
    avl.append(soup.find('p', {'class': 'availability'}).getText().replace('\n', '').strip()[10:12] + ' available')#un poco de manejo de strings


# Vamos a verificar que todos poseen sus nombres y demás atributos

# In[190]:


len(libros_url), len(names), len(stock), len(img_urls), len(categories), len(ratings), len(upc), len(type_of), len(price_with_tax), len(price_without_tax), len(tax), len(no_reviews)


# ## 7) Almacenando valores en un dataframe y exportando a CSV
# Una vez obtenidas las listas con los valores que solicitaron en github, podemos crear nuestro dataframe con el formato adecuado que nos solicitaron. Como sabemos, los df se construyen a partir de diccionarios, así que usaremos las llaves (keys) para el nombre de cada columna y las series/listas para rellenar las filas. 

# In[259]:


df = pd.DataFrame({'Title': names, 'Price': price_with_tax, 'Stock': stock, "Category": categories, 
                             "Cover": img_urls, "UPC": upc, "Product Type": type_of, "Price (excl. tax)": price_without_tax,
                             "Price (incl. tax)" : price_with_tax, "Tax" : tax, "Availability" : avl, "Number of reviews" : no_reviews 
                            })
df.head()


# ## 7.1) Un poco de manejo de datos en dataframes 
# Podemos percatarnos que en categorías hay un problema con el nombre de esta (ejemplo mystery_32), vamos a arreglarlo

# In[269]:


l = []
for i in df['Category']:
    l.append(i.split('_')[0])
df['Category'] = l


# In[270]:


df.head()


# ## 8) Exportando a CSV 
# finalmente con nuestro dataFrame creado con el formato requerido, vamos a exportarlo como csv para futuros análisis

# In[272]:


df.to_csv('encargo_scrapping_books_Luis_Saavedra_Carretero.csv', index = False)


# ## 9) creando txt con requerimientos para este proyecto
# Al estar utilizando Anaconda, utilizo este comando para crear automáticamente los requerimientos

# In[ ]:


conda list -e > requirements.txt


# ## 10) Conclusiones
# <br> 
# Ya finalizada esta entrega podemos afirmar que la tarea de web Scrapping es crucial para obtener información relevante. Claramente siempre teniendo ética y respetando las políticas de seguridad (siempre consultando al robot.txt) y además utilizar siempre para fines de mejorar la calidad de los servicios y no para destruir sistemas, etc. 
