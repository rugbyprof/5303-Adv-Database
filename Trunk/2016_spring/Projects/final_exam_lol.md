# Mongo DB!

## Overview:

Your going to create a mongoDB. Don't worry, I'm doing all the work (mostly) so you can just relax. The hardest part is getting all the definitions from the web :) After you have all the definitions, you will insert them into a mongoDB that you will create. Here we go...


### Define the following

|             |              |             |              |
|:------------|:-------------|:------------|:-------------|
| ACID | Atomicity | BLOB | B-tree |
| Cardinality | Cascade | Commit | Compound Key |
| Concurrency | Consistency | Deadlock | Distributed Database |
| Foreign Key | Index | Inner Join | Join |
| JSON | Key | Mirroring | Natural Join |
| NoSQL | Outer Join  | Primary Key | Referential Integrity |
| Relational Model | Remote Procedure Call  | Rollback | Scalability |
| Stored Procedure  | Synchronization | Data Warehouse | Encryption |
| Entity-Relationship Diagram | Isolation | Data Mining | Normalization |
| Object-Oriented Database | Postgres | sql server | mysql |
| oracle | Schema | snapshot | SQL Injection Attacks |
| self join | view |   **Find 4 more database**     |    **words to make a total of 50!**   |



### Create a json file

- This file will contain all your definitions to be loaded (all at once) into a mongoDB collection.
- Your file needs to be formatted as follows (one definition per line):

```json
{"word":"ACID","definition":"this is the definition of acid"},
{"word":"Atomicity","definition":"this is the definition of atomicity"}
...
{"word":"View","definition":"This is the definition of view. It's a very long definition."}
```

### Log onto the server and into Mongo

- Log onto cs3.mwsu.edu
- Type the following: `mongo`
- View existing datbases. Command: `show databases`. 
- You should see:
    - griffin
    - local
    - test
    - (maybe more if other groups beat you here)
- Create a database for your group. Command: `use databasename` (STOP! Ask me what to name it.)
- Create a collection for your definitions. Command: `db.createCollection('db_defs')`
- Exit mongodb. Command: `exit`
- Now load your json file into your collection:
    - `mongoimport --db YourDBName --collection db_defs --jsonArray < yourjsonfile.json`
- If it was successful (no errors) you should be able to log back into mongo and view your definitions by doing the following:
    - `mongo` # login
    - `use YourDatabaseName` # select your database
    - `db.db_defs.find()` # select * from your collection
- If you see all 50 words, then move on to the next step.
    
### Email Me!

- You need to send me an email like the following:

```
subject: 5303 Mongo Final
body: 
    
Names In Group:
    Name 1
    Name 2
    
Database Name:
    YourDatabaseName
    

Collection Name:
    YourCollectionName
    
    

