# MongoDB - Data Modelling
Source: https://www.tutorialspoint.com/mongodb/

Data in MongoDB has a flexible schema.documents in the same collection do not need to have the same set of fields or structure, and common fields in a collectionâ€™s documents may hold different types of data.

## Some considerations while designing schema in MongoDB

*   Design your schema according to user requirements.

*   Combine objects into one document if you will use them together. Otherwise separate them (but make sure there should not be need of joins).

*   Duplicate the data (but limited) because disk space is cheap as compare to compute time.

*   Do joins while write, not on read.

*   Optimize your schema for most frequent use cases.

*   Do complex aggregation in the schema

## Example

Suppose a client needs a database design for his blog website and see the differences between RDBMS and MongoDB schema design. Website has the following requirements.

*   Every post has the unique title, description and url.

*   Every post can have one or more tags.

*   Every post has the name of its publisher and total number of likes.

*   Every Post have comments given by users along with their name, message, data-time and likes.

*   On each post there can be zero or more comments.

In RDBMS schema design for above requirements will have minimum three tables.

![RDBMS Schema Design](https://d3vv6lp55qjaqc.cloudfront.net/items/3H043U2P190O1x2a1V1i/rdbms.png?X-CloudApp-Visitor-Id=1094421)

While in MongoDB schema design will have one collection post and has the following structure:

```
{
   _id: POST_ID
   title: TITLE_OF_POST, 
   description: POST_DESCRIPTION,
   by: POST_BY,
   url: URL_OF_POST,
   tags: [TAG1, TAG2, TAG3],
   likes: TOTAL_LIKES, 
   comments: [	
      {
         user:'COMMENT_BY',
         message: TEXT,
         dateCreated: DATE_TIME,
         like: LIKES 
      },
      {
         user:'COMMENT_BY',
         message: TEXT,
         dateCreated: DATE_TIME,
         like: LIKES
      }
   ]
}
```

So while showing the data, in RDBMS you need to join three tables and in mongodb data will be shown from one collection only.



# MongoDB - Create Database

## The use Command

MongoDB **use DATABASE_NAME** is used to create database. The command will create a new database, if it doesn't exist otherwise it will return the existing database.

### Syntax:

Basic syntax of **use DATABASE** statement is as follows:


```
use DATABASE_NAME
```

### Example:

If you want to create a database with name **<mydb>**, then **use DATABASE** statement would be as follows:

```
>use mydb
switched to db mydb
```

To check your currently selected database use the command **db**

```
>db
mydb
```

If you want to check your databases list, then use the command **show dbs**.

```

>show dbs
local     0.78125GB
test      0.23012GB
```

Your created database (mydb) is not present in list. To display database you need to insert atleast one document into it.

```
>db.movie.insert({"name":"tutorials point"})
>show dbs
local      0.78125GB
mydb       0.23012GB
test       0.23012GB
```

In mongodb default database is test. If you didn't create any database then collections will be stored in test database.



# MongoDB - Drop Database


## The dropDatabase() Method

MongoDB **db.dropDatabase()** command is used to drop a existing database.

### Syntax:

Basic syntax of **dropDatabase()** command is as follows:

```
db.dropDatabase()
```

This will delete the selected database. If you have not selected any database, then it will delete default 'test' database

### Example:

First, check the list available databases by using the command **show dbs**

```
>show dbs
local      0.78125GB
mydb       0.23012GB
test       0.23012GB
>
```

If you want to delete new database **<mydb>**, then **dropDatabase()** command would be as follows:

```
>use mydb
switched to db mydb
>db.dropDatabase()
>{ "dropped" : "mydb", "ok" : 1 }
>
```

Now check list of databases

```
>show dbs
local      0.78125GB
test       0.23012GB
>
```



# MongoDB - Create Collection

## The createCollection() Method

MongoDB **db.createCollection(name, options)** is used to create collection.

### Syntax:

Basic syntax of **createCollection()** command is as follows

```
db.createCollection(name, options)
```

In the command, **name** is name of collection to be created. **Options** is a document and used to specify configuration of collection

<table class="table table-bordered">

<tbody>

<tr>

<th style="width:25%;">Parameter</th>

<th style="width:25%;">Type</th>

<th>Description</th>

</tr>

<tr>

<td>Name</td>

<td>String</td>

<td>Name of the collection to be created</td>

</tr>

<tr>

<td>Options</td>

<td>Document</td>

<td>(Optional) Specify options about memory size and indexing</td>

</tr>

</tbody>

</table>

Options parameter is optional, so you need to specify only name of the collection. Following is the list of options you can use:

<table class="table table-bordered">

<tbody>

<tr>

<th style="width:15%;">Field</th>

<th style="width:15%;">Type</th>

<th>Description</th>

</tr>

<tr>

<td>capped</td>

<td>Boolean</td>

<td>(Optional) If true, enables a capped collection. Capped collection is a collection fixed size collecction that automatically overwrites its oldest entries when it reaches its maximum size. **If you specify true, you need to specify size parameter also.**</td>

</tr>

<tr>

<td>autoIndexID</td>

<td>Boolean</td>

<td>(Optional) If true, automatically create index on _id field.s Default value is false.</td>

</tr>

<tr>

<td>size</td>

<td>number</td>

<td>(Optional) Specifies a maximum size in bytes for a capped collection. If **If capped is true, then you need to specify this field also.**</td>

</tr>

<tr>

<td>max</td>

<td>number</td>

<td>(Optional) Specifies the maximum number of documents allowed in the capped collection.</td>

</tr>

</tbody>

</table>

While inserting the document, MongoDB first checks size field of capped collection, then it checks max field.

### Examples:

Basic syntax of **createCollection()** method without options is as follows

```
>use test
switched to db test
>db.createCollection("mycollection")
{ "ok" : 1 }
>
```

You can check the created collection by using the command **show collections**

```
>show collections
mycollection
system.indexes
```

Following example shows the syntax of **createCollection()** method with few important options:

```
>db.createCollection("mycol", { capped : true, autoIndexID : true, size : 6142800, max : 10000 } )
{ "ok" : 1 }
>
```

In mongodb you don't need to create collection. MongoDB creates collection automatically, when you insert some document.

```
>db.tutorialspoint.insert({"name" : "tutorialspoint"})
>show collections
mycol
mycollection
system.indexes
tutorialspoint
>
```

# MongoDB - Drop Collection

## The drop() Method

MongoDB's **db.collection.drop()** is used to drop a collection from the database.

### Syntax:

Basic syntax of **drop()** command is as follows

```
db.COLLECTION_NAME.drop()
```

### Example:

First, check the available collections into your database **mydb**

```
>use mydb
switched to db mydb
>show collections
mycol
mycollection
system.indexes
tutorialspoint
>
```

Now drop the collection with the name **mycollection**

```
>db.mycollection.drop()
true
>
```

Again check the list of collections into database

```
>show collections
mycol
system.indexes
tutorialspoint
>
```

drop() method will return true, if the selected collection is dropped successfully otherwise it will return false

# MongoDB - Datatypes

MongoDB supports many datatypes whose list is given below:

*   **String** : This is most commonly used datatype to store the data. String in mongodb must be UTF-8 valid.

*   **Integer** : This type is used to store a numerical value. Integer can be 32 bit or 64 bit depending upon your server.

*   **Boolean** : This type is used to store a boolean (true/ false) value.

*   **Double** : This type is used to store floating point values.

*   **Min/ Max keys** : This type is used to compare a value against the lowest and highest BSON elements.

*   **Arrays** : This type is used to store arrays or list or multiple values into one key.

*   **Timestamp** : ctimestamp. This can be handy for recording when a document has been modified or added.

*   **Object** : This datatype is used for embedded documents.

*   **Null** : This type is used to store a Null value.

*   **Symbol** : This datatype is used identically to a string however, it's generally reserved for languages that use a specific symbol type.

*   **Date** : This datatype is used to store the current date or time in UNIX time format. You can specify your own date time by creating object of Date and passing day, month, year into it.

*   **Object ID** : This datatype is used to store the documentâ€™s ID.

*   **Binary data** : This datatype is used to store binay data.

*   **Code** : This datatype is used to store javascript code into document.

*   **Regular expression** : This datatype is used to store regular expression



# MongoDB - Insert Document

## The insert() Method

To insert data into MongoDB collection, you need to use MongoDB's **insert()** or **save()**method.

### Syntax

Basic syntax of **insert()** command is as follows âˆ’

```
>db.COLLECTION_NAME.insert(document)
```

### Example

```>db.mycol.insert({
   _id: ObjectId(7df78ad8902c),
   title: 'MongoDB Overview', 
   description: 'MongoDB is no sql database',
   by: 'tutorials point',
   url: 'http://www.tutorialspoint.com',
   tags: ['mongodb', 'database', 'NoSQL'],
   likes: 100
})
```

Here **mycol** is our collection name, as created in previous tutorial. If the collection doesn't exist in the database, then MongoDB will create this collection and then insert document into it.

In the inserted document if we don't specify the _id parameter, then MongoDB assigns an unique ObjectId for this document.

_id is 12 bytes hexadecimal number unique for every document in a collection. 12 bytes are divided as follows âˆ’

```
_id: ObjectId(4 bytes timestamp, 3 bytes machine id, 2 bytes process id, 3 bytes incrementer)
```

To insert multiple documents in single query, you can pass an array of documents in insert() command.

### Example

```
>db.post.insert([
   {
      title: 'MongoDB Overview', 
      description: 'MongoDB is no sql database',
      by: 'tutorials point',
      url: 'http://www.tutorialspoint.com',
      tags: ['mongodb', 'database', 'NoSQL'],
      likes: 100
   },

   {
      title: 'NoSQL Database', 
      description: "NoSQL database doesn't have tables",
      by: 'tutorials point',
      url: 'http://www.tutorialspoint.com',
      tags: ['mongodb', 'database', 'NoSQL'],
      likes: 20, 
      comments: [ 
         {
            user:'user1',
            message: 'My first comment',
            dateCreated: new Date(2013,11,10,2,35),
            like: 0 
         }
      ]
   }
])
```

To insert the document you can use **db.post.save(document)** also. If you don't specify **_id** in the document then **save()** method will work same as **insert()** method. If you specify _id then it will replace whole data of document containing _id as specified in save() method.

# MongoDB - Query Document

## The find() Method

To query data from MongoDB collection, you need to use MongoDB's **find()** method.

### Syntax

Basic syntax of **find()** method is as follows

```
>db.COLLECTION_NAME.find()
```

**find()**method will display all the documents in a non structured way.

## The pretty() Method

To display the results in a formatted way, you can use **pretty()** method.

### Syntax

```
>db.mycol.find().pretty()
```

## Example

```
>db.mycol.find().pretty()
{
   "_id": ObjectId(7df78ad8902c),
   "title": "MongoDB Overview", 
   "description": "MongoDB is no sql database",
   "by": "tutorials point",
   "url": "http://www.tutorialspoint.com",
   "tags": ["mongodb", "database", "NoSQL"],
   "likes": "100"
}
>
```

Apart from find() method there is **findOne()** method, that returns only one document.

## RDBMS Where Clause Equivalents in MongoDB

To query the document on the basis of some condition, you can use following operations

<table class="table table-bordered">

<tbody>

<tr>

<th>Operation</th>

<th>Syntax</th>

<th>Example</th>

<th style="width:35%;">RDBMS Equivalent</th>

</tr>

<tr>

<td>Equality</td>

<td>{<key>:<value>}</td>

<td>db.mycol.find({"by":"tutorials point"}).pretty()</td>

<td>where by = 'tutorials point'</td>

</tr>

<tr>

<td>Less Than</td>

<td>{<key>:{$lt:<value>}}</td>

<td>db.mycol.find({"likes":{$lt:50}}).pretty()</td>

<td>where likes < 50</td>

</tr>

<tr>

<td style="width:35%;">Less Than Equals</td>

<td>{<key>:{$lte:<value>}}</td>

<td>db.mycol.find({"likes":{$lte:50}}).pretty()</td>

<td>where likes <= 50</td>

</tr>

<tr>

<td>Greater Than</td>

<td>{<key>:{$gt:<value>}}</td>

<td>db.mycol.find({"likes":{$gt:50}}).pretty()</td>

<td>where likes > 50</td>

</tr>

<tr>

<td>Greater Than Equals</td>

<td>{<key>:{$gte:<value>}}</td>

<td>db.mycol.find({"likes":{$gte:50}}).pretty()</td>

<td>where likes >= 50</td>

</tr>

<tr>

<td>Not Equals</td>

<td>{<key>:{$ne:<value>}}</td>

<td>db.mycol.find({"likes":{$ne:50}}).pretty()</td>

<td>where likes != 50</td>

</tr>

</tbody>

</table>

## AND in MongoDB

### Syntax

In the **find()** method if you pass multiple keys by separating them by ',' then MongoDB treats it **AND** condition. Basic syntax of **AND** is shown below âˆ’

```
>db.mycol.find({key1:value1, key2:value2}).pretty()
```

### Example

Below given example will show all the tutorials written by 'tutorials point' and whose title is 'MongoDB Overview'

```
>db.mycol.find({"by":"tutorials point","title": "MongoDB Overview"}).pretty()
{
   "_id": ObjectId(7df78ad8902c),
   "title": "MongoDB Overview", 
   "description": "MongoDB is no sql database",
   "by": "tutorials point",
   "url": "http://www.tutorialspoint.com",
   "tags": ["mongodb", "database", "NoSQL"],
   "likes": "100"
}
>
```

For the above given example equivalent where clause will be ` where by='tutorials point' AND title = 'MongoDB Overview' ` You can pass any number of key, value pairs in find clause.

## OR in MongoDB

### Syntax

To query documents based on the OR condition, you need to use **$or** keyword. Basic syntax of **OR** is shown below âˆ’

```
>db.mycol.find(
   {
      $or: [
         {key1: value1}, {key2:value2}
      ]
   }
).pretty()
```

### Example

Below given example will show all the tutorials written by 'tutorials point' or whose title is 'MongoDB Overview'

```
>db.mycol.find({$or:[{"by":"tutorials point"},{"title": "MongoDB Overview"}]}).pretty()
{
   "_id": ObjectId(7df78ad8902c),
   "title": "MongoDB Overview", 
   "description": "MongoDB is no sql database",
   "by": "tutorials point",
   "url": "http://www.tutorialspoint.com",
   "tags": ["mongodb", "database", "NoSQL"],
   "likes": "100"
}
>
```

## Using AND and OR together

### Example

Below given example will show the documents that have likes greater than 100 and whose title is either 'MongoDB Overview' or by is 'tutorials point'. Equivalent sql where clause is **'where likes>10 AND (by = 'tutorials point' OR title = 'MongoDB Overview')'**

```
>db.mycol.find({"likes": {$gt:10}, $or: [{"by": "tutorials point"},
   {"title": "MongoDB Overview"}]}).pretty()
{
   "_id": ObjectId(7df78ad8902c),
   "title": "MongoDB Overview", 
   "description": "MongoDB is no sql database",
   "by": "tutorials point",
   "url": "http://www.tutorialspoint.com",
   "tags": ["mongodb", "database", "NoSQL"],
   "likes": "100"
}
>
```

# MongoDB - Update Document


MongoDB's **update()** and **save()** methods are used to update document into a collection. The update() method update values in the existing document while the save() method replaces the existing document with the document passed in save() method.

## MongoDB Update() method

The update() method updates values in the existing document.

### Syntax

Basic syntax of **update()** method is as follows

```
>db.COLLECTION_NAME.update(SELECTIOIN_CRITERIA, UPDATED_DATA)
```

### Example

Consider the mycol collection has following data.

```json 
{ "_id" : ObjectId(5983548781331adf45ec5), "title":"MongoDB Overview"}
{ "_id" : ObjectId(5983548781331adf45ec6), "title":"NoSQL Overview"}
{ "_id" : ObjectId(5983548781331adf45ec7), "title":"Tutorials Point Overview"}
```

Following example will set the new title 'New MongoDB Tutorial' of the documents whose title is 'MongoDB Overview'

```
>db.mycol.update({'title':'MongoDB Overview'},{$set:{'title':'New MongoDB Tutorial'}})
>db.mycol.find()
{ "_id" : ObjectId(5983548781331adf45ec5), "title":"New MongoDB Tutorial"}
{ "_id" : ObjectId(5983548781331adf45ec6), "title":"NoSQL Overview"}
{ "_id" : ObjectId(5983548781331adf45ec7), "title":"Tutorials Point Overview"}
>
```

By default mongodb will update only single document, to update multiple you need to set a paramter 'multi' to true.

```
>db.mycol.update({'title':'MongoDB Overview'},
   {$set:{'title':'New MongoDB Tutorial'}},{multi:true})
```

## MongoDB Save() Method

The **save()** method replaces the existing document with the new document passed in save() method

### Syntax

Basic syntax of mongodb **save()** method is shown below âˆ’

```
>db.COLLECTION_NAME.save({_id:ObjectId(),NEW_DATA})
```

### Example

Following example will replace the document with the _id '5983548781331adf45ec7'

```
>db.mycol.save(
   {
      "_id" : ObjectId(5983548781331adf45ec7), "title":"Tutorials Point Overview",
         "by":"Tutorials Point"
   }
)
>db.mycol.find()
{ "_id" : ObjectId(5983548781331adf45ec5), "title":"Tutorials Point New Topic",
   "by":"Tutorials Point"}
{ "_id" : ObjectId(5983548781331adf45ec6), "title":"NoSQL Overview"}
{ "_id" : ObjectId(5983548781331adf45ec7), "title":"Tutorials Point Overview"}
>
```



# MongoDB - Delete Document

## The remove() Method

MongoDB's **remove()** method is used to remove document from the collection. remove() method accepts two parameters. One is deletion criteria and second is justOne flag

1.  **deletion criteria :** (Optional) deletion criteria according to documents will be removed.

2.  **justOne :** (Optional) if set to true or 1, then remove only one document.

### Syntax:

Basic syntax of **remove()** method is as follows

```
>db.COLLECTION_NAME.remove(DELLETION_CRITTERIA)
```

### Example

Consider the mycol collectioin has following data.

```json 
{"_id" : ObjectId(5983548781331adf45ec5), "title":"MongoDB Overview"}
{ "_id" : ObjectId(5983548781331adf45ec6), "title":"NoSQL Overview"}
{ "_id" : ObjectId(5983548781331adf45ec7), "title":"Tutorials Point Overview"}
```

Following example will remove all the documents whose title is 'MongoDB Overview'

```
>db.mycol.remove({'title':'MongoDB Overview'})
>db.mycol.find()
{ "_id" : ObjectId(5983548781331adf45ec6), "title":"NoSQL Overview"}
{ "_id" : ObjectId(5983548781331adf45ec7), "title":"Tutorials Point Overview"}
>
```

## Remove only one

If there are multiple records and you want to delete only first record, then set **justOne** parameter in **remove()** method

```>db.COLLECTION_NAME.remove(DELETION_CRITERIA,1)
```

## Remove All documents

If you don't specify deletion criteria, then mongodb will delete whole documents from the collection. **This is equivalent of SQL's truncate command.**

```>db.mycol.remove({})
>db.mycol.find()
>
```



# MongoDB - Projection

In mongodb projection meaning is selecting only necessary data rather than selecting whole of the data of a document. If a document has 5 fields and you need to show only 3, then select only 3 fields from them.

## The find() Method

MongoDB's **find()** method, explained in [MongoDB Query Document](http://www.tutorialspoint.com/mongodb/mongodb_query_document.htm) accepts second optional parameter that is list of fields that you want to retrieve. In MongoDB when you execute **find()** method, then it displays all fields of a document. To limit this you need to set list of fields with value 1 or 0\. 1 is used to show the field while 0 is used to hide the field.

### Syntax:

Basic syntax of **find()** method with projection is as follows

```
>db.COLLECTION_NAME.find({},{KEY:1})
```

### Example

Consider the collection mycol has the following data

```json "_id" : ObjectId(5983548781331adf45ec5), "title":"MongoDB Overview"}
{ "_id" : ObjectId(5983548781331adf45ec6), "title":"NoSQL Overview"}
{ "_id" : ObjectId(5983548781331adf45ec7), "title":"Tutorials Point Overview"}
```

Following example will display the title of the document while quering the document.

```>db.mycol.find({},{"title":1,_id:0})
{"title":"MongoDB Overview"}
{"title":"NoSQL Overview"}
{"title":"Tutorials Point Overview"}
>
```

Please note **_id** field is always displayed while executing **find()** method, if you don't want this field, then you need to set it as 0



# MongoDB - Limit Records


## The Limit() Method

To limit the records in MongoDB, you need to use **limit()** method. **limit()** method accepts one number type argument, which is number of documents that you want to displayed.

### Syntax:

Basic syntax of **limit()** method is as follows

```
>db.COLLECTION_NAME.find().limit(NUMBER)
```

### Example

Consider the collection myycol has the following data

```json 
{"_id" : ObjectId(5983548781331adf45ec5), "title":"MongoDB Overview"}
{ "_id" : ObjectId(5983548781331adf45ec6), "title":"NoSQL Overview"}
{ "_id" : ObjectId(5983548781331adf45ec7), "title":"Tutorials Point Overview"}
```

Following example will display only 2 documents while quering the document.

```
>db.mycol.find({},{"title":1,_id:0}).limit(2)
{"title":"MongoDB Overview"}
{"title":"NoSQL Overview"}
>
```

If you don't specify number argument in **limit()** method then it will display all documents from the collection.

## MongoDB Skip() Method

Apart from limit() method there is one more method **skip()** which also accepts number type argument and used to skip number of documents.

### Syntax:

Basic syntax of **skip()** method is as follows

```>db.COLLECTION_NAME.find().limit(NUMBER).skip(NUMBER)
```

### Example:

Following example will only display only second document.

```
>db.mycol.find({},{"title":1,_id:0}).limit(1).skip(1)
{"title":"NoSQL Overview"}
>
```

Please note default value in **skip()** method is 0



# MongoDB - Sort Records



## The sort() Method

To sort documents in MongoDB, you need to use **sort()** method. **sort()** method accepts a document containing list of fields along with their sorting order. To specify sorting order 1 and -1 are used. 1 is used for ascending order while -1 is used for descending order.

### Syntax:

Basic syntax of **sort()** method is as follows

```
>db.COLLECTION_NAME.find().sort({KEY:1})
```

### Example

Consider the collection myycol has the following data

```json 
{"_id" : ObjectId(5983548781331adf45ec5), "title":"MongoDB Overview"}
{ "_id" : ObjectId(5983548781331adf45ec6), "title":"NoSQL Overview"}
{ "_id" : ObjectId(5983548781331adf45ec7), "title":"Tutorials Point Overview"}
```

Following example will display the documents sorted by title in descending order.

```>db.mycol.find({},{"title":1,_id:0}).sort({"title":-1})
{"title":"Tutorials Point Overview"}
{"title":"NoSQL Overview"}
{"title":"MongoDB Overview"}
>
```

Please note if you don't specify the sorting preference, then **sort()** method will display documents in ascending order.



# MongoDB - Indexing


Indexes support the efficient resolution of queries. Without indexes, MongoDB must scan every document of a collection to select those documents that match the query statement. This scan is highly inefficient and require the mongodb to process a large volume of data.

Indexes are special data structures, that store a small portion of the data set in an easy to traverse form. The index stores the value of a specific field or set of fields, ordered by the value of the field as specified in index.

## The ensureIndex() Method

To create an index you need to use ensureIndex() method of mongodb.

### Syntax:

Basic syntax of **ensureIndex()** method is as follows()

```
>db.COLLECTION_NAME.ensureIndex({KEY:1})
```

Here key is the name of field on which you want to create index and 1 is for ascending order. To create index in descending order you need to use -1.

### Example

```
>db.mycol.ensureIndex({"title":1})
>
```

In **ensureIndex()** method you can pass multiple fields, to create index on multiple fields.

```
>db.mycol.ensureIndex({"title":1,"description":-1})
>
```

**ensureIndex()** method also accepts list of options (which are optional), whose list is given below:

<table class="table table-bordered">

<tbody>

<tr>

<th style="width:10%;">Parameter</th>

<th style="width:10%;">Type</th>

<th>Description</th>

</tr>

<tr>

<td>background</td>

<td>Boolean</td>

<td>Builds the index in the background so that building an index does not block other database activities. Specify true to build in the background. The default value is **false**.</td>

</tr>

<tr>

<td>unique</td>

<td>Boolean</td>

<td>Creates a unique index so that the collection will not accept insertion of documents where the index key or keys match an existing value in the index. Specify true to create a unique index. The default value is **false**.</td>

</tr>

<tr>

<td>name</td>

<td>string</td>

<td>The name of the index. If unspecified, MongoDB generates an index name by concatenating the names of the indexed fields and the sort order.</td>

</tr>

<tr>

<td>dropDups</td>

<td>Boolean</td>

<td>Creates a unique index on a field that may have duplicates. MongoDB indexes only the first occurrence of a key and removes all documents from the collection that contain subsequent occurrences of that key. Specify true to create unique index. The default value is **false**.</td>

</tr>

<tr>

<td>sparse</td>

<td>Boolean</td>

<td>If true, the index only references documents with the specified field. These indexes use less space but behave differently in some situations (particularly sorts). The default value is **false**.</td>

</tr>

<tr>

<td>expireAfterSeconds</td>

<td>integer</td>

<td>Specifies a value, in seconds, as a TTL to control how long MongoDB retains documents in this collection.</td>

</tr>

<tr>

<td>v</td>

<td>index version</td>

<td>The index version number. The default index version depends on the version of mongodb running when creating the index.</td>

</tr>

<tr>

<td>weights</td>

<td>document</td>

<td>The weight is a number ranging from 1 to 99,999 and denotes the significance of the field relative to the other indexed fields in terms of the score.</td>

</tr>

<tr>

<td>default_language</td>

<td>string</td>

<td>For a text index, the language that determines the list of stop words and the rules for the stemmer and tokenizer. The default value is **english**.</td>

</tr>

<tr>

<td>language_override</td>

<td>string</td>

<td>For a text index, specify the name of the field in the document that contains, the language to override the default language. The default value is language.</td>

</tr>

</tbody>

</table>



# MongoDB - Aggregation



Aggregations operations process data records and return computed results. Aggregation operations group values from multiple documents together, and can perform a variety of operations on the grouped data to return a single result. In sql count(*) and with group by is an equivalent of mongodb aggregation.

## The aggregate() Method

For the aggregation in mongodb you should use **aggregate()** method.

### Syntax:

Basic syntax of **aggregate()** method is as follows

```>db.COLLECTION_NAME.aggregate(AGGREGATE_OPERATION)
```

### Example:

In the collection you have the following data:

```json
{
   _id: ObjectId(7df78ad8902c)
   title: 'MongoDB Overview', 
   description: 'MongoDB is no sql database',
   by_user: 'tutorials point',
   url: 'http://www.tutorialspoint.com',
   tags: ['mongodb', 'database', 'NoSQL'],
   likes: 100
},
{
   _id: ObjectId(7df78ad8902d)
   title: 'NoSQL Overview', 
   description: 'No sql database is very fast',
   by_user: 'tutorials point',
   url: 'http://www.tutorialspoint.com',
   tags: ['mongodb', 'database', 'NoSQL'],
   likes: 10
},
{
   _id: ObjectId(7df78ad8902e)
   title: 'Neo4j Overview', 
   description: 'Neo4j is no sql database',
   by_user: 'Neo4j',
   url: 'http://www.neo4j.com',
   tags: ['neo4j', 'database', 'NoSQL'],
   likes: 750
},
```

Now from the above collection if you want to display a list that how many tutorials are written by each user then you will use **aggregate()** method as shown below:

```
> db.mycol.aggregate([{$group : {_id : "$by_user", num_tutorial : {$sum : 1}}}])
{
   "result" : [
      {
         "_id" : "tutorials point",
         "num_tutorial" : 2
      },
      {
         "_id" : "Neo4j",
         "num_tutorial" : 1
      }
   ],
   "ok" : 1
}
>
```

Sql equivalent query for the above use case will be **select by_user, count(*) from mycol group by by_user**

In the above example we have grouped documents by field **by_user** and on each occurance of by_user previous value of sum is incremented. There is a list available aggregation expressions.

<table class="table table-bordered">

<tbody>

<tr>

<th style="width:10%;">Expression</th>

<th style="width:50%">Description</th>

<th>Example</th>

</tr>

<tr>

<td>$sum</td>

<td>Sums up the defined value from all documents in the collection.</td>

<td>db.mycol.aggregate([{$group : {_id : "$by_user", num_tutorial : {$sum : "$likes"}}}])</td>

</tr>

<tr>

<td>$avg</td>

<td>Calculates the average of all given values from all documents in the collection.</td>

<td>db.mycol.aggregate([{$group : {_id : "$by_user", num_tutorial : {$avg : "$likes"}}}])</td>

</tr>

<tr>

<td>$min</td>

<td>Gets the minimum of the corresponding values from all documents in the collection.</td>

<td>db.mycol.aggregate([{$group : {_id : "$by_user", num_tutorial : {$min : "$likes"}}}])</td>

</tr>

<tr>

<td>$max</td>

<td>Gets the maximum of the corresponding values from all documents in the collection.</td>

<td>db.mycol.aggregate([{$group : {_id : "$by_user", num_tutorial : {$max : "$likes"}}}])</td>

</tr>

<tr>

<td>$push</td>

<td>Inserts the value to an array in the resulting document.</td>

<td>db.mycol.aggregate([{$group : {_id : "$by_user", url : {$push: "$url"}}}])</td>

</tr>

<tr>

<td>$addToSet</td>

<td>Inserts the value to an array in the resulting document but does not create duplicates.</td>

<td>db.mycol.aggregate([{$group : {_id : "$by_user", url : {$addToSet : "$url"}}}])</td>

</tr>

<tr>

<td>$first</td>

<td>Gets the first document from the source documents according to the grouping. Typically this makes only sense together with some previously applied â€œ$sortâ€-stage.</td>

<td>db.mycol.aggregate([{$group : {_id : "$by_user", first_url : {$first : "$url"}}}])</td>

</tr>

<tr>

<td>$last</td>

<td>Gets the last document from the source documents according to the grouping. Typically this makes only sense together with some previously applied â€œ$sortâ€-stage.</td>

<td>db.mycol.aggregate([{$group : {_id : "$by_user", last_url : {$last : "$url"}}}])</td>

</tr>

</tbody>

</table>

## Pipeline Concept

In UNIX command shell pipeline means the possibility to execute an operation on some input and use the output as the input for the next command and so on. MongoDB also support same concept in aggregation framework. There is a set of possible stages and each of those is taken a set of documents as an input and is producing a resulting set of documents (or the final resulting JSON document at the end of the pipeline). This can then in turn again be used for the next stage an so on.

Possible stages in aggregation framework are following:

*   **$project:** Used to select some specific fields from a collection.
*   **$match:** This is a filtering operation and thus this can reduce the amount of documents that are given as input to the next stage.
*   **$group:** This does the actual aggregation as discussed above.
*   **$sort:** Sorts the documents.
*   **$skip:** With this it is possible to skip forward in the list of documents for a given amount of documents.
*   **$limit:** This limits the amount of documents to look at by the given number starting from the current position.s
*   **$unwind:** This is used to unwind document that are using arrays. when using an array the data is kind of pre-joinded and this operation will be undone with this to have individual documents again. Thus with this stage we will increase the amount of documents for the next stage.



# MongoDB - Replication



Replication is the process of synchronizing data across multiple servers. Replication provides redundancy and increases data availability with multiple copies of data on different database servers, replication protects a database from the loss of a single server. Replication also allows you to recover from hardware failure and service interruptions. With additional copies of the data, you can dedicate one to disaster recovery, reporting, or backup.

## Why Replication?

*   To keep your data safe
*   High (24*7) availability of data
*   Disaster Recovery
*   No downtime for maintenance (like backups, index rebuilds, compaction)
*   Read scaling (extra copies to read from)
*   Replica set is transparent to the application

## How replication works in MongoDB

MongoDB achieves replication by the use of replica set. A replica set is a group of **mongod** instances that host the same data set. In a replica one node is primary node that receives all write operations. All other instances, secondaries, apply operations from the primary so that they have the same data set. Replica set can have only one primary node.

1.  Replica set is a group of two or more nodes (generally minimum 3 nodes are required).
2.  In a replica set one node is primary node and remaining nodes are secondary.
3.  All data replicates from primary to secondary node.
4.  At the time of automatic failover or maintenance, election establishes for primary and a new primary node is elected.
5.  After the recovery of failed node, it again join the replica set and works as a secondary node.

A typical diagram of mongodb replication is shown in which client application always interact with primary node and primary node then replicate the data to the secondary nodes.

![MongoDB Replication](/mongodb/images/replication.png)

## Replica set features

*   A cluster of N nodess
*   Anyone node can be primary
*   All write operations goes to primary
*   Automatic failover
*   Automatic Recovery
*   Consensus election of primary

## Set up a replica set

In this tutorial we will convert standalone mongod instance to a replica set. To convert to replica set follow the below given steps:

*   Shutdown already running mongodb server.

Now start the mongodb server by specifying **--replSet** option. Basic syntax of **--replSet** is given below:

```mongod 
--port "PORT" --dbpath "YOUR_DB_DATA_PATH" --replSet "REPLICA_SET_INSTANCE_NAME"
```

### Example

```mongod 
--port 27017 --dbpath "D:\set up\mongodb\data" --replSet rs0
```

It will start a mongod instance with the name rs0, on port 27017\. Now start the command prompt and connect to this mongod instance. In mongo client issue the command **rs.initiate()** to initiate a new replica set. To check the replica set configuration issue the command **rs.conf()**. To check the status of replica sete issue the command **rs.status()**.

## Add members to replica set

To add members to replica set, start mongod instances on multiple machines. Now start a mongo client and issue a command **rs.add()**.

### Syntax:

Basic syntax of **rs.add()** command is as follows:

```
>rs.add(HOST_NAME:PORT)
```

### Example

Suppose your mongod instance name is **mongod1.net** and it is running on port **27017**. To add this instance to replica set issue the command **rs.add()** in mongo client.

```
>rs.add("mongod1.net:27017")
>
```

You can add mongod instance to replica set only when you are connected to primary node. To check whether you are connected to primary or not issue the command **db.isMaster()** in mongo client.



# MongoDB - Sharding



## Sharding

Sharding is the process of storing data records across multiple machines and it is MongoDB's approach to meeting the demands of data growth. As the size of the data increases, a single machine may not be sufficient to store the data nor provide an acceptable read and write throughput. Sharding solves the problem with horizontal scaling. With sharding, you add more machines to support data growth and the demands of read and write operations.

## Why Sharding?

*   In replication all writes go to master node

*   Latency sensitive queries still go to master

*   Single replica set has limitation of 12 nodes

*   Memory can't be large enough when active dataset is big

*   Local Disk is not big enough

*   Vertical scaling is too expensive

## Sharding in MongoDB

Below given diagram shows the sharding in MongoDB using sharded cluster.

![MongoDB Sharding](https://d3vv6lp55qjaqc.cloudfront.net/items/1S0545331B112c2E0X3v/sharding.png?X-CloudApp-Visitor-Id=1094421)

In the above given diagram there are three main components which are described below:

*   **Shards:** Shards are used to store data. They provide high availability and data consistency. In production environment each shard is a separate replica set.

*   **Config Servers:** Config servers store the cluster's metadata. This data contains a mapping of the cluster's data set to the shards. The query router uses this metadata to target operations to specific shards. In production environment sharded clusters have exactly 3 config servers.

*   **Query Routers:** Query Routers are basically mongos instances, interface with client applications and direct operations to the appropriate shard. The query router processes and targets operations to shards and then returns results to the clients. A sharded cluster can contain more than one query router to divide the client request load. A client sends requests to one query router. Generally a sharded cluster have many query routers.



# MongoDB - Create Backup



## Dump MongoDB Data

To create backup of database in mongodb you should use **mongodump** command. This command will dump all data of your server into dump directory. There are many options available by which you can limit the amount of data or create backup of your remote server.

### Syntax:

Basic syntax of **mongodump** command is as follows


```
>mongodump
```

### Example

Start your mongod server. Assuming that your mongod server is running on localhost and port 27017\. Now open a command prompt and go to bin directory of your mongodb instance and type the command **mongodump**

Consider the mycol collection has following data.

```
>mongodump
```

The command will connect to the server running at **127.0.0.1** and port **27017** and back all data of the server to directory **/bin/dump/**. Output of the command is shown below:

![DB Stats](https://d3vv6lp55qjaqc.cloudfront.net/items/2F2d2V3s3X312Q3h0g2a/mongodump.png?X-CloudApp-Visitor-Id=1094421)

There are a list of available options that can be used with the **mongodump** command.

This command will backup only specified database at specified path

<table class="src">

<tbody>

<tr>

<th style="width:40%">Syntax</th>

<th style="width:30%">Description</th>

<th>Example</th>

</tr>

<tr>

<td>mongodump --host HOST_NAME --port PORT_NUMBER</td>

<td>This commmand will backup all databases of specified mongod instance.</td>

<td>mongodump --host tutorialspoint.com --port 27017</td>

</tr>

<tr>

<td>mongodump --dbpath DB_PATH --out BACKUP_DIRECTORY</td>

<td>mongodump --dbpath /data/db/ --out /data/backup/</td>

</tr>

<tr>

<td>mongodump --collection COLLECTION --db DB_NAME</td>

<td>This command will backup only specified collection of specified database.</td>

<td>mongodump --collection mycol --db test</td>

</tr>

</tbody>

</table>

## Restore data

To restore backup data mongodb's **mongorestore** command is used. This command restore all of the data from the back up directory.

### Syntax

Basic syntax of **mongorestore** command is

```
>mongorestore
```

Output of the command is shown below:

![DB Stats](https://d3vv6lp55qjaqc.cloudfront.net/items/2l0i39353t2T1K323Z11/mongorestore.png?X-CloudApp-Visitor-Id=1094421)



# MongoDB - PHP



To use mongodb with php you need to use mongodb php driver. Download the driver from the url [Download PHP Driver](https://s3.amazonaws.com/drivers.mongodb.org/php/index.html). Make sure to download latest release of it. Now unzip the archive and put php_mongo.dll in your PHP extension directory ("ext" by default) and add the following line to your php.ini file âˆ’

```php
extension = php_mongo.dll
```

## Make a connection and Select a database

To make a connection, you need to specify database name, if database doesn't exist then mongodb creates it automatically.

Code snippets to connect to database would be as follows âˆ’

```php
<?php
   // connect to mongodb
   $m = new MongoClient();

   echo "Connection to database successfully";
   // select a database
   $db = $m->mydb;

   echo "Database mydb selected";
?>
```

When program is executed, it will produce the following result âˆ’

```
Connection to database successfully
Database mydb selected
```

## Create a collection

Code snippets to create a collection would be as follows âˆ’

```php
<?php
   // connect to mongodb
   $m = new MongoClient();
   echo "Connection to database successfully";

   // select a database
   $db = $m->mydb;
   echo "Database mydb selected";
   $collection = $db->createCollection("mycol");
   echo "Collection created succsessfully";
?>
```

When program is executed, it will produce the following result âˆ’

```
Connection to database successfully
Database mydb selected
Collection created succsessfully
```

## Insert a document

To insert a document into mongodb, **insert()** method is used.

Code snippets to insert a documents âˆ’

```php
<?php
   // connect to mongodb
   $m = new MongoClient();
   echo "Connection to database successfully";

   // select a database
   $db = $m->mydb;
   echo "Database mydb selected";
   $collection = $db->mycol;
   echo "Collection selected succsessfully";

   $document = array( 
      "title" => "MongoDB", 
      "description" => "database", 
      "likes" => 100,
      "url" => "http://www.tutorialspoint.com/mongodb/",
      "by", "tutorials point"
   );

   $collection->insert($document);
   echo "Document inserted successfully";
?>
```

When program is executed, it will produce the following result âˆ’

```php
Connection to database successfully
Database mydb selected
Collection selected succsessfully
Document inserted successfully
```

## Find all documents

To select all documents from the collection, find() method is used.

Code snippets to select all documents âˆ’

```php
<?php
   // connect to mongodb
   $m = new MongoClient();
   echo "Connection to database successfully";

   // select a database
   $db = $m->mydb;
   echo "Database mydb selected";
   $collection = $db->mycol;
   echo "Collection selected succsessfully";

   $cursor = $collection->find();
   // iterate cursor to display title of documents

   foreach ($cursor as $document) {
      echo $document["title"] . "\n";
   }
?>
```

When program is executed, it will produce the following result âˆ’

```
Connection to database successfully
Database mydb selected
Collection selected succsessfully
{
   "title": "MongoDB"
}
```

## Update a document

To update a document , you need to use update() method.

In the below given example we will update the title of inserted document to **MongoDB Tutorial**. Code snippets to update a document âˆ’

```php
<?php
   // connect to mongodb
   $m = new MongoClient();
   echo "Connection to database successfully";

   // select a database
   $db = $m->mydb;
   echo "Database mydb selected";
   $collection = $db->mycol;
   echo "Collection selected succsessfully";

   // now update the document
   $collection->update(array("title"=>"MongoDB"), 
      array('$set'=>array("title"=>"MongoDB Tutorial")));
   echo "Document updated successfully";

   // now display the updated document
   $cursor = $collection->find();

   // iterate cursor to display title of documents
   echo "Updated document";

   foreach ($cursor as $document) {
      echo $document["title"] . "\n";
   }
?>
```

When program is executed, it will produce the following result âˆ’

```
Connection to database successfully
Database mydb selected
Collection selected succsessfully
Document updated successfully
Updated document
{
   "title": "MongoDB Tutorial"
}
```

## Delete a document

To delete a document , you need to use remove() method.

In the below given example we will remove the documents that has title **MongoDB Tutorial**. Code snippets to delete document âˆ’

```php
<?php
   // connect to mongodb
   $m = new MongoClient();
   echo "Connection to database successfully";

   // select a database
   $db = $m->mydb;
   echo "Database mydb selected";
   $collection = $db->mycol;
   echo "Collection selected succsessfully";

   // now remove the document
   $collection->remove(array("title"=>"MongoDB Tutorial"),false);
   echo "Documents deleted successfully";

   // now display the available documents
   $cursor = $collection->find();

   // iterate cursor to display title of documents
   echo "Updated document";

   foreach ($cursor as $document) {
      echo $document["title"] . "\n";
   }
?>
```

When program is executed, it will produce the following result âˆ’

```
Connection to database successfully
Database mydb selected
Collection selected succsessfully
Documents deleted successfully
```

In the above given example second parameter is boolean type and used for **justOne** field of **remove()** method.

Remaining mongodb methods **findOne(), save(), limit(), skip(), sort()** etc works same as explained in above tutorial.

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>
