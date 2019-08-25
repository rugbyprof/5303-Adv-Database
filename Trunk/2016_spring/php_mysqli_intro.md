## Php Mysql Intro
Source: http://codular.com/php-mysqli

### Connecting

```php
$db = new mysqli('localhost', 'user', 'pass', 'demo');

if($db->connect_errno > 0){
    die('Unable to connect to database [' . $db->connect_error . ']');
}
```

### Querying

```php
$sql = <<<SQL
    SELECT *
    FROM `users`
    WHERE `live` = 1 
SQL;

// or

$sql = "SELECT *
    FROM `users`
    WHERE `live` = 1 ";

if(!$result = $db->query($sql)){
    die('There was an error running the query [' . $db->error . ']');
}
```

### Output query results

```php
while($row = $result->fetch_assoc()){
    echo $row['username'] . '<br />';
}
```

### Number of returned rows

```php

echo 'Total results: ' . $result->num_rows;

```

### Number of affected rows

```php

echo 'Total rows updated: ' . $db->affected_rows;

```

### Free result

```php
$result->free();
```

### CRUD Operations 



In Database applications the acronym CRUD refers to all of the major functions that are implemented in relational database applications. Each letter in the acronym can map to a standard SQL statement or HTTP method:

| Operation       | SQL      | HTTP      |
|-----------------|----------|-----------|
|Create           | 	INSERT	| PUT / POST |
|Read (Retrieve)	|  SELECT  |	GET	      |
|Update (Modify)  |	UPDATE	| PUT / PATCH |
|Delete (Destroy)	| DELETE   |	DELETE	   |




```php

```

http://sqlzoo.net/w/index.php?title=SELECT_basics&oldid=13738

