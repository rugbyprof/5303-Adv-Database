# Airport Reservation System

## Spring 2015
Due: `Wednesday, December 2`<sup>nd</sup>`by 1700 hrs.`

### Description


Every database should be designed such that data can be subsequently queried and used in some informative manner either to display or be used in some subsequent processing. Below are a list of queries that I would expect you to be able to perform on your database. Using your current schema, create the necessary SQL code to fulfill each request below. If you find that you cannot fulfill the request, then you may need to question your schema.  

### Test data

Every database needs to be populated with test data. A good place to get users is: https://randomuser.me/api/. 

As far as Aircraft ,Flights , and Reservations you can either enter them all by hand via a query interface, or write scripts to randomly create data. If you do enter them all by hand, you can always "export" the database to get a list of insert statements that created the data.

At a minimum, I would save all the sql queries run to load test data, this is in your best interest if you should ever have to "re-populate" your database. 

There should always be enough test data to ensure each query is working correctly. 

### Part 0

To organize the project up till now, create a folder called `dbProject` and place all files (code) and documents (relational diagram, requirements,etc) within the folder. This folder should be available on every persons Github repo thats in your group.


### Part 1 - Load Test Data

Create a file called `load_data.sql` and place all insert statements within this file necessary to load your test data.


### Part 1 - Querying

Using your test data, provide the answers to the following queries:

1. Show all passengers.
2. Show all administrators that have access. 
3. Show all reservations organized by `Flight Number`. 
4. Show the `Tail Number` and `status` of all aircraft. 
5. Show a history of reservations for passenger `X`.
6. Add a new customer (passenger).
7. Add a new administrator (worker).
8. Determine if a specific flight is full.
9. Find all flights that are delayed.
10. Cancel a reservation.
11. Show a history of flights that each aircraft was assigned to. 
12. Add a new user.
13. List all flights in which a passenger requested a `vegetarian` meal.
14. Show a list of all current flights, their status, and how full (via a percentage) they are.
15. Show all flights leaving `X` and going to `Y` (where X & Y are cities or airports).
16. Show all flights leaving `X` and going to `Y` on date `Z`
17. Show all flights leaving `X` and going to `Y` on date `Z` where departure time is in between `T1` and `T2` 
17. List all planes according to capacity.
17. Show remaining number of `Isle` / `Window` seats available on a specific flight.  
18. Select the number of available `First Class` / `Business` / `Coach` seats available for a given flight.
19. Alter a reservation.
20. Determine the fare of a flight (`Fare = $50 + (Distance * $0.11)`)

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

