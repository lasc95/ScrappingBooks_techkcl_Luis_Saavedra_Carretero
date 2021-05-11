import unittest
import bs4 
from functions import *
#algunas pruebas unitarias

class Test(unittest.TestCase):
    def setUp(self):
        print('Realizando pruebas')
    
    def test_obtenerYConvertirURL_true(self):
        """
        Prueba diseñada para función obtenerYConvertirURL
        """
        url = 'http://books.toscrape.com/index.html'
        actual = obtenerYConvertirURL(url)
        self.assertTrue(type(actual) is bs4.BeautifulSoup)
    
    def test_obtenerYConvertirURL_false(self):
        """
        Prueba diseñada para función obtenerYConvertirURL en caso de que sea fallido
        """
        url = 'http://books.asd.com'
        actual = obtenerYConvertirURL(url)
        self.assertRaises(Exception, actual)
    
    def test_obtener_libros_true(self):
        """
        Prueba diseñada para funcion obtenerLibroUrls(url). en este caso, comparando con el primer enlace obtenido
        """
        url = 'http://books.toscrape.com/index.html'
        actual = obtenerLibroUrls(url)
        print('actual es: ', actual[0])
        self.assertEqual(actual[0], 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html')
    
    def test_obtener_libros_false(self):
        """
        Prueba diseñada para funcion obtenerLibroUrls(url). en este caso con un error en pasar nuestra url
        """
        url = 'http://books.toscrape.com/ind.html'
        actual = obtenerLibroUrls(url)
        self.assertRaises(Exception, actual)
        


if __name__ == '__main__':
    unittest.main()