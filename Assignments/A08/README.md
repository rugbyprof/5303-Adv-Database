## Assignment 8 - Redis ~~Api~~ Something
#### Due: 12-06-2021 (MONDAY @ 5:45 p.m.)

## Overview

One issue with redis is its inability to store complex structures.  If you  have gone through the overview from RealPython [here](https://realpython.com/python-redis/) then you know that redis is known for its fast but simple data structures. They are somewhat limiting, but redis wasn't built to replace DBMS's. 

### DBMS

In a relational database world (**DBMS**) , we have the ability to create complex relationships between tables that themselves can have strict definitions on the data stored. There are stored procedures, triggers, and cascading events that assist with data integrity.  This is the tool used when there are many different, but somehow related, data components that need stored and queried. This is the defacto standard or the "all in one" data storage tool currently (IMHO). 

<img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/imdb_schema.png" width="400">

### Mongo

Then there is **MongoDB**. This removed the parts of **DBMS**'s that programmers didn't want to deal with. A "schema" or set of data rules that are enforced when data is entered, altered, and even deleted. Programmers (myself included) don't always want to headache of designing the backend, when all we want to do is "save stuff" and "get stuff". Ok, maybe "get stuff with a filter" or "get stuff sorted". Mongo provided all this functionality using a "document" storage mentality. By "document" I really mean JSON, since they go hand in hand. Mongo was born in 2007 and JSON's popularity started rising in 2005 pushing XML out of the way as the (then) current data definition standard. Below is the same data in JSON and XML. I think you can see why JSON took over in popularity. It's not just because of it's slightly more concise syntax. Read [THIS](https://twobithistory.org/2017/09/21/the-rise-and-rise-of-json.html) if you are interested.

```json
{"employees":[
  { "firstName":"John", "lastName":"Doe" },
  { "firstName":"Anna", "lastName":"Smith" },
  { "firstName":"Peter", "lastName":"Jones" }
]}
```

```xml
<employees>
  <employee>
    <firstName>John</firstName> <lastName>Doe</lastName>
  </employee>
  <employee>
    <firstName>Anna</firstName> <lastName>Smith</lastName>
  </employee>
  <employee>
    <firstName>Peter</firstName> <lastName>Jones</lastName>
  </employee>
</employees>
```

Mongo didn't become popular just because programmers were lazy and didn't want to define database schemas. It also had to do with the onslaught of big data, and the DBMS's of the day not capable of handling the issues that came with big data. A big issue (no pun intended) was the partitioning of data stores. Clustering, partitioning, and scalability were not very friendly in the DBMS world. They were built in to Mongo however, making it easier to scale large databases. As time goes on, another "need" arises. 

### Redis

The need for fast memory resident data started appearing. With websites wanting the ability to "scale" or do things dynamically, having data structures that were queryable, fast, and distributable became highly sought after. [Redis](https://en.wikipedia.org/wiki/Redis) was born in 2009 written as an in house solution to monitoring web logs in order to help with scalability. 

Redis offers what we typically think of as "data structures" as storage containers. Some examples are Sets, Lists, Hashes (dictionary) all of which are available with lots of built in functions to find, update, and deleted items or entire containers worth of data. There is no dispute that Redis is fast, but where there are some unfounded grumblings is in how Redis stores and retrieves JSON. And this bring me to your assignment. 

## Assignment

We don't have time for a full fledged comparison of a bunch of databases, do I thought we would compare how each of these three: Mysql (or MariaDB)<sup>[1]</sup>, MongoDB, and Redis. The comparison will be by running scripts locally ~~and via Api calls from an external source~~. 

### Variables
Variables that impact performance:
- Database size
- Server Specs
- Responsiveness (if network is used)
- Load (if multiple clients are employed)
- Type of data
  - integers, strings, etc.
  - large vs small objects
- Transaction types:
  - Insertions 
  - Searches
  - Updates
  - Deletes
- Combinations of Transactions:
  - Heavy Insertions with low searches , updates, and deletes
  - Search heavy low insertion (after initial db load) and low updates / deletes
  - etc. 

### Experiment

The experiment should time each transaction and calculate averages. But each aggregation should be applied to a database that is configured with slight differences using the above variables. 

- Insert `N` objects
- Do `n` searches for single values (comprised of strings, int's, etc.)
- Do `n` searches for multiple values 
- Do `n` updates to existing documents (or tuples, or data structures)
- Do `n` deletes

You should vary `N` and `n` to determine whether each database performs differently not only under differing load types, but under different sizes as well. One possible approach could be:

- Set `N`, where `N` is number of items being inserted, to:
  - 50000
  - 100000
  - 500000
  - 1 Million
  - Possibly more depending on server specs
- Then using a percentage of `N` to determine how many transactions of different types to run, you  can tailor the load on the database (document store, key value store). For example you can increase or decrease specific transaction types for each experiment before moving onto the next transaction type:
  - Run 1
    - Searches = .5 * `N`
    - Updates = 1.5 * `N`
    - Deletes = .25 * `N`
  - Run 2
    - Searches = .75 * `N`
    - Updates = 1.5 * `N`
    - Deletes = .25 * `N`
  - Run 3
    - Searches = 1 * `N`
    - Updates = 1.5 * `N`
    - Deletes = .25 * `N`
  - Run `N`
    - etc.

By organizing the amounts for each transaction type before hand, you can structure your experiments and save results much easier.

However, this approach is feasible: 

  - Run `X`
    - Searches = random(0.25 , 3.0) * `N`
    - Updates = random(0.25 , 3.0) * `N`
    - Deletes = random(0.25 , 0.75) * `N`


I'm sure your groups will come with good experiments. Just get creative.


## Deliverables

- Presentation of a summary of your findings with charts during final exam time.
- Of course all rules about putting code and results on github apply.


### Resources

- https://redis.com/redis-best-practices/data-storage-patterns/json-storage/
- https://redis.com/redis-best-practices/data-storage-patterns/object-hash-storage/
- https://github.com/RedisJSON/redisjson-py
- https://github.com/michael-mri/serialized-redis
- https://stackoverflow.com/questions/15219858/how-to-store-a-complex-object-in-redis-using-redis-py



[1] https://mariadb.com/kb/en/incompatibilities-and-feature-differences-between-mariadb-102-and-mysql-57/


