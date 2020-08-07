import requests
from bs4 import BeautifulSoup
import re
import pickle
import os
from booksDAO import BooksDAO
import csv

original_link = 'http://books.toscrape.com/'
link_book = 'http://books.toscrape.com/catalogue'
link_pages='http://books.toscrape.com/catalogue/category/books/'

_id = 0
_all = []
def getDesc(link):
    request = requests.get(link)
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
    img_link = soup.find_all('div',class_='item active')[0].find('img',src=True)['src'].split('..')[2]
    availability = soup.find('table',class_='table').find_all('tr')[5].find('td').text
    qnt = int(re.sub('[^0-9]', '', availability))
    availability = availability.split('(')[0]
    
    #desc = soup.find('article',class_='product_page').find_all('p')[1].text
    
    img_link = original_link + img_link
    
    if len(soup.find("p",class_='star-rating')['class'])>0:
        stars = soup.find("p",class_='star-rating')['class'][1]
        if "one" in stars.lower():
            star_rating = 1
        elif "two" in stars.lower():
            star_rating = 2
        elif "three" in stars.lower():
            star_rating = 3
        elif "four" in stars.lower():
            star_rating = 4
        elif "five" in stars.lower():
            star_rating = 5
        else:
            star_rating = -1 
                    
    return {"title":titulo,
            "price_incl":preco_incl,
            "price_excl":preco_excl,
            "link":link_livro,
            "product_type":product_type,
            "UPC":UPC,
            "tax":tax,
            "review_number":nmbr_review,
            "star_rating":star_rating,
            "img_link":img_link,
            "amount":qnt,
            "availability":availability}

def getBooks(link,categoria,cat,useMongo):
    global _id
    global _all
    request = requests.get(link)
    soup = BeautifulSoup(request.text,'html.parser')
    livros_pag = soup.find_all("section")[0].find_all('div')[1].find('ol').find_all('li')
    next_page = soup.find('li',class_='next')
    allBooks = []
    
    if livros_pag != None:
        if useMongo:
            dao = BooksDAO()  
        for livro in livros_pag:
            link = livro.find('a',href=True)
            descricao = getDesc(link_book+link['href'].split('..')[3])
            descricao['g:id'] = _id
            print(str(_id)+' - '+descricao['link'])
            _id +=1
            descricao['category'] = categoria
            if useMongo:
                dao.update({'g:id':descricao['g:id']},descricao,upsert=True)
            allBooks.append(descricao)
            _all.append(descricao)

        if useMongo:    
            dao.close()
        if next_page != None:
            getBooks(link_pages+categoria+'/'+next_page.find('a',href=True)['href'],categoria,cat,useMongo)

    return (allBooks)





def getCategories(soup,useMongo):
    _id = 0
    div = soup.find_all('div',class_='side_categories')
    uls = div[0].find_all('ul')
    lis = uls[1].find_all('li')
    
    lista_links = []
    categorias = []
    for l in lis:
        link = l.find('a',href=True)
        lista_links.append(original_link + link['href'])
        categorias.append(link.text.strip())

    books = [] 
    for i,link_cat in enumerate(lista_links):
        categoria = categorias[i]
        allbooks = getBooks(link_cat,link_cat.split('/')[6],categoria,useMongo)
        books.append(allbooks)

    with open('books.csv','w') as f:
        title = "id,title;price_incl;price_excl;link;product_type;UPC;tax;review_number;star_rating;img_link;amount;availability,category"
        cw = csv.DictWriter(f,title,delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        cw.writeheader()
        cw.writerows(_all)
    print('finished')


if __name__ == "__main__":
    res = requests.get('http://books.toscrape.com/')
    assert res.status_code == 200,'error'
    soup = BeautifulSoup(res.text,'html.parser')
    useMongo = False
    getCategories(soup,useMongo)


