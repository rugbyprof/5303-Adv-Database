<?php

// Do the connection
$conn = mysqli_connect('localhost', 'AirRouteUser','mGSlVjWXU1fxufcs' ,'AirRoutesV2');
if (mysqli_connect_errno()) {
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
}else{
    echo "Connected...\n";
}

  /* change character set to utf8 */
if (!$conn->set_charset("utf8")) {
    printf("Error loading character set utf8: %s\n", $conn->error);
} else {
    printf("Current character set: %s\n", $conn->character_set_name());
}

$data = file_get_contents('cities.json');

$json = json_decode($data,true);

// {
//     "country": "AD",
//     "name": "les Escaldes",
//     "lat": "42.50729",
//     "lng": "1.53414"
//   },

$i = 0;
foreach($json as $row){
    print_r($row);
    $a = $row['country'];
    $b = mb_convert_encoding($row['name'], 'UTF-8', 'UTF-8');
    $c = $row['lat'];
    $d = $row['lng'];

    $sql = "INSERT INTO cities VALUES ('{$i}','{$a}','{$b}','{$c}','{$d}')";
    $result = $conn->query($sql);
    $i++;


}