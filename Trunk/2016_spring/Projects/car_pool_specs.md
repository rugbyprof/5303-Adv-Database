## Car Pool Management System

### Requirements specification

We will design and implement a simple interactive with a relational database backend that implements a car pooling management system. The project will be split in four parts. The first part will be done individually (so that everyone will have to think over the design of the system and have a good understanding of the problems involved). The next three parts will be done in groups of two students (so that everyone can have someone else in class to share the happy and unhappy experiences during the implementation).

This system will manage information for both daily commutes and non-daily trips. It will have a registration process that collects required information about a user and provides services afterward for updating required information, adding/deleting/updating requests and other information, querying information, matching requests, etc.

The registration process needs to be completed by all users prior to use of any of the provided services. During this registration, the following required information will be collected:

* login name
* password
* last name
* first name
* status (student resident / student commuter / faculty / staff)
* if student commuter or faculty or staff: 
    * residence address (street, town, state, zip code, nearest major intersection)
* if student resident: 
    * on campus address (street, room no)
* for student: major and status (freshman / sophomore / junior / senior / graduate)
* for faculty or staff: department and position
* contact phone number
* contract email address

Once registered, a user can change the required information and can add, change, or delete the following optional information of him or herself at any time. Personal information:

* age
* sex
* cars owned (manufacturer, model, year)
* smoker / non smoker
* preference (driver only / share driving / passenger only)
* range of cost compensation requested / offered
* if student commuter or faculty or staff: current method of commuting (drive alone / bus / train / car pool / other).

For daily commutes: a valid time frame (semester), and the following information daily or for some days of the week:

* start and end times
* flexibility arrival and departure times (yes / no) and by how many minutes
For non-daily trips, the following information:
* date of trip
* reason of trip (e.g., football game)
* from and to addresses
* departure and / or arrival times
* flexibility arrival and / or departure times (yes / no) and by how many minutes
* ride offered / requested
* if ride offered: car and maximum number of passengers
* if ride requested: number of passengers
* range of cost compensation requested / offered
* notes

Additional information (assuming we will put the system on the web):

* how did you find this system / website (friend / employer / internet site / newspaper)
* if previous is internet site: name the website
* comments

When new commutes or trips information is added, the system will automatically query existing information to report any matches. The system will allow the users to search by address, weekday / date, time, driver or passenger, a combination of them, etc. Obsolete information will be automatically deleted by the system.

The system will have a number of integrity constraints. For example:
- Each user can have at most one daily commute schedule
- Only car owners may offer rides
- The end time must be after start time
- etc.


* * *

**What to do?** Your task for the first project assignment is to use Mysql Workbench or Phpmyadmin Designer to create and design your database. 

More specifically:

- Create your tables with the correct data types and primary keys.
- Create the relationships between tables and necessary foreign keys.
- You must use one of the afore mentioned visualization tools to complete this task.

**Deliverables:** A digital document showing your DB design. Below is an example from Mysql Workbench:

![](https://s3.amazonaws.com/f.cl.ly/items/2R0q41330k2k0N1O2G31/diagram.png)

**Reminder:** You must work individually and the work you turn in must be your own.  