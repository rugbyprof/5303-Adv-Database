http://sqlzoo.net/w/index.php?title=More_JOIN_operations&oldid=13943

movie
Field name	Type	Notes
id	INTEGER	An arbitrary unique identifier
title	CHAR(70)	The name of the film - usually in the language of the first release.
yr	DECIMAL(4)	Year of first release.
director	INT	A reference to the actor table.
budget	INTEGER	How much the movie cost to make (in a variety of currencies unfortunately).
gross	INTEGER	How much the movie made at the box office.
Example
id	title	yr	director	budget	gross
10003	"Crocodile" Dundee II	1988	38	15800000	239606210
10004	'Til There Was You	1997	49	10000000	
actor
Field name	Type	Notes
id	INTEGER	An arbitrary unique identifier
name	CHAR(36)	The name of the actor (the term actor is used to refer to both male and female thesps.)
Example
id	name
20	Paul Hogan
50	Jeanne Tripplehorn
casting
Field name	Type	Notes
movieid	INTEGER	A reference to the movie table.
actorid	INTEGER	A reference to the actor table.
ord	INTEGER	The ordinal position of the actor in the cast list. The
star of the movie will have ord value 1 the co-star will have
value 2, ...
Example
movieid	actorid	ord
10003	20	4
10004	50	1


##1

List the films where the yr is 1962 [Show id, title]

```
SELECT id, title
 FROM movie
 WHERE yr=1962
```
##2
Give year of 'Citizen Kane'.

```
SELECT yr
FROM movie
WHERE title like 'Citizen Kane'
```
##3

List all of the Star Trek movies, include the id, title and yr (all of these movies include the words Star Trek in the title). Order results by year.

```
SELECT id, title, yr
FROM movie
WHERE title LIKE '%Star%Trek%'
ORDER BY yr
```

##4
What are the titles of the films with id 11768, 11955, 21191
```
SELECT title
FROM movie
WHERE id IN ('11768','11955','21191')
```


##5

What id number does the actress 'Glenn Close' have?

```
SELECT id
FROM actor
WHERE name LIKE 'Glenn Close'
```

##6

What is the id of the film 'Casablanca'
 

```
SELECT id
FROM movie
WHERE title LIKE 'Casablanca'
```

##7

Obtain the cast list for 'Casablanca'.
what is a cast list?
Use movieid=11768, this is the value that you obtained in the previous question.

```
SELECT B.name
FROM movie A, actor B, casting C
WHERE C.movieid = '11768'
AND B.id = C.actorid
AND A.id = C.movieid
```
##8

Obtain the cast list for the film 'Alien'

```
SELECT B.name
FROM movie A, actor B, casting C
WHERE C.movieid = A.id
AND B.id = C.actorid
AND A.title = 'Alien'
```

##9

List the films in which 'Harrison Ford' has appeared

```
SELECT B.title
FROM actor A, movie B, casting C
WHERE A.name = 'Harrison Ford' 
AND B.id = C.movieid
AND A.id = C.actorid
```

##10

List the films where 'Harrison Ford' has appeared - but not in the starring role. [Note: the ord field of casting gives the position of the actor. If ord=1 then this actor is in the starring role]

```
SELECT B.title
FROM actor A, movie B, casting C
WHERE A.name = 'Harrison Ford' 
AND B.id = C.movieid
AND A.id = C.actorid
AND C.ord <> 1
```

##11
List the films together with the leading star for all 1962 films.

```
SELECT A.title, B.name
FROM movie A, actor B, casting C
WHERE A.id = C.movieid
AND A.yr = '1962'
AND C.ord = '1'
AND C.actorid = B.id
```
##12
Which were the busiest years for 'John Travolta', show the year and the number of movies he made each year for any year in which he made more than 2 movies.

```
SELECT yr,COUNT(title) FROM
  movie JOIN casting ON movie.id=movieid
         JOIN actor   ON actorid=actor.id
WHERE name='John Travolta'
GROUP BY yr
HAVING COUNT(title)=(SELECT MAX(c) FROM
(SELECT yr,COUNT(title) AS c FROM
   movie JOIN casting ON movie.id=movieid
         JOIN actor   ON actorid=actor.id
 WHERE name='John Travolta'
 GROUP BY yr) AS t
)
```

##13

List the film title and the leading actor for all of the films 'Julie Andrews' played in.

```
SELECT m.title,a.name
FROM movie m,actor a,casting c
WHERE m.id IN (
     SELECT m.id
     FROM movie m, actor a, casting c
     WHERE a.name = 'Julie Andrews'
     AND a.id = c.actorid
     AND m.id = c.movieid)
AND c.ord = '1'
AND a.id = c.actorid
AND m.id = c.movieid
```


```
SELECT DISTINCT m.title, a.name
FROM (SELECT movie.*
      FROM movie
      JOIN casting
      ON casting.movieid = movie.id
      JOIN actor
      ON actor.id = casting.actorid
      WHERE actor.name = 'Julie Andrews') AS m
JOIN (SELECT actor.*, casting.movieid AS movieid
      FROM actor
      JOIN casting
      ON casting.actorid = actor.id
      WHERE casting.ord = 1) as a
ON m.id = a.movieid
ORDER BY m.title;
```

##14

Obtain a list, in alphabetical order, of actors who've had at least 30 starring roles.

```
SELECT actor.name
FROM actor
JOIN casting
ON casting.actorid = actor.id
WHERE casting.ord = 1
GROUP BY actor.name
HAVING COUNT(*) >= 30;
```
##15

List the films released in the year 1978 ordered by the number of actors in the cast.

```
SELECT movie.title,COUNT(casting.actorid) as ActorCount
FROM movie
JOIN casting
ON casting.movieid = movie.id
WHERE movie.yr = '1978'
GROUP BY movie.id
ORDER BY ActorCount DESC
```

##16
List all the people who have worked with 'Art Garfunkel'.

```
SELECT a.name
  FROM (SELECT movie.*
          FROM movie
          JOIN casting
            ON casting.movieid = movie.id
          JOIN actor
            ON actor.id = casting.actorid
         WHERE actor.name = 'Art Garfunkel') AS m
  JOIN (SELECT actor.*, casting.movieid
          FROM actor
          JOIN casting
            ON casting.actorid = actor.id
         WHERE actor.name != 'Art Garfunkel') as a
    ON m.id = a.movieid;
```

```
SELECT actor.name
FROM casting,actor
WHERE casting.movieid IN(
    SELECT casting.movieid
    FROM casting, actor
    WHERE actor.name = 'Art Garfunkel'
    AND casting.actorid = actor.id)
AND casting.actorid = actor.id
AND actor.name <> 'Art Garfunkel'
```

