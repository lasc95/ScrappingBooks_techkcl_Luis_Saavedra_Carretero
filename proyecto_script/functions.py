from bs4 import BeautifulSoup as bs
import requests as rq

def getAndParseURL(url):
    """
    Función que tiene como objetivo obtener/parsear cualquier 
    página, mediante su url
    """
    try:
        result = rq.get(url)
        soup = bs(result.text, 'html.parser')
        return(soup)
    except Exception as err:
        return err

    


def obtenerLibroUrls(url):
    """
    Función para obtener libros desde cualquier página 
    (de bookstoscrape).
    """
    try:
        soup = getAndParseURL(url)
        return(["/".join(url.split("/")[:-1]) + "/" + x.div.a.get('href') for x in soup.findAll("article", class_ = "product_pod")])
    except Exception as err:
        return err




def obtenerDatosLibros(libros_url, names, stock, img_urls, categories, ratings, upc, type_of, price_without_tax, price_with_tax,tax, no_reviews, avl):
    #vamos a obtener toda la data de los libros
    diccionario_todo = {}
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
        avl.append(soup.find('p', {'class': 'availability'}).getText().replace('\n', '').strip()[10:12] + ' available')
    
    diccionario_todo['name'] = names
    diccionario_todo['stock'] = stock 
    diccionario_todo['img_urls'] = img_urls
    diccionario_todo['categories'] = categories
    diccionario_todo['ratings'] = ratings
    diccionario_todo['upc'] = upc 
    diccionario_todo['type_of'] = type_of
    diccionario_todo['price_whitout_tax'] = price_without_tax
    diccionario_todo['price_with_tax'] = price_with_tax
    diccionario_todo['tax'] = tax 
    diccionario_todo['no_reviews'] = no_reviews
    diccionario_todo['alv'] = avl
    return diccionario_todo