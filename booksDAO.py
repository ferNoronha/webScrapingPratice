from connection import Connection
import json
#mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false

class BooksDAO:
    def __init__(self):
        client = 'mongodb://localhost'
        port = 27017
        database = 'Testes'
        collection = 'Books'
        self.con = Connection(client,port,database,collection)

    def insert(self,documents):    
        return self.con.insert(documents)

    def update(self, key:'_id',value,documents):
        query={key:value}
        values={'$set':documents}
        return self.con.update(query,values)

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

    #def insertError()
