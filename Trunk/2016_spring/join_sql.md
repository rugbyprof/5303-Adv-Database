http://sqlzoo.net/w/index.php?title=The_JOIN_operation&oldid=13614

game
id	mdate	stadium	team1	team2
1001	8 June 2012	National Stadium, Warsaw	POL	GRE
1002	8 June 2012	Stadion Miejski (Wroclaw)	RUS	CZE
1003	12 June 2012	Stadion Miejski (Wroclaw)	GRE	CZE
1004	12 June 2012	National Stadium, Warsaw	POL	RUS
...

goal
matchid	teamid	player	gtime
1001	POL	Robert Lewandowski	17
1001	GRE	Dimitris Salpingidis	51
1002	RUS	Alan Dzagoev	15
1001	RUS	Roman Pavlyuchenko	82
...

eteam
id	teamname	coach
POL	Poland	Franciszek Smuda
RUS	Russia	Dick Advocaat
CZE	Czech Republic	Michal Bilek
GRE	Greece	Fernando Santos
...

## 1
The first example shows the goal scored by 'Bender'.
Show matchid and player name for all goals scored by Germany. `teamid = 'GER'`

```sql
SELECT matchid,player FROM goal 
  WHERE teamid = 'GER'
```
## 2
From the previous query you can see that Lars Bender's goal was scored in game 1012. Notice that the column matchid in the goal table corresponds to the id column in the game table.

Show id, stadium, team1, team2 for game 1012

```sql
SELECT id,stadium,team1,team2
  FROM game 
 WHERE id = '1012'
```

## 3
You can combine the two steps into a single query with a JOIN. You will get all the game details and all the goal details if you use

```
SELECT *
  FROM game JOIN goal ON (id=matchid)
```

Show the player, teamid and mdate and for every German B. `teamid='GER'`

```
SELECT player, teamid , mdate
  FROM game JOIN goal ON (id=matchid)
WHERE teamid='GER'
```
```
SELECT B.player, B.teamid , A.mdate
  FROM game A  JOIN goal B ON (A.id=B.matchid)
WHERE B.teamid='GER'
```

## 4


Use the same JOIN as in the previous question.

Show the team1, team2 and player for every goal scored by a player called Mario `player LIKE 'Mario%'`

```
SELECT A.team1, A.team2 , B.player
  FROM game A  JOIN goal B ON (A.id=B.matchid)
WHERE player LIKE 'Mario%'
```


## 5 

The table eteam gives details of every national team including the coach. You can JOIN goal to eteam using the phrase goal JOIN eteam on teamid=id

Show player, teamid, coach, gtime for all goals scored in the first 10 minutes `gtime<=10`

```
SELECT A.player, A.teamid,B.coach,  A.gtime
  FROM goal A  JOIN eteam B ON (A.teamid=B.id)
 WHERE A.gtime<=10
 ```

```
SELECT A.player, A.teamid,B.coach,  A.gtime
  FROM goal A , eteam B
 WHERE A.gtime<=10
AND A.teamid = B.id
```

## 6

To JOIN game with eteam you could use either
game JOIN eteam ON (team1=eteam.id) or game JOIN eteam ON (team2=eteam.id)
Notice that because id is a column name in both game and eteam you must specify eteam.id instead of just id

List the the dates of the matches and the name of the team in which 'Fernando Santos' was the team1 coach.

```
select A.mdate,B.teamname
FROM game A, eteam B
WHERE A.team1 = B.id
AND B.coach = 'Fernando Santos'
```


## 7

List the player for every goal scored in a game where the stadium was 'National Stadium, Warsaw'

```
SELECT A.player 
FROM goal A, game B
WHERE B.stadium = 'National Stadium, Warsaw'
AND A.matchid = B.id
```


## 8

The example query shows all goals scored in the Germany-Greece quarterfinal.
Instead show the name of all players who scored a goal against Germany.

HINT
Select goals scored only by non-German players in matches where GER was the id of either team1 or team2.
You can use teamid!='GER' to prevent listing German players.
You can use DISTINCT to stop players being listed twice.

```
SELECT distinct(B. player)
FROM game A, goal B
WHERE A.id = B.matchid
AND (A.team1 = 'GER' OR A.team2 = 'GER')
AND B.teamid != 'GER'
```

## 9

Show teamname and the total number of goals scored.
COUNT and GROUP BY
You should COUNT(*) in the SELECT line and GROUP BY teamname

```
SELECT teamname , count(teamid)
  FROM eteam JOIN goal ON id=teamid
 GROUP BY teamname
```

## 10

Show the stadium and the number of goals scored in each stadium.

```
SELECT A.stadium, count(B. matchid)
FROM game A, goal B
WHERE A.id = B.matchid
GROUP BY A.stadium
```


## 11

For every match involving 'POL', show the matchid, date and the number of goals scored.

```
SELECT matchid, mdate, COUNT(*)
FROM game JOIN goal ON matchid = id
WHERE (team1 = 'POL' OR team2 = 'POL')
GROUP BY matchid
```


## 12

For every match where 'GER' scored, show matchid, match date and the number of goals scored by 'GER'


```
SELECT B.matchid, A.mdate, count(B.matchid)
FROM game A, goal B
WHERE B.teamid = 'GER'
AND A.id = B.matchid
GROUP BY B.matchid
```

```
SELECT matchid, mdate, COUNT(*)
FROM goal JOIN game ON matchid = id
WHERE teamid = 'GER'
GROUP BY matchid
```

## 13

```
SELECT A.mdate, 
       A.team1, 
       SUM(CASE WHEN B.teamid = A.team1
           THEN 1
           ELSE 0
           END) AS score1,
       A.team2,
       SUM(CASE WHEN B.teamid = A.team2
           THEN 1
           ELSE 0
           END) AS score2
FROM game A, goal B
WHERE A.id = B.matchid
GROUP BY A.id
ORDER BY A.mdate, B.matchid, A.team1, A.team2
```

```
SELECT mdate,
  team1,
 SUM( CASE WHEN teamid=team1 THEN 1 ELSE 0 END) score1,
team2,
 SUM(CASE WHEN teamid=team2 THEN 1 ELSE 0 END) score2
  FROM game JOIN goal ON matchid = id
GROUP BY id
ORDER BY mdate,matchid,team1,team2
```