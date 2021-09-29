### Assignment 4 - SqlZoo.
#### Due: 09-20-2021 (Monday @ 5:00 p.m.)


### References For You  

* https://realpython.com/python-mysql/
* https://realpython.com/fastapi-python-web-apis/
* https://realpython.com/api-integration-in-python/
* https://sqlzoo.net

### Overview

* Create your own local database of the SqlZoo data using the data files located at the following address:
https://cs.msutexas.edu/~griffin/data/SqlZoo/

* You should have these tables:
  * buses 
  * euro2012 
  * movies 
  * nobel	 
  * teachers 
  * world

* Then proceed to create all of the queries to answer each of the questions at https://sqlzoo.net for the specific topics below.
  * https://sqlzoo.net/wiki/SELECT_basics
  * https://sqlzoo.net/wiki/SELECT_from_WORLD_Tutorial
  * https://sqlzoo.net/wiki/SELECT_from_Nobel_Tutorial
  * https://sqlzoo.net/wiki/SELECT_within_SELECT_Tutorial
  * https://sqlzoo.net/wiki/SUM_and_COUNT
  * https://sqlzoo.net/wiki/The_JOIN_operation


### Discussion 

* Using https://realpython.com/fastapi-python-web-apis/ create a folder on your server `/var/www/html/Apis/sqlzoo` and implement an API that consists of GET requests only corresponding with the answers to your SqlZoo solutions to each question.
* Each SqlZoo query has an `id` associated with it (question number) so we will use these identifiers to invoke a specific query. One problem is that each set of questions has questions that number from 1 * N so well use route names to differentiate between question sets. The following list of routes are all `GET` routes. We will also implement 1 `POST` routes for the `teachers` table,and one `PUT` OR `PATCH` route for the `world` table.  Don't worry about a `DELETE` for this project.

### GET Routes:
  * Basics
    * Sqlzoo Problem Set: https://sqlzoo.net/wiki/SELECT_basics
    * Route Name : basics
    * Example Route: http://Your.IP.Address:8001/basics/   (returns all queries)
    * Example Route: http://Your.IP.Address:8001/basics/{id}
  * World Tutorial
    * Sqlzoo Problem Set: https://sqlzoo.net/wiki/SELECT_from_WORLD_Tutorial
    * Route Name : world
    * Example Route: http://Your.IP.Address:8001/world/   (returns all queries)
    * Example Route: http://Your.IP.Address:8001/world/{id}
  * Nobel Tutorial
    * Sqlzoo Problem Set: https://sqlzoo.net/wiki/SELECT_from_Nobel_Tutorial
    * Route Name : nobel
    * Example Route: http://Your.IP.Address:8001/nobel/   (returns all queries)
    * Example Route: http://Your.IP.Address:8001/nobel/{id}
  * Select Within Tutorial
    * Sqlzoo Problem Set: https://sqlzoo.net/wiki/SELECT_within_SELECT_Tutorial
    * Route Name : within
    * Example Route: http://Your.IP.Address:8001/within/    (returns all queries)
    * Example Route: http://Your.IP.Address:8001/within/{id}
  * Sum and Count 
    * Sqlzoo Problem Set: https://sqlzoo.net/wiki/SUM_and_COUNT
    * Route Name : aggregate
    * Example Route: http://Your.IP.Address:8001/aggregate/   (returns all queries)
    * Example Route: http://Your.IP.Address:8001/aggregate/{id}
  * Join operations
    * Sqlzoo Problem Set: https://sqlzoo.net/wiki/The_JOIN_operation
    * Route Name : joins
    * Example Route: http://Your.IP.Address:8001/joins/   (returns all queries)
    * Example Route: http://Your.IP.Address:8001/joins/{id}
  * All
    * Sqlzoo Problem Set: All of them
    * Route Name : all
    * Example Route: http://Your.IP.Address:8001/all
    * Returns ALL of the previous routes with all id's
  
#### Examples:

**Route:** http://Your.IP.Address:8001/basics/3

**Question**:
Which countries are not too small and not too big? BETWEEN allows range checking (range specified is inclusive of boundary values). The example below shows countries with an area of 250,000-300,000 sq. km. Modify it to show the country and the area for countries with an area between 200,000 and 250,000.

**Runs**: 
```sql
SELECT name, area FROM world
  WHERE area BETWEEN 200000 AND 250000
```

**Returns**:
```json
{
   "question":"Which countries are not too small and not too big? BETWEEN allows range checking (range specified is inclusive of    
              boundary values). The example below shows countries with an area of 250,000-300,000 sq. km. Modify it to show the country and the area for countries with an area between 200,000 and 250,000.",
   "sql":"SELECT name, area FROM world
          WHERE area BETWEEN 200000 AND 250000",
   "results":[
      {
         "name":"Belarus",
         "area":207600
      },
      {
         "name":"Ghana",
         "area":238533
      },
      {
         "name":"Guinea",
         "area":245857
      },
      {
         "name":"Guyana",
         "area":214969
      },
      {
         "name":"Laos",
         "area":236800
      },
      {
         "name":"Romania",
         "area":238391
      },
      {
         "name":"Uganda",
         "area":241550
      },
      {
         "name":"United Kingdom",
         "area":242900
      }
   ]
}
```
**Route:** http://Your.IP.Address:8001/aggregate/3


**Question**:
How many countries have an area of at least 1000000

**Runs**: 
```sql
SELECT count(*) as count
FROM world
where area > 1000000
```

**Returns**:
```json
{
   "question":"Which countries are not too small and not too big? BETWEEN allows range checking (range specified is inclusive of    
              boundary values). The example below shows countries with an area of 250,000-300,000 sq. km. Modify it to show the country and the area for countries with an area between 200,000 and 250,000.",
   "sql":"SELECT name, area FROM world
          WHERE area BETWEEN 200000 AND 250000",
   "results":[
      {
        "count":29
      }
   ]
}
```


### POST Routes:
	 
  * Insert a new row into the `teachers` table.
  * Route: http://Your.IP.Address:8001/teacher/
  * Data Body must include all fields:

```json
{
  "id" : "int(11)"
  "dept" : "int(11)"
  "name" : "varchar(50)"
  "phone" : "varchar(50)"
  "mobile" : "varchar(50)"
}
```

### PUT Routes:
	 
  * Update the `world` table.
  * Route: http://Your.IP.Address:8001/world/
  * Data Body:
  
  * **MUST:** 
    * Include the primary key: `name` varchar(50)
  
  * **OPTIONAL:**
    * "continent" varchar(60)
    * "area" decimal(10,0)
    * "population" decimal(11,0)
    * "gdp" decimal(14,0)
    * "capital" varchar(60)
    * "tld" varchar(5)
    * "flag" varchar(255)

Example:
* Update the country Botswana to have a larger population.
```json
{
  "name" : "Botswana",
  "population" : "2094904"
}
```

* Update the country of The United States Of America to have a new capital and new flag.
```json
{
  "name" : "United States",
  "capital" : "Texas",
  "flag":"https://upload.wikimedia.org/wikipedia/commons/f/f7/Flag_of_Texas.svg"
}
```


### Deliverables

* Create a page that shows all routes so they can be clicked on to run when I go here: http://Your.IP.Address:8001/
* I should see all of your routes or if you can add to the docs some how, that would be sufficient when  going here: http://Your.IP.Address:8001/docs 
* The corresponding code for sqlzoo should be in a folder called `A04` inside an assignments folder which ends up on your Github repo.
