## Assignment 7 - Advising (with Mongo OR SQLite)
#### Due: 11-03-2021 (Wednesday @ 5:00 p.m.)

## Overview

Every semester students must make a schedule and get advised. A small software tool to search for existing classes in the current course schedule could be very convenient depending on the search mechanisms offered (more about this in the requirements). However, to perform something seemingly so simple will take more work than one might think, so be prepared. The customer just needs a database backend, and and API to interact with the database for now. You have a few choices for a database: Mongo, Mysql, or SQLite (for something new to learn). I will let each group choose the database that they are most comfortable with. Mongo and Mysql run quite well on a Mac instance, and SQLite is built for a small(ish) robust database completely stored in a local file! These all work well with the customers hardware requirements.

## Data Sources

In this folder there is a [schedules](schedules/README.md) folder that contains the pdf's and json versions of a semesters schedule. The processed pdf's are not 100% accurate, but there is enough consistency to build a **database of courses** with them. The most important data file is for the current or upcoming semester. Creating a historical database of courses and advising actions will be a nice bi-product of this project. In the [code_files](code_files/README.md) folder there is code to download and convert pdf's to json, but that is also not necessarily part of this project. I included it just in case we get to the point where "refreshing" our data becomes important.

Ultimately the goal is to "query" the schedule looking for courses that fit some search criteria. Thats why we will save as much course data as we can glean from the published pdf. 

### Course Info

* **Col**: Abbreviation of College
* **Crn**: Unique identifier for a course
* **Subj**: Subject of course (CMPS, NURS, etc.)
* **Crse**: Course number (4483, 1013, etc.)
* **Sect**: Section number (101,200,10x,etc.),
* **Title**: String title of course,
* **PrimaryInstructor**: Professors name,
* **Max**: Max enrollment (40, 30, etc.),
* **Curr**: Current enrollment (integer <= Max),
* **Aval**: Available seats (Max * Curr),
* **Days**: Days offered (TR, MWF, MW,etc.),
* **Begin**: Start time (1100am, 200pm, etc.),
* **End**: End time (1220pm, etc.)
* **Bldg**: Abbreviation for building (MY, FA, BO, etc.),
* **Room**: Room number (136, 127A, etc.)

Since one primary goal is to generate advising forms, we would need to store student information that could be used to populate form fields.

### Student Info

* First Name
* Last Name
* M Number
* Classification
* Email
* Gpa
* Github username


### Advising Form Info

The only "report" I have a requirement for right now is an advising form. This will list the courses a student was advised to take in a given semester. The user should be able to lookup past forms and create new ones.

* Semester
* Year
* Student
* List of Courses
* Date Created


## API Requirements

Let me list several possible "queries" or "actions" to help determine possible database design and api routes.

### POST

* Add course
* Add student
* Add advising form

### PUT

* Edit Course
* Edit Student
* Edit Form

### GET

#### Student Based Routes

* Get list of students
* Get students by:  
  * Name
  * M-Number
  * Gpa (equal to or greater / less than)

#### Course Based Routes

* Find course(s) by
  * `CRN` (unique id)
  * `Subj` (subject)
  * `Crse` (course number)
  * `Instructor Name`
  * `Bldg` (building)
  
* Find courses between `Begin`  & `End` times
* Find closed courses
* Find courses with a partial title search
* Find courses by `Bldg` (building) and `Room`

#### Advising Forms

* Find all advising forms
* Find form by student
* Find form by semester
* Find form by year
* Find form with any combination of above (student, semester, year)

## Interface

* This part is up to you. I will accept console based (with some minimum requirements), or GUI based, or Web based.
>Console and gui may not be platform independent. Ensuring your project runs on linux, mac, and windows is a big deal.

* The requirements for each teams interface will be slightly different depending on choice.

## Deliverables

### Database
- Initial choice and design: Oct 27<sup>th</sup>.
- Implementation and test data loaded: Nov 3<sup>rd</sup>

### API
- Initial choice and 50% of routes completed: Nov 3<sup>rd</sup>
- All routes completed: Nov 10<sup>th</sup>

### Interface
- Choice of console, gui, web: Oct 27<sup>th</sup>
- Initial design of interface with 20% working model: Nov 10<sup>th</sup>
- Completed project: Nov 17<sup>th</sup>

### Presentations

- Initial Choice discussion: Oct 27th
- 







