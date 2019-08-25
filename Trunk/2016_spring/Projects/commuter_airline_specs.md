# Airport Reservation System

## Spring 2015

### Description


You will design and implement a simple interactive system based on a relational database that will support a small regional airline and its flight management and reservation functions. 


### Specifications / Requirements:

This system will manage a small regional commuter airline network. 

- There are daily flights between different cities that fly at the same time each day (for example, there is a daily flight from Wichita Falls, TX to Oklahoma City, OK at 1:00pm). 
- Each flight arrives at its destination at the same time each day. 
- Each flight is assigned a particular type of aircraft, such as a Boeing 727, and each aircraft type has a particular set of seat numbers and seating capacity. 
- Also each flight has a certain fare which will depend on the seat class (coach, business, or first class), and also on the day of the week it flies.

The airline plans to offer an online system to its prospective passengers, allowing them to enter preferences concerning reservations they want to make. For example, a passenger will be able to enter a request for a reservation on a flight that goes from Wichita Falls to Amarillo next Tuesday or Wednesday morning. The passenger wants to fly business class, eat a kosher meal and sit in a window seat. So the options are: 
- a desired source and destination, 
- a preferred time to fly, 
- a meal preference (kosher, vegetarian, regular), 
- a preferred seat (aisle, window), 
- and a preferred flight class (coach, business, first class.)
- It is highly likely that the same passenger may make multiple reservations on multiple flights over a reasonable period of time.

Operations that will have to be performed include the following. A prospective passenger can enter or modify a reservation preference. A prospective passenger can query to see if a particular flight has not been canceled and has available seats in various classes. An airline representative can add new flights with all their necessary information of source and destination location and times, aircraft type assigned to a flight, fares, etc. An airline representative can alter properties of a flight, and in particular can cancel a particular flight, such as next Thursday's flight from Wichita Falls to Houston. An airline representative can also query to find what passengers have reservations on what flights.

There will also be the ability for a passenger to see what flights meet his or her stated preferences, or to see whether a particular flight is full. There will also be a facility to make a reservation.

This classification does not imply any particular table arrangement. You are responsible for arranging the data items into tables, determining the relationships among tables and identifying the key attributes. 

You should include indices in your tables to speed up query processing. You should base your choice of indices on the type and expected frequency of the queries. Finally, you should specify and enforce integrity constraints on the data.

You will create your relational model using Mysql Workbench or Phpmyadmin Designer. 


![](https://s3.amazonaws.com/f.cl.ly/items/2R0q41330k2k0N1O2G31/diagram.png)

### Data / Actions

#### Passengers

1. UUID
2. Last Name
3. First Name
4. Street Address
5. City
6. State
7. Zip Code
1. Credit Card No.
1. Expiration month
1. Expiration year
1. CVC Code
1. E-Mail Address
1. Password
1. Contact Phone
1. Flight number
1. Flight date 
1. The seat number
1. The meal type the passenger will be served (kosher, vegetarian, etc.). 

#### Reservations

1. Flight number
1. Flight date 
1. The seat number
1. The meal type the passenger will be served (kosher, vegetarian, etc.).
1. Cost (based on price of jet

#### Aircraft

1. Tail Number (tail numbers are unique for all aircraft)
1. Manufacture
1. Model
1. Capacity (Number of passengers)
1. Status (1 = Good, 0 = Being Repaired)
1. Airline


#### Flights

1. From 
2. To
3. Tail Number 
4. Status (delayed, ontime, cancelled)
5. Departure Time
6. Arrival Time

### Transaction Support

#### Customer Transactions

* Register with system
* Make or Change a reservation
* Lookup a reservation
* Cancel a reservation
* Customers should not have access to any data accept their own

### Admin Transactions

* Add / Edit / Delete Aircraft from system
* Add / Edit / Delete Flights from the system
* Generate passenger manifests
* Change the status of an Aircraft
* Change the status of a Flight
* Add flights to the system

More when we talk...
