

## Sample Database

### game

|   id | mdate        | stadium                   | team1   | team2   |
|-----:|:-------------|:--------------------------|:--------|:--------|
| 1001 | 8 June 2012  | National Stadium Warsaw   | POL     | GRE     |
| 1002 | 8 June 2012  | Stadion Miejski (Wroclaw) | RUS     | CZE     |
| 1003 | 12 June 2012 | Stadion Miejski (Wroclaw) | GRE     | CZE     |
| 1004 | 12 June 2012 | National Stadium, Warsaw  | POL     | RUS     |


### goal

|   matchid | teamid   | player               |   gtime |
|----------:|:---------|:---------------------|--------:|
|     1001	 | POL      | Robert Lewandowski   |      17 |
|      1001 | GRE      | Dimitris Salpingidis |      51 |
|      1002 | RUS      | Alan Dzagoev         |      15 |
|      1001 | RUS      | Roman Pavlyuchenko   |     	82 |

### eteam

| id   | teamname       | coach            |
|:-----|:---------------|:-----------------|
| POL  | Poland         | Franciszek Smuda |
| RUS  | Russia         | Dick Advocaat    |
| CZE  | Czech Republic | Michal Bilek     |
| GRE  | Greece         | Fernando Santos  |


## Questions

1. You want to find the stadium where player 'Dimitris Salpingidis' scored.

2. List the the dates of the matches and the name of the team in which 'Fernando Santos' was the team1 coach.

3. List the player for every goal scored in a game where the stadium was 'National Stadium, Warsaw'