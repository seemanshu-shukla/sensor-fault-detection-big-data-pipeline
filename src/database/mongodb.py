import pymongo
import os


import certifi
ca = certifi.where()

class MongodbOperation:

    def __init__(self) -> None:

        self.client = pymongo.MongoClient(os.getenv('MONGO_DB_URL'),tlsCAFile=ca)
        self.db_name="ineuron"   #Can change this db name. With this name db will be create in the mongodb cluster

    def insert_many(self,collection_name,records:list):  #Batch insertion. Here we need to set the number of records to be inserted each batch run. Choosing this number is based on experimentation but having a right number can reduce the performance drastically.
        self.client[self.db_name][collection_name].insert_many(records)

    def insert(self,collection_name,record):  #Real time or single insertion
        self.client[self.db_name][collection_name].insert_one(record)
        
