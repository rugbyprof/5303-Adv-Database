### Title: Sql Flight Assignment###
### Your Name: Saboor Ahmed Siddiqie  

#### Question 1:
Print a passenger list for flight 3 on 4-1

SQL:
```
SELECT passengers.passid, name
FROM passengers
join pass_ticketed 
on passengers.passid=pass_ticketed.passid
WHERE fltno =3
AND DATE =  '4-1'
```

#### Answer:
```
passid | name
----- | ----
1102 | Duck, Donald
1011 | Wayne, John
1012 | Mazurki, Mike
1013 | Marvin, Lee
1014 | Romero, Cesar
1015 | Lamour, Dorothy
```


#### Question 2:
Print a passenger list for flight 5 on 4-2

SQL:
```
SELECT passid, name
FROM passengers
WHERE passid
IN (

SELECT passid
FROM pass_ticketed
WHERE fltno =5
AND DATE =  '4-2'
)
```

#### Answer:
```
passid | name	
------ | -----
1101	|Mouse, Mickey
1104	|Moose, Bullwinkle
```

#### Question 3:
Print a list of all overbooked flights.

SQL:
```
select b.acno,b.bfltno as fltno,b.bdate as date 
from (
SELECT fltno,date, COUNT( passid ) as count1
FROM pass_ticketed
GROUP BY fltno,date) a
join 
(
SELECT a.acno as acno,capacity,aa.fltno as bfltno,aa.date as bdate 
FROM aircraft a
join aircraft_assignments aa
on a.acno=aa.acno
group by aa.acno,aa.fltno,aa.date) b
on a.fltno=b.bfltno and a.date=b.bdate
where a.count1>=b.capacity;
```

#### Answer:
```
acno |	fltno	| date	
---- | ----- | -------
N173WY |	2	|4-1
N173WY |	5	|4-1
```



#### Question 4:
Print a list of passengers with more than one ticket.

SQL:
```
select name 
from passengers 
where passid in
(
select a.passid
from 
(
    select passid, count(passid) as ticket_booked
    from pass_ticketed
    group by passid
) a
where a.ticket_booked>1
) 
;
```

#### Answer:
```
name	
Simpson, Richard
Halverson, Ranette
Carpenter, Stewart
Mouse, Mickey
Duck, Donald
Moose, Bullwinkle
Wayne, John
Mazurki, Mike
Marvin, Lee
Lamour, Dorothy
```




#### Question 5:
Print a list of passengers with more than one ticket on the same day.

SQL:
```
select name 
from passengers 
where passid 
in 
(
select a.passid
from 
(
select passid, count(passid) as ticket_booked,date 
from pass_ticketed
group by passid,date
)  a
)
;
```

#### Answer:
```
name	
Simpson, Richard
Halverson, Ranette
Carpenter, Stewart
Griffin, Terry
Hinds, Bill
Mouse, Mickey
Duck, Donald
Bunny, Bugs
Moose, Bullwinkle
Fudd, Elmer
Wayne, John
Mazurki, Mike
Marvin, Lee
Romero, Cesar
Lamour, Dorothy
```

#### Question 6:
Print a list of flights that use aircraft N173WY.

SQL:
```
select acno,fltno 
from aircraft_assignments 
where acno='N173WY'
;
```

#### Answer:
```
acno | fltno	
---- | -----
N173WY |	2
N173WY |	5
N173WY |	1
N173WY |	4
```

#### Question 7:
Print a list of pilots who fly on April 1.

SQL:
```
select distinct p.name
from pilots p
join pilot_assignments pa
on p.pilotid=pa.pilotid
where pa.date='4-1'
;
```

#### Answer:
```
name	
Wright, Orville
Post, Wiley
Lindergh, Charles
Yeager, Chuck
```



#### Question 8:
Print a list of pilots who fly on both days.

SQL:
```
select name 
from pilots
where pilotid 
in
(
select pilotid
from pilot_assignments
where date='4-2' and pilotid 
in
(
    select pilotid
    from pilot_assignments
    where date='4-1'
)
)
;
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
select name
from pilots
where pilotid 
in
(
select pilotid 
from pilot_assignments
group by pilotid,date
having count(date)>1
)
;
```

#### Answer:
```
name	
Wright, Orville
Lindergh, Charles
Post, Wiley
Lovell, James
Wittman. Steve
```

#### Question 10:
Print a List of flights that do not have a complete crew.

SQL:
```
select aaa.acno,aaa.type,aaa.capacity,aaa.pilots,a1.pilotassigned
from aircraft aaa
join 
(
select acno,a.fltno,a.date,a.count1 as pilotassigned
from aircraft_assignments aa
join 
(
select fltno,date, count(pilotid) as count1
from pilot_assignments
group by fltno,date
) a
on aa.fltno=a.fltno and aa.date=a.date
) a1
on aaa.acno=a1.acno    
where aaa.pilots>a1.pilotassigned
;
```

#### Answer:
```
acno	|type |	capacity |	pilots |	pilotassigned	
---- | ---- | -------- | ------- | --------------
N412B	|DC-3 |	21 |	2 |	1
N747UA	|B-747 |	300 |	3 |	2
N412B	|DC-3 |	21 |	2 |	1
```


#### Question 11:
Print of list of flights where destination is DFW.

SQL:
```
select * 
from flights
where destination='DFW'
;
```

#### Answer:
```
fltno |	date |	origin |	destination	
----- |----- | ------- | ------------
4 |	4-1 |	DIA |	DFW
5 |	4-1 |	ORD |	DFW
6 |	4-2 |	LAX |	DFW
4 |	4-2 |	DIA |	DFW
5 |	4-2 |	ORD |	DFW
```


#### Question 12:
Print a list of flights where origin or destination is LAX.

SQL:
```
select * 
from flights
where origin = 'LAX' or destination='LAX'
;
```

#### Answer:
```
fltno |	date |	origin |	destination	
----- | ---- | ------ | ------------
3 |	4-1 |	DFW |	LAX
6 |	4-2 |	LAX |	DFW
3 |	4-2 |	DFW |	LAX
```


#### Question 13:
Print the origin and destination of flights with passenger equals Duck, Donald or Wayne, John.

SQL:
```
select origin,destination
from flights f
join (
select distinct fltno,date
from pass_ticketed pt
join passengers p
on pt.passid=p.passid
where p.name like '%DUCK%'
OR p.name like '%Donald%'
or p.name like '%Wayne%'
or p.name like '%John%'
) a
on f.fltno=a.fltno and f.date=a.date
;
```

#### Answer:
```
origin |	destination	
------ | ------------
DFW |	LAX
DIA |	DFW
ORD |	DFW
LAX |	DFW
```

#### Question 14:
Print a list of flight numbers and origins.

SQL:
```
select  distinct fltno,origin
from flights
;
```

#### Answer:
```
fltno |	origin
----- | ------
1 |	DFW
2 |	DFW
3 |	DFW
4 |	DIA
5 |	ORD
6 |	LAX
```

#### Question 15:
Print a list of aircraft types from equipment assigned where pilot number=1030.

SQL:
```
SELECT distinct a.acno, a.type
FROM aircraft a
JOIN aircraft_assignments aa ON a.acno = aa.acno
JOIN pilot_assignments pa ON aa.fltno = pa.fltno
WHERE pa.pilotid =1030
;
```

#### Answer:
```
acno |	type	
---- | -----
N35A |	B-18
N173WY |	C-172
```

#### Question 16:
Print a list of pilots who fly with at least two other pilots.

SQL:
```
select p.Name,p.pilotid,aa.date,aa.fltno
from aircraft_assignments aa
join pilot_assignments pa
on aa.date=pa.date and aa.fltno=pa.fltno
join aircraft a
on a.acno=aa.acno
join pilots p
on p.pilotid=pa.pilotid
where a.pilots>=3
;
```

#### Answer:
```
Name |	pilotid |	date |	fltno	
-----| ------- | ----- | --------
Boyington, | Greg |	2033 |	4-2 |	3
Hoover, | Bob |	3102 |	4-2 |	3
```

#### Question 17:
Print a list of pilots who fly only one type of plane.

```
Note: I tried a lot to solve the query but I don't think I got the right 
answer but I got a query and answer which seem appropriate.
```

SQL:
```
select name 
from pilots p
join 
(
select pilotid,fltno,date,count(fltno) uniq
from pilot_assignments
group by pilotid
having uniq=1
) a
on a.pilotid=p.pilotid
```

#### Answer:
```
name	
Boyington, Greg
Hoover, Bob
```

#### Question 18:
Print a list of passengers booked on flights assigned to pilot=1030.

SQL:
```
select name 
from passengers 
where passid in 
(
select p.passid
from pass_ticketed p
join pilot_assignments pa
on p.fltno=pa.fltno and p.date=pa.date
where pa.pilotid=1030
)
;
```

#### Answer:
```
name	
Simpson, Richard
Halverson, Ranette
Carpenter, Stewart
Griffin, Terry
```

#### Question 19:
Print a list of pilots assigned to fly plane=N35A.

SQL:
```
select name 
from pilots
where pilotid 
in
(
select distinct pilotid
from pilot_assignments pa
join aircraft_assignments aa
on pa.fltno=aa.fltno and pa.date=aa.date
where aa.acno='N35A'
)
;
```

#### Answer:
```
name	
Wright, Orville
Post, Wiley
Lovell, James
Wittman. Steve
```


