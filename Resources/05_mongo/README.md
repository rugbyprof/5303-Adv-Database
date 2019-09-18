## Create a Collection

### Choose a DB

```
use music
```

However, the database isn't actually created until you insert data into it:

```
db.artists.insert({ artistname: "The Tea Party" })
```

```
show databases
```

### Create a collection

#### On the fly

```
db.artists.insert({ artistname: "The Tea Party" })
```

#### Explicitly
```
db.createCollection("producers")
```

## Create a Document

### Create A Document

#### The insert() Method

```
db.artists.insert({ artistname: "Jorn Lande" })
```

#### The Mongo ID

The `_id` that MongoDB provides is a 12-byte ObjectId value. It is made up of the following values;

- a 4-byte value representing the seconds since the Unix epoch,
- a 3-byte machine identifier,
- a 2-byte process id, and
- a 3-byte counter, starting with a random value.

#### Create Multiple Documents

```
db.artists.insert(
   [
     { artistname: "The Kooks" },
     { artistname: "Bastille" },
     { artistname: "Gang of Four" }
   ]
)
```

#### Embedded Documents

A document can contain other documents, arrays, and arrays of documents.

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

#### The insertOne() Method

```
db.musicians.insertOne({ _id: 1, name: "Ian Gillan", instrument: "Vocals" })
```

#### Embedded Documents

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

#### The insertMany() Method

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

#### Embedded Documents

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
## Query a Collection

#### Return all Documents

```
db.musicians.find()
```

#### Add Filtering Criteria

```
db.artists.find({ artistname : "Deep Purple" })
```

#### Format the Results

```
db.artists.find({ artistname : "Deep Purple" }).pretty()
```

#### More Filtering Options


**AND Conditions**

```
db.musicians.find( { instrument: "Drums", born: { $lt: 1950 } } )

```

#### OR Conditions

```
db.musicians.find(
   {
     $or: [ { instrument: "Drums" }, { born: { $lt: 1950 } } ]
   }
)
```

#### The $in Operator

```
db.musicians.find( { instrument: { $in: [ "Vocals", "Guitar" ] } } )
```

#### Query an Array of Documents

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

## Projection Queries


#### Without

```
db.musicians.find( { instrument: "Vocals"} )
```

#### With

```
db.musicians.find( { instrument: "Vocals" }, { name: 1 } )
```

#### Mixing Inclusions and Exclusions

**Error**
```
db.musicians.find( { instrument: "Vocals" }, { name: 1, born: 0 } )
```

**Allowed**
```
db.musicians.find( { instrument: "Vocals" }, { _id: 0, instrument: 0 } )
```

## Limit the Results of a Query

#### Without Limit

```
db.artists.find( { albums: { $exists: false }} )
```

#### With Limit

```
db.artists.find( { albums: { $exists: false }} ).limit(3)
```

#### skip() Method

```
db.artists.find( { albums: { $exists: false }} ).limit(3).skip(1)
```


```
db.artists.find( { albums: { $exists: false }} ).skip(3)
```

## Sort the Results of a Query

#### Without Sort

```
db.musicians.find( )
```

#### With sort() in Ascending Order

```
db.musicians.find( ).sort( { name: 1 } )
```

#### With sort() in Descending Order

```
db.musicians.find( ).sort( { name: -1 } )
```

#### Multiple Fields

```
db.musicians.find( ).sort( { instrument: 1, born: 1 } )
```

```
db.musicians.find( ).sort( { instrument: 1, born: -1 } )
```

#### Sort with Limits

```
db.musicians.find( ).limit(3).sort( { name: 1, born: -1 } )
```

**If we switch name to descending order**
```
db.musicians.find( ).limit(3).sort( { name: -1, born: -1 } )
```

## Create a Relationship

- Embedded documents.
- Referenced documents.

### Embedded documents

#### One-to-One Relationship

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

#### One-to-Many Relationship

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

### Referenced Documents

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

```
db.musicians.insert(
    {
        _id : 9,
        name : "Geddy Lee",
        instrument : [ "Bass", "Vocals", "Keyboards" ],
        artist_id : 4
    }
)

db.musicians.insert(
    {
        _id : 10,
        name : "Alex Lifeson",
        instrument : [ "Guitar", "Backing Vocals" ],
        artist_id : 4
    }
)

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

- `$lookup` = left outer join :\


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
### When to use Embedded Documents vs Referenced Documents

#### When to use Embedded Relationships

- One of the main benefits of using the embedded relationship method is performance. When the relationship is embedded within the document, queries will run faster than if they were spread out over multiple documents. MongoDB only needs to return the one document, rather than joining multiple documents in order to retrieve the relationships. This can provide a major performance boost — especially when working with lots of data.

- Embedded relationships also make queries easier to write. Rather than writing complex queries that join many documents via their unique identifier, you can return all related data within a single query.

- Another consideration to keep in mind is that, MongoDB can only ensure atomicity at a document level. Document updates to a single document are always atomic, but not for multiple documents.

- When multiple users are accessing the data, there's always a chance that two or more users will try to update the same document with different data. In this case, MongoDB will ensure that no conflict occurs and only one set of data is updated at a time. MongoDB cannot ensure this across multiple documents.

- So in general, embedded relationships can be used in most cases, as long as the document remains within the size limit (16 megabytes at the time of writing), and/or its nesting limit (100 levels deep at the time of writing).

- However, embedded relationships aren't appropriate for all occasions. There may be situations where it makes more sense to create a document referenced relationship.

#### When to use Referenced Relationships

- For data that needs to be repeated across many documents, it can be helpful to have them in their own separate document. This can reduce errors and help in keeping the data consistent (while bearing in mind that multiple-document updates are not atomic).

- Using the above example, one musician could be a member (or ex-member) of many bands. Some might also produce albums for other artists, teach students, run clinics, etc. Also, a lot of data could be stored against each musician. So having a separate document for each musician makes sense in this case.

- Also, if you think your embedded documents might exceed the file size limit imposed by MongoDB, then you'll need to store some data in separate documents.

## Update a Document

```
db.musicians.find({ _id: 6 }).pretty()
```

```
db.musicians.update(
        { _id: 6 }, 
        { $set:{ instrument : [ "Vocals", "Guitar", "Sitar" ] } }
    )
```

```
db.musicians.find({ _id: 6 }).pretty()
```

### The save() Method

The `save()` method is a cross between `update()` and `insert()`. When you use the `save()` method, if the document exists, it will be udpated. If it doesn't exist, it will be created.

```
db.producers.save({ _id: 1, name: "Bob Rock" })
```

```
db.producers.find()
```

## Export Data

Export a Collection to a JSON File

```
mongoexport --db music --collection artists --out /data/dump/music/artists.json
```

Export a Collection to a CSV File

```
mongoexport --db music --collection artists --type=csv --fields _id,artistname --out /data/dump/music/artists.csv
```

Export the results of a Query

```
mongoexport --db music --collection artists --query '{"artistname": "Miles Davis"}' --out /data/dump/music/miles_davis.json
```

#### The --sort Option

```
mongoexport --db music --collection artists --limit 3 --sort '{_id: 1}' --out /data/dump/music/3_artists_sorted.json
```

#### The --skip Option

```
mongoexport --db music --collection artists --limit 3 --sort '{_id: 1}' --skip 2 --out /data/dump/music/3_artists_sorted_skipped.json
```

#### The --pretty Option

```
mongoexport --db music --collection artists --query '{"artistname": "Miles Davis"}' --pretty --out /data/dump/music/miles_davis_pretty.json
```

## Delete a Document

### Delete One
```
db.artists.find( { artistname: { $in: [ "The Kooks", "Gang of Four", "Bastille" ] } } )
```

```
db.artists.deleteOne( { artistname: { $in: [ "The Kooks", "Gang of Four", "Bastille" ] } } )
```

```
db.artists.find( { artistname: { $in: [ "The Kooks", "Gang of Four", "Bastille" ] } } )
```


### Delete Many

```
db.artists.deleteMany( { artistname: { $in: [ "The Kooks", "Gang of Four", "Bastille" ] } } )
```

### Remove

```
db.artists.remove( { artistname: "AC/DC" } )
```

### Delete all Documents

```
db.artists.remove( {} )
```

## Drop Collection

```
db.artists.drop()
```

## Import Data

### Json

```
mongoimport --db music --file /data/dump/music/artists.json
```

#### Specify a Collection

```
mongoimport --db music --collection jazz --file /data/dump/music/miles_davis.json
```

### Csv

```
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
```

```
mongoimport --db music --collection catalog --type csv --headerline --file /data/dump/music/catalog.csv
```

#### Without Header Row

```
Mutt Lange, 1948
John Petrucci, 1967
DJ Shadow, 1972
George Clinton, 1941
```

```
mongoimport --db music --collection producers --type csv --fields name,born --file /data/dump/music/producers.csv
```

