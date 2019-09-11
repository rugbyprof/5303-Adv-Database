## Example Queries and Scripts 

#### Scripts

- [insert_data.php](./insert_data.php)
- [load_cities.php](./load_cities.php)

#### Joins

<sup> Ref: https://en.wikipedia.org/wiki/Join_(SQL) </sup>


<img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/table_join_syntax.jpg" width="400">


***Inner Join***

<sup> Ref: https://en.wikipedia.org/wiki/Join_(SQL)#Inner_join</sup>

```sql
SELECT plane_codes.*, 
       planes.NAME 
FROM   plane_codes 
       INNER JOIN planes 
               ON plane_codes.pid = planes.id 
```

```sql
SELECT * 
FROM   `airlines` 
       INNER JOIN world_codes 
               ON `world_codes`.id = `airlines`.`code` 
```


#### Derived Table 

<sup>Ref: http://www.mysqltutorial.org/mysql-derived-table/</sup>

A derived table is a query that performs an intermediate query for a multitude of reasons.
It my be that it is joining multiple tables to "collect" data into one place, then allowing
you to query that concise data set. 

```sql
SELECT Count(*) 
FROM   (SELECT * 
        FROM   `airlines` 
        WHERE  active = 'Y' 
               AND country = 'United States') AS derived_table_alias 
```

#### Sub Select

<sup>Ref: http://www.mysqltutorial.org/mysql-subquery/</sup>

Find all the routes that have a destination airport somewhere in the pacific time zone.
```sql
SELECT * 
FROM   routes 
WHERE  dest_ap_id IN (SELECT airport_id 
                      FROM   `airports` 
                      WHERE  tz LIKE '%Pacific%') 
```


#### Derived Table + Sub Select

Find the plane name for a plane with the code 'CR2'
This could be done way easier. Just giving compound examples. 

```sql
SELECT name 
FROM   (SELECT `plane_codes`.*, 
               `planes`.name 
        FROM   `plane_codes` 
               INNER JOIN `planes` 
                       ON `plane_codes`.pid = `planes`.id) AS alias 
WHERE  code = 'CR2' 
```

#### Union Example

This example combines both of the different code types into a single list of IATA and ICAO codes.

```sql
SELECT code 
FROM   (SELECT DISTINCT( iata ) AS code 
        FROM   `airports`) AS alias 
UNION 
SELECT code 
FROM   (SELECT DISTINCT( icao ) AS code 
        FROM   `airports`) AS alias2  
```


#### Insert Into

```sql
INSERT INTO `airline_codes` 
            (`airline_codes`.`aid`, 
             `airline_codes`.`iata`, 
             `airline_codes`.`icao`) 
SELECT `airlines`.`airline_id`, 
       `airlines`.`iata`, 
       `airlines`.`icao` 
FROM   `airlines` 
```

#### Update 

```sql
UPDATE `airlines`, 
       `world_codes` 
SET    `airlines`.`code` = `world_codes`.`id` 
WHERE  `airlines`.`iata` = `world_codes`.`iata` 
       AND `airlines`.`icao` = `world_codes`.`icao` 
```

