<?php

// Do the connection
$conn = mysqli_connect('localhost', 'AirRouteUser','mGSlVjWXU1fxufcs' ,'AirRoutes');
if (mysqli_connect_errno()) {
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
}else{
    echo "Connected...\n";
}

/**
 * Clean strings for processing
 */
function cleanData($data){
    // remove commas from field
    if(strpos($data,",")){
        $data = str_ireplace(",","",$data);
    }

    // escapae string if it has single quotes
    if(strpos($data,"'")){
        $data = addslashes($data);
    }

    // get rid of \N
    if($data == "\N"){
        $data = NULL;
    }

    return $data;
}

// read directory of files
$files = scandir('./flight_data');

// remove the . and .. from array
array_shift($files);
array_shift($files);

// files to process
$data_files = [];

// loop through directory
foreach($files as $file){
    // if file has a '.dat' grab name
    if(strpos($file,'.dat')){
        $data_files[] = $file;
    }
}

// Associative array of filename => column names
$columns['airlines.dat'] = ['Airline_ID','Name','Alias','IATA','ICAO','Callsign','Country','Active'];
$columns['airports.dat'] = ['Airport_ID','Name','City','Country','IATA','ICAO','Latitude','Longitude','Altitude','Timezone','DST','TZ',' Type','Source','LonLat'];
$columns['planes.dat'] = ['Id','Name','IATA','ICAO'];
$columns['routes.dat'] = ['Id','Airline','Airline_ID','Source_AP','Source_AP_ID','Dest_AP','Dest_AP_ID','CodeShare','Stops','Equipment'];

// loop through each data file
foreach($data_files as $file){

    // grab column names
    $cnames = $columns[$file];

    // remove .dat from file name
    list($tableName,$null) = explode('.',$file);

    // empty table in DB
    $conn->query("TRUNCATE {$tableName};");

    // read entire file as a string csv
    $csv = array_map('str_getcsv', file($file));


    // Process each row
    $i = 0;
    foreach($csv as $row){
        
        $debug = [];

        // Build insertion query
        $A = "INSERT INTO {$tableName} ";

        // adds column names to query 
        $B = "(".implode(',',$cnames).") ";
        $C = "VALUES (";

        // If first column name is Id add $i as id value
        if($cnames[0] == 'Id'){
            $C .= "'{$i}',";
        }

        // add values to be inserted
        foreach($row as $val){
            $val = cleanData($val);
            $debug[] = $val;
            $C .= "'{$val}',";
        }

        // trim off last trailing comma 
        $C = rtrim($C,",");

        // if its airports pull out lat lon 
        // and build a point type
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

        // add last paren
        $D = ");";

        // concat all parts
        $sql = "{$A}{$B}{$C}{$D}";

        // run query
        $result = $conn->query($sql);

        // print errors
        if(!$result){
            echo "Error message: ". $conn->error."\n";
            echo "File: {$file} Row: {$i}\n";
            print_r($debug);
            echo $sql;
            exit;
        }
        
        $i++;
    }

}

