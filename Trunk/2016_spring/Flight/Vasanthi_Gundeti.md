### Title: Sql Flight Assignment
### Name: Vasantha Gundeti

#### Question 1:
Print a passenger list for flight 3 on 4-1

SQL:
'''
select name
from passengers 
join pass_ticketed on passengers.passid=pass_ticketed.passid
where fltno='3' and date='4-1'
'''

#### Answer:
'''
name
Duck, Donald
Wayne, John
Mazurki, Mike
Marvin, Lee
Romero, Cesar
Lamour, Dorothy
'''

####Question 2:
Print a passenger list for flight 5 on 4-2

SQL:
'''
select name
from passengers join pass_ticketed on passengers.passid=pass_ticketed.passid
where fltno='5' and date='4-2'
'''

####Answer:
'''
name
Mouse, Mickey
Moose, Bullwinkle
'''

####Question 3:
Print a list of all overbooked flights

SQL:
'''
'''

####Answer:
'''
'''

####Question 4:
Print a list of passengers with more than one ticket

SQL:
'''
select passengers.name 
from passengers
join pass_ticketed on passengers.passid=pass_ticketed.passid
group by passengers.passid
having count(pass_ticketed.passid)>1 and count(date)>1
'''

####Answer:
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

####Question 5:
Print a list of passengers with more than one ticket on the same day.

SQL:
'''
select passengers.name 
from passengers
where passid in
(
select passid
from pass_ticketed 
group by passid, date
having count( * ) >1
)
'''

####Answer:
'''
Simpson, Richard
Carpenter, Stewart
Duck, Donald
Wayne, John
Marvin, Lee
Lamour, Dorothy
'''

####Question 6:
Print a list of flights that use aircraft N173WY.

SQL:
'''
select fltno
from aircraft_assignments 
join aircraft on aircraft.acno=aircraft_assignments.acno
where aircraft_assignments.acno='N173WY'
'''

####Answer:
'''
fltno
2
5
1
4
'''

####Question 7:
Print a list of pilots who fly on April 1.

SQL:
'''
select distinct name
from pilots 
join pilot_assignments on pilots.pilotid=pilot_assignments.pilotid
where date='4-1'
'''

####Answer:
'''
name
Wright, Orville
Post, Wiley
Lindergh, Charles
Yeager, Chuck
'''

####Question 8:
Print a list of pilots who fly on both days

SQL:
'''
select name 
from pilots 
join pilot_assignments on pilot_assignments.pilotid=pilots.pilotid
group by pilot_assignments.pilotid 
having count(fltno)>=2 and count(distinct date)= 2
'''

####Answer:
'''
name
Yeager, Chuck
Wright, Orville
Post, Wiley
'''


####Question 9:
Print a list of pilots who have two flights on the same day.

SQL:
'''
select pilot_assignments.pilotid,date 
from pilot_assignments 
join pilots on pilot_assignments.pilotid=pilots.pilotid
group by pilot_assignments.pilotid 
having count(fltno)>=2 and count(distinct date)<= 2
'''
####Answer:
'''
pilotid date
29    4-2
241   4-2
1030  4-2
2137  4-1
4315  4-2
7305  4-1
'''

####Question 10:
Print a List of flights that do not have a complete crew.

SQL:
'''
'''
####Answer:
'''
'''

####Question 11:
Print of list of flights where destination is DFW.

SQL:
'''
select distinct fltno
from flights
where destination='dfw'
'''

####Answer:
'''
fltno
4
5
6
'''


####Question 12:
Print a list of flights where origin or destination is LAX

SQL:
'''
select distinct fltno
from flights
where origin='lax' or destination='lax'
'''

####Answer:
'''
fltno
3
6
'''

####Question 13:
Print the origin and destination of flights with passenger equals Duck, Donald or Wayne, John.

SQL:
'''
select distinct origin, destination
from flights 
join pass_ticketed ON flights.fltno = pass_ticketed.fltno
join passengers ON pass_ticketed.passid = passengers.passid
where name =  'Duck, Donald'
or name =  'Wayne, John'
'''

####Answer:
'''
origin	destination	
DFW	  LAX
LAX	  DFW
ORD	  DFW
DIA	  DFW
'''

####Question 14:
Print a list of flight numbers and origins.

SQL:
'''
select distinct fltno,origin
from flights
'''
####Answer:
'''
fltno origin
1   DFW
2   DFW
3   DFW
4   DIA
5   ORD
6   LAX
'''


####Question 15:
Print a list of aircraft types from equipment assigned where pilot number=1030.

SQL:
'''
select distinct type
from aircraft
join aircraft_assignments on aircraft_assignments.acno=aircraft.acno
join pilot_assignments on pilot_assignments.fltno=aircraft_assignments.fltno
where pilotid='1030'
'''
####Answer:
'''
type
B-18
C-172
'''

####Question 16:
Print a list of pilots who fly with at least two other pilots.

SQL:
'''
select name 
from pilots 
join aircraft on aircraft_assignments.acno=aircraft.acno
join pilot_assignments on pilot.pilotid=pilot_assignments.pilotid
join aircraft_assignments on pilot_assignments.fltno=aircraft_assignments.fltno
where pilots>=3
'''

####Answer:
'''
'''


####Question 17:
Print a list of pilots who fly only one type of plane.

SQL:
'''
'''
####Answer:
'''
'''

####Question 18:
Print a list of passengers booked on flights assigned to pilot=1030.

SQL:
'''
select distinct name
from passengers
join pass_ticketed on passengers.passid=pass_ticketed.passid 
join pilot_assignments on pass_ticketed.fltno=pilot_assignments.fltno
where pilotid='1030'
'''

####Answer:
'''
name
Simpson, Richard
Halverson, Ranette
Griffin, Terry
Bunny, Bugs
Carpenter, Stewart
Wayne, John
'''

####Question 19:
Print a list of pilots assigned to fly plane=N35A.

SQL:
'''
select distinct name
from pilots
join pilot_assignments on pilots.pilotid=pilot_assignments.pilotid
join aircraft_assignments on aircraft_assignments.fltno=pilot_assignments.fltno
join aircraft on aircraft.acno=aircraft_assignments.acno
where aircraft.acno='N35A'
'''

####Answer:
'''
name
Wright, Orville
Post, Wiley
Lindergh, Charles
Lovell, James
Wittman. Steve
'''






