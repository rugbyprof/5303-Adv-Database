<?php

// Do the connection
$conn = mysqli_connect('localhost', 'AirRouteUser','mGSlVjWXU1fxufcs' ,'AirRoutes');
if (mysqli_connect_errno()) {
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
}else{
    echo "Connected...\n";
}

$files = scandir('.');

array_shift($files);
array_shift($files);

$data_files = [];

foreach($files as $file){
    if(strpos($file,'.dat')){
        $data_files[] = $file;
    }
}

function cleanData($data){
    if(strpos($data,",")){
        $data = str_ireplace(",","",$data);
    }

    if(strpos($data,"'")){
        $data = addslashes($data);
    }

    if($data == "\N"){
        $data = NULL;
    }

    return $data;
}

$columns['airlines.dat'] = ['Airline_ID','Name','Alias','IATA','ICAO','Callsign','Country','Active'];
$columns['airports.dat'] = ['Airport_ID','Name','City','Country','IATA','ICAO','Latitude','Longitude','Altitude','Timezone','DST','TZ',' Type','Source','LonLat'];
$columns['planes.dat'] = ['Id','Name','IATA','ICAO'];
$columns['routes.dat'] = ['Id','Airline','Airline_ID','Source_AP','Source_AP_ID','Dest_AP','Dest_AP_ID','CodeShare','Stops','Equipment'];

foreach($data_files as $file){

    $cnames = $columns[$file];

    list($tableName,$null) = explode('.',$file);

    // read entire file as a string csv
    $csv = array_map('str_getcsv', file($file));

    // echo"\n";
    // print_r($cnames);
    // echo"\n";
    // print(sizeof($csv[0]));

    //$fp = fopen('goedata.sql','w');

    $i = 0;
    foreach($csv as $row){
        
        // if(sizeof($row) != sizeof($cnames)){
        //     echo"Counts don't match on row {$i} for {$file}!\n";
        // }

        $A = "INSERT INTO {$tableName} ";
        $B = "(".implode(',',$cnames).") ";
        $C = "VALUES (";

        foreach($row as $val){
            $val = cleanData($val);
            $C .= "'{$val}',";
        }

        $C = rtrim($C,",");

        if($file == 'airports.dat'){
            if(sizeof($row) > 14){
                $lat = $row[7];
                $lon = $row[8];
            }else{
                $lat = $row[6];
                $lon = $row[7];                
            }
            $C .= ",GeomFromText('POINT({$lon} {$lat})')";
        }


        $D = ");";

        echo"{$A}{$B}{$C}{$D}\n";
        
        //fwrite($fp,$sql);
        $i++;
    }

}

