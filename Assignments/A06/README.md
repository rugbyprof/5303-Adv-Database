## Assignment 6 - Movies DB (but with Mongo)
#### Due: 10-10-2021 (Monday @ 5:00 p.m.)

### References For You  

1. [Installing MongoDB](https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-20-04)
   
2. [Secure MongoDB](https://www.digitalocean.com/community/tutorials/how-to-secure-mongodb-on-ubuntu-20-04)

```mongo
db.createUser({user: "adminguru",pwd: passwordPrompt(),roles: [ { role: "userAdminAnyDatabase", db: "admin" }, "readWriteAnyDatabase" ]})
```

3. [Remote Access to Mongo](https://www.digitalocean.com/community/tutorials/how-to-configure-remote-access-for-mongodb-on-ubuntu-20-04)

```
mongodb://your.ip.address:27017
```

4. [Py Mongo](https://www.digitalocean.com/community/tutorials/how-to-perform-crud-operations-in-mongodb-using-pymongo-on-ubuntu-20-04)


### Loading Database

Using your code that loaded the data for [A05](../A05/README.md), store all information that is associated with movies that have a release year of **1950** and later. Ignore the same items as before.

### API

- This Api will run on `port 8003` on your server.
- Any data returned by a route will be paginated with a preset page size (typically about 1000).
- Therefore you need a way to provide a starting row for subsequent queries.
- Using an api library of your choice, create a folder on your server `/var/www/html/Apis/mongoMovie` and implement an API for the movies DB. 
- In fact, you can rename the api folder for A05 to `/var/www/html/Apis/sqlMovie` if you want.
- Below are a list of the minimum routes that need to be available.

#### Routes

- Movies 
  - Find all
  - Filter on (any field in table)[year,runtime(min/max)]
    - e.g. return all movies in 1961
    - e.g. return all movies with runtime > 90
    - e.g. return all movies with runtime between 80 and 100
  - Filter on actor or actress (id)
    - e.g. return all movies associated with a specific actress
    - e.g. return all movies associated with a set of actors and actresses
  - Filter on genre(s)
    - e.g return all movies in a specified genre
- People
  - Find all
  - Filter on name (first or last)
  - Filter on movie (id)
  - Filter on genre(s)
  - Filter on "worked with `id` or `ids`" 
    - e.g. find all actors and actresses that worked with `id`
  - Filter on profession
- Genre
  - Find all
- Profession
  - Find all

### Deliverables

* As of now you should have a fastApi instance always running and ready on your server:
  * at port 8001 corresponding to your [sqlZoo assignment](../A04/README.md).
  * at port 8002 corresponding to your [Imdb assignment](../A05/README.md).
* A similar api should obviously be available on port 8003 for this mongo assignment.
* Create a folder in your assignments folder called `A06` and place any and all documents in this folder. 
* Most importantly is a **README describing your project** and all the files. Help for [comments](../../Resources/03-Comments/README.md) and [readmees](../../Resources/04-Readmees/README.md) are in the [Resources](../../Resources/README.md) folder.
