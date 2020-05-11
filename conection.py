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

    def select(self, query):
        print(query)
        return self.collection.find(query)

    def insert(self, documents):
        x = self.collection.insert_many(documents)
        return x.inserted_ids
    
    def update(self, query, values):
        x = self.collection.find_one_and_update(query, values)
        return x['_id']
    
    def delete(self, query):
        x = self.collection.delete_many(query)
        return x.deleted_count
