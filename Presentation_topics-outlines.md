## PostGres vs Mysql 

- We know that PostGreSQL and MySQL are both RDBMS’s so thats nothing new.
- Mysql has some spin offs (MariaDB, Percona), why is that? Why doesn't PostgreSQL have any? (This point may not be quantifiable and it's ok to give us opionion based answer).
- Your going to have to really pick apart both DB’s and tell us from a low level where each DB excels or struggles:
    - Acid Complience
    - Table Locking
    - Json Support
    - Joins
    - Data Integrity
    - Data Types
    - Transactions and Rollbacks
    - Performance Tuning
    - Non-SQL compliant Functions (Mysql added a bunch)
    - Etc.
        
- I would discuss the similarities first, the major differences, then get into the minor differences.
- Approach this like your presenting to your boss at work, and he needs to choose Mysql or PostgreSQL based on the upcoming project the company is starting. The problem is that be didn’t tell you what the project was so you have to discuss all differences so he can make a choice. 
- In the end there is no winner, but I should be able to choose based on what project I have to implement.

Decent Article: https://www.quora.com/What-are-pros-and-cons-of-PostgreSQL-and-MySQL<br>
https://www.wikivs.com/wiki/MySQL_vs_PostgreSQL

## Apache Cassandra

- Describe NoSql /  RDBMS and their basic differences (use loosely based definitions just to compare).
- Define the concept of a "distributed database". Give examples of some other distributed DB’s.
- Is Apache Cassandra an RDBMS or NoSQL DB? 
    - It’s NoSql, but it has a SQL like syntax so explain how this is so.
- What are the differences between Cassandra and other NoSql DB’s
- How does it store data?
    - Does it use traditional data structures?
    - https://wiki.apache.org/cassandra/DataModel
    - Database denormalization (define it and describe it and discuss why it can speed things up)
        - What would some of the negative side effects of denormalization? 
- How does cassandra perform against RDBMS’s?
- Does Cassandra support joins, subqueries, etc?
- Does Cassandra support transactions?
- Summary and Conclusions.

https://academy.datastax.com/demos/brief-introduction-apache-cassandra

## SQL lite

- Describe traditional RDBMS (general overview to lay groundwork):
    - how it stores data
    - disk access
    - transactions 
    - etc.
- Describe SQLite as it compares to a traditional RDBMS.
    - How does it store data
    - Can it be server based or is it end user only?
    - Does it scale smoothly (work well if it gets large)?
    - Does it provide all functionality of traditional RDBMS?
    - Can SQLite support multiple users and multiple DB’s?
    - What would the major market be for SqlLite (what apps / software gravitates toward SqlLite)?
- MOST IMPORTANTLY (discuss comparable alternatives):
    - http://www.developereconomics.com/five-popular-databases-for-mobile/
    - Berkeley DB 
    - You should pick 2-3 alternatives to describe almost as thoroughly as you do sqlite. 

## No SQL DB VS RDBMS

- Define No Sql and Rdbms (overview of each with loose definitions) 
- Discuss general storage methods for generic Rdbms 
    - B+ Trees 
    - When does data get written (Write Through, Write Back)
   - Discuss memory resident items vs items written to disk (indexing)
- Now give examples using actual DBMS’s (Oracle, Sql Server, Mysql, Postgres , etc.) You don’t have to use all of them.
- Discuss general storage methods for NoSql. You will probably need examples using companies (Mongo, Redis, CouchDB,etc)
    - **Key-Value Store** – It has a Big Hash Table of keys & values {Example- Riak, Amazon S3 (Dynamo), Redis}
    - **Document-based Store** - It stores documents made up of tagged elements. {Example- CouchDB, MongoDB}
    - **Column-based Store** - Each storage block contains data from only one column, {Example- HBase, Cassandra}
    - **Graph-based**  - A network database that uses edges and nodes to represent and store data. {Example- Neo4J}
- Now we know enough about Rdbms and NoSql so give us an objective comparison of plusses and minuses for each. 
- Images are good to show differences (one example, use more)
    - http://image.slidesharecdn.com/iforum-sqlvsnosql-150418133743-conversion-gate01/95/iforum-2015-sql-vs-nosql-7-638.jpg?cb=1429364572

- Decent Article: http://www.3pillarglobal.com/insights/exploring-the-different-types-of-nosql-databases
- Image came from here: http://www.slideshare.net/DenisReznik/iforum-sql-vs-nosql

## BigData (As applied to NOSQL and RDBMS)

Below is a brainstorm of questions from me. 
It will flow logically like a presentation should, but I am brainstorming, so if something doesn’t make sense please come clarify

I will use “THEM” and “THEY” meaning “No Sql” and “Rdbms” together.

- What is Big Data and the “No Sql” movement? (just an overview and loose definitions, because you will be more specific in comparing THEM )
    - Define all the terms:
        - Big Data
        - No Sql
        - Rdbms
- Describe the differences between THEM. (now you can be more specific in comparing the two).  Below are some questions that may help you describe the differences.
    - Use companies   (like mysql postgres oracle mongodb redis) when describing differences
    - When should we use one or the other?
    - What types of businesses or platforms use either of THEM
        - Data companies? Gaming companies. Companies that have so much data they can’t process it?
        - Is it just for data analytics and or data mining? Or can it be used for business and e-commerce?
    - Is there ever a clear cut decision between one of THEM?
- Big Data tends to be paired with No Sql, is this always the choice? Are there alternatives allowing companies to stick with Rdbms?
- Are there any Hybrid databases (both No Sql and Rdbms)?
- Are there any Rdbms’s that are made for big data?
- Conclusions

- Don’t forget to discuss performance!
- And try to use images when describing things. 
- I found this presentation: http://www.slideshare.net/Muratakal/rdbms-vs-nosql
- Theres a bunch more on that site. It’s ok to use others materials. Just cite them.

## Spatial Extensions in RDBMS 

- What is a spatial extension?
- What does this add to the traditional RDBMS? 
    -  Additional data types (points, linestrings, multiLinestrings, etc.)
    -  Additional functions added (distance, area, length,crosses,intersects,etc.)
    -  Additional operators (e.g. `A @ B` means A is contained by B). Give us more examples of these types of operations. 
- How does this effect querying?
    - Give examples of types of queries (nearest neighbor, point in polygon, intersection, etc.) 
- How does this effect indexing?
    - Obviously by querying spatial data, our indexes must also adapt. Discuss the changes in approaches to indexing data.
    - R-Trees is an obvious choice for indexing, but what is actually implemented in some of the common DB's (oracle, postgres, mysql) 
- What kind of performance can we expect with spatial queries?
- Emphasize the DB's that we discuss the most, you can mention others if they have features that are interesting. 
- http://www.cubrid.org/blog/dev-platform/20-minutes-to-understanding-spatial-database/
- http://postgis.net/docs/manual-1.3/ch06.html#id439526
- https://dev.mysql.com/doc/refman/5.0/en/opengis-geometry-model.html



    



