<?php
$apiKey = "2gpz379wejgc2f6annps7qkz";
$stop = 10;

$keyWords = [
    'ipad',
    'ipod',
    'segway',
    'iphone 6',
    'samsung galaxy',
    'laptop',
    'android',
    'tablet',
    'applewatch',
    'bluetooth'
];

for($start=1;$start<=$stop;$start++){
    foreach($keyWords as $keyword){
        $keyword = urlencode($keyword);
        $url = "http://api.walmartlabs.com/v1/search?apiKey={$apiKey}&query={$keyword}&sort=bestseller&responseGroup=full&start={$start}&numItems=25";
        echo"{$url}\n";
        file_put_contents('jsonData/'.$keyword.'-'.$start.'.json',get_data($url));
        sleep(1);
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