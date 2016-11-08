## Mongo DB Project

This will be a three part project:

1. Load the data into mongoDB using pymongo  (Due: 2 Nov)
2. Run a set of query's getting a feel for performance. (Due: 7 Nov)
    - May be informational: [Coming in Mongo 3.2]( https://www.mongodb.com/blog/post/joins-and-other-aggregation-enhancements-coming-in-mongodb-3-2-part-1-of-3-introduction)
3. Create an API using flask to use as our DB intermediary. (Due: TBD)

### Part 1:
Part one of the project will be to load the dataset downloaded from here: https://www.yelp.com/dataset_challenge/dataset. 

Here is a python script using pymongo to help load your data. This will NOT work if you simply cut and past. Read the comments.

```python
"""
Place this script inside your yelp data directory and call it load_yelp.py for example.
The script expects your files to be named:
    business.json
    checkin.json
    review.json
    tip.json
    user.json

First TEST the script by simply running it. If it's not in the proper location or 
your files are named incorrectly it will error. When your ready to run it live change
TEST = False. 

Do not forget to change DATABASENAME!!
"""
import os
import json

from pymongo import MongoClient
from bson import Binary, Code

DATABASENAME = 'nameyourdatabasehere'
TEST = True

client = MongoClient('localhost', 27017)
if not TEST:
    db = client[DATABASENAME]

# Inside your yelp data directory, rename your files accordingly:
files = ['business.json','checkin.json','review.json','tip.json','user.json']

# This function to add a proper 2D "loc [x,y]" object to the document
# Make sure you create a 2D index after this file runs !!!
# e.g. db.yelp.business.createIndex({"loc":"2d"})
def add_2D_location(json):
    if 'longitude' in json and 'latitude' in json:
        loc = [json['longitude'],json['latitude']]
        json['loc'] = loc
    return json

"""
Following loops through the file list creating collections of name:
    yelp.business
    yelp.checkin
    yelp.review
    yelp.tip
    yelp.user
"""
for file in files:
    name,ext  = file.split('.')
    collection_name = 'yelp.'+name
    print(collection_name)
    
    # Creates collection in mongo here: 
    if not TEST:
        collection = db[collection_name]
    
    # Deletes documents from collection every time it's run
    if not TEST:
        result = collection.delete_many({})
    
    # Open actual data file and read a line at a time
    f = open(file)
    for line in f:
        # read a line, convert to json, add 2D location
        line = add_2D_location(json.loads(line))
        
        # insert into collection
        if not TEST:
            collection.insert(line)
       
```

Each file is composed of a single object type, one json-object per-line. Use the python script provided in this directory to help you get each of these data sets loaded into your mongo instance.

Before you put all of your data in one collection, read the following: https://docs.mongodb.com/manual/data-modeling/ and use this to decide how your data should be modeled. Should it be left as is? Should some of the documents be embedded within some other documents? Can there be a performance increase in either solution?

This article brings up an interesting way to name your collections using dot '.' notation. For your project it could be a handy organizational tool. It also discusses `capped` collections, another interesting topic (that we probably don't need for this project).
http://www.w3resource.com/mongodb/databases-documents-collections.php


### business
```python
{
    "type": "business",
    "business_id": (encrypted business id),
    "name": (business name),
    "neighborhoods": [(hood names)],
    "full_address": (localized address),
    "city": (city),
    "state": (state),
    "latitude": latitude,
    "longitude": longitude,
    "stars": (star rating, rounded to half-stars),
    "review_count": review count,
    "categories": [(localized category names)]
    "open": True / False (corresponds to closed, not business hours),
    "hours": {
        (day_of_week): {
            "open": (HH:MM),
            "close": (HH:MM)
        },
        ...
    },
    "attributes": {
        (attribute_name): (attribute_value),
        ...
    },
}
```
### review
```python
{
    "type": "review",
    "business_id": (encrypted business id),
    "user_id": (encrypted user id),
    "stars": (star rating, rounded to half-stars),
    "text": (review text),
    "date": (date, formatted like "2012-03-14"),
    "votes": {(vote type): (count)},
}
```
### user
```python
{
    "type": "user",
    "user_id": (encrypted user id),
    "name": (first name),
    "review_count": (review count),
    "average_stars": (floating point average, like 4.31),
    "votes": {(vote type): (count)},
    "friends": [(friend user_ids)],
    "elite": [(years_elite)],
    "yelping_since": (date, formatted like "2012-03"),
    "compliments": {
        (compliment_type): (num_compliments_of_this_type),
        ...
    },
    "fans": (num_fans),
}
```
### check-in
```python
{
    "type": "checkin",
    "business_id": (encrypted business id),
    "checkin_info": {
        "0-0": (number of checkins from 00:00 to 01:00 on all Sundays),
        "1-0": (number of checkins from 01:00 to 02:00 on all Sundays),
        ...
        "14-4": (number of checkins from 14:00 to 15:00 on all Thursdays),
        ...
        "23-6": (number of checkins from 23:00 to 00:00 on all Saturdays)
    }, # if there was no checkin for a hour-day block it will not be in the dict
}
```
### tip
```python
{
    "type": "tip",
    "text": (tip text),
    "business_id": (encrypted business id),
    "user_id": (encrypted user id),
    "date": (date, formatted like "2012-03-14"),
    "likes": (count),
}
```
### photos (from the photos auxiliary file)
This file is formatted as a JSON list of objects.
```python
[
    {
        "photo_id": (encrypted photo id),
        "business_id" : (encrypted business id),
        "caption" : (the photo caption, if any),
        "label" : (the category the photo belongs to, if any)
    },
    {...}
]
```

## Part 2

Some sources:
- https://docs.mongodb.com/v3.2/reference/operator/aggregation/match/
- https://docs.mongodb.com/v3.2/reference/operator/aggregation/group/

### Typical Queries

1. Find all restaurants with zip code `X or Y` 
    -` Using 89117 and 89122 answer = 1083`
1. Find all restaurants in city `X`
    - `Las Vegas results in 20382`
1. Find the restaurants within 5 miles of `lat , lon`
    - `This Lon,Lat [ -80.839186,35.226504 ] gives ~ 290`
1. Find all the reviews for restaurant `X`
    - `business_id hB3kH0NgM5LkEWMnMMDnHw results in 20 `
1. Find all the reviews for restaurant `X` that are 5 stars.
    - `business_id P1fJb2WQ1mXoiudj8UE44w results in 25`
1. Find all the users that have been 'yelping' for over 5 years.

1. Find the `business` that has the `tip` with the most ***likes***.

1. Find the average `review_count` for users.

1. Find all the users that are considered `elite`.

1. Find the longest `elite` user.

1. Of `elite` users, whats the average number of years someone is `elite`.


### Difficult?

1. Find the probable city a user lives in based on a set of reviews 

1. Find the busiest checkin times for all businesses in the `75205 & 75225` zip codes.

1. Find the business with the most checkins from Friday at 5pm until Sunday morning at 2am. 

1. Given a restaurant, count the number of reviews by star. Should have 5 different counts, one for each star.

1. Find all restaurants with over a `3.5 star rating` average rating.

### Some Help

```python
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

```
