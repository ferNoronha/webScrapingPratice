import requests
from bs4 import BeautifulSoup
import re
import pickle
import os
from booksDAO import BooksDAO

original_link = 'http://books.toscrape.com/'
link_book = 'http://books.toscrape.com/catalogue'
link_pages='http://books.toscrape.com/catalogue/category/books/'

_id = 0

def getDesc(link):
    request = requests.get(link)
    assert request.status_code==200,f'not found'
    soup = BeautifulSoup(request.text,'html.parser')
    livro = soup.find_all('div',class_='product_main')[0]
    titulo = livro.find('h1').text
    preco_incl = soup.find('table',class_='table').find_all('tr')[3].find('td').text
    preco_incl = re.search('[0-9.]+', preco_incl).group()
    preco_excl = soup.find('table',class_='table').find_all('tr')[2].find('td').text
    preco_excl = re.search('[0-9.]+', preco_excl).group()
    link_livro = link
    product_type = soup.find('table',class_='table').find_all('tr')[1].find('td').text
    UPC = soup.find('table',class_='table').find_all('tr')[0].find('td').text
    tax = soup.find('table',class_='table').find_all('tr')[4].find('td').text
    tax = re.search('[0-9.]+', tax).group()
    nmbr_review = soup.find('table',class_='table').find_all('tr')[6].find('td').text
    availibility = soup.find('table',class_='table').find_all('tr')[5].find('td').text
    #desc = soup.find('article',class_='product_page').find_all('p')[1].text
    img_link = soup.find_all('div',class_='item active')[0].find('img',src=True)['src']
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
            #"descricao":desc,
            "img_link":img_link,
            "quantidade":qnt,
            "disponibilidade":availibility}

def getBooks(link,categoria,cat):
    global _id
    request = requests.get(link)
    assert request.status_code==200,f'not found'
    soup = BeautifulSoup(request.text,'html.parser')
    livros_pag = soup.find_all("section")[0].find_all('div')[1].find('ol').find_all('li')
    next_page = soup.find('li',class_='next')
    allBooks = []
    
    if livros_pag != None:
        dao = BooksDAO()    
        for livro in livros_pag:
            link = livro.find('a',href=True)
            descricao = getDesc(link_book+link['href'].split('..')[3])
            descricao['g:id'] = _id
            print(str(_id)+' - '+descricao['link'])
            _id +=1
            descricao['category'] = categoria
            dao.update({'g:id':descricao['g:id']},descricao,upsert=True)
            allBooks.append(descricao)
        dao.close()
        if next_page != None:
            getBooks(link_pages+categoria+'/'+next_page.find('a',href=True)['href'],categoria,cat)

    return (allBooks)





def getCategories(soup):
    _id = 0
    div = soup.find_all('div',class_='side_categories')
    uls = div[0].find_all('ul')
    lis = uls[1].find_all('li')
    
    lista_links = []
    categorias = []
    for l in lis:
        link = l.find('a',href=True)
        #conteudo = l.find('a')
        lista_links.append(original_link + link['href'])
        categorias.append(link.text.strip())

    books = [] 
    for i,link_cat in enumerate(lista_links):
        categoria = categorias[i]
        print(categoria)
        allbooks = getBooks(link_cat,link_cat.split('/')[6],categoria)
        books.append(allbooks)
    

    
    

    #for i in books:
    #    for j in i:
            #dao.update({'g:id':j['g:id']},j,upsert=True)
    print('finalizou')


if __name__ == "__main__":
    res = requests.get('http://books.toscrape.com/')
    dao = BooksDAO()
    assert res.status_code == 200,dao.insertError("Response"+res.status_code)
    dao.close()
    soup = BeautifulSoup(res.text,'html.parser')
    getCategories(soup)


