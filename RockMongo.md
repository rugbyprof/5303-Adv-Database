## RockMongo

Source: http://www.sitepoint.com/rockmongo-for-php-powered-mongodb-administration/

By default, MongoDB provides the interactive JavaScript-based mongo shell which can be used for performing database operations. Although this shell may be the best approach to start with MongoDB queries, a GUI tool to administer the service is always useful.

There are many such GUI tools available, like Rockmongo, PHPMoAdmin, Fang of Mango, UMongo, MongoExplorer, and MongoVUE, to name just a few. When it comes to using MongoDB with PHP-based projects, Rockmongo and PHPMoAdmin are good options. In this article, we’ll take a look at Rockmongo.

Rockmongo is an open source MongoDB administration tool written in PHP5. You’ll become familiar with using Rockmongo to create databases, collections and documents, query collections, and import and export data. Ready?

### Getting Started
(Already done for you.)

The requirements for running Rockmongo are:

1. a web server running PHP
2. PHP 5.1.6 or higher with session support
3. the php_mongo extension for MongoDB

__Up to 'Inserting Documents' is tailored for [04-MongoDB-Intro.md](https://github.com/rugbyprof/5303-Adv-Database/blob/master/04-MongoDB-Intro.md)__

Goto: http://cs2.mwsu.edu/rockmongo/ and login. The default username and password is “admin” and “admin”. 

![](https://s3.amazonaws.com/f.cl.ly/items/0e1c2u1R3u0f461E0a3M/rockmongo-01.png)

As you can see, the home page lists basic information about MongoDB Server location and connection, PHP Web Server and MongoDB settings. The left panel shows the list of databases and collections.

### Creating Databases and Collections

The Databases tab lists all of the database available on the MongoDB server. To create a new database, do the following:

One:

![](https://s3.amazonaws.com/f.cl.ly/items/3e2S0X3b0y4541061t11/createdb1.png)

Two:

![](https://s3.amazonaws.com/f.cl.ly/items/1o1n2R3V090z160z413U/createdb2.png)

Then enter the name of your database and click Create (use your cs2 username). The newly created database will appear in the left panel. Everyone will have access to everyone else's collection, so be respectful.

To create a new collection:

1. Click on your database
2. Click on Create
3. Name your Database `random_people`

![](https://s3.amazonaws.com/f.cl.ly/items/1V3F281d0v391a0e1m2L/create_collection.png)

When you provide the collection information, don’t worry about the Is Capped field. It’s safe to leave it unchecked.


The new collection will appear in the left panel under the database. You can click on the collection to list all of the documents in it. (Note that Mongo DB creates a default system.indexes collection when you create first collection in a database.)



### Inserting Documents
To insert documents, click on the Insert tab and then the name of the collection.

We can specify the new document structure either as JSON or a PHP array. Choosing either format doesn’t make any difference to the document formed, it’s just a matter of comfort for developers.

JSON:

```json
{
   "user": {
     "gender": "female",
     "name": {
       "title": "ms",
       "first": "manuela",
       "last": "velasco" 
    },
     "location": {
       "street": "1969 calle de alberto aguilera",
       "city": "la coruña",
       "state": "asturias",
       "zip": "56298" 
    } 
  } 
}
```

PHP Array:

```php
array(
   "user" => array(
     "gender" => "female",
     "name" => array(
       "title" => "ms",
       "first" => "manuela",
       "last" => "velasco" 
    ),
     "location" => array(
       "street" => "1969 calle de alberto aguilera",
       "city" => "la coruña",
       "state" => "asturias",
       "zip" => "56298" 
    )
  )
)
```

After specifying the document, click on Save. 

![](https://s3.amazonaws.com/f.cl.ly/items/1z2J1V3P1S1J120W2M35/mongoIDexample.png)

Notice that MongoDB automatically added an ID to your document for you.

To view the documents inside a collection, click on the collection in the left panel and you will see a list of all of the documents in the content area. The records most recently inserted will appear first.

### Updating, Deleting, and Duplicating Documents

You can update, delete or duplicate any document by clicking on the corresponding options provided on each document. Clicking on any of the links will take the document to edit mode where you can make changes in either JSON or PHP as you did earlier.

![](https://s3.amazonaws.com/f.cl.ly/items/460g2Q01202x1n3Q1P1w/mongoupdatedeleteexample.png)

### Querying Documents
Querying the database is one of the important functions of any database administration tool. Whenever you click on a collection, you will find a text area on the top of the page for running queries against it.

![](https://s3.amazonaws.com/f.cl.ly/items/3h183r170U3y072Q3L0S/findquery.png)

Like the documents, query expressions can also be specified either as JSON or a PHP array. There are three action options available in the drop down: findAll, remove, and modify.

- findAll: This is the default option. Specify the find condition and click on Submit Query. The matching documents will appear in the search results.
- remove: This is similar to modify in that you just have to specify the condition for selecting documents, but the action removes the matching documents from the collection.
- modify: When you click on modify, you will see two text sections. The first section is to specify the condition for matching documents and the other is to specify the update script. This feature can be used to do bulk-updates.

The query:

```json
{
    "user.gender": "male"
}
```

On the following data

```json
[{
  "user": {
    "gender": "male",
    "name": {
      "title": "mr",
      "first": "corey",
      "last": "andrews"
    },
    "location": {
      "street": "7453 church street",
      "city": "preston",
      "state": "tayside",
      "zip": "I30 7AE"
    }
  }
},
{
  "user": {
    "gender": "female",
    "name": {
      "title": "miss",
      "first": "ethel",
      "last": "obrien"
    },
    "location": {
      "street": "8846 blossom hill rd",
      "city": "ballarat",
      "state": "queensland",
      "zip": 38342
    }
  }
},
{
  "user": {
    "gender": "male",
    "name": {
      "title": "mr",
      "first": "elouan",
      "last": "faure"
    },
    "location": {
      "street": "4557 esplanade du 9 novembre 1989",
      "city": "courbevoie",
      "state": "morbihan",
      "zip": 19843
    }
  }
},
{
  "user": {
    "gender": "female",
    "name": {
      "title": "ms",
      "first": "manuela",
      "last": "velasco"
    },
    "location": {
      "street": "1969 calle de alberto aguilera",
      "city": "la coruña",
      "state": "asturias",
      "zip": "56298"
    }
  }
}]
```

returns:

```json 
[{
  "user": {
    "gender": "male",
    "name": {
      "title": "mr",
      "first": "elouan",
      "last": "faure"
    },
    "location": {
      "street": "4557 esplanade du 9 novembre 1989",
      "city": "courbevoie",
      "state": "morbihan",
      "zip": 19843
    }
  }
},
{
  "user": {
    "gender": "male",
    "name": {
      "title": "mr",
      "first": "corey",
      "last": "andrews"
    },
    "location": {
      "street": "7453 church street",
      "city": "preston",
      "state": "tayside",
      "zip": "I30 7AE"
    }
  }
}]
```

The original tutorial at http://www.sitepoint.com/rockmongo-for-php-powered-mongodb-administration/ has a little more to offer. This version was tailored to get you up and going for your assignment.



