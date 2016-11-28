import glob
import ntpath
import os
import json

from pymongo import MongoClient
from bson import Binary, Code

client = MongoClient('localhost', 27017)
db = client['5303DB']

business = db.yelp.business
checking = db.yelp.checkin
review = db.yelp.review
tip = db.yelp.tip
user = db.yelp.user


def yelpingSince(n):
    users = user.find({})

    data = []

    for u in users:
        date = u["yelping_since"]
        year = date[2]+date[3]
        if int(year) - n >= 0:        
            data.append(u)
    return data 
        

def yelpAvgStars(n):

    reviews = review.find({})
    
    data = {}
    
    for rev in reviews:
        if not rev['business_id'] in data:
            data[rev['business_id']] = []
        
        data[rev['business_id']].append(float(rev['stars']))
    
    for key,val in data.items():
        data[key] = sum(val) / len(val)
        
    print(data)
    



if __name__=='__main__':
    print(yelpAvgStars(3))
