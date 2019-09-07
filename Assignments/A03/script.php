<?php
/**
 * This is an example php script that will:
 * 
 * 1: Connect to a mysql database on the local machine (cs2 server)
 * 2: Create a table called users (typically I would do that with phpMyAdmin)
 * 3: Add a primary key to the table (again phpMyadmin would be better)
 * 4: Opens a json formatted file, and loads it into the users table
 * 
 * You need to fill in the username, password, and database to make this 
 * script work for you.
 * 
 */

// Turn errors off later make the -1 a 0
error_reporting(-1);

// Fill in your connection info
$host = 'localhost';
$username = '';
$password = '';
$database = '';

// Do the connection
$conn = mysqli_connect($host, $username, $password, $database);
if (mysqli_connect_errno()) {
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
}else{
    echo "Connected...\n";
}

// Drop a Table 
///////////////////////////////////////////////////////////////

// I did the drop because I ran this script multiple times and 
// wanted a clean slate every time. You can remove this
// if you want
$sql = "DROP TABLE `users`;";
$conn->query($sql);


// Create a Table
///////////////////////////////////////////////////////////////

// create your sql statement
$sql = "CREATE TABLE `users` ( 
    `id` int(11) NOT NULL, 
    `first_name` varchar(32) NOT NULL, 
    `last_name` varchar(32) NOT NULL, 
    `email` varchar(127) NOT NULL, 
    `gender` varchar(7) NOT NULL, 
    `ip_address` varchar(15) NOT NULL 
    );";

// run your sql statement
$result = $conn->query($sql);

// if it was successful lets alter the table and add a key
if($result){
    $sql = "ALTER TABLE `users` ADD PRIMARY KEY (`id`);";
    $conn->query($sql);
}

// Add data to Table
///////////////////////////////////////////////////////////////

// opens and reads entire file in one line
$data = file_get_contents('users.json');

// turns json string into a php associative array 
$data = json_decode($data,true);

// loops through the array putting one user in $u at every iteration
foreach($data as $u){

    // some names have apostrophes so we need to
    // escape those or query qill fail
    $fname = addslashes($u['first_name']);
    $lname = addslashes($u['last_name']);

    // Build the insert statement pulling out the values from $u
    $sql = "INSERT INTO users VALUES ('{$u['id']}','{$fname}','{$lname}',
                                    '{$u['email']}','{$u['gender']}','{$u['ip_address']}');";
    print($sql)."\n";
    $result = $conn->query($sql);

    if(!$result){
        echo "Error message: ". $conn->error;
    }
}

