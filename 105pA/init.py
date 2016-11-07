from datetime import datetime as dt
from datetime import timedelta as td

from pymongo import MongoClient
from utils import pwhash

mongo = MongoClient('localhost', 27017)
col = mongo['105pa']['wow']

col.delete_many({})

users = [{'name':   'user1',
          'passwd': pwhash('wasay')},
         {'name':   'user2',
          'passwd': pwhash('wasay123')},
         {'name':   'user3',
          'passwd': pwhash('OwO_OwO_OwO')}]
col.insert_many(users)
