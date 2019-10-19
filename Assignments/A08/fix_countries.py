#!/usr/local/bin/python3
"""
This file cleans the ufo collection and removes and lat/lon pairs that are not numbers
allowing us to create a spatial index and do distance queries.
"""
import pymongo  # package for working with MongoDB
import os
from geojson_rewind import rewind
import json

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["armageddon"]
countries = db["countries"]
countries_geo = db["countries_geo"]

for obj in countries.find():
    mongo_id = obj["_id"]
    del(obj["_id"])
    name = obj["properties"]["ADMIN"]
    obj["name"] = name

    path = "/Users/griffin/1-Courses/5303-Adv-Database/Resources/01_Random_Data/countries/"+name+".geojson"

    if not os.path.exists(path):
        f = open(path,"w")
        f.write(json.dumps(obj))
        f.close()
    else:
        f = open(path,"r")
        obj = f.read()
        obj = json.loads(obj)
        name = obj["name"]
        del(obj["name"])
        
        geojson = {}
        geojson["location"] = {}
        
        rgeometry = rewind(obj["geometry"])

        geojson["location"]["type"] = "Feature"
        geojson["properties"] = {"name":name,"size":0}
        geojson["location"]["geometry"] = rgeometry

        countries_geo.insert_one(geojson)