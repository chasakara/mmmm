import pymongo
import os
from os import path
if path.exists("env.py"):
    import env 

MONGODB_URI = os.getenv("MONGO_URI")
DBS_NAME = os.getenv("DBS_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print("Mongo is connected!")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e
        
conn = mongo_connect(MONGODB_URI)

coll = conn[DBS_NAME][COLLECTION_NAME]

documents = list(coll.find())
print(documents)
for doc in documents:
    print(doc)