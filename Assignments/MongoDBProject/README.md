## Mongo DB Project

This will be a three part project:

1. Load the data into mongoDB using pymongo 
2. Run a set of query's getting a feel for performance.
    - May be informational: [Coming in Mongo 3.2]( https://www.mongodb.com/blog/post/joins-and-other-aggregation-enhancements-coming-in-mongodb-3-2-part-1-of-3-introduction)
3. Create an API using flask to use as our DB intermediary. 

### Part 1:
Part one of the project will be to load the dataset downloaded from here: https://www.yelp.com/dataset_challenge/dataset. 

Each file is composed of a single object type, one json-object per-line. Use the python script provided in this directory to help you get each of these data sets loaded into your mongo instance.

Before you put all of your data in one collection, read the following: https://docs.mongodb.com/manual/data-modeling/ and use this to decide how your data should be modeled. Should it be left as is? Should some of the documents be embedded within some other documents? Can there be a performance increase in either solution?

This article brings up an intersting way to name your collections using dot '.' notation. For your project it could be a handy organizational tool. It also discusses `capped` collections, another interesting topic (that we probably don't need for this project).
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
