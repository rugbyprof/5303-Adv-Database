## First Assignment

#### Part 2 Due: Wednesday September 2nd by Midnight

### Description

Now that your table is created and sitting there in your database, it's time to load it with data. You saw many of the 
possible errors in class when we don't choose the correct data types for columns. Make sure you adjust your tables accordingly
so that the data received from `api.randomusers.me` will fit correctly. 

Look at the following file for help with your php database connection commands:[php_mysqli_intro.md](https://github.com/rugbyprof/5303-Adv-Database/blob/master/php_mysqli_intro.md).

Remember the JSON object returned from `api.randomusers.me`. An example can be seen in the previous assignment.

### Obtaining Data
```php
// Gets 1000 users from the randomuser api, and loads it into a variable called $json
$json = file_get_contents("http://api.randomuser.me/?results=1000");

// This turns the variable into a PHP object
$json_array = json_decode($json);
```

### Accessing the Object

You can access individual values by using the following syntax:
```php
// This gets the gender of the 1st user in the result set
$gender = $json_array->results[0]->user->gender;

// This gets the first name of the 2nd user in the result set
$street = $json_array->results[1]->user->location->street;
```

Or, you can loop through the entire result set using something similar to the follwing:
```php
  for($i=0;$i<sizeof($json_array->results);$i++){
  	$gender = $json_array->results[$i]->user->gender;
  	$street = $json_array->results[$i]->user->location->street;
  	...
  	...
	}
```

### Inserting Data

Again, look at [php_mysqli_intro.md](https://github.com/rugbyprof/5303-Adv-Database/blob/master/php_mysqli_intro.md) for examples on running querys.

### Results / Deliverables

- A script called `load_db.php` in your `assignment1` folder.
- A file called `create_table.sql` in the `assignment1` folder that contains the "exported sql" for your `Users` table (done from phpmyadmin). ONLY for the table (NO DATA);
- A table called `Users` in your phpMyAdmin database.
- 1000 __unique__ users in your table.
- Copy the `assignment1` folder into your github repository and push it to github.
