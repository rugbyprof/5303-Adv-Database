Not Done!!!

### What is MongoDB?

> MongoDB (from "humongous") is a scalable, high-performance, open source NoSQL database.

### Document database

`MongoDB` is a document database, which means that instead of storing "rows" in "tables" like a relational database, "documents" are stored in "collections."  Documents are basically `JSON` objects (technically `BSON`). This is to be distinguished from other NoSQL-type databases such as key-value cache and store (e.g. Redis).


### Document

![](http://docs.mongodb.org/manual/_images/crud-annotated-document.png)

### Collections

![](http://docs.mongodb.org/manual/_images/crud-annotated-collection.png)

### CRUD

CRUD is an acronym that stands for:  `C`reate, `R`ead, `U`pdate and `D`elete. Below are links to MongoDB's version of CRUD operations. I pulled the images for `document` and `collections` because it's the chosen storage organization that drives Mongo. A `document` is just a `json` object, and a `collection` is just a bunch of `json` objects stored together (use 'folder' as an analogy).  To view additional information about simple operations on documents and collections visit the mongo tutorials below:

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

From the above snippet, make the following changes, then run it in a php file:

```php

// select a database (Use YOUR username (e.g. griffin, vgundeti, apatel, etc.)
$db = $m->YourUserName;

```

I changed `$db = $m->YourUserName;` to `$db = $m->griffin;` and I now have a collection called `cartoons` in my database.

![](https://s3.amazonaws.com/f.cl.ly/items/3e1o24141R471x0c0N1l/cartoonresult.png)

Ok, here's another example:

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

