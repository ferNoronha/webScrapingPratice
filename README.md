# Web Scraping

This application will do data collection (web scraping) in [books to scrap](http://books.toscrape.com/), save in a csv file and insert on mongoDB if you want.


## Installation using conda

With Anaconda installed create your environment and activate it:
```bash
conda create -n yourenvname python=3.6

conda activate yourenvname

```
In root folder, use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.txt.

```bash
pip install -r requirements.txt
```

## Usage
First of all, if you would like to insert on mongodb, you have to set your configFile.ini with your mongodb configs, like Uri, Port, Database and Collection.

If you wouldn't like to insert on mongo, you have to change your useMongo variable to False

```python
if __name__ == "__main__":
    res = requests.get('http://books.toscrape.com/')
    assert res.status_code == 200,'error'
    soup = BeautifulSoup(res.text,'html.parser')
    useMongo = True #here
    getCategories(soup,useMongo)
```
To run this code just run in your prompt:
```bash
python scraping.py
```

## License
[MIT](https://choosealicense.com/licenses/mit/)