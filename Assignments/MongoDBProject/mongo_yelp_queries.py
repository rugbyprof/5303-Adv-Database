import os
import json
import re
import operator 

from pymongo import MongoClient
from bson import Binary, Code
from bson.son import SON

DATABASENAME = '5303DB'

client = MongoClient('localhost', 27017)
db = client[DATABASENAME]

# help on counting stars question
if raw_input("Run find 5 star reviews?: ") == 'y':
    result = db.yelp.review.aggregate([ 
        { "$match": {"stars":5}},
        { "$group": { "_id": "null", "count": { "$sum": 1 } } }
    ])

    for row in result:
        print(row) 

# help on distance query

if raw_input("Run find businesses within 100 miles of Charlotte?: ") == 'y':
    cities = {}
    # finds all "businesses" within 100 miles of "-80.8428955,35.2203102" (Charlotte NC)
    result = db.yelp.business.find( { "loc": { "$geoWithin": { "$centerSphere": [ [-80.8428955,35.2203102] , 100 / 3963.2 ] } } } )
    count = 0
    for row in result:
        city = row['city'].lower().strip()
        if not city in cities:
            cities[city] = 0
        cities[city] += 1
        count += 1
    print(cities)
    print(count)

if raw_input("Run find elite users?: ") == 'y':
    result = db.yelp.user.find({"elite":{"$ne":[]}},{"_id":0,"user_id":1,"name":1,"elite":1})

    for row in result:
        print(row['name'],len(row['elite']),row['elite'][0])



x = int(raw_input("Run find top X cities that majority businesses are in? (enter integer between 1 and 50 or 0 to quit): "))
cities = {}
if x > 0:
    result = db.yelp.business.find()

    for row in result:
        city = row['city']
        if not city in cities:
            cities[city] = 0
        cities[city] += 1 
    
    sorted_dict = sorted(cities.items(), key=operator.itemgetter(1), reverse=True)

    for i in range(x):
        print(sorted_dict[i])
