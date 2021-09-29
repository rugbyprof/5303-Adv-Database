# Schema Discussion

This was the result of our in class discussion about normalizing your data from the IMDB data files.

## People

### Table: name.basics.ts

This collection of people data will result in the creation of:
- A Persons table (of course)
- Professions Table : contains unique profession names and id's
- Persons Professions: 1 to many relationship between a person and 1 or more professions 
- Known For : A table with a 1 to many relationship between a person and 1 or more movie id's

Original Columns:

| nconst    | primaryName  | birthYear | deathYear | primaryProfession              | knownForTitles                          |
| :-------- | :----------- | :-------- | :-------- | :----------------------------- | :-------------------------------------- |
| nm0000001 | Fred Astaire | 1899      | 1987      | soundtrack,actor,miscellaneous | tt0072308,tt0053137,tt0050419,tt0031983 |

#### Adjustments

- Id, Birth, Died were all ok as is
- Name is split into multiple fields
- primaryProfession split into other table 
- knownForTitles split into other table
  
#### Example adjusted table:

| nid   | First  | Last    | Birth | Died |
| :---- | :----- | :------ | :---- | :--- |
| n0004 | John   | Belushi | 1949  | 1982 |
| n0005 | Ingmar | Bergman | 1918  | 2007 |


### Professions Table

- Table of all professions and corresponding id

| nid  | profession |
| :--- | :--------- |
| p001 | actor      |
| p002 | soundtrack |
| p003 | writer     |
| p004 | director   |

### Persons Profession

- Table associating one or more professions with a person

| nid  | profession |
| :--- | :--------- |
| n004 | p001       |
| n004 | p002       |
| n004 | p003       |
| n005 | p003       |
| n005 | p004       |
| n005 | p001       |

### KnownFor

| nid  | mid  |
| ---- | ---- |
| n004 | m003 |
| n004 | m004 |
| n004 | m006 |
| n004 | m100 |
| n005 | m200 |
| n005 | m201 |
| n005 | m202 |
| n005 | m300 |


## Movies

### Table: title.basics.ts

This collection of movie data will result in the creation of:
- A movies table (of course)
- Genres Table : contains unique genres and id's
- Movie Genres: 1 to many relationship between a movie and 1 or more genres 


Original Columns:

 | tconst    | titleType | primaryTitle           | originalTitle          | isAdult | startYear | endYear | runtimeMinutes | genres            |
 | :-------- | :-------- | :--------------------- | :--------------------- | :------ | :-------- | :------ | :------------- | :---------------- |
 | tt0000001 | short     | Carmencita             | Carmencita             | 0       | 1894      | \N      | 1              | Documentary,Short |
 | tt0000002 | short     | Le clown et ses chiens | Le clown et ses chiens | 0       | 1892      | \N      | 5              | Animation,Short   |

- tconst =  mid
- titleType is now category id and category is in its own table
- Got rid of extra title and end year.
- genre split into another table
  
Example adjusted table:

 | mid   | Title                  | isAdult | year | runtimeMinutes |
 | :---- | :--------------------- | :------ | :--- | :------------- |
 | m0001 | Carmencita             | 0       | 1894 | 1              |
 | m0001 | Le clown et ses chiens | 0       | 1892 | 5              |


### Genres Table

- Table of all categories and corresponding id

| gid   | genre   |
| :---- | :------ |
| g001 | Action  |
| g002 | Drama   |
| g003 | Romance |

### Movie Genres

- Table associating a movie with one or more categories

| mid   | gid   |
| :---- | :---- |
| m0001 | g001 |
| m0001 | g002 |
| m0002 | g001 |


