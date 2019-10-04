<?php
//https://www.plumislandmedia.net/mysql/stored-function-haversine-distance-computation/


$conn = mysqli_connect('localhost', '', '', '');
if (mysqli_connect_errno()) {
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
}else{
    echo "Connected...\n";
}

//https://stackoverflow.com/questions/14750275/haversine-formula-with-php
/**
 * Calculates the great-circle distance between two points, with
 * the Haversine formula.
 * @param float $latitudeFrom Latitude of start point in [deg decimal]
 * @param float $longitudeFrom Longitude of start point in [deg decimal]
 * @param float $latitudeTo Latitude of target point in [deg decimal]
 * @param float $longitudeTo Longitude of target point in [deg decimal]
 * @param float $earthRadius Mean earth radius in [miles]
 * @return float Distance between points in [miles] (same as earthRadius)
 */
function haversine($latitudeFrom, $longitudeFrom, $latitudeTo, $longitudeTo, $earthRadius = 3963){
    // convert from degrees to radians
    $latFrom = deg2rad($latitudeFrom);
    $lonFrom = deg2rad($longitudeFrom);
    $latTo = deg2rad($latitudeTo);
    $lonTo = deg2rad($longitudeTo);
  
    $latDelta = $latTo - $latFrom;
    $lonDelta = $lonTo - $lonFrom;
  
    $angle = 2 * asin(sqrt(pow(sin($latDelta / 2), 2) +
      cos($latFrom) * cos($latTo) * pow(sin($lonDelta / 2), 2)));
    return $angle * $earthRadius;
}

//https://www.dougv.com/2009/07/calculating-the-bearing-and-compass-rose-direction-between-two-latitude-longitude-coordinates-in-php/
function bearing($lat1,$lon1,$lat2,$lon2){
    $bearing = (rad2deg(atan2(sin(deg2rad($lon2) - deg2rad($lon1)) 
            * cos(deg2rad($lat2)), cos(deg2rad($lat1)) 
            * sin(deg2rad($lat2)) - sin(deg2rad($lat1)) 
            * cos(deg2rad($lat2)) * cos(deg2rad($lon2) - deg2rad($lon1)))) + 360) % 360;

    return $bearing;
}

function getCompassDirection($bearing) {
    $tmp = round($bearing / 22.5);
    switch($tmp) {
       case 1:
          $direction = "NNE";
          break;
       case 2:
          $direction = "NE";
          break;
       case 3:
          $direction = "ENE";
          break;
       case 4:
          $direction = "E";
          break;
       case 5:
          $direction = "ESE";
          break;
       case 6:
          $direction = "SE";
          break;
       case 7:
          $direction = "SSE";
          break;
       case 8:
          $direction = "S";
          break;
       case 9:
          $direction = "SSW";
          break;
       case 10:
          $direction = "SW";
          break;
       case 11:
          $direction = "WSW";
          break;
       case 12:
          $direction = "W";
          break;
       case 13:
          $direction = "WNW";
          break;
       case 14:
          $direction = "NW";
          break;
       case 15:
          $direction = "NNW";
          break;
       default:
          $direction = "N";
    }
    return $direction;
 }

function get_airports_equator($distance=200){
    global $conn;

    $sql = "SELECT Name, haversine(Latitude,Longitude,0,Longitude) as distance, Latitude, Longitude ,TZ
    FROM `airports` 
    WHERE haversine(Latitude,Longitude,0,Longitude) < {$distance}
    ORDER BY RAND()";

    $result = $conn->query($sql);

    $airports = [];
   
    while($row = mysqli_fetch_assoc($result)){

        $airports[] = $row;

    }

    return array_values($airports);
}


function filter_landing_spots($ap,$jump=500){
    for($i=0;$i<sizeof($ap);$i++){
        for($j=0;$j<sizeof($ap);$j++){
            $lat1 = $ap[$i]['Latitude'];
            $lon1 = $ap[$i]['Longitude'];
            $lat2 = $ap[$j]['Latitude'];
            $lon2 = $ap[$j]['Longitude'];
            $d = haversine($lat1,$lon1,$lat2,$lon2);

            if($d > 0){

            }

        }
    }
    return $legs;
}



/**
 * getGeoJson
 * 
 * Description:
 *      Creates a GeoJson from an array of points
 */
function buildGeoJson($airports){
    $json = [];                         // empty json array
    $json['type']='FeatureCollection';  // add top level key to be a 'FeatureCollection'
    $json['feautures'] = [];            // now push on an array with the key 'feautures'


    // loop through result set and build a php associative array to be encoded as a json (geojson) object
    foreach($airports as $airport){
        // push a new "object" (feature) onto our features array
        $json['feautures'][] = ['type'=>'Feature',
                                'geometry'=>[
                                    'type'=>'Point',
                                    'coordinates'=>[$airport['Longitude']*1.0,$airport['Latitude']*1.0]],
                                    "properties"=> [
                                        "title" =>"{$airport['Name']}",
                                        "description"=>"{$airport['TZ']}",
                                        "marker-size"=>"medium",
                                        "marker-symbol"=>"airport",
                                        "marker-color"=>"#f00",
                                        "stroke"=>"#555555",
                                        "stroke-opacity" =>1,
                                        "stroke-width"=>2,
                                        "fill" => "#555555",
                                        "fill-opacity" => 0.5
                                    ]
                                ]; 
    }

    for($i=1;$i<sizeof($airports);$i++){
       
        $json['features'][] = ['type'=>'Feature',
                                'geometry'=>[
                                    'type'=>"LineString",
                                    'coordinates'=>[
                                        
                                            [$airports[$i-1]['Longitude']*1.0,$airports[$i-1]['Latitude']*1.0],
                                            [$airports[$i]['Longitude']*1.0,$airports[$i]['Latitude']*1.0]
                                        ]
                                        
                                ],
                                    "properties"=> [
                                            "title" =>"Flight Path",
                                            "description"=>"Leg {$i}",
                                            "stroke"=>"#555555",
                                            "stroke-opacity" =>1,
                                            "stroke-width"=>2,
                                            "fill" => "#555555",
                                            "fill-opacity" => 0.5
                                        ]
                                    
                                        ];
    }                       
    
    // dump to output (json pretty adds newlines and indentation)
    file_put_contents("round_the_world.geojson",json_encode($json,JSON_PRETTY_PRINT));

}

$airports = get_airports_equator();
$spots = filter_landing_spots($airports);

print_r($spots);
