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

def write_country_file(name,geometry):
    location = os.path.join(path,name+'.geojson')

    shp = shapely.geometry.shape(geometry)
    shp = shp.buffer(1e-12, resolution=0)
    geojson = shapely.geometry.mapping(shp)

    f = open(location,"w")
    f.write(json.dumps(geojson))
    f.close()

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["armageddon"]
countries = db["countries"]
countries_geo = db["countries_geo"]

count = 0

for obj in countries.find():
    mongo_id = obj["_id"]
    del(obj["_id"])
    name = obj["properties"]["ADMIN"]
<<<<<<< HEAD
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
=======

    if not os.path.exists(os.path.join(path,name+'.geojson')):
        write_country_file(name, obj["geometry"])
    
    f = open(os.path.join(path,name+'.geojson'),"r")
    wound_geo = f.read()
    geojson = json.loads(rewind(wound_geo))

    
    loc = {"name":name,"location":{"type":"feature","geometry":geojson}}

    countries_geo.insert(loc)

    
>>>>>>> 35f0246d63fc076b5710203d2392f162cacddb52
