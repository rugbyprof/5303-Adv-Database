# Online Carpool System

## Spring 2015
Due: `Wednesday, December 2`<sup>nd</sup>`by 1700 hrs.`

### Description


Every database should be designed such that data can be subsequently queried and used in some informative manner either to display or be used in some subsequent processing. Below are a list of queries that I would expect you to be able to perform on your database. Using your current schema, create the necessary SQL code to fulfill each request below. If you find that you cannot fulfill the request, then you may need to question your schema.  

### Test data

Every database needs to be populated with test data. A good place to get users is: https://randomuser.me/api/. 

As far as trips , feedback , and car indo, etc. you can either enter them all by hand via a query interface, or write scripts to randomly create data. If you do enter them all by hand, you can always "export" the database to get a list of insert statements that created the data.

At a minimum, I would save all the sql queries run to load test data, this is in your best interest if you should ever have to "re-populate" your database. 

There should always be enough test data to ensure each query is working correctly. 

### Part 0

To organize the project up till now, create a folder called `dbProject` and place all files (code) and documents (relational diagram, requirements,etc) within the folder. This folder should be available on every persons Github repo thats in your group.


### Part 1 - Load Test Data

Create a file called `load_data.sql` and place all insert statements within this file necessary to load your test data.


### Part 1 - Querying

Using your test data, provide the answers to the following queries:

1. Show all users.
2. Show all users that are students and own a car. 
3. Find the user that logged the most trips.
4. Calculate the longest trip (miles). 
5. Find the average cost of a trip.
6. Find the user that has the best feedback. 
7. Show all feedback for each user.
8. Show all feedback for each user within the last month.
9. Find the user that has the most time in route (total, and monthly).
10. Show all different types of cars.
11. Find the ratio of men / smokers to woman / smokers. 
12. Find all commuters that ride with someone in the same major.
13. List the person who gives the most feedback.
14. Find all commuters who offer rides on Fridays.
15. Add a new user.
16. Add a new trip.
17. List the department that has the least number of commuters.
18. Find the cheapest / most expensive trips.

> Note: I created these queries while looking at the requirements, to point out shortcomings of each groups schema. You won't have to implement all of these in your final web project.

Place your answers in the project folder, in a file called `query_data.sql` using the following format:

```
### Title: Online Carpool System
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

