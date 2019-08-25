### Title: Sql Flight Assignment
### Name: Sudha Mallavarapu

#### Question 1:
Print a passenger list for flight 3 on 4-1

SQL:
```
SELECT A.NAME 
FROM passengers A JOIN pass_ticketed B ON (A.passid = B.passid) 
WHERE fltno='3' AND date='4-1'
```

#### Answer:
```
NAME
Duck, Donald
Wayne, John
Mazurki, Mike
Marvin, Lee
Romero, Cesar
Lamour, Dorothy
```

#### Question 2:
Print a passenger list for flight 5 on 4-2

SQL:
```
SELECT A.NAME 
FROM passengers A JOIN pass_ticketed B ON (A.passid = B.passid) 
WHERE fltno='5' AND date='4-2'
```

#### Answer:
```
NAME
Mouse, Mickey
Moose, Bullwinkle
```

#### Question 3:
Print a list of all overbooked flights.

SQL:
```
SELECT C.fltno, A.capacity ,COUNT(passid) as num
FROM aircraft A JOIN aircraft_assignments B ON A.acno=B.acno
JOIN pass_ticketed C on B.fltno=C.fltno AND B.date = C.date
GROUP BY C.fltno, C.date
HAVING num > A.capacity
```

#### Answer:
```
fltno capacity num
2		3		6
```

#### Question 4:
Print a list of passengers with more than one ticket

SQL:
```
SELECT A.name 
FROM passengers A JOIN pass_ticketed B ON (A.passid = B.passid ) 
GROUP BY B.passid
HAVING COUNT(*) > 1
```

#### Answer:
```
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
```

#### Question 5:
Print a list of passengers with more than one ticket on the same day

SQL:
```
SELECT A.name
FROM passengers A JOIN pass_ticketed B ON (A.passid = B.passid ) 
GROUP BY B.date AND B.passid
HAVING (COUNT(*) > 1) 
```

#### Answer:
```
name
Simpson, Richard
```

#### Question 6:
Print a list of flights that use aircraft N173WY.

SQL:
```
SELECT fltno
FROM aircraft_assignments
WHERE acno='N173WY'
```

#### Answer:
```
fltno
2
5
1
4
```
#### Question 7:
Print a list of pilots who fly on April 1.

SQL:
```
SELECT A.name
FROM pilots A JOIN pilot_assignments B ON (A.pilotid = B.pilotid)
WHERE date='4-1'
```

#### Answer:
```
name
Wright, Orville
Post, Wiley
Lindergh, Charles
Yeager, Chuck
Wright, Orville
Post, Wiley
Lindergh, Charles
```

#### Question 8:
Print a list of pilots who fly on both days

SQL:
```
SELECT name from pilots where pilotid IN
(
SELECT pilotid 
FROM pilot_assignments
WHERE date='4-2' and pilotid IN
(
SELECT pilotid
FROM pilot_assignments
WHERE date='4-1'
)    
)
```

#### Answer:
```
name
Wright, Orville
Yeager, Chuck
Post, Wiley
```

#### Question 9:
Print a list of pilots who have two flights on the same day.

SQL:
```
SELECT A.name, COUNT(date) as num 
FROM pilots A 
JOIN pilot_assignments B ON A.pilotid=B.pilotid 
GROUP BY B.pilotid, B.date
HAVING num>1
```

#### Answer:
```
name                        num
Wittman. Steve	2
Wright, Orville	2
Lindergh, Charles	2
Lovell, James	2
Post, Wiley	2 
```

#### Question 10:
Print a List of flights that do not have a complete crew

SQL:
```
SELECT C.fltno,A.pilots,A.acno,COUNT(pilotid) AS num 
FROM aircraft A 
JOIN aircraft_assignments B ON A.acno = B.acno 
JOIN pilot_assignments C ON B.fltno = C.fltno  and B.date=C.date
GROUP BY C.fltno,C.date having num<A.pilots
```

#### Answer:
```
fltno pilots acno num
3 2 N412B 1
3 3 N747UA 2
6 2 N412B 1
```

#### Question 11:
Print of list of flights where destination is DFW

SQL:
```
SELECT fltno from flights where destination='DFW'
```

#### Answer:
```
fltno
4
5
6
4
5
```

#### Question 12:
Print a list of flights where origin or destination is LAX

SQL:
```
SELECT fltno from flights where origin='LAX' OR destination='LAX'
```

#### Answer:
```
fltno
3
6
3
```

#### Question 13:
Print the origin and destination of flights with passenger equals Duck, Donald or Wayne, John

SQL:
```
SELECT A.origin,A.destination
FROM flights A 
JOIN pass_ticketed B ON A.fltno=B.fltno 
JOIN passengers C ON B.passid=C.passid 
WHERE C.name='Duck, Donald' OR C.name='Wayna, John'
```

#### Answer:
```
origin destination
DFW LAX
DFW LAX
ORD DFW
ORD DFW
```

#### Question 14:
Print a list of flight numbers and origins.

SQL:
```
SELECT DISTINCT fltno,origin FROM flights
```

#### Answer:
```
fltno origin
1 		DFW
2		DFW
3 		DFW
4 		DIA
5 		ORD
6 		LAX

```

#### Question 15:
Print a list of aircraft types from equipment assigned where pilot number=1030.

SQL:
```
SELECT A.type
FROM aircraft A 
JOIN aircraft_assignments B ON A.acno=B.acno
JOIN pilot_assignments C on B.fltno=C.fltno
WHERE C.pilotid='1030'
```

#### Answer:
```
type
B-18
C-172
B-18
C-172
B-18
C-172
```

#### Question 16:
Print a list of pilots who fly with at least two other pilots

SQL:
```
SELECT A.name,A.pilotid 
FROM pilots A
JOIN pilot_assignments B ON A.pilotid=B.pilotid
JOIN aircraft_assignments C ON B.fltno = C.fltno AND B.date=C.date 
JOIN aircraft D ON D.acno=C.acno
WHERE D.pilots>2
```

#### Answer:
```

name
pilotid
Boyington, Greg
2033
Hoover, Bob
3102
```

#### Question 17:
Print a list of pilots who fly only one type of plane.

SQL:
```
SELECT C.name 
FROM aircraft_assignments A 
JOIN pilot_assignments B ON A.fltno = B.fltno AND A.date = B.date
JOIN pilots C ON C.pilotid = B.pilotid
GROUP BY B.fltno
HAVING count(acno) = 1
```

#### Answer:
```
name
Yeager, Chuck
```

#### Question 18:
Print a list of passengers booked on flights assigned to pilot=1030.

SQL:
```
Print a list of passengers booked on flights assigned to pilot=1030.
SELECT A.name
FROM passengers A 
JOIN pass_ticketed B ON A.passid=B.passid
JOIN pilot_assignments C on B.fltno=C.fltno
WHERE C.pilotid='1030'
```

#### Answer:
```
name
Simpson, Richard
Halverson, Ranette
Griffin, Terry
Bunny, Bugs
Carpenter, Stewart
Simpson, Richard
Halverson, Ranette
Wayne, John
Simpson, Richard
Halverson, Ranette
Griffin, Terry
Bunny, Bugs
Carpenter, Stewart
```
#### Question 19:
Print a list of pilots assigned to fly plane=N35A.

SQL:
```
select name 
from pilots 
where pilotid 
IN
(
select distinct pa.pilotid
from aircraft_assignments aa
join pilot_assignments pa
on aa.fltno=pa.fltno
where aa.acno='N35A'
)
```

#### Answer:
```
Name
Wright, Orville
Lindergh, Charles
Post, Wiley
Lovell, James
Wittman. Steve
```
