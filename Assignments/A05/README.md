## Assignment 5 - Movies DB.
#### Due: 10-04-2021 (Monday @ 5:00 p.m.)

### References For You  

* https://realpython.com/python-mysql/
* https://realpython.com/fastapi-python-web-apis/
* https://realpython.com/api-integration-in-python/
* https://datasets.imdbws.com/

#### Unicode!!
* https://realpython.com/python-encodings-guide/

### Overview

We have a huge amount of data given to us by the IMDB website in 7 different files. The overall goal is to create your own local database of the movie data using the files located at the following address:
https://datasets.imdbws.com/. This will of course involve a many stage process.

* Getting all files
* Uncompressing the files.
* Processing each file into a usable format OR 
* Re-Organize the files by filtering / combining them to fit a schema

### IMDB Files

A summary of the IMDB files can be found [HERE](ImdbInfo.md) and help processing the files can be found [HERE](processing_tsv.md). There are snippets to download and process tsv files to help get you started. Its Python and it works, but if you ask Byron, he probably could write something better in C++. 

### Creating Tables

We had a discussion in class summarized (and more) [HERE](db_design_start.md).

- Below is an example set of sql queries that creates a table for people, professions, and then associates a person with one or more professions in the final table. Notice the foreign keys. 

- If we were to delete an actor from the `Person` table, you want that action to cascade down to the `PersonsProfession` table and remove any entries for an actor.

- What if a profession changed its name? Does that propagate anywhere?

- However, be careful with constraints, as deleting an actor shouldn't also delete any professions they were associated with, as other persons may be associated with those professions.

```sql
CREATE TABLE Person(
  pid   VARCHAR(10),
  first VARCHAR(32),
  last  VARCHAR(32),
  birth    INT(4),
  died    INT(4),
  PRIMARY KEY (id)
);

CREATE TABLE Profession(
  proid   VARCHAR(10),
  profession   VARCHAR(64),
  PRIMARY KEY (proid)
);

CREATE TABLE PersonsProfession(
  pid   VARCHAR(10),
  proid   VARCHAR(10),
  PRIMARY KEY (pid,proid),
  FOREIGN KEY (pid) REFERENCES Person(pid),
  FOREIGN KEY (proid) REFERENCES Profession(proid)
);
```

#### Your Tables

- Create your db tables as you see fit, as long as they are normalized, and have proper constraints created through the use of foreign keys and their actions. Look up `On Delete` and `On Update`

### Schema

This is an example visual schema produced by phpMyAdmin. It is not the visual schema for the tables above, but you should create one for your final DB design and place it the folder along with other assignment docs.

<img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/imdb_schema.png" width="600">

### Loading Database

There is obviously an issue with the size of the IMDB files which has caused issues when attempting to load all the data. So, part of this assignment will be to correctly filter the loading data and only store information that are associated with movies that have a release year of **1950** and later. You can ignore `title.akas.tsv.gz` and `title.episode.tsv.gz`. But the rest should contain relevant data.

### API

- This Api will run on `port 8002` on your server.
- Any data returned by a route will be paginated with a preset page size (typically about 1000).
- Therefore you need a way to provide a starting row for subsequent queries.
- Using an api library of your choice, create a folder on your server `/var/www/html/Apis/movie` and implement an API for the movies DB. 
- Below are a list of the minimum routes that need to be available.

#### Routes

- Movies 
  - Find all
  - Filter on (any field in table)[year,runtime(min/max)]
    - e.g. return all movies in 1961
    - e.g. return all movies with runtime > 90
    - e.g. return all movies with runtime between 80 and 100
  - Filter on actor or actress (id)
    - e.g. return all movies associated with a specific actress
    - e.g. return all movies associated with a set of actors and actresses
  - Filter on genre(s)
    - e.g return all movies in a specified genre
- People
  - Find all
  - Filter on name (first or last)
  - Filter on movie (id)
  - Filter on genre(s)
  - Filter on "worked with `id` or `ids`"
    - e.g. find all actors and actresses that worked with `id`
  - Filter on profession
- Genre
  - Find all
- Profession
  - Find all

### Deliverables

* As of now you should have a fastApi instance always running and ready on your server at port 8001 corresponding to your [sqlZoo assignment](../A04/README.md).
* A similar api should be available and running on port 8002 for this assignment.
* So when someone goes here: http://Your.IP.Address:8002/ they will see available routes to run, with some examples.
* Create a folder in your assignments folder called `A05` and place any and all documents in this folder. 
* Most importantly is a README describing your project and all the files. Help for [comments](../../Resources/03-Comments/README.md) and [readmees](../../Resources/04-Readmees/README.md) are in the [Resources](../../Resources/README.md) folder.

