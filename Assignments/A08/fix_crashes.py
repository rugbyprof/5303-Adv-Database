#!/usr/local/bin/python3
"""
This file cleans the ufo collection and removes and lat/lon pairs that are not numbers
allowing us to create a spatial index and do distance queries.
"""
import pymongo  # package for working with MongoDB
import json
import os
import requests


def geo_locate(**kwargs):
    Location = kwargs.pop('Location',False)
    AirportCode = kwargs.pop('AirportCode',False)


    if Location:
        city,state = Location.split(',')
        city = city.strip()
        state = state.strip()

    url = "https://nominatim.openstreetmap.org/search?format=json"

    if city:
        url = f"{url}&city={city}"
    if state: 
        url = f"{url}&state={state}"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:    
        return None


path = "./"


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["armageddon"]
airports = db["airports"]
crashes = db["plane_crashes"]

count = 0

for obj in crashes.find():
    mongo_id = obj["_id"]
    
    lat = obj["Latitude"]
    lon = obj["Longitude"]
    if lat and lon:
        lat = lat.strip()
        lon = lon.strip()
        if len(lat):
            lat = float(lat)
        else:
            lat = False
        if len(lon):
            lon = float(lon)
        else:
            lon = False

        
        if (lat or lon):
            count += 1
            print(lat,lon)
    else:
        location = obj["Location"]
        print(location)
        if location:
            response = geo_locate(Location=location)
            print(response)

print(count)
    