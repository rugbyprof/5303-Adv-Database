## Barebones Refactor - Worst Flight Planner Step 2
#### Due: Monday September 16 <sup>th</sup>

### Overview

The first step was to load our database of planes, airlines, airports, and routes. While doing so you should have started to get a little comfortable with the data and how each table relates to each other. I know I did, and was frustrated with how the tables were organized. We will discuss in class various ways the we could re-design the table structures aka `Normalize the data`. 

[Normalization](https://en.wikipedia.org/wiki/Database_normalization) simply means organize the data to reduce redundancy. 

Do I want you to `normalize` the database? Yes and no. I want you to totally re-factor its structure, meaning I care about redundancy, but I also care about unnecessary columns and whether or not they will help our ultimate goal of flight planning. 


### New Structure 

I want you to create a new set of tables with a different structure from the original. Use a different pre-fix in your database for this new set to keep them seperate from the original.

You can combine columns, eliminate columns, create new values to replace old possible compound values, etc.

Some points of interest:

- Do the IATA or ICAO codes help us in any way?
- Does storing the city name and country name in airports help us? 
- The plane codes. Do they help us?
- The routes table is really ... confusing.

I think you can come up with a cleaner structure using computed integer id's as a basis for almost every relationship between the tables. 

We will discuss this more in class.

#### Deliverables

- I will log in to phpmyadmin and see:
    - Newly redesigned tables populated with data
    - A different set of id's to create relationships between tables.
    - Appropriate data type assigned to each column
    - Primary keys assigned for each table


