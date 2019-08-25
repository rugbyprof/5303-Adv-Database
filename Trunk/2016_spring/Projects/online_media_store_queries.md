# Online Media System

## Spring 2015
Due: `Wednesday, December 2`<sup>nd</sup>`by 1700 hrs.`

### Description


Every database should be designed such that data can be subsequently queried and used in some informative manner either to display or be used in some subsequent processing. Below are a list of queries that I would expect you to be able to perform on your database. Using your current schema, create the necessary SQL code to fulfill each request below. If you find that you cannot fulfill the request, then you may need to question your schema.  

### Test data

Every database needs to be populated with test data. A good place to get users is: https://randomuser.me/api/. 

As far as orders , uploads , and suppliers, etc. you can either enter them all by hand via a query interface, or write scripts to randomly create data. If you do enter them all by hand, you can always "export" the database to get a list of insert statements that created the data.

At a minimum, I would save all the sql queries run to load test data, this is in your best interest if you should ever have to "re-populate" your database. 

There should always be enough test data to ensure each query is working correctly. 

### Part 0

To organize the project up till now, create a folder called `dbProject` and place all files (code) and documents (relational diagram, requirements,etc) within the folder. This folder should be available on every persons Github repo thats in your group.


### Part 1 - Load Test Data

Create a file called `load_data.sql` and place all insert statements within this file necessary to load your test data.


### Part 1 - Querying

Using your test data, provide the answers to the following queries:

1. Show all customers.
2. Show all media files for each type. 
3. Add a new media item. 
4. Edit a media item. 
5. Find all media items over 3Mb.
6. Find the sum of orders for each month.
7. Find the supplier that provides the most media.
8. List all the downloads for customer `X`.
9. List all the downloads for customer `X` arranged by type.
10. Find the average profits for a given year (what item sold for - what item paid for). Remember some items are sold retail or on sale.  
11. Show all customers from New York that have purchased over 10 items. 
12. Add a new customer.
13. List the most searched for media files.
14. List the customer representatives by amount sold all time.
15. List the customer representatives by amount sold by year.
15. List the customer representatives by amount sold this month.
16. List all orders over $100.
17. What is the average time between placing an order and receiving the order.
18. List all music files by category (e.g. Hard Rock, Techno, Indie), then alphabetically by artist. Or list all movies by category (e.g. Comedy, Action, Romance), then alphabetically by title.
19. List the best selling items in each category.


> Note: I created these queries while looking at the requirements, to point out shortcomings of each groups schema. You won't have to implement all of these in your final web project.

Place your answers in the project folder, in a file called `query_data.sql` using the following format:

```
### Title: Commuter Airline Test Queries
### Names: Member1, Member2 Member3 ...

#### Question 1:
Show all passengers.

SQL:
'''
SELECT * .....
FROM .... 
WHERE ...
'''

#### Answer:
'''
Your answer here
'''

```

Use the same question format for each answer. Points will be deducted for wrong formatting. 
>Note: In the example, I had to use single quotes (''') instead of backticks (```) so the markdown interpreter wouldn't convert them to markdown.

