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

After specifying the document, click on Save. Similarly, go ahead and insert other documents.



To view the documents inside a collection, click on the collection in the left panel and you will see a list of all of the documents in the content area. The records most recently inserted will appear first.

Updating, Deleting, and Duplicating Documents
You can update, delete or duplicate any document by clicking on the corresponding options provided on each document. Clicking on any of the links will take the document to edit mode where you can make changes in either JSON or PHP as you did earlier.



Querying Documents
Querying the database is one of the important functions of any database administration tool. Whenever you click on a collection, you will find a text area on the top of the page for running queries against it.



Like the documents, query expressions can also be specified either as JSON or a PHP array. There are three action options available in the drop down: findAll, remove, and modify.

findAll: This is the default option. Specify the find condition and click on Submit Query. The matching documents will appear in the search results.
remove: This is similar to modify in that you just have to specify the condition for selecting documents, but the action removes the matching documents from the collection.
modify: When you click on modify, you will see two text sections. The first section is to specify the condition for matching documents and the other is to specify the update script. This feature can be used to do bulk-updates.
Using Explain
This is one of the most useful features and probably the one I like the most in Rockmongo. The explain query is frequently used to analyze queries and their index usages. As shown below, you can specify your find query and then click on the Explain button. This will give all the cursor details for the query.



Importing and Exporting Databases
Import and export features are useful for when you want to backup the database. The import/export functionality in Rockmongo does the same task as the mongoimport and mongoexport functions.

To export a database or collection, click the Export tab. Check all the checkboxes for the collections you want to export. Check the Download option as well, and then click on Export. It will give you a downloadable JavaScript file containing the entire exported database.



To import the data in another database, go to that database and click on the Import tab. Choose the JS file you just downloaded, and the entire dataset will be imported to the database.

Conclusion
There are a lot of other features in Rockmongo that I’m sure you’ll want to explore once you start working with it. In this article I’ve covered only the most frequently used features to help you get a head start with it. If you have any questions related to the article, feel free to post your comments!

