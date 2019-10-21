#!/usr/local/bin/python3
"""
This file cleans the ufo collection and removes and lat/lon pairs that are not numbers
allowing us to create a spatial index and do distance queries.
"""
import pymongo  # package for working with MongoDB
import shapely.geometry
from geojson_rewind import rewind
import json
import os

path = "/Users/griffin/Code/Courses/1-Current_Courses/5303-Adv-Database/Resources/01_Random_Data/countries/"



client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["armageddon"]
meteorites = db["meteorites"]

count = 0

for obj in meteorites.find():
    mongo_id = obj["_id"]
    latlon = obj["GeoLocation"]
    latlon = latlon.strip("(")
    latlon = latlon.strip(")")
    if "," in latlon:
        lat,lon = latlon.split(",")
    
        print(float(lat),float(lon))
        #print(lat,lon)
        meteorites.update_one({'_id':mongo_id}, {"$set": {"loc" : { "type": "Point", "coordinates": [ lon, lat ] }}}, upsert=False)

    
