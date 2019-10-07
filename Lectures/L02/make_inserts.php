<?php

function processCSV($filename){
    // read entire file as a string csv
    $csv = array_map('str_getcsv', file($filename));

    return $csv;
}

$csv = processCSV('../../Resources/01_Random_Data/airports.dat');

$fp = fopen('goedata.sql','w');

foreach($csv as $row){
    
    $lat = 6;
    $lon = 7;   

    if(sizeof($row) > 14){
        $lat = 7;
        $lon = 8;
    }

    $sql = "INSERT INTO geoTable (id,name, geoPoint) VALUES ('{$row[0]}','{$row[5]}', GeomFromText('POINT({$row[$lon]} {$row[$lat]})') );\n";
    
    fwrite($fp,$sql);
}