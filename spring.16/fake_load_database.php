<?php

$dbinfo = json_decode(file_get_contents("db.config.example.json"));

print_r($dbinfo);
$myDB = new myMysqli($dbinfo->user,$dbinfo->password,$dbinfo->host,$dbinfo->dbname);

print_r($db_info);
