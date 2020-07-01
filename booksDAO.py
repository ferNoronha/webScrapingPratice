from connection import Connection
import json
from os import getenv 
#mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false

CLIENT = 'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false'
DATABASE = 'Testes'
PORT = 27017
COLLECTION = 'Books'

class BooksDAO:
    def __init__(self):
        print(CLIENT)
        self.con = Connection(CLIENT,PORT,DATABASE,COLLECTION)

    def insert(self,documents):    
        return self.con.insert(documents)

    def update(self, query,value,upsert=False):
        values={'$set':value}
        return self.con.update(query,values,upsert)

    def delete(self,key:'_id',value):
        return True

    def get(self, key, value):
        query={}
        for i, k in enumerate(key):
            query[k] = value[i]
        print(query)
        return self.con.get(query)

    def getAll(self):
        return True

    def insertError(self,value):
        return self.con.error(value)
    
    def close(self):
        self.con.__del__()
        del self
    
    def __del__(self):
        del self
