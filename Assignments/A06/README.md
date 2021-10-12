## Assignment 6 - Restaurants DB (with Mongo)
#### Due: 10-10-2021 (Monday @ 5:00 p.m.)

### References For You  

1. [Installing MongoDB](https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-20-04)
   
2. ~~[Secure MongoDB](https://www.digitalocean.com/community/tutorials/how-to-secure-mongodb-on-ubuntu-20-04)~~

```mongo
db.createUser({user: "adminguru",pwd: passwordPrompt(),roles: [ { role: "userAdminAnyDatabase", db: "admin" }, "readWriteAnyDatabase" ]})
```

3. [Remote Access to Mongo](https://www.digitalocean.com/community/tutorials/how-to-configure-remote-access-for-mongodb-on-ubuntu-20-04)

```
mongodb://your.ip.address:27017
```

4. [Py Mongo](https://www.digitalocean.com/community/tutorials/how-to-perform-crud-operations-in-mongodb-using-pymongo-on-ubuntu-20-04)


### Loading Database

The [restaurants.json](restaurant.json) from this folder can be loaded using a command similar to the following:

```
mongoimport --db=YourDbName --collection=YourCollectionName --type=json --file=fileName.json
```

### Example PyMongo Queries

```python
 # used to turn string id to Mongo _id
import pymongo
import pprint
import random

# connect to mongodb
cnx = pymongo.MongoClient("mongodb://localhost:27017/")
# use businessData
db = cnx["businessData"]
# choose collection
coll = db['restaurants']


def listAllCollections(dbName=None):
    """
    Description:
        lists all collections in a db (just as an example)
    Params:
        dbName (string) : name of database to view collections (optional)
    Returns:
        list
    """
    if dbName:
        collections = cnx[dbName].list_collection_names()
    else:
        collections = db.list_collection_names()

    return collections

def findAllRestaurants():
    """
    Description: 
        Find all restaurants in collection
    Params:
        None
    Returns: 
        dict : {"result":list,"size":int}
    """
    
    res = list(coll.find())
    
    return {"result":res,"count":len(res)}

def findCuisineCounts():
    """
    Description: 
        Count all restaurants that serve a specific cuisine
    Params:
        None
    Returns: 
        list of cuisine counts
    """

    results = db['restaurants'].aggregate([

        # Group the documents and "count" via $sum on the values
        { "$group": 
            {
                "_id": '$cuisine',
                "count": { "$sum": 1 }
            }
        }
    ])

    return list(results)

def findRestaurantsByCuisine(cuisine=None):
    """
    Description: 
        Find all restaurants that serve a specific cuisine
    Params:
        cuisine (string) : type of restaurant to find
    Returns: 
        list
    """

    if cuisine == None:
        res = findCuisineCounts()
        cuisine = random.choice(res)['_id']

    res = coll.find({ 'cuisine': cuisine})

    return list(res)

if __name__=='__main__':
    print("\n","="*80,"\n","="*80)
    print("\nList all collections in 'moviesDb':\n")
    res = listAllCollections(dbName='moviesDb')
    print(res)

    print("\n","="*80,"\n","="*80)
    print("\nList counts of all restaurants:\n")
    res = findAllRestaurants()
    print(res["count"])

    print("\n","="*80,"\n","="*80)
    print("\nList counts of all unique cuisines:\n")
    res = findCuisineCounts()
    pprint.pprint(res)

    print("\n","="*80,"\n","="*80)
    print("\nList restaurants by cuisine (no param = random cuisine) and only print 5:\n")
    res = findRestaurantsByCuisine()
    pprint.pprint(res[:5])




```

### API

- This Api will run on `port 8003` on your server.
- Any data returned by a route will be paginated with a preset page size (typically about 1000).
- Therefore you need a way to provide a starting row for subsequent queries.
- Using an api library of your choice, create a folder on your server `/var/www/html/Apis/mongoRestaurants` and implement an API for the restaurants DB. 
- In fact, you can could rename the api folder for A05 to `/var/www/html/Apis/sqlMovie` if you want. (still OK)
- Below are a list of the minimum routes that need to be available.

#### Routes

- Restaurants 
  - Find all restaurants (paginated result)
  - Find unique restaurant categories
  - Find all restaurants in a category
  - Find all restaurants in a list of 1 or more zip codes
  - Find all restaurants near Point(x,y)
  - Find all restaurants with a min rating of X



### Deliverables

* As of now you should have a fastApi instance always running and ready on your server:
  * at port 8001 corresponding to your [sqlZoo assignment](../A04/README.md).
  * at port 8002 corresponding to your [Imdb assignment](../A05/README.md).
* A similar api should obviously be available on port 8003 for this mongo assignment.
* Create a folder in your assignments folder called `A06` and place any and all documents in this folder. 
* Most importantly is a **README describing your project** and all the files. Help for [comments](../../Resources/03-Comments/README.md) and [readmees](../../Resources/04-Readmees/README.md) are in the [Resources](../../Resources/README.md) folder.
