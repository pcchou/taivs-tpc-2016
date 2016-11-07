from pymongo import MongoClient

mongo = MongoClient('localhost', 27017)
col = mongo['105pc']['data']

col.delete_many({})

data = [{'count': 0}]
col.insert_many(data)
