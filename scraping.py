import requests
from bs4 import BeautifulSoup
import re
import pickle
import os


original_link = 'http://books.toscrape.com/'
link_book = 'http://books.toscrape.com/catalogue'

def getDesc(link):
    request = requests.get(link)
    assert request.status_code==200,f'not found'
    soup = BeautifulSoup(request.text,'html.parser')
    livro = soup.find_all('div',class_='product_main')[0]
    titulo = livro.find('h1').text
    preco_incl = livro.find('table',class_='table').find_all('tr')[3].find('td').text
    preco_excl = livro.find('table',class_='table').find_all('tr')[2].find('td').text
    link_livro = link
    product_type = livro.find('table',class_='table').find_all('tr')[1].find('td').text
    UPC = livro.find('table',class_='table').find_all('tr')[0].find('td').text
    tax = livro.find('table',class_='table').find_all('tr')[4].find('td').text
    nmbr_review = livro.find('table',class_='table').find_all('tr')[6].find('td').text
    availibility = livro.find('table',class_='table').find_all('tr')[5].find('td').text
    desc = livro.find('article',class_='product_page').find('p').text
    img_link = livro.find_all('div',class_='item active')[0].find('img',src=True)['src']
    qnt = int(re.sub('[^0-9]', '', availibility))
    availibility = availibility.split('(')[0]

    return {"titulo":titulo,
            "preco_incl":preco_incl,
            "preco_excl":preco_excl,
            "link":link_livro,
            "product_type":product_type,
            "UPC":UPC,
            "tax":tax,
            "numero_review":nmbr_review,
            "descricao":desc,
            "img_link":img_link,
            "quantidade":qnt,
            "disponibilidade":availibility}


    
    






def getBooks(link):
    #print(link)
    requ = requests.get(link)
    assert requ.status_code==200,f'not found'
    soup = BeautifulSoup(requ.text,'html.parser')
    livros_pag = soup.find_all("section")[0].find_all('div')[1].find_all('li')
    
    for livro in livros_pag:
        link = livro.find('a',href=True)
        book = getDesc(link_book+link['href'].split('..')[3])





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
        categories.append(conteudo.text.strip())
    #print(categories)

    '''{"titulo":titulo,
    "preco_excl":preco_semtaxa,
    "preco_incl":preco_comtaxa,
    "descricao":descricao,
    "link":link,
    "img":img,
    "product_type":pt,
    "tax":impostos,
    "availibility":{"inStock":true,"qnt":2},
    "reviews":numberreviews,
    "quantidade_estrela":2,
    "category":categoria,
    "UPC":UPC
    }'''
    dic = {}
    list_prod = []
    for i,link_cat in enumerate(lista_links):
        categoria = categories[i]
        getBooks(link_cat)
        


if __name__ == "__main__":  
    res = requests.get('http://books.toscrape.com/')
    assert res.status_code == 200,f"Response{res.status_code}"
    soup = BeautifulSoup(res.text,'html.parser')
    getCategories(soup)


