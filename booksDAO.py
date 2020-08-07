from connection import Connection
import json
from os import getenv
import configparser

Config = configparser.RawConfigParser()
Config.read("configFile.ini")

class BooksDAO:
    def __init__(self):
        self.con = Connection(Config.get('mongoSection','Uri'),int(Config.get('mongoSection','Port')),Config.get('mongoSection','Database'),Config.get('mongoSection','Collection'))

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
