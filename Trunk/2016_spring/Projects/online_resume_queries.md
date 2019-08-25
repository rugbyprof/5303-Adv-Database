# Online Resume System

## Spring 2015
Due: `Wednesday, December 2`<sup>nd</sup>`by 1700 hrs.`

### Description


Every database should be designed such that data can be subsequently queried and used in some informative manner either to display or be used in some subsequent processing. Below are a list of queries that I would expect you to be able to perform on your database. Using your current schema, create the necessary SQL code to fulfill each request below. If you find that you cannot fulfill the request, then you may need to question your schema.  

### Test data

Every database needs to be populated with test data. A good place to get users is: https://randomuser.me/api/. 

As far as Posted Jobs , Interviews , and Companys, etc. you can either enter them all by hand via a query interface, or write scripts to randomly create data. If you do enter them all by hand, you can always "export" the database to get a list of insert statements that created the data.

At a minimum, I would save all the sql queries run to load test data, this is in your best interest if you should ever have to "re-populate" your database. 

There should always be enough test data to ensure each query is working correctly. 

### Part 0

To organize the project up till now, create a folder called `dbProject` and place all files (code) and documents (relational diagram, requirements,etc) within the folder. This folder should be available on every persons Github repo thats in your group.


### Part 1 - Load Test Data

Create a file called `load_data.sql` and place all insert statements within this file necessary to load your test data.


### Part 1 - Querying

Using your test data, provide the answers to the following queries:

1. Show all job seekers.
2. Show all employees. 
3. Calculate the charge for job seeker `X`. 
4. Calculate the charge for company `X`. 
5. Find the company with the most jobs.
6. Find the average # of interviews for all active users.
7. Add a new administrator (worker).
8. Find the customer representative with most interviews.
9. Produce a list of job suggestions for a given job seeker (based on that job seeker's past interviews).
10. Find the company that generated the most interviews this month (or any and all months). 
11. Find all interviews that were done last year. 
12. Add a new job seeker.
13. List the most searched for categories.
14. Find job seeker with most scheduled interviews (meaning they are scheduled, but not completed).
15. Find all jobs within category `X`.
16. Find all jobs within category `X` and subcategory `Y'
17. Find the count of currently posted jobs in each category and list from most to least.
18. Find the count of past posted jobs in each category and list from most to least.
19. Find the count of all posted jobs in each category and list by month.
20. Add a job seeker  
21. Alter a posted job.

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

