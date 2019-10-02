#!/usr/local/bin/python3
import pymongo  # package for working with MongoDB

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["ufos"]
sightings = db["sightings"]


count = 0

for obj in sightings.find():
    mongo_id = obj["_id"]
    lat = obj["latitude"]
    lon = obj["longitude"]
    #print(lat,lon)
    lati = isinstance(lat, int)
    loni = isinstance(lon, int) 
    flat = isinstance(lat, float)
    flon = isinstance(lon, float)
    if (lati or flat) and (flat or flon):
        sightings.update_one({'_id':mongo_id}, {"$set": {"loc" : { "type": "Point", "coordinates": [ lon, lat ] }}}, upsert=False)
    else:
        print(f"Removing: {lat},{lon}")
        sightings.remove({'_id':mongo_id})
        count += 1
        
        

print(f"Count removed: {count}")