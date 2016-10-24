import glob
import ntpath
import os
import json

from pymongo import MongoClient
from bson import Binary, Code

client = MongoClient('localhost', 27017)
db = client['yourdatabasename']
collection = db.yelp



files =  glob.glob("./yelp_challenge_dataset/*.json")

for file in files:
f = open(file)
    for line in f:
        line = json.loads(line)
        collection.insert(line)
