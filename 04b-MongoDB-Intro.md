## Assignment 4
Due: Wednesday Sep 30 (by class time 4:00 pm) 

### What is MongoDB?

> MongoDB (from "humongous") is a scalable, high-performance, open source NoSQL database.

### Document database

`MongoDB` is a document database, which means that instead of storing "rows" in "tables" like a relational database, "documents" are stored in "collections."  Documents are basically `JSON` objects (technically `BSON`). This is to be distinguished from other NoSQL-type databases such as key-value cache and store (e.g. Redis).


### Document

![](https://s3.amazonaws.com/f.cl.ly/items/1a2I0U040Y2V413m3a3I/document.png)

### Collections

![](https://s3.amazonaws.com/f.cl.ly/items/2p2x1g00252P2q0o2N3M/collection.png)

### CRUD

CRUD is an acronym that stands for:  `C`reate, `R`ead, `U`pdate and `D`elete. Below are links to MongoDB's version of CRUD operations. I pulled the images for `document` and `collections` because it's the chosen storage organization that drives Mongo. A `document` is just a `json` object, and a `collection` is just a bunch of `json` objects stored together (like in a folder).  To view additional information about simple operations on documents and collections visit the mongo tutorials below:

- http://docs.mongodb.org/manual/core/crud-introduction/
- http://docs.mongodb.org/manual/core/read-operations-introduction/
- http://docs.mongodb.org/manual/core/write-operations-introduction/

Crud operations are made a little easier using `RockMongo`, but of course, you won't always have a crutch such as that to help you. It's definitely a good tool to help visualize results, and perform simple queries. But what if (just like in a previous assignment) we wanted to insert 1000+ documents (people) into our collection? Well, lets start a little slower using some PHP.

### Inserting Documents via Php

Below is an example pulled straight from http://php.net/manual/en/mongo.tutorial.php. 

```php
<?php

// connect
$m = new MongoClient();

// select a database
$db = $m->comedy;

// select a collection (analogous to a relational database's table)
$collection = $db->cartoons;

// add a record
$document = array( "title" => "Calvin and Hobbes", "author" => "Bill Watterson" );
$collection->insert($document);

// add another record, with a different "shape"
$document = array( "title" => "XKCD", "online" => true );
$collection->insert($document);

// find everything in the collection
$cursor = $collection->find();

// iterate through the results
foreach ($cursor as $document) {
    echo $document["title"] . "\n";
}

?>
```

From the above snippet, make the following changes:

From

```php

// select a database
$db = $m->comedy;

```

To:

```php

// select a database (Use YOUR username (e.g. griffin, vgundeti, apatel, etc.)
$db = $m->YourUserName;

```

I changed `$db = $m->YourUserName;` to `$db = $m->griffin;` and I now have a collection called `cartoons` in my database. This means that the `cartoon` collection didn't exist, BUT by simply using `$collection = $db->cartoons;` in my code, it created it for me.

![](https://s3.amazonaws.com/f.cl.ly/items/3e1o24141R471x0c0N1l/cartoonresult.png)

Here's another example:

```php
<?php

// connect
$m = new MongoClient();

// select a database
$db = $m->griffin;

// select a collection (analogous to a relational database's table)
$collection = $db->cartoons;

$json = '
{
    "title":"The Far Side",
    "author":"Gary Larson"
}
';

$document = json_decode($json);

// add a record
$collection->insert($document);

?>
```

The important part of this code is the ease in which I inserted:

```php
$json = '
{
    "title":"The Far Side",
    "author":"Gary Larson"
    "funny":"True"
}
';
```

Now our database looks like:

![](https://s3.amazonaws.com/f.cl.ly/items/2c0A2i41061C143K2m25/phpCartoonResults.png)

Notice how:

1. It was very easy to insert a `json object` (document) into the collection.
2. None of the `documents` are have exactly the same structure.

MongoDB isn't worried about having perfect table structures with normalized data split out into many tables with relationships. It's worried about getting "documents" of data without all the "joining" that happens in an RDBMS. That doesn't means you can't do joins in MongoDB, but it does mean I'm not going to cover it right now :)

Finally....

### Your Assignment

- Create a database in MongoDB that is the same as your cs2 username.
- Create a collection in your database called `random_people` in your database.
- Using parts of your code from assignment 2 (that accesses the random people api) along with the above examples and write a php script to load 1000 individuals into your `random_people` collection.

### Results / Deliverables

- A script called load_mongo_db.php in your assignment4 folder.
- A database with the same name as your cs2 username.
- A collection called `random_people` in your database.
- Approx 1000+ random users in your table (unique not enforced right now)
- Copy the assignment4 folder into your github repository and push it to github.
