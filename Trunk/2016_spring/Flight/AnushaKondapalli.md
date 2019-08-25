### Title: Sql Flight Assignment
### Name: Anusha Kondapalli
…………………………………………………………………………..
###Question 1:
Print a passenger list for flight 3 on 4-1

SQL :
'''
SELECT name
FROM passengers
JOIN pass_ticketed ON passengers.passid = pass_ticketed.passid
WHERE fltno =3
AND DATE =  '4-1'
LIMIT 0 , 30

###Answer:
'''
name
Duck, Donald
Wayne, John
Mazurki, Mike
Marvin, Lee
Romero, Cesar
Lamour, Dorothy
'''

###Question 2:
Print a passenger list for flight 5 on 4-2
 
SQL :
'''
SELECT name
FROM passengers
JOIN pass_ticketed ON passengers.passid = pass_ticketed.passid
WHERE fltno =5
AND DATE =  '4-2'
LIMIT 0 , 30

###Answer:
'''
name
Mouse, Mickey
Moose, Bullwinkle
'''

###Question 3:
Print a list of all overbooked flights.

SQL :
'''
SELECT ac.acno
FROM (

SELECT aa.acno, COUNT( * ) AS capc
FROM pass_ticketed pt, aircraft_assignments aa
WHERE pt.fltno = aa.fltno
AND pt.date = aa.date
GROUP BY pt.fltno, pt.date
)ac, aircraft a
WHERE ac.acno = a.acno
AND ac.capc > a.capacity
LIMIT 0 , 30
'''

###Answer:
'''
acno
N173WY
'''

###Question 4:
Print a list of passengers with more than one ticket.

SQL :
'''
SELECT name
FROM passengers
JOIN pass_ticketed ON passengers.passid = pass_ticketed.passid
GROUP BY pass_ticketed.passid
HAVING COUNT( * ) >1
LIMIT 0 , 30
'''

###Answer:
'''
name
Simpson, Richard
Halverson, Ranette
Carpenter, Stewart
Wayne, John
Mazurki, Mike
Marvin, Lee
Lamour, Dorothy
Mouse, Mickey
Duck, Donald
Moose, Bullwinkle
'''

###Question 5:
Print a list of passengers with more than one ticket on the same day.

SQL :
'''
SELECT passengers.name
FROM passengers
WHERE passengers.passid
IN (

SELECT pass_ticketed.passid
FROM pass_ticketed
GROUP BY pass_ticketed.passid, pass_ticketed.date
HAVING COUNT( * ) >1
)
LIMIT 0 , 30
'''

###Answer
'''
name
Simpson, Richard
Carpenter, Stewart
Duck, Donald
Wayne, John
Marvin, Lee
Lamour, Dorothy
'''

###Question 6:
Print a list of flights that use aircraft N173WY.

SQL:
'''
SELECT DISTINCT (
fltno
)
FROM aircraft_assignments
WHERE acno =  'N173WY'
LIMIT 0 , 30

'''

###Answer
'''
fltno
2
5
1
4
'''


###Question 7:
Print a list of pilots who fly on April 1.

SQL:
'''
SELECT DISTINCT (
pilots.name
)
FROM pilots
JOIN pilot_assignments
WHERE pilot_assignments.pilotid = pilots.pilotid
AND pilot_assignments.date =  '4-1'
LIMIT 0 , 30

'''

###Answer
'''
name
Wright, Orville
Post, Wiley
Lindergh, Charles
Yeager, Chuck
'''

###Question 8:
Print a list of pilots who fly on both days.

SQL:
'''
SELECT a.pilotid
FROM pilot_assignments a, pilot_assignments b
WHERE a.pilotid = b.pilotid
AND a.date != b.date
GROUP BY a.pilotid
'''

###Answer
'''
pilotid
241
1030
7305
'''

###Question 9:
Print a list of pilots who have two flights on the same day.

SQL:
'''
SELECT pilot_assignments.pilotid
FROM pilot_assignments
GROUP BY pilot_assignments.pilotid, pilot_assignments.date
HAVING COUNT( * ) =2
LIMIT 0 , 30
'''

###Answer
'''

pilotid
29
1030
2137
4315
7305
'''
--------------------------------------------------------------------
###Question 10:
Print a List of flights that do not have a complete crew.

SQL:
'''

'''

###Answer
'''

'''
--------------------------------------------------------------------------------

###Question 11:
Print of list of flights where destination is DFW.

SQL:
'''
SELECT DISTINCT (
fltno
)
FROM flights
WHERE destination =  'DFW'
LIMIT 0 , 30
'''

###Answer
'''
fltno
4
5
6
'''

###Question 12:
Print a list of flights where origin or destination is LAX

SQL:
'''
SELECT DISTINCT (
fltno
)
FROM flights
WHERE destination =  'LAX' or origin='LAX'
LIMIT 0 , 30
'''

###Answer
'''
fltno
3
6
'''

###Question 13:
Print the origin and destination of flights with passenger equals Duck, Donald or Wayne, John.

SQL:
'''
SELECT DISTINCT (
f.origin
), f.destination
FROM flights f
INNER JOIN pass_ticketed pt ON f.fltno = pt.fltno
INNER JOIN passengers p ON p.passid = pt.passid
WHERE p.name =  'Duck, Donald'
OR p.name =  'Wayne, John'
LIMIT 0 , 30
'''

###Answer
'''
origin  destination
DFW     LAX
LAX     DFW
ORD     DFW
DIA     DFW
'''

###Question 14:
Print a list of flight numbers and origins

SQL:
'''
SELECT DISTINCT (
fltno
), origin
FROM flights
LIMIT 0 , 30

'''

###Answer
'''

fltno  origin
1      DFW
2      DFW
3      DFW
4      DIA
5      ORD
6      LAX
'''

###Question 15:
Print a list of aircraft types from equipment assigned where pilot number=1030.

SQL:
'''
SELECT DISTINCT (
a.type
)
FROM aircraft a
INNER JOIN aircraft_assignments aa ON a.acno = aa.acno
INNER JOIN pilot_assignments p ON aa.fltno = p.fltno
WHERE p.pilotid =  '1030'
LIMIT 0 , 30

'''

###Answer
'''
type
B-18
C-172
'''
--------------------------------------------------------------------
###Question 16:
Print a list of pilots who fly with at least two other pilots.

SQL:
'''
SELECT a.pilotid
FROM (

SELECT pa.pilotid, pa.date, pa.fltno
FROM pilot_assignments pa
GROUP BY pa.date, pa.fltno
HAVING COUNT( * ) >2
)a, pilot_assignments ps
WHERE a.date = ps.date
AND a.fltno = ps.fltno
LIMIT 0 , 30

'''

###Answer
'''
 MySQL returned an empty result set (i.e. zero rows).
'''
---------------------------------------------------------------
###Question 17:
Print a list of pilots who fly only one type of plane.

SQL:
'''


'''

###Answer
'''

'''
-------------------------------------------------------------------
###Question 18:
Print a list of passengers booked on flights assigned to pilot=1030.

SQL:
'''
SELECT DISTINCT (
passid
)
FROM pass_ticketed
JOIN pilot_assignments ON pilot_assignments.fltno = pass_ticketed.fltno
WHERE pilotid =  '1030'
LIMIT 0 , 30

'''

###Answer
'''
passid
1001
1002
1004
1103
1003
1011
'''

###Question 19:
Print a list of pilots assigned to fly plane=N35A..

SQL:
'''
SELECT DISTINCT (
pilotid
)
FROM pilot_assignments
JOIN aircraft_assignments ON aircraft_assignments.fltno = pilot_assignments.fltno
WHERE acno =  'N35A'
LIMIT 0 , 30
'''

###Answer
'''
pilotid
1030
7305
2137
4315
29
'''