SELECT distinct(stadium)
FROM game
WHERE (team1 = 'GRE' OR team2 = 'GRE')
AND game.id NOT IN (
SELECT matchid
FROM goal
WHERE goal.player = 'Dimitris Salpingidis')
