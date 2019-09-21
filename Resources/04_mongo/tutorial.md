
## How to Access MongoDB

You can access MongoDB via the MongoDB Shell, or from within your programming environment using a MongoDB driver.
Once you have started a MongoDB instance (i.e. by using the mongod command), you can now connect to that instance and start working with MongoDB.

You can use your computer's Terminal or Command Prompt to connect and run commands directly from the MongoDB Shell.
You can also connect to a running MongoDB instance via your programming environment by using a MongoDB driver.

### MongoDB Shell (mongo)
Throughout this tutorial we'll use the MongoDB Shell (called mongo) to connect to our running MongoDB instance.
The mongo shell is an interactive JavaScript interface to MongoDB and it is included in the MongoDB package. You can use the mongo shell to query and update data, as well as perform administrative functions.
The MongoDB Shell is located in the same place as the other binaries. So to run it, open a new Terminal/Command Prompt window and enter mongo (Linux/Mac) or mongo.exe (Windows).
This assumes that the path has been added to your PATH. If it hasn't, you'll need to provide the full path.

Be sure to leave the mongod process open in its own Terminal/Command window. The above commands should be entered into a different Terminal/Command window to the one that the mongod process was started in.

Connect from your Programming Environment
You can also connect to MongoDB from within your programming environment. 
The MongoDB website maintains a list of MongoDB drivers that can be used to connect to MongoDB.
This page includes drivers for the following languages:

C
C++ (legacy)
C++11
C#
Java
Node.js
Perl
PHP
Python
Motor
Ruby
Scala

Once you have connected to the mongod process, you can create a database.



## MongoDB - Create a Database

### In MongoDB, you create a database by switching to a non-existent database, then inserting data into it. 

There is no `CREATE DATABASE` statement in MongoDB like there is in SQL. To create a database in MongoDB, simply switch to a non-existent database, then insert data into it.

To switch databases, run the use statement. If the database doesn't already exist, it will be created:


```mongo
use music
```

This results in the following message:

```
switched to db music
```

However, the database isn't actually created until you insert data into it:

```
db.artists.insert({ artistname: "The Tea Party" })
```

	
The above statement creates a collection and inserts a document into it. 
It will generate the following message:

WriteResult({ "nInserted" : 1 })

You can see the database in your list of databases by issuing the following command:

```
show databases
```

Here's an example of the output:

```
local  0.000GB
music  0.000GB
test   0.005GB
```

In this case, three databases are displayed, one of which is our newly created database (music).
You can also run the following line to view the contents of your database:

```
db.artists.find()
```


	
Which should result in output like this:

```
{ "_id" : ObjectId("5780fbf948ef8c6b3ffb0149"), "artistname" : "The Tea Party" }
```

As you can see, our name/value pair is now stored in the new database. MongoDB has also inserted an _id field. If you don't provide an _id field, MongoDB provides it for you.


## MongoDB - Create a Collection

### You can create a collection using the createCollection() method, or on the fly as you insert a document.

Collections are like containers for related documents. They are typically used to group documents of a similar topic. For example, you could have collection names such as users, pageviews, posts, comments, etc.

When we created our database, we created a collection called artists. This collection will contain documents with artist details, such as the artists' names, albums they've released, etc.

### Two ways to Create a Collection

Here are two ways of creating collections:
- You can create a collection on the fly when inserting a document (using the insert() method. 
- You can also create a collection explicitly, using the createCollection() method.

### On the Fly
When you use the insert() method to insert a document, you specify the collection that the document will be inserted into. If the collection doesn't already exist, it will be created.

This is the method that we used previously when we created our artists collection while inserting a document.
Here's the code that we used:

```
db.artists.insert({ artistname: "The Tea Party" })
```

	
In this case, the artists collection didn't previously exist so it was created for us.
Using the createCollection() Method
You can also create collections using the createCollection() method. This allows you to create a collection without inserting a document. 
Here's an example of using the createCollection() method:

```
db.createCollection("producers")
```

### With Options

You can also specify options for the collection by using the db.createCollection(name, options) syntax.
Here's an example:

```
db.createCollection("log", { capped : true, size : 4500500, max : 4000 } )
```

	
The fields available as of MongoDB version 3.2 are as follows.


| Field       | Type    | Description                                                                                                                                                                                                                                                |
| :---------- | :------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| capped      | boolean | When set to true, creates a capped collection. A capped collection is a fixed-sized collection that automatically overwrites its oldest entries when it reaches its maximum size. If you specify true, you must also set a maximum size in the size field. |
| autoIndexId | boolean | Specify false to disable the automatic creation of an index on the _id field. As of MongoDB version 3.2, this field is deprecated, and it will be removed in version 3.4.|
| size |number| Maximum size in bytes for a capped collection. Only used with capped collections (it is ignored in other collections). |
| max | number | Maximum number of documents allowed in the capped collection. Note that the size field takes precedence over the max field. If the collection reaches its size limit before the document limit has been reached, MongoDB will remove documents anyway. |
| usePowerOf2Sizes | boolean | Only available in the MMAPv1 storage engine. This field has been deprecated since version 3.0. | 
| noPadding| boolean| Only available in the MMAPv1 storage engine. Disables the power of 2 sizes allocation for the collection. Defaults to false.|
|storageEngine| document | Only available in the WiredTiger storage engine. Allows configuration to the storage engine on a per-collection basis when creating a collection. Syntax is as follows: `{ <storage-engine-name>: <options> }` | 
| validator | document | Allows you to specify validation rules or expressions for the collection. Note that validation is only applied when inserting and updating data. Therefore, data that already exists in the database is not validated (until it is updated). | 



### MongoDB provides the insert() method (and two others) for adding documents to a database.

MongoDB provides the following three methods for inserting documents into a database:

- insert()
- insertOne()
- insertMany()

### The insert() Method

The insert() method inserts one or more documents into a collection. Each document is provided as a parameter. The collection name is prepended to the insert() method.

Here's the syntax for inserting a single document:

```
db.collectionName.insert({ name: "value" })
```

	
In the above example, the document consists of `{ name: "value" }`. This is a JSON document. JSON documents consist of one or more name/value pairs, enclosed in curly braces {}.

MongoDB uses JSON documents to store data, so that's why we insert documents in this format.

We've already used this method previously when we created a database.

Let's add another document to our database:

```
db.artists.insert({ artistname: "Jorn Lande" })
```
	
This inserts a document with `{ artistname: "Jorn Lande" }` as its contents.

Now, if we search the artists collection, we will see two documents (including the one we created previously):

```
> db.artists.find()
{ "_id" : ObjectId("5780fbf948ef8c6b3ffb0149"), "artistname" : "The Tea Party" }
{ "_id" : ObjectId("5781c9ac48ef8c6b3ffb014a"), "artistname" : "Jorn Lande" }
```

Note that MongoDB has created an `_id` field for the documents. If you don't specify one, MongoDB will create one for you. However, you can provide this field when doing the insert if you prefer to have control over the value of the `_id` field.

```
db.artists.insert({ _id: 1, artistname: "AC/DC" })
```
	
Result:

```
> db.artists.find()
{ "_id" : ObjectId("5780fbf948ef8c6b3ffb0149"), "artistname" : "The Tea Party" }
{ "_id" : ObjectId("5781c9ac48ef8c6b3ffb014a"), "artistname" : "Jorn Lande" }
{ "_id" : 1, "artistname" : "AC/DC" }
```

The `_id` that MongoDB provides is a 12-byte ObjectId value. It is made up of the following values;

- a 4-byte value representing the seconds since the Unix epoch,
- a 3-byte machine identifier,
- a 2-byte process id, and
- a 3-byte counter, starting with a random value.

### Create Multiple Documents

You can insert multiple documents within a single insert() method.

In this example, we insert three documents:

```
db.artists.insert(
   [
     { artistname: "The Kooks" },
     { artistname: "Bastille" },
     { artistname: "Gang of Four" }
   ]
)
```

	
Note that the documents are provided as an array. The documents are enclosed in square brackets [], and they are separated by commas.

Running the above code results in the following message:

```
BulkWriteResult({
	"writeErrors" : [ ],
	"writeConcernErrors" : [ ],
	"nInserted" : 3,
	"nUpserted" : 0,
	"nMatched" : 0,
	"nModified" : 0,
	"nRemoved" : 0,
	"upserted" : [ ]
})
```

### Embedded Documents

A document can contain other documents, arrays, and arrays of documents.

You can also provide multiple name/value pairs within a document by separating them with a comma.

```
db.artists.insert({
    artistname : "Deep Purple",
    albums : [
                {
                    album : "Machine Head",
                    year : 1972,
                    genre : "Rock"
                }, 
                {
                    album : "Stormbringer",
                    year : 1974,
                    genre : "Rock"
                }
            ]
})
```
	
Result:

```
WriteResult({ "nInserted" : 1 })
```

### Parameters

The `insert()` method accepts the following parameters.


| Parameter | Type | Description | 
|:----------|:-----|:------------|
| document | document or array | A document or array of documents to insert into the collection (as in the above examples). |
| writeConcern | document | Optional parameter. This is a document expressing the write concern. A write concern describes the level of acknowledgement requested from MongoDB for write operations to a standalone mongod or to replica sets or to sharded clusters. |
| ordered | boolean | Optional parameter. If the value is set to true, MongoDB will perform an ordered insert of the documents in the array, and if an error occurs with one of documents, MongoDB will return without processing the remaining documents in the array. 
If the value is set to false, MongoDB will perform an unordered insert, and if an error occurs with one of documents, the remaining documents in the array will continue to be processed. | 


### The insertOne() Method

You can also use the `insertOne()` method to insert a single document into a collection:

```
db.musicians.insertOne({ _id: 1, name: "Ian Gillan", instrument: "Vocals" })
```

	
Here, we've specified a non-existent collection. As with the insert() method, the specified collection will be created if it doesn't already exist.
You'll notice that the output is different to when you use the insert() method:

```
{ "acknowledged" : true, "insertedId" : 1 }
```

### Embedded Documents

As with insert(), you can insert embedded documents and arrays of documents:

```
db.artists.insertOne({
    artistname : "Miles Davis",
    albums : [
                {
                    album : "Kind of Blue",
                    year : 1959,
                    genre : "Jazz"
                }, 
                {
                    album : "Bitches Brew",
                    year : 1970,
                    genre : "Jazz"
                }
            ]
})
```

	
Result:

```
{
	"acknowledged" : true,
	"insertedId" : ObjectId("578214f048ef8c6b3ffb0159")
}
```

### The insertMany() Method

As the name suggests, you can use insertMany() to insert multiple documents:

```
db.musicians.insertMany(
   [
     { _id: 2, name: "Ian Paice", instrument: "Drums", born: 1948 },
     { _id: 3, name: "Roger Glover", instrument: "Bass", born: 1945 },
     { _id: 4, name: "Steve Morse", instrument: "Guitar", born: 1954 },
     { _id: 5, name: "Don Airey", instrument: "Keyboards", born: 1948 },
     { _id: 6, name: "Jeff Martin", instrument: "Vocals", born: 1969 },
     { _id: 7, name: "Jeff Burrows", instrument: "Drums", born: 1968 },
     { _id: 8, name: "Stuart Chatwood", instrument: "Bass", born: 1969 },
   ]
)
```


	
Again, the output when using `insertMany()` is different than if you'd inserted multiple documents using the `insert()` method:

```
{
	"acknowledged" : true,
	"insertedIds" : [
		2,
		3,
		4,
		5,
		6,
		7,
		8
	]
}
```

### Embedded Documents

```
db.artists.insertMany(
[
{
    artistname : "Robben Ford",
    albums : [
                {
                    album : "Bringing it Back Home",
                    year : 2013,
                    genre : "Blues"
                }, 
                {
                    album : "Talk to Your Daughter",
                    year : 1988,
                    genre : "Blues"
                }
            ]
}, {
    artistname : "Snoop Dogg",
    albums : [
                {
                    album : "Tha Doggfather",
                    year : 1996,
                    genre : "Rap"
                }, 
                {
                    album : "Reincarnated",
                    year : 2013,
                    genre : "Reggae"
                }
            ]
}
])
```
	
Result:

```
{
	"acknowledged" : true,
	"insertedIds" : [
		ObjectId("578217c248ef8c6b3ffb015a"),
		ObjectId("578217c248ef8c6b3ffb015b")
	]
}
```

## MongoDB - Query a Collection


### MongoDB provides the db.collection.find() method to query documents within a collection.

The `db.collection.find()` selects documents in a collection and returns a cursor to the selected documents.

### Return all Documents

This example returns all documents from the musicians collection:

```
db.musicians.find()
```

	
Result:

```
{ "_id" : 1, "name" : "Ian Gillan", "instrument" : "Vocals" }
{ "_id" : 2, "name" : "Ian Paice", "instrument" : "Drums", "born" : 1948 }
{ "_id" : 3, "name" : "Roger Glover", "instrument" : "Bass", "born" : 1945 }
{ "_id" : 4, "name" : "Steve Morse", "instrument" : "Guitar", "born" : 1954 }
{ "_id" : 5, "name" : "Don Airey", "instrument" : "Keyboards", "born" : 1948 }
{ "_id" : 6, "name" : "Jeff Martin", "instrument" : "Vocals", "born" : 1969 }
{ "_id" : 7, "name" : "Jeff Burrows", "instrument" : "Drums", "born" : 1968 }
{ "_id" : 8, "name" : "Stuart Chatwood", "instrument" : "Bass", "born" : 1969 }
```

It returns all documents because we didn't pass any parameters as filtering criteria.

The above query is a shortened version of `db.musicians.find( {} )`. In the above query, we omitted the curly braces {}. This is perfectly valid when working with MongoDB.

### Add Filtering Criteria

You can filter the results down by providing only the criteria that you're interested in.

For example, if we're only interested in Deep Purple from the artists collection:

```
db.artists.find({ artistname : "Deep Purple" })
```
	
Result:

```
{ "_id" : ObjectId("5781f85d48ef8c6b3ffb0150"), "artistname" : "Deep Purple", "albums" : [ { "album" : "Machine Head", "year" : 1972, "genre" : "Rock" }, { "album" : "Stormbringer", "year" : 1974, "genre" : "Rock" } ] }
```

### Format the Results

You might find the above results a bit hard to read. The document is returned as one long line of text. 
You can use the `pretty()` method to format the results so that they're a bit easier to read.
Just append `pretty()` to the end, like this:

```
db.artists.find({ artistname : "Deep Purple" }).pretty()
```
	
Result:

```
{
	"_id" : ObjectId("5781f85d48ef8c6b3ffb0150"),
	"artistname" : "Deep Purple",
	"albums" : [
		{
			"album" : "Machine Head",
			"year" : 1972,
			"genre" : "Rock"
		},
		{
			"album" : "Stormbringer",
			"year" : 1974,
			"genre" : "Rock"
		}
	]
}
```

### More Filtering Options

Here are some more ways of filtering results.

#### Specify AND Conditions

You can specify that only documents containing two or more specified values should be returned.

In this example, we specify that only musicians who play drums and where born before 1950 should be returned. Only documents that match both criteria will be returned.

```
db.musicians.find( { instrument: "Drums", born: { $lt: 1950 } } )
```

Result:

```
{ "_id" : 2, "name" : "Ian Paice", "instrument" : "Drums", "born" : 1948 }
```

#### Specify OR Conditions
 
You can also specify that either one or the other value should be true. As long as one of the conditions are true, the document will be returned.
In this example, we want documents that contain musicians that either play drums, or were born before 1950.

```
db.musicians.find(
   {
     $or: [ { instrument: "Drums" }, { born: { $lt: 1950 } } ]
   }
)
```
	
Result:

```
{ "_id" : 2, "name" : "Ian Paice", "instrument" : "Drums", "born" : 1948 }
{ "_id" : 3, "name" : "Roger Glover", "instrument" : "Bass", "born" : 1945 }
{ "_id" : 5, "name" : "Don Airey", "instrument" : "Keyboards", "born" : 1948 }
{ "_id" : 7, "name" : "Jeff Burrows", "instrument" : "Drums", "born" : 1968 }
```

#### The $in Operator

The `$in` operator allows you to provide a list of values. If a document contains any of those values, it will be returned.

Using the following example, we're searching for all musicians who are either on vocals, or play guitar.

```
db.musicians.find( { instrument: { $in: [ "Vocals", "Guitar" ] } } )
```
	
Result

```
{ "_id" : 1, "name" : "Ian Gillan", "instrument" : "Vocals" }
{ "_id" : 4, "name" : "Steve Morse", "instrument" : "Guitar", "born" : 1954 }
{ "_id" : 6, "name" : "Jeff Martin", "instrument" : "Vocals", "born" : 1969 }
```

#### Query an Array of Documents

This example queries an array of documents. It finds albums that were released after the year 2000.

```
db.artists.find(
   {
      albums: {
                $elemMatch: {
                     year: { $gt: 2000 }
                }
      }
   }
).pretty()
```
	
Result:

```
{
	"_id" : ObjectId("578217c248ef8c6b3ffb015a"),
	"artistname" : "Robben Ford",
	"albums" : [
		{
			"album" : "Bringing it Back Home",
			"year" : 2013,
			"genre" : "Blues"
		},
		{
			"album" : "Talk to Your Daughter",
			"year" : 1988,
			"genre" : "Blues"
		}
	]
}
{
	"_id" : ObjectId("578217c248ef8c6b3ffb015b"),
	"artistname" : "Snoop Dogg",
	"albums" : [
		{
			"album" : "Tha Doggfather",
			"year" : 1996,
			"genre" : "Rap"
		},
		{
			"album" : "Reincarnated",
			"year" : 2013,
			"genre" : "Reggae"
		}
	]
}
```

You'll notice that these results also contain albums from earlier than 2000. This is correct — it's the way document-oriented databases work. Any query will return the whole document (but only those documents that match the specified criteria). 

### The db.collection.findOne() Method

You can use the `db.collection.findOne()` method to return one document that satisfies the specified query criteria.

If multiple documents satisfy the criteria, only the first one is returned, as determined by the natural order of the documents on disk.

So searching a whole collection like this:

```
db.musicians.findOne( )
```
	
Will only return one document:

```
{ "_id" : 1, "name" : "Ian Gillan", "instrument" : "Vocals" }
```

If we change the `findOne()` to `find()` like this:

```
db.musicians.find( )
```

We see that there are actually 8 documents in the collection:

```
{ "_id" : 1, "name" : "Ian Gillan", "instrument" : "Vocals" }
{ "_id" : 2, "name" : "Ian Paice", "instrument" : "Drums", "born" : 1948 }
{ "_id" : 3, "name" : "Roger Glover", "instrument" : "Bass", "born" : 1945 }
{ "_id" : 4, "name" : "Steve Morse", "instrument" : "Guitar", "born" : 1954 }
{ "_id" : 5, "name" : "Don Airey", "instrument" : "Keyboards", "born" : 1948 }
{ "_id" : 6, "name" : "Jeff Martin", "instrument" : "Vocals", "born" : 1969 }
{ "_id" : 7, "name" : "Jeff Burrows", "instrument" : "Drums", "born" : 1968 }
{ "_id" : 8, "name" : "Stuart Chatwood", "instrument" : "Bass", "born" : 1969 }
```


## MongoDB - Projection Queries

A projection query is a query where you specify which fields should be returned.

In MongoDB, when you query a collection using the `db.collection.find()` method, you can specify which fields you would like to have returned.

You can do this by including the field names in your query, and adding a 1 or 0 next to them, to specify whether it should be returned or not. This is a projection parameter. A projection parameter of 1 will display the field and a 0 will hide it.

### Example

First let's do a query without projection (so we can see how many fields are returned):

#### Without Projection

```
db.musicians.find( { instrument: "Vocals"} )
```

Result:

```
{ "_id" : 1, "name" : "Ian Gillan", "instrument" : "Vocals" }
{ "_id" : 6, "name" : "Jeff Martin", "instrument" : "Vocals", "born" : 1969 }
```

#### With Projection

Now, let's use projection to display just the name field:

```
db.musicians.find( { instrument: "Vocals" }, { name: 1 } )
```

Result:

```
{ "_id" : 1, "name" : "Ian Gillan" }
{ "_id" : 6, "name" : "Jeff Martin" }
```

You will notice that the _id field is automatically included, even if you don't specify it. You can exclude this field by using a 0 against it:

```
db.musicians.find( { instrument: "Vocals" }, { _id: 0, name: 1 } )
```
	
Result:

```
{ "name" : "Ian Gillan" }
{ "name" : "Jeff Martin" }
```

#### Mixing Inclusions and Exclusions

You can't mix 1s and 0s (with the exception of the _id field). If you try to mix inclusions and exclusions, like this:

```
db.musicians.find( { instrument: "Vocals" }, { name: 1, born: 0 } )
```

You'll end up with this error:

```
Error: error: {
	"waitedMS" : NumberLong(0),
	"ok" : 0,
	"errmsg" : "Projection cannot have a mix of inclusion and exclusion.",
	"code" : 2
}
```

So to you either include fields or exclude them — not both.

Here's an example of specifying fields by exclusion:

```
db.musicians.find( { instrument: "Vocals" }, { _id: 0, instrument: 0 } )
```

Result:

```
{ "name" : "Ian Gillan" }
{ "name" : "Jeff Martin", "born" : 1969 }
```

## MongoDB - Limit the Results of a Query


#### Return only the number of documents you need with the limit() method.

In MongoDB, you can use the `limit()` method to specify a maximum number of documents for a cursor to return.

When you query a collection using the `db.collection.find()` method, you can append `limit()` to specify the limit.

### Example

First let's do a query without a limit (so we can see how many documents are returned):

Without a Limit

```
db.artists.find( { albums: { $exists: false }} )
```


Result:

```
{ "_id" : ObjectId("5780fbf948ef8c6b3ffb0149"), "artistname" : "The Tea Party" }
{ "_id" : ObjectId("5781c9ac48ef8c6b3ffb014a"), "artistname" : "Jorn Lande" }
{ "_id" : 1, "artistname" : "AC/DC" }
{ "_id" : ObjectId("5781d7f248ef8c6b3ffb014d"), "artistname" : "The Kooks" }
{ "_id" : ObjectId("5781d7f248ef8c6b3ffb014e"), "artistname" : "Bastille" }
{ "_id" : ObjectId("5781d7f248ef8c6b3ffb014f"), "artistname" : "Gang of Four" }
```

#### With a Limit

OK, so let's limit the results to say, 3 documents:

```
db.artists.find( { albums: { $exists: false }} ).limit(3)
```
	
Result:

```
{ "_id" : ObjectId("5780fbf948ef8c6b3ffb0149"), "artistname" : "The Tea Party" }
{ "_id" : ObjectId("5781c9ac48ef8c6b3ffb014a"), "artistname" : "Jorn Lande" }
{ "_id" : 1, "artistname" : "AC/DC" }
```

In our query, we're using the $exists operator to check for the existence of a field. In this case we exclude those artists that have an albums field in the document.

This could easily be switched around to `{ $exists: true }` to include only those artists with an albums field.

#### Add the `skip()` Method

You can use the `skip()` method to skip to a document within the cursor. In other words, you can control where MongoDB begins returning the results.

```
db.artists.find( { albums: { $exists: false }} ).limit(3).skip(1)
```
	
Result:

```
{ "_id" : ObjectId("5781c9ac48ef8c6b3ffb014a"), "artistname" : "Jorn Lande" }
{ "_id" : 1, "artistname" : "AC/DC" }
{ "_id" : ObjectId("5781d7f248ef8c6b3ffb014d"), "artistname" : "The Kooks" }
```

So you can see that it skipped the first result, but still returned 3 documents.

Note that `skip()` can be used on any query (not just ones with `limit()`).

For example, the query at the top of this page returned 6 documents. If we add skip(3), we will end up with the last 3 documents:

```
db.artists.find( { albums: { $exists: false }} ).skip(3)
```

Result:

```
{ "_id" : ObjectId("5781d7f248ef8c6b3ffb014d"), "artistname" : "The Kooks" }
{ "_id" : ObjectId("5781d7f248ef8c6b3ffb014e"), "artistname" : "Bastille" }
{ "_id" : ObjectId("5781d7f248ef8c6b3ffb014f"), "artistname" : "Gang of Four" }
```


## MongoDB - Sort the Results of a Query


#### In MongoDB, you can sort the results of a query by using the limit() method.

In MongoDB, when you query a collection using the `db.collection.find()` method, you can append the `sort()` method to specify how the results should be sorted. 

The `sort()` method specifies a sort order for the cursor.

When using the `sort()` method, you must provide the sort order as a parameter. This must be a JSON document that defines the sort order. It will typically contain one or more fields, each followed by either 1 or -1, depending on whether the sort should be in ascending or descending order.

### Example

First let's do a query without using sort() (so we can see the natural sort order):

Without `sort()`

```
db.musicians.find( )


		var exampleCode1 = CodeMirror.fromTextArea(document.getElementById("example1"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
```

Result:

```
{ "_id" : 1, "name" : "Ian Gillan", "instrument" : "Vocals" }
{ "_id" : 2, "name" : "Ian Paice", "instrument" : "Drums", "born" : 1948 }
{ "_id" : 3, "name" : "Roger Glover", "instrument" : "Bass", "born" : 1945 }
{ "_id" : 4, "name" : "Steve Morse", "instrument" : "Guitar", "born" : 1954 }
{ "_id" : 5, "name" : "Don Airey", "instrument" : "Keyboards", "born" : 1948 }
{ "_id" : 6, "name" : "Jeff Martin", "instrument" : "Vocals", "born" : 1969 }
{ "_id" : 7, "name" : "Jeff Burrows", "instrument" : "Drums", "born" : 1968 }
{ "_id" : 8, "name" : "Stuart Chatwood", "instrument" : "Bass", "born" : 1969 }
```

With `sort()` in Ascending Order

A value of 1 next to a field name specifies that the documents should be sorted by the specified field in ascending order.

Here we sort the results by name in ascending order:

```
db.musicians.find( ).sort( { name: 1 } )
```
	
Result:

```
{ "_id" : 5, "name" : "Don Airey", "instrument" : "Keyboards", "born" : 1948 }
{ "_id" : 1, "name" : "Ian Gillan", "instrument" : "Vocals" }
{ "_id" : 2, "name" : "Ian Paice", "instrument" : "Drums", "born" : 1948 }
{ "_id" : 7, "name" : "Jeff Burrows", "instrument" : "Drums", "born" : 1968 }
{ "_id" : 6, "name" : "Jeff Martin", "instrument" : "Vocals", "born" : 1969 }
{ "_id" : 3, "name" : "Roger Glover", "instrument" : "Bass", "born" : 1945 }
{ "_id" : 4, "name" : "Steve Morse", "instrument" : "Guitar", "born" : 1954 }
{ "_id" : 8, "name" : "Stuart Chatwood", "instrument" : "Bass", "born" : 1969 }
```

With `sort()` in Descending Order

A value of -1 next to a field name specifies descending order.

Here we sort the results by name in descending order:

```
db.musicians.find( ).sort( { name: -1 } )
```

Result:

```
{ "_id" : 8, "name" : "Stuart Chatwood", "instrument" : "Bass", "born" : 1969 }
{ "_id" : 4, "name" : "Steve Morse", "instrument" : "Guitar", "born" : 1954 }
{ "_id" : 3, "name" : "Roger Glover", "instrument" : "Bass", "born" : 1945 }
{ "_id" : 6, "name" : "Jeff Martin", "instrument" : "Vocals", "born" : 1969 }
{ "_id" : 7, "name" : "Jeff Burrows", "instrument" : "Drums", "born" : 1968 }
{ "_id" : 2, "name" : "Ian Paice", "instrument" : "Drums", "born" : 1948 }
{ "_id" : 1, "name" : "Ian Gillan", "instrument" : "Vocals" }
{ "_id" : 5, "name" : "Don Airey", "instrument" : "Keyboards", "born" : 1948 }
```

#### Multiple Fields

You can sort by multiple fields. Just separate each field by a comma. When you do this, the documents will be sorted by the first field specified, then the next, and so on. 

Here, we sort by the instrument field, followed by the born field. If two or more musicians play the same instrument, the born field determines how they are sorted relative to each other.

```
db.musicians.find( ).sort( { instrument: 1, born: 1 } )
```

Result:

```
{ "_id" : 3, "name" : "Roger Glover", "instrument" : "Bass", "born" : 1945 }
{ "_id" : 8, "name" : "Stuart Chatwood", "instrument" : "Bass", "born" : 1969 }
{ "_id" : 2, "name" : "Ian Paice", "instrument" : "Drums", "born" : 1948 }
{ "_id" : 7, "name" : "Jeff Burrows", "instrument" : "Drums", "born" : 1968 }
{ "_id" : 4, "name" : "Steve Morse", "instrument" : "Guitar", "born" : 1954 }
{ "_id" : 5, "name" : "Don Airey", "instrument" : "Keyboards", "born" : 1948 }
{ "_id" : 1, "name" : "Ian Gillan", "instrument" : "Vocals" }
{ "_id" : 6, "name" : "Jeff Martin", "instrument" : "Vocals", "born" : 1969 }
```

And just to see how the second field can affect the order, switch it to a negative value (descending):

```
db.musicians.find( ).sort( { instrument: 1, born: -1 } )
```

Result:

```
{ "_id" : 8, "name" : "Stuart Chatwood", "instrument" : "Bass", "born" : 1969 }
{ "_id" : 3, "name" : "Roger Glover", "instrument" : "Bass", "born" : 1945 }
{ "_id" : 7, "name" : "Jeff Burrows", "instrument" : "Drums", "born" : 1968 }
{ "_id" : 2, "name" : "Ian Paice", "instrument" : "Drums", "born" : 1948 }
{ "_id" : 4, "name" : "Steve Morse", "instrument" : "Guitar", "born" : 1954 }
{ "_id" : 5, "name" : "Don Airey", "instrument" : "Keyboards", "born" : 1948 }
{ "_id" : 6, "name" : "Jeff Martin", "instrument" : "Vocals", "born" : 1969 }
{ "_id" : 1, "name" : "Ian Gillan", "instrument" : "Vocals" }
```

Sort with Limit

You can use `sort()` with `limit()` to sort the results of the limited result set.

Here we limit the results to 3 documents:

```
db.musicians.find( ).limit(3).sort( { name: 1, born: -1 } )
```

Result:

```
{ "_id" : 5, "name" : "Don Airey", "instrument" : "Keyboards", "born" : 1948 }
{ "_id" : 1, "name" : "Ian Gillan", "instrument" : "Vocals" }
{ "_id" : 2, "name" : "Ian Paice", "instrument" : "Drums", "born" : 1948 }
```

If we switch name to descending order:

```
db.musicians.find( ).limit(3).sort( { name: -1, born: -1 } )
```

Result:

```
{ "_id" : 8, "name" : "Stuart Chatwood", "instrument" : "Bass", "born" : 1969 }
{ "_id" : 4, "name" : "Steve Morse", "instrument" : "Guitar", "born" : 1954 }
{ "_id" : 3, "name" : "Roger Glover", "instrument" : "Bass", "born" : 1945 }
```

Note that in this case, born has no effect, as there is never more than one result for a given name. 

#### Comparing Different Types

When comparing values of different BSON types, MongoDB uses the following comparison order, from lowest to highest:

- MinKey (internal type)
- Null
- Numbers (ints, longs, doubles)
- Symbol, String
- Object
- Array
- BinData
- ObjectId
- Boolean
- Date
- Timestamp
- Regular Expression
- MaxKey (internal type)

Note that non-existent fields are treated the same as a null value (or empty BSON object).


## MongoDB - Create a Relationship

#### To create a relationship in MongoDB, either embed a BSON document within another, or reference it from another.

MongoDB databases work differently to relational databases. This is also true of relationships.

In MongoDB, you can create a relationship using one of the following two methods:

- Embedded documents. 
- Referenced documents.

The method you use will depend on the data, and how you intend to query that data.

### Embedded Relationships

With MongoDB, you can embed documents within documents. Therefore, a single document can contain its own relationships.
In fact, we already created a relationship using this method back when we first created a document.

#### One-to-One Relationship

A one-to-one relationship is where the parent document has one child, and the child has one parent.

For example, a business rule might say that an artist can only have one address and that the address can only belong to one artist.
The following code creates a one-to-one relationship, embedded within the document.

```
db.artists.insert(
    {
        _id : 2,
        artistname : "Prince",
        address :   {
                        street : "Audubon Road",
                        city : "Chanhassen",
                        state : "Minnesota",
                        country : "United States"
                    }
    }
)
```
	
Result:

```
WriteResult({ "nInserted" : 1 })
```

#### One-to-Many Relationship

A one-to-many relationship is where the parent document can have many child documents, but the child documents can only have one parent document.

So, another business rule might say that one artist can have many albums, but an album can only belong to one artist.

Running the following code will create a one-to-many relationship:

```
db.artists.insert(
    {
        _id : 3,
        artistname : "Moby",
        albums : [
                    {
                        album : "Play",
                        year : 1999,
                        genre : "Electronica"
                    }, 
                    {
                        album : "Long Ambients 1: Calm. Sleep.",
                        year : 2016,
                        genre : "Ambient"
                    }
                ]
    }
)
```

Result:

```
WriteResult({ "nInserted" : 1 })
```

### Document Referenced Relationships

You can use a document reference to create a relationship. Rather than embedding the child document into the parent document (like we did above), you separate the child document out into to its own stand alone document.

So we could do this:

#### Parent Document

```
db.artists.insert(
    {
        _id : 4,
        artistname : "Rush"
    }
)
```

#### Child Documents

We'll insert 3 child documents — one for each band member:

```
db.musicians.insert(
    {
        _id : 9,
        name : "Geddy Lee",
        instrument : [ "Bass", "Vocals", "Keyboards" ],
        artist_id : 4
    }
)
```

```
db.musicians.insert(
    {
        _id : 10,
        name : "Alex Lifeson",
        instrument : [ "Guitar", "Backing Vocals" ],
        artist_id : 4
    }
)
```

```
db.musicians.insert(
    {
        _id : 11,
        name : "Neil Peart",
        instrument : "Drums",
        artist_id : 4
    }
)
```

	
#### Querying the Relationship

After inserting the above two documents, you can use $lookup to perform a left outer join on the two collections.

This, in conjunction with the aggregate() method, and $match to specify the specific artist you're interested in, will return parent and child documents in one.

```
db.artists.aggregate([
    {
      $lookup:
        {
          from: "musicians",
          localField: "_id",
          foreignField: "artist_id",
          as: "band_members"
        }
   },
   { $match : { artistname : "Rush" } }
]).pretty()
```
	
Result:

```
{
	"_id" : 4,
	"artistname" : "Rush",
	"band_members" : [
		{
			"_id" : 9,
			"name" : "Geddy Lee",
			"instrument" : [
				"Bass",
				"Vocals",
				"Keyboards"
			],
			"artist_id" : 4
		},
		{
			"_id" : 10,
			"name" : "Alex Lifeson",
			"instrument" : [
				"Guitar",
				"Backing Vocals"
			],
			"artist_id" : 4
		},
		{
			"_id" : 11,
			"name" : "Neil Peart",
			"instrument" : "Drums",
			"artist_id" : 4
		}
	]
}
```

You can see that the first two fields are from the artists collection, and the rest of it is from the musicians collection.

So if you only query the artists collection by itself: 

```
db.artists.find( { artistname : "Rush" } )
```

You'd only get this:

```
{ "_id" : 4, "artistname" : "Rush" }
```

No related data is returned.

### When to use Embedded Documents vs Referenced Documents
Both methods of creating relationships have their pros and cons. There are times you might use embedded documents, and other times you'll use referenced documents.

### When to use Embedded Relationships

One of the main benefits of using the embedded relationship method is performance. When the relationship is embedded within the document, queries will run faster than if they were spread out over multiple documents. MongoDB only needs to return the one document, rather than joining multiple documents in order to retrieve the relationships. This can provide a major performance boost — especially when working with lots of data.

Embedded relationships also make queries easier to write. Rather than writing complex queries that join many documents via their unique identifier, you can return all related data within a single query.

Another consideration to keep in mind is that, MongoDB can only ensure atomicity at a document level. Document updates to a single document are always atomic, but not for multiple documents.

When multiple users are accessing the data, there's always a chance that two or more users will try to update the same document with different data. In this case, MongoDB will ensure that no conflict occurs and only one set of data is updated at a time. MongoDB cannot ensure this across multiple documents.
So in general, embedded relationships can be used in most cases, as long as the document remains within the size limit (16 megabytes at the time of writing), and/or its nesting limit (100 levels deep at the time of writing). 
However, embedded relationships aren't appropriate for all occasions. There may be situations where it makes more sense to create a document referenced relationship.

#### When to use Referenced Relationships
For data that needs to be repeated across many documents, it can be helpful to have them in their own separate document. This can reduce errors and help in keeping the data consistent (while bearing in mind that multiple-document updates are not atomic).
Using the above example, one musician could be a member (or ex-member) of many bands. Some might also produce albums for other artists, teach students, run clinics, etc. Also, a lot of data could be stored against each musician. So having a separate document for each musician makes sense in this case.
Also, if you think your embedded documents might exceed the file size limit imposed by MongoDB, then you'll need to store some data in separate documents.


## MongoDB - Update a Document

#### Use the update() method or save() method to update documents in MongoDB.

In MongoDB, both the `update()` method and the `save()` method can be used to update a document. 
The `update()` method updates values in an existing document or documents, while the `save()` method replaces a document with the document passed in as a parameter.

However, the `update()` method can also replace the whole document, depending on the parameter that's passed in.

### The update() Method

Here's an example of the `update()` method.

First, let's select a record to update:

```
db.musicians.find({ _id: 6 }).pretty()
```

Result:

```
{
	"_id" : 6,
	"name" : "Jeff Martin",
	"instrument" : "Vocals",
	"born" : 1969
}
```

Jeff actually does a lot more than just sing. So let's add some more instruments. We'll use the $set operator to update a single field.

```
db.musicians.update(
        { _id: 6 }, 
        { $set:{ instrument : [ "Vocals", "Guitar", "Sitar" ] } }
    )


		var exampleCode2 = CodeMirror.fromTextArea(document.getElementById("example2"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
```

Result:

```
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
```

Now if we do another query, we see that the document has been updated as specified:

```
db.musicians.find({ _id: 6 }).pretty()
```
	
Result:

```
{
	"_id" : 6,
	"name" : "Jeff Martin",
	"instrument" : [
		"Vocals",
		"Guitar",
		"Sitar"
	],
	"born" : 1969
}
```

Some more options:

- If the field does not exist, the $set operator will add a new field with the specified value, provided that the new field does not violate a type constraint.
- You can also use { upsert: true } to create a new document when no document matches the query.
- You can use { multi: true } to update multiple documents that meet the query criteria. By default, this option is set to false, so only one document is updated if you don't set it to true.

#### The save() Method

The `save()` method is a cross between `update()` and `insert()`. When you use the `save()` method, if the document exists, it will be udpated. If it doesn't exist, it will be created.

If you don't specify an `_id` field, MongoDB will create a document with an `_id` that contains a ObjectId value (as per an `insert()`).
If you specify an `_id` field, it performs an update with `{ upsert: true }`, meaning, it creates a new document if no document matches the query. 
We don't currently have any documents in our producers collection. Let's create one using the `save()` method:

```
db.producers.save({ _id: 1, name: "Bob Rock" })
```

Result:

```
WriteResult({ "nMatched" : 0, "nUpserted" : 1, "nModified" : 0, "_id" : 1 })
```

Now if we search the producers collection, we see our newly created record:

```
db.producers.find()


		var exampleCode5 = CodeMirror.fromTextArea(document.getElementById("example5"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
```

Result:

```
{ "_id" : 1, "name" : "Bob Rock" }
```


## MongoDB - Export Data

#### In MongoDB, you can export data using the mongoexport utility.

You can use the `mongoexport` utility to export data from your MongoDB database, to a JSON or CSV file.
The utility is located in the MongoDB bin directory (eg, /mongodb/bin). When you run the utility, provide the name of the database, the collection, and the file you want it to be exported to.
To export data, first open a new Terminal/Command Prompt window, then type the applicable command.
Export a Collection to a JSON File
Here, we use mongoexport to export the artists collection to a JSON file:



mongoexport --db music --collection artists --out /data/dump/music/artists.json


		var exampleCode1 = CodeMirror.fromTextArea(document.getElementById("example1"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Resulting message:

2016-07-12T09:57:37.613+0700	connected to: localhost
2016-07-12T09:57:37.614+0700	exported 13 records

Resulting file:

{"_id":{"$oid":"5780fbf948ef8c6b3ffb0149"},"artistname":"The Tea Party"}
{"_id":{"$oid":"5781c9ac48ef8c6b3ffb014a"},"artistname":"Jorn Lande"}
{"_id":1.0,"artistname":"AC/DC"}
{"_id":{"$oid":"5781d7f248ef8c6b3ffb014d"},"artistname":"The Kooks"}
{"_id":{"$oid":"5781d7f248ef8c6b3ffb014e"},"artistname":"Bastille"}
{"_id":{"$oid":"5781d7f248ef8c6b3ffb014f"},"artistname":"Gang of Four"}
{"_id":{"$oid":"5781f85d48ef8c6b3ffb0150"},"artistname":"Deep Purple","albums":[{"album":"Machine Head","year":1972.0,"genre":"Rock"},{"album":"Stormbringer","year":1974.0,"genre":"Rock"}]}
{"_id":{"$oid":"578214f048ef8c6b3ffb0159"},"artistname":"Miles Davis","albums":[{"album":"Kind of Blue","year":1959.0,"genre":"Jazz"},{"album":"Bitches Brew","year":1970.0,"genre":"Jazz"}]}
{"_id":{"$oid":"578217c248ef8c6b3ffb015a"},"artistname":"Robben Ford","albums":[{"album":"Bringing it Back Home","year":2013.0,"genre":"Blues"},{"album":"Talk to Your Daughter","year":1988.0,"genre":"Blues"}]}
{"_id":{"$oid":"578217c248ef8c6b3ffb015b"},"artistname":"Snoop Dogg","albums":[{"album":"Tha Doggfather","year":1996.0,"genre":"Rap"},{"album":"Reincarnated","year":2013.0,"genre":"Reggae"}]}
{"_id":2.0,"artistname":"Prince","address":{"street":"Audubon Road","city":"Chanhassen","state":"Minnesota","country":"United States"}}
{"_id":3.0,"artistname":"Moby","albums":[{"album":"Play","year":1999.0,"genre":"Electronica"},{"album":"Long Ambients 1: Calm. Sleep.","year":2016.0,"genre":"Ambient"}]}
{"_id":4.0,"artistname":"Rush"}


If you find that you can't run mongoexport, be sure that you've either exited the mongo utility, or opened a new Terminal/Command Prompt window before running mongoexport, as it is a separate utility.


The above command assumes that the MongoDB bin directory is in your PATH. If it's not, you will need to use the full path to the mongoexport file. For example, /mongodb/bin/mongoexport or wherever your MongoDB deployment is installed.


If you don't provide a file path for the exported file, it will be created wherever you are located when you run the command. Either provide the full path, or navigate to where you'd like the data file to be written before you run the command.

Export a Collection to a CSV File
To export to a CSV file, add --type=csv to the command.
You must also specify the fields in the MongoDB documents to export.
Here, we use mongoexport to export the artists collection to a CSV file. We export the _id and artistname fields. We've also given the file name a .csv extension.

mongoexport --db music --collection artists --type=csv --fields _id,artistname --out /data/dump/music/artists.csv


		var exampleCode2 = CodeMirror.fromTextArea(document.getElementById("example2"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Resulting message:

2016-07-12T10:16:33.111+0700	connected to: localhost
2016-07-12T10:16:33.114+0700	exported 13 records

Resulting CSV file:

_id,artistname
ObjectId(5780fbf948ef8c6b3ffb0149),The Tea Party
ObjectId(5781c9ac48ef8c6b3ffb014a),Jorn Lande
1,AC/DC
ObjectId(5781d7f248ef8c6b3ffb014d),The Kooks
ObjectId(5781d7f248ef8c6b3ffb014e),Bastille
ObjectId(5781d7f248ef8c6b3ffb014f),Gang of Four
ObjectId(5781f85d48ef8c6b3ffb0150),Deep Purple
ObjectId(578214f048ef8c6b3ffb0159),Miles Davis
ObjectId(578217c248ef8c6b3ffb015a),Robben Ford
ObjectId(578217c248ef8c6b3ffb015b),Snoop Dogg
2,Prince
3,Moby
4,Rush

Export the results of a Query
You can use the --query option to specify a query to export. The query must be enclosed in single quotes.
Here, we export details on Miles Davis to a JSON file:

mongoexport --db music --collection artists --query '{"artistname": "Miles Davis"}' --out /data/dump/music/miles_davis.json


		var exampleCode3 = CodeMirror.fromTextArea(document.getElementById("example3"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Resulting message:

2016-07-12T10:32:19.794+0700	connected to: localhost
2016-07-12T10:32:19.795+0700	exported 1 record

Resulting JSON file:

{"_id":{"$oid":"578214f048ef8c6b3ffb0159"},"artistname":"Miles Davis","albums":[{"album":"Kind of Blue","year":1959.0,"genre":"Jazz"},{"album":"Bitches Brew","year":1970.0,"genre":"Jazz"}]}

Other Options
The mongoexport utility provides a number of options. Here are some potentially useful ones.
The --limit Option
Limits the number of documents in the export.

mongoexport --db music --collection artists --limit 3 --out /data/dump/music/3_artists.json


		var exampleCode4 = CodeMirror.fromTextArea(document.getElementById("example4"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Resulting file:

{"_id":{"$oid":"5780fbf948ef8c6b3ffb0149"},"artistname":"The Tea Party"}
{"_id":{"$oid":"5781c9ac48ef8c6b3ffb014a"},"artistname":"Jorn Lande"}
{"_id":1.0,"artistname":"AC/DC"}

The --sort Option
Specifies how the results are ordered.
Here, we sort the file by the _id field in ascending order (i.e. 1). To make it descending, use a -1.

mongoexport --db music --collection artists --limit 3 --sort '{_id: 1}' --out /data/dump/music/3_artists_sorted.json


		var exampleCode5 = CodeMirror.fromTextArea(document.getElementById("example5"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Resulting file:

{"_id":1.0,"artistname":"AC/DC"}
{"_id":2.0,"artistname":"Prince","address":{"street":"Audubon Road","city":"Chanhassen","state":"Minnesota","country":"United States"}}
{"_id":3.0,"artistname":"Moby","albums":[{"album":"Play","year":1999.0,"genre":"Electronica"},{"album":"Long Ambients 1: Calm. Sleep.","year":2016.0,"genre":"Ambient"}]}

The --skip Option
Allows you to instruct mongoexport to skip a number of documents before starting the export operation.

mongoexport --db music --collection artists --limit 3 --sort '{_id: 1}' --skip 2 --out /data/dump/music/3_artists_sorted_skipped.json


		var exampleCode6 = CodeMirror.fromTextArea(document.getElementById("example6"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Resulting file:

{"_id":3.0,"artistname":"Moby","albums":[{"album":"Play","year":1999.0,"genre":"Electronica"},{"album":"Long Ambients 1: Calm. Sleep.","year":2016.0,"genre":"Ambient"}]}
{"_id":4.0,"artistname":"Rush"}
{"_id":{"$oid":"5780fbf948ef8c6b3ffb0149"},"artistname":"The Tea Party"}

The --pretty Option
Outputs documents in a more readable JSON format.

mongoexport --db music --collection artists --query '{"artistname": "Miles Davis"}' --pretty --out /data/dump/music/miles_davis_pretty.json


		var exampleCode7 = CodeMirror.fromTextArea(document.getElementById("example7"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Resulting file:

{
	"_id": {
		"$oid": "578214f048ef8c6b3ffb0159"
	},
	"artistname": "Miles Davis",
	"albums": [
		{
			"album": "Kind of Blue",
			"year": 1959.0,
			"genre": "Jazz"
		},
		{
			"album": "Bitches Brew",
			"year": 1970.0,
			"genre": "Jazz"
		}
	]
}


 Update a Document
Delete a Document 


		@media screen and (max-width: 575px) {
			.ad .responsive-bottom {
				width: 320px;
			}
		}	
	





		(adsbygoogle = window.adsbygoogle || []).push({});
		


MongoDB - Delete a Document

		@media screen and (max-width: 575px) {
			.responsive-top {
				width: 320px;
			}
			.responsive-top {
				height: 100px;
			}
		}
	





		(adsbygoogle = window.adsbygoogle || []).push({});
		


 Export Data
Drop a Collection 

In MongoDB, you can delete documents using one of three methods.
MongoDB provides three methods for deleting documents:

db.collection.deleteOne()
db.collection.deleteMany()
db.collection.remove()

The db.collection.deleteOne() Method
The db.collection.deleteOne() deletes only one document, even if more than one document matches the criteria.
Here's an example of the db.collection.deleteOne() method to delete a single document.
First, let's run a query that returns multiple results:



db.artists.find( { artistname: { $in: [ "The Kooks", "Gang of Four", "Bastille" ] } } )


		var exampleCode1 = CodeMirror.fromTextArea(document.getElementById("example1"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Results:

{ "_id" : ObjectId("5781d7f248ef8c6b3ffb014d"), "artistname" : "The Kooks" }
{ "_id" : ObjectId("5781d7f248ef8c6b3ffb014e"), "artistname" : "Bastille" }
{ "_id" : ObjectId("5781d7f248ef8c6b3ffb014f"), "artistname" : "Gang of Four" }

OK, so we know there are three documents that match that criteria.
Now let's use the exact same filtering criteria for our db.collection.deleteOne() method:

db.artists.deleteOne( { artistname: { $in: [ "The Kooks", "Gang of Four", "Bastille" ] } } )


		var exampleCode2 = CodeMirror.fromTextArea(document.getElementById("example2"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Resulting message:

{ "acknowledged" : true, "deletedCount" : 1 }

So only one document was deleted, even though three documents matched the criteria.
Let's run the find() query again to see which documents remain:

db.artists.find( { artistname: { $in: [ "The Kooks", "Gang of Four", "Bastille" ] } } )


		var exampleCode3 = CodeMirror.fromTextArea(document.getElementById("example3"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Results:

{ "_id" : ObjectId("5781d7f248ef8c6b3ffb014e"), "artistname" : "Bastille" }
{ "_id" : ObjectId("5781d7f248ef8c6b3ffb014f"), "artistname" : "Gang of Four" }

The db.collection.deleteMany() Method
The db.collection.deleteMany() method deletes all documents that match the criteria.
So let's run the db.collection.deleteMany() method with the exact same criteria as our previous example. Remember, two records remain. Let's see if db.collection.deleteMany() deletes both:

db.artists.deleteMany( { artistname: { $in: [ "The Kooks", "Gang of Four", "Bastille" ] } } )


		var exampleCode4 = CodeMirror.fromTextArea(document.getElementById("example4"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Resulting message:

{ "acknowledged" : true, "deletedCount" : 2 }

So the remaining two records were deleted.
The db.collection.remove() Method
The db.collection.remove() method deletes a single document or all documents that match the specified criteria.
Here, we delete all documents where the artist name is "AC/DC". 

db.artists.remove( { artistname: "AC/DC" } )


		var exampleCode5 = CodeMirror.fromTextArea(document.getElementById("example5"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Results:

WriteResult({ "nRemoved" : 1 })

In this case, there's only one AC/DC :)
The justOne Option
You can use the justOne parameter to limit the remove operation to just one document (just like using db.collection.deleteOne()).
Here's an example.
First, let's run a query that returns multiple documents:

db.musicians.find( { born: { $lt: 1950 } } )


		var exampleCode6 = CodeMirror.fromTextArea(document.getElementById("example6"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Results:

{ "_id" : 2, "name" : "Ian Paice", "instrument" : "Drums", "born" : 1948 }
{ "_id" : 3, "name" : "Roger Glover", "instrument" : "Bass", "born" : 1945 }
{ "_id" : 5, "name" : "Don Airey", "instrument" : "Keyboards", "born" : 1948 }

Now we'll delete one of those records using the justOne option. Again, we'll use the exact same filtering criteria:

db.musicians.remove( { born: { $lt: 1950 } }, { justOne: 1 } )


		var exampleCode7 = CodeMirror.fromTextArea(document.getElementById("example7"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Resulting message:

WriteResult({ "nRemoved" : 1 })

Now let's run the same query to see which documents are remaining: 

db.musicians.find( { born: { $lt: 1950 } } )


		var exampleCode8 = CodeMirror.fromTextArea(document.getElementById("example8"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Results:

{ "_id" : 3, "name" : "Roger Glover", "instrument" : "Bass", "born" : 1945 }
{ "_id" : 5, "name" : "Don Airey", "instrument" : "Keyboards", "born" : 1948 }

Delete all Documents in a Collection
You can delete all documents in a collection simply by omitting any filtering criteria.
Let's delete all documents in the artists collection:

db.artists.remove( {} )


		var exampleCode9 = CodeMirror.fromTextArea(document.getElementById("example9"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Resulting message:

WriteResult({ "nRemoved" : 8 })


If you receive a Error: remove needs a query error, check that you haven't forgotten to include the curly braces. You still need to include these.


 Export Data
Drop a Collection 


		@media screen and (max-width: 575px) {
			.ad .responsive-bottom {
				width: 320px;
			}
		}	
	





		(adsbygoogle = window.adsbygoogle || []).push({});
		


MongoDB - Drop a Collection

		@media screen and (max-width: 575px) {
			.responsive-top {
				width: 320px;
			}
			.responsive-top {
				height: 100px;
			}
		}
	





		(adsbygoogle = window.adsbygoogle || []).push({});
		


 Delete a Document
Import Data 

To drop a collection in MongoDB, use the db.collection.drop() method.
In MongoDB, the db.collection.drop() method removes the collection from the database. If the collection exists, it will return true, if it doesn't exist, it will return false.
Drop a Collection that Exists
Here, we'll use db.collection.drop() to drop a collection that exists.
First, let's quickly check to see which collections we have in our music database:



show collections


		var exampleCode1 = CodeMirror.fromTextArea(document.getElementById("example1"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Results:

artists
musicians
producers

OK, so we'll delete the artists collection.

db.artists.drop()


		var exampleCode2 = CodeMirror.fromTextArea(document.getElementById("example2"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Resulting message:

true

So the collection was dropped. We can take another quick look to see which collections we have now:

show collections


		var exampleCode3 = CodeMirror.fromTextArea(document.getElementById("example3"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Results:

musicians
producers


Note that the db.collection.drop() method doesn't accept any parameters. Just run it as specified above. 

Attempt to Drop a Collection that doesn't Exist
So now that there's no longer an artists collection in our database, let's try to drop it and see what message we get:

db.artists.drop()


		var exampleCode4 = CodeMirror.fromTextArea(document.getElementById("example4"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Resulting message:

false

It returned false because the collection doesn't exist.

 Delete a Document
Import Data 


		@media screen and (max-width: 575px) {
			.ad .responsive-bottom {
				width: 320px;
			}
		}	
	





		(adsbygoogle = window.adsbygoogle || []).push({});
		


MongoDB - Import Data

		@media screen and (max-width: 575px) {
			.responsive-top {
				width: 320px;
			}
			.responsive-top {
				height: 100px;
			}
		}
	





		(adsbygoogle = window.adsbygoogle || []).push({});
		


 Drop a Collection
Create a Backup 

Use the mongoimport utility to import data into a MongoDB database.
MongoDB provides the mongoimport utility that can be used to import JSON, CSV, or TSV files into a MongoDB database.
mongoimport is located in the bin directory (eg, /mongodb/bin or wherever you installed it). 
To import data, open a new Terminal/Command Prompt window and enter mongoimport followed by parameters such as database name, collection name, source file name, etc.

If you find that you can't run mongoimport, be sure that you've either exited the mongo utility, or opened a new Terminal/Command Prompt window before running mongoexport, as it is a separate utility.

Import JSON File
Here's an example of running mongoimport to import a JSON file.
You might remember that we previously used mongoexport to export the artists collection to a JSON file.
We later dropped the artists collection altogether. 
Now, we'll import that collection back into our database.



mongoimport --db music --file /data/dump/music/artists.json


		var exampleCode1 = CodeMirror.fromTextArea(document.getElementById("example1"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Resulting message:

2016-07-12T13:34:04.904+0700	no collection specified
2016-07-12T13:34:04.905+0700	using filename 'artists' as collection
2016-07-12T13:34:04.911+0700	connected to: localhost
2016-07-12T13:34:04.968+0700	imported 13 documents


If you don't specify a collection name, a collection is created based on the name of the file (minus any extension).

Now, let's switch back to our mongo Terminal/Command Prompt window and retrieve the list of collections in our database:

show collections


		var exampleCode2 = CodeMirror.fromTextArea(document.getElementById("example2"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Result:

artists
musicians
producers

Now we'll query our revived collection.

db.artists.find()


		var exampleCode3 = CodeMirror.fromTextArea(document.getElementById("example3"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Result:

{ "_id" : 1, "artistname" : "AC/DC" }
{ "_id" : ObjectId("5781d7f248ef8c6b3ffb014d"), "artistname" : "The Kooks" }
{ "_id" : ObjectId("5780fbf948ef8c6b3ffb0149"), "artistname" : "The Tea Party" }
{ "_id" : ObjectId("5781d7f248ef8c6b3ffb014f"), "artistname" : "Gang of Four" }
{ "_id" : ObjectId("5781d7f248ef8c6b3ffb014e"), "artistname" : "Bastille" }
{ "_id" : ObjectId("5781c9ac48ef8c6b3ffb014a"), "artistname" : "Jorn Lande" }
{ "_id" : ObjectId("5781f85d48ef8c6b3ffb0150"), "artistname" : "Deep Purple", "albums" : [ { "album" : "Machine Head", "year" : 1972, "genre" : "Rock" }, { "album" : "Stormbringer", "year" : 1974, "genre" : "Rock" } ] }
{ "_id" : ObjectId("578214f048ef8c6b3ffb0159"), "artistname" : "Miles Davis", "albums" : [ { "album" : "Kind of Blue", "year" : 1959, "genre" : "Jazz" }, { "album" : "Bitches Brew", "year" : 1970, "genre" : "Jazz" } ] }
{ "_id" : ObjectId("578217c248ef8c6b3ffb015a"), "artistname" : "Robben Ford", "albums" : [ { "album" : "Bringing it Back Home", "year" : 2013, "genre" : "Blues" }, { "album" : "Talk to Your Daughter", "year" : 1988, "genre" : "Blues" } ] }
{ "_id" : 2, "artistname" : "Prince", "address" : { "street" : "Audubon Road", "city" : "Chanhassen", "state" : "Minnesota", "country" : "United States" } }
{ "_id" : 4, "artistname" : "Rush" }
{ "_id" : 3, "artistname" : "Moby", "albums" : [ { "album" : "Play", "year" : 1999, "genre" : "Electronica" }, { "album" : "Long Ambients 1: Calm. Sleep.", "year" : 2016, "genre" : "Ambient" } ] }
{ "_id" : ObjectId("578217c248ef8c6b3ffb015b"), "artistname" : "Snoop Dogg", "albums" : [ { "album" : "Tha Doggfather", "year" : 1996, "genre" : "Rap" }, { "album" : "Reincarnated", "year" : 2013, "genre" : "Reggae" } ] }

Specify a Collection Name
You can use the --collection argument to provide a name of the collection that the data should go into.
Let's import another file, but this time, specify a collection name:

mongoimport --db music --collection jazz --file /data/dump/music/miles_davis.json


		var exampleCode4 = CodeMirror.fromTextArea(document.getElementById("example4"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Resulting message:

2016-07-12T14:09:01.793+0700	connected to: localhost
2016-07-12T14:09:01.849+0700	imported 1 document

Now switch back to mongo and check the list of collections:

show collections


		var exampleCode5 = CodeMirror.fromTextArea(document.getElementById("example5"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Resulting message:

artists
jazz
musicians
producers

And finally, query the jazz collection:

db.jazz.find().pretty()


		var exampleCode6 = CodeMirror.fromTextArea(document.getElementById("example6"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Resulting message:

{
	"_id" : ObjectId("578214f048ef8c6b3ffb0159"),
	"artistname" : "Miles Davis",
	"albums" : [
		{
			"album" : "Kind of Blue",
			"year" : 1959,
			"genre" : "Jazz"
		},
		{
			"album" : "Bitches Brew",
			"year" : 1970,
			"genre" : "Jazz"
		}
	]
}

Import CSV File
You can import a CSV file by using --type csv.
If the CSV file has a header row, use --headerline to tell mongoimport to use the first line to determine the name of the fields in the resulting document.
If the CSV file doesn't have a header row, use the --fields parameter to set the field names.
With Header Row
Here's an example of importing a document with a header row.
The contents of the CSV file:

_id,albumname,artistname
1,Killers,"Iron Maiden"
2,Powerslave,"Iron Maiden"
12,"Somewhere in Time","Iron Maiden"
3,"Surfing with the Alien","Joe Satriani"
10,"Flying in a Blue Dream","Joe Satriani"
11,"Black Swans and Wormhole Wizards","Joe Satriani"
6,"Out of the Loop","Mr Percival"
7,"Suck on This",Primus
8,"Pork Soda",Primus
9,"Sailing the Seas of Cheese",Primus

Import the file:

mongoimport --db music --collection catalog --type csv --headerline --file /data/dump/music/catalog.csv


		var exampleCode7 = CodeMirror.fromTextArea(document.getElementById("example7"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Query the collection:

> db.catalog.find()
{ "_id" : 2, "albumname" : "Powerslave", "artistname" : "Iron Maiden" }
{ "_id" : 1, "albumname" : "Killers", "artistname" : "Iron Maiden" }
{ "_id" : 3, "albumname" : "Surfing with the Alien", "artistname" : "Joe Satriani" }
{ "_id" : 12, "albumname" : "Somewhere in Time", "artistname" : "Iron Maiden" }
{ "_id" : 10, "albumname" : "Flying in a Blue Dream", "artistname" : "Joe Satriani" }
{ "_id" : 6, "albumname" : "Out of the Loop", "artistname" : "Mr Percival" }
{ "_id" : 7, "albumname" : "Suck on This", "artistname" : "Primus" }
{ "_id" : 8, "albumname" : "Pork Soda", "artistname" : "Primus" }
{ "_id" : 11, "albumname" : "Black Swans and Wormhole Wizards", "artistname" : "Joe Satriani" }
{ "_id" : 9, "albumname" : "Sailing the Seas of Cheese", "artistname" : "Primus" }

Without Header Row
Here's another CSV file, but this one doesn't have a header row:

Mutt Lange, 1948
John Petrucci, 1967
DJ Shadow, 1972
George Clinton, 1941

Now we'll import it and specify the field names to use:

mongoimport --db music --collection producers --type csv --fields name,born --file /data/dump/music/producers.csv


		var exampleCode8 = CodeMirror.fromTextArea(document.getElementById("example8"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Query the collection:

> db.producers.find()
{ "_id" : 1, "name" : "Bob Rock" }
{ "_id" : ObjectId("5784a3a5dfad478c015f6b72"), "name" : "John Petrucci", "born" : 1967 }
{ "_id" : ObjectId("5784a3a5dfad478c015f6b73"), "name" : "Mutt Lange", "born" : 1948 }
{ "_id" : ObjectId("5784a3a5dfad478c015f6b74"), "name" : "George Clinton", "born" : 1941 }
{ "_id" : ObjectId("5784a3a5dfad478c015f6b75"), "name" : "DJ Shadow", "born" : 1972 }

You'll see that the ObjectId field has been automatically created and populated for us. 
Also, we already had one document in this collection before we ran the import: { "_id" : 1, "name" : "Bob Rock" }. Therefore, you can see that the import has simply added to the collection (as opposed to replacing it and all its contents).

You can use the same method to import TSV files. Simply use --type tsv.


 Drop a Collection
Create a Backup 


		@media screen and (max-width: 575px) {
			.ad .responsive-bottom {
				width: 320px;
			}
		}	
	





		(adsbygoogle = window.adsbygoogle || []).push({});
		


MongoDB - Create a Backup

		@media screen and (max-width: 575px) {
			.responsive-top {
				width: 320px;
			}
			.responsive-top {
				height: 100px;
			}
		}
	





		(adsbygoogle = window.adsbygoogle || []).push({});
		


 Import Data
Drop a Database 

To create a backup in MongoDB, either copy the files directly, or use one of several backup/management tools.
There are several ways to backup a MongoDB database:

Copy the data files
Use mongodump
Use MongoDB Cloud Manager
Use Ops Manager

Copy the Data Files
You can copy the underlying data files that MongoDB uses to store data. These are located in the data directory.
The default location of the data directory is /data/db, however, if you use a different location you will need to use that instead.
You should copy the whole directory for a complete backup.
You can also use snapshots if the volume supports it. For example, on Linux, use LVM (Logical Volume Manager) to create a snapshot, then you can copy from that snapshot to your backup site/remote location.
Use mongodump
You can use mongodump to backup the data and mongorestore to restore it.
To quickly backup all contents of the running server, open a new Terminal/Command Prompt, change to a directory that you want the /dump folder to be created in, and type the following:



mongodump


		var exampleCode1 = CodeMirror.fromTextArea(document.getElementById("example1"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	

You will need provide the full path if the MongoDB bin directory is not in your PATH.


If you find that you can't run mongodump, be sure that you've either exited the mongo utility, or opened a new Terminal/Command Prompt window before running mongodump, as it is a separate utility.

Resulting message:

2016-07-12T15:44:34.467+0700	writing music.artists to 
2016-07-12T15:44:34.467+0700	writing music.musicians to 
2016-07-12T15:44:34.467+0700	writing music.catalog to 
2016-07-12T15:44:34.468+0700	done dumping music.artists (13 documents)
2016-07-12T15:44:34.469+0700	done dumping music.musicians (10 documents)
2016-07-12T15:44:34.469+0700	done dumping music.catalog (10 documents)
2016-07-12T15:44:34.470+0700	writing music.producers to 
2016-07-12T15:44:34.470+0700	writing music.jazz to 
2016-07-12T15:44:34.470+0700	done dumping music.producers (5 documents)
2016-07-12T15:44:34.470+0700	done dumping music.jazz (1 document)
2016-07-12T15:44:34.534+0700	writing test.restaurants to 
2016-07-12T15:44:34.705+0700	done dumping test.restaurants (25359 documents)

And here's what that looks like on my Mac's Finder:

As you can see, it has created a folder called dump, then a folder for each database, then dumped all collections and their metadata into the respective database folder. I've expanded the music database folder to show the files within that directory.

Note that mongodump overwrites output files if they exist in the backup data folder, so be sure to move or rename any files you need to keep before running mongodump again.

Backup a Single Database
You can backup a single database by specifying the name of the database in the --db parameter:

mongodump --db=music


		var exampleCode2 = CodeMirror.fromTextArea(document.getElementById("example2"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Backup a Single Collection
You can backup a single collection by specifying the name of the collection in the --collection parameter:

mongodump --db=music --collection=artists


		var exampleCode3 = CodeMirror.fromTextArea(document.getElementById("example3"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Specify a Backup Location
Use the --out parameter to specify the directory that you'd like the backup to be written to:

mongodump --db music --out /data/backups


		var exampleCode4 = CodeMirror.fromTextArea(document.getElementById("example4"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
More Options
mongodump has many more options for specifying how the data is backed up. You can always run mongodump --help to see which options are available.
Restoring a mongodump Backup
You can restore any mongodump  backup by running mongorestore. which works in a similar way to mongodump.
See mongorestore --help for more info.

mongodump and mongorestore are mainly intended for smaller deployments, and for partial backup and restores based on a query, syncing from production to staging or development environments, or changing the storage engine of a standalone.
For larger systems, or sharded clusters, or replica sets, use a more robust backup system, such MongoDB Cloud Manager or Ops Manager.

MongoDB Cloud Manager
MongoDB Cloud Manager is a hosted platform for managing MongoDB.
You can use MongoDB Cloud Manager to continually back up MongoDB replica sets and sharded clusters by reading the oplog data from your MongoDB deployment.
MongoDB Cloud Manager works on a subscription basis. More info here.
Ops Manager
Ops Manager is like MongoDB Cloud Manager, except it is installed on your local environment (i.e. not in the cloud). So you can use it for monitoring, automating, and backup up your MongoDB deployment.
Ops Manager is available to MongoDB Subscribers. 

 Import Data
Drop a Database 


		@media screen and (max-width: 575px) {
			.ad .responsive-bottom {
				width: 320px;
			}
		}	
	





		(adsbygoogle = window.adsbygoogle || []).push({});
		


MongoDB - Drop a Database

		@media screen and (max-width: 575px) {
			.responsive-top {
				width: 320px;
			}
			.responsive-top {
				height: 100px;
			}
		}
	





		(adsbygoogle = window.adsbygoogle || []).push({});
		


 Create a Backup
Database Tutorials 

To drop a collection in MongoDB, use either the db.dropDatabase() method, or the dropDatabase command.
In MongoDB, you can drop a database by switching to that database and running either the db.dropDatabase() method or the dropDatabase command.
The db.dropDatabase() Method
Here, we'll use db.dropDatabase() method to drop the current database.
First, let's check our list of databases:

> show databases
local  0.000GB
music  0.000GB
test   0.005GB

Check out list of databases again:

> show databases
local  0.000GB
test   0.005GB

The music database is no longer with us.
The dropDatabase Command
You can also use the dropDatabase command to do the same thing. 



use test
db.runCommand( { dropDatabase: 1 } )


		var exampleCode1 = CodeMirror.fromTextArea(document.getElementById("example1"), {
				mode: "text/javascript",
				tabMode: "indent",
				styleActiveLine: false,
				lineNumbers: false,
				lineWrapping: true,
				theme: "q-dark"
		});
	
Resulting message:

{ "dropped" : "test", "ok" : 1 }

And our list of databases has shrunk again:

> show databases
local  0.000GB


 Create a Backup
Database Tutorials 


		@media screen and (max-width: 575px) {
			.ad .responsive-bottom {
				width: 320px;
			}
		}	
	





		(adsbygoogle = window.adsbygoogle || []).push({});
		

