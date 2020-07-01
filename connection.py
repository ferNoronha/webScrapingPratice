from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
#mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false

class Connection:
    def __init__(self, client, port, database, collection):
        self.conn = MongoClient(client, port)
        self.database = self.conn[database]
        self.collection = self.database[collection]
        try:
            self.conn.admin.command('ismaster')
        except ConnectionFailure:
            raise ConnectionFailure("error")

    def get(self, query):
        print(query)
        return self.collection.find(query)

    def insert(self, documents):
        x = self.collection.insert_many(documents)
        return x.inserted_ids
    
    def error(self,documents):
        x = self.database['LogBooks'].insert_one(documents)
        return True
    
    def update(self, query, values, upsert=False):
        x = self.collection.update_many(query,values,upsert)
        return True
    
    def delete(self, query):
        x = self.collection.delete_many(query)
        return x.deleted_count
    
    def __del__(self):
        self.conn.close()
