<?php
$apiKey = "2gpz379wejgc2f6annps7qkz";
// $stop = 21;
// $start = 11;
// $num_items=25;
// $total_calls = 440;

$stop = 25;
$start = 1;
$num_items=25;
$total_calls = 1803;

$temp = "http://api.walmartlabs.com/v1/search?apiKey=2gpz379wejgc2f6annps7qkz&sort=bestseller&responseGroup=full&start=1&query=iPad+Tablets&numItems=25";

$keyWords = [
    'rc+toys',
    'iPhone+case',
    'samsung+case',
    'imac',
    'macbook',
    'applewatch',
    'bluetooth',
    'fitbit',
    'fitbit+accessories',
    'thumb+drive',
    'game+controller',
    'chromebook',
    'hp+laptop',
    '2-in-1+laptops',
    'touchscreen+laptops',
    'hard+drives+storage',
    'rca+laptop',
    'mice+keyboards',
    'monitors'
];

//$keyWords = json_decode(file_get_contents('my_categories.json'));

foreach($keyWords as $keyword){
    for($i=$start ; $i<=$stop ; $i++ , $total_calls++){
        //$keyword = urlencode($keyword);
        $url = "http://api.walmartlabs.com/v1/search?apiKey={$apiKey}&query={$keyword}&sort=bestseller&responseGroup=full&start={$i}&query={$keyword}&numItems=25";
        echo"{$url}\n";
        echo'jsonData/'.fileName($total_calls,'json')."\n";
        file_put_contents('jsonData/'.fileName($total_calls,'json'),get_data($url));
        sleep(.3);
        if($total_calls >= 4500){
            echo"Stopping ...\n";
            echo"keyword = {$keyword}\n";
            echo"page = {$i}\n";
            exit;
        }
    }
}
 

function get_data($url) {
	$ch = curl_init();
	$timeout = 5;
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, $timeout);
	$data = curl_exec($ch);
	curl_close($ch);
	return json_encode(json_decode($data),JSON_PRETTY_PRINT);
}

function fileName($value,$ext,$len=5){
    return str_pad($value, $len, '0', STR_PAD_LEFT).".".$ext;
}