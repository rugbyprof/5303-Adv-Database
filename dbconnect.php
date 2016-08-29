
<?php

  $DB_host = "localhost";
  $DB_user = "george";
  $DB_pass = "************";
  $DB_name = "5303-advdb";

  $conn = new MySQLi($DB_host,$DB_user,$DB_pass,$DB_name);

     if($conn->connect_errno)
     {
         die("ERROR : -> ".$conn->connect_error);
     }

?>

