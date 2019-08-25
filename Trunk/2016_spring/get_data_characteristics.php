<?php


$json = file_get_contents("http://api.randomuser.me/?results=1000");

$json_array = json_decode($json);


$sizes = array();

$sizes['gender'] = 0 ;
$sizes['title'] = 0 ;
$sizes['first'] = 0 ;
$sizes['last']  = 0 ;
$sizes['street']  = 0 ;
$sizes['city'] = 0 ;
$sizes['state'] = 0 ;
$sizes['zip']  = 0 ;
$sizes['email']  = 0 ;
$sizes['username'] = 0 ;
$sizes['password']  = 0 ;
$sizes['dob']  = 0 ;
$sizes['phone']  = 0 ;
$sizes['medium'] = 0 ;

for($i=0;$i<sizeof($json_array->results);$i++){
	$g = $json_array->results[$i]->user->gender;
	$t = $json_array->results[$i]->user->name->title;
	$f = $json_array->results[$i]->user->name->first;
	$l = $json_array->results[$i]->user->name->last;
	$s = $json_array->results[$i]->user->location->street;
	$c = $json_array->results[$i]->user->location->city;
	$st = $json_array->results[$i]->user->location->state;
	$z = $json_array->results[$i]->user->location->zip;
	$e = $json_array->results[$i]->user->email;
	$u = $json_array->results[$i]->user->username;
	$p = $json_array->results[$i]->user->password;
	$d = $json_array->results[$i]->user->dob;
	$ph = $json_array->results[$i]->user->phone;
	$pi = $json_array->results[$i]->user->picture->medium;


    $sizes['gender'] = $sizes['gender'] < strlen($g) ? strlen($g) : $sizes['gender'];
	$sizes['title'] = $sizes['title'] < strlen($t) ?  strlen($t) : $sizes['title'] ;
	$sizes['first'] = $sizes['first'] < strlen($f) ?  strlen($f) : $sizes['first'] ;
	$sizes['last'] = $sizes['last'] < strlen($l) ?  strlen($l) : $sizes['last'] ;
	$sizes['street'] = $sizes['street'] < strlen($s) ?  strlen($s) : $sizes['street'] ;
	$sizes['city'] = $sizes['city'] < strlen($c) ?  strlen($c) : $sizes['city'] ;
	$sizes['state'] = $sizes['state'] < strlen($st) ?  strlen($st) : $sizes['state'] ;
	$sizes['zip'] = $sizes['zip'] < strlen($z) ?  strlen($z) : $sizes['zip'] ;
	$sizes['email'] = $sizes['email'] < strlen($e) ?  strlen($e) : $sizes['email'] ;
	$sizes['username'] = $sizes['username'] < strlen($u) ?  strlen($u) : $sizes['username'] ;
	$sizes['password'] = $sizes['password'] < strlen($p) ?  strlen($p) : $sizes['password'] ;
	$sizes['dob'] = $sizes['dob'] < strlen($d) ? strlen($d) : $sizes['dob']  ;
	$sizes['phone'] = $sizes['phone'] < strlen($ph) ?  strlen($ph) : $sizes['phone'] ;
	$sizes['medium'] = $sizes['medium'] < strlen($pi) ?  strlen($pi) : $sizes['medium'] ;
}
    print_r($sizes);
