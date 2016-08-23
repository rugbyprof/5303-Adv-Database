#### Logging In

```
mongo
```

#### Showing databases

```
show databases
```

### Using a database

```
use datbaseName
```

### Showing collections in a database

```
show collections
```

### Select All

```
Select * from Collection

db.collection.find()

//or

db.collection.find().pretty()
```
### Select with Projection (Where Clause)

```
SELECT *
FROM Collection
WHERE _id = '01030'

db.food.find({'_id':'01020'}).pretty()

```
