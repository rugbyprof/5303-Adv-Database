### Sql Assignment

Write SQL data definition language creating the tables required to set up the Database, and SQL data manipulation to insert tuples into the following Database and queries to answer the questions listed below. 

The program is to manage the airline flights, aircraft, passengers and pilots. The relations to be represented include: 

#### These are the flights scheduled for the 2 days in question:

|FLTNO	|	DATE	|	ORIGIN	|	DESTINATION |
|-------|-------|---------|-------------|
|1	|	4-1	|	DFW	|	DIA |
|2	|	4-1	|	DFW	|	ORD |
|3	|	4-1	|	DFW	|	LAX  |
|4	|	4-1	|	DIA	|	DFW |
|5	|	4-1	|	ORD	|	DFW |
|6	|	4-2	|	LAX	|	DFW |
|1	|	4-2	|	DFW	|	DIA |
|2	|	4-2	|	DFW	|	ORD |
|3	|	4-2	|	DFW	|	LAX |
|4	|	4-2	|	DIA	|	DFW |
|5	|	4-2	|	ORD	|	DFW |

#### The Airline has the Following aircraft:

|ACNO	|	TYPE	|	CAPACITY	|	PILOTS|
|-------|-------|---------|-------------|
|N173WY	|	C-172	|	3	|		1|
|N35A	|	B-18	|	9		|	2|
|N412B	|	DC-3	|	21	|		2|
|N747UA	|	B-747	|	300	|		3|

#### These are the airline’s pilots:

|PILOTID|		NAME|
|---------|-------------|
|1030	|	Wright, Orville|
|2137	|	Lindberg, Charles|
|0241	|	Yeager, Chuck|
|7305	|	Post, Wiley|
|2033	|	Boyington, Greg|
|4315	|	Lovell, James|
|3102	|	Hoover, Bob|
|0029	|	Tibbets, Paul|

#### A List of passengers for April 1st and 2nd. 

|PASSID	|	NAME|
|---------|-------------|
|1001	|	Simpson, Richard|
|1002	|	Halverson, Ranette|
|1003	|	Carpenter, Stewart|
|1004	|	Griffin, Terry|
|1005	|	Gordon, Scott|
|1101	|	Mouse, Mickey|
|1102	|	Duck, Donald|
|1103	|	Bunny, Bugs|
|1104	|	Moose, Bullwinkle|
|1105	|	Fudd, Elmer|
|1011 |		Wayne, John|
|1012	|	Mazurki, Mike|
|1013	|	Marvin, Lee|
|1014	|	Romero, Cesar|
|1015	|	Lamour, Dorothy |

#### The aircraft assignments are:

|ACNO	|	FLTNO	|	DATE|
|-------|---------|-------------|
|N35A	|	1	|	4-1 |
|N173WY	|	2	|	4-1 |
|N412B	|	3	|	4-1 |
|N35A	|	4	|	4-1 |
|N173WY	|	5	|	4-1 |
|N412B	|	6	|	4-2 |
|N173WY	|	1	|	4-2 |
|N35A	|	2	|	4-2 |
|N747UA	|	3	|	4-2 |
|N173WY	|	4	|	4-2 |
|N35A	|	5	|	4-2 |

#### The pilot assignments are:

|PILOTID	|	FLTNO	|	DATE|
|-------|---------|-------------|
|1030	|	1	|	4-1 |
|7305	|	1	|	4-1 |
|2137 |	2	|	4-1 |
|0241	|	3	|	4-1 |
|1030	|	4	|	4-1 |
|7305	|	4	|	4-1 |
|2137	|	5	|	4-1 |
|0241	|	6	|	4-2 |
|1030	|	1	|	4-2 |
|4315	|	2	|	4-2 |
|0029	|	2	|	4-2 |
|2033	|	3	|	4-2 |
|3102	|	3	|	4-2 |
|7305	|	4	|	4-2 |
|4315	|	5	|	4-2 |
|0029	|	5	|	4-2 |


#### The passengers ticketed are:

|PASSID	|	FLTNO	|	DATE|
|-------|---------|-------------|
|1001	|	1	|	4-1 |
|1002	|	1	|	4-1 |
|1003	|	2	|	4-1 |
|1004	|	1	|	4-1 |
|1005	|	2	|	4-1 |
|1101	|	2	|	4-1 |
|1102	|	3	|	4-1 |
|1103	|	1	|	4-1 |
|1104	|	2	|	4-1 |
|1105	|	2	|	4-1 |
|1011	|	3	|	4-1 |
|1012	|	3	|	4-1 |
|1013	|	3	|	4-1 |
|1014	|	3	|	4-1 |
|1015	|	3	|	4-1 |
|1001	|	4	|	4-2 |
|1002	|	4	|	4-2 |
|1101	|	5	|	4-2 |
|1104	|	5	|	4-2 |
|1011	|	6	|	4-2 |
|1012	|	6	|	4-2 |
|1013	|	6	|	4-2 |
|1001	|	2	|	4-1 |
|1003	|	1	|	4-1 |
|1102	|	5	|	4-1 |
|1011	|	4	|	4-1 |
|1013	|	5	|	4-1 |
|1015	|	5	|	4-1 |

#### Answer the following queries.

1. Print a passenger list for flight 3 on 4-1
2. Print a passenger list for flight 5 on 4-2
3. Print a list of all overbooked flights.
4. Print a list of passengers with more than one ticket.
5. Print a list of passengers with more than one ticket on the same day.
6. Print a list of flights that use aircraft N173WY.
7. Print a list of pilots who fly on April 1.
8. Print a list of pilots who fly on both days.
9. Print a list of pilots who have two flights on the same day.
10. Print a List of flights that do not have a complete crew.
11. Print of list of flights where destination is DFW.
12. Print a list of flights where origin or destination is LAX
13. Print the origin and destination of flights with passenger equals Duck, Donald or Wayne, John.
14. Print a list of flight numbers and origins.
15. Print a list of aircraft types from equipment assigned where pilot number=1030.
16. Print a list of pilots who fly with at least two other pilots. 
17. Print a list of pilots who fly only one type of plane.
18. Print a list of passengers booked on flights assigned to pilot=1030.
19. Print a list of pilots assigned to fly plane=N35A.
