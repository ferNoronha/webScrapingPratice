import requests
from bs4 import BeautifulSoup
import re
import pickle
import os


original_link = 'http://books.toscrape.com/'

def getCategories(soup):
    div = soup.find_all('div',class_='side_categories')
    uls = div[0].find_all('ul')
    lis = uls[1].find_all('li')
    
    lista_links = []
    categories = []
    for l in lis:
        link = l.find('a',href=True)
        conteudo = l.find('a')
        lista_links.append(original_link + link['href'])
        categories.append(conteudo)
    print(categories)

if __name__ == "__main__":  
    res = requests.get('http://books.toscrape.com/')
    assert res.status_code == 200,f"Response{res.status_code}"
    soup = BeautifulSoup(res.text,'html.parser')
    getCategories(soup)


