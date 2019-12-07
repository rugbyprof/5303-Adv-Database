<?php

$data = file("jack_handy.txt");

print_r($data);

$new_data = [];

foreach($data as $line){
    $shift = random_int(1,23);
    $line = str_split(strtoupper($line));
    for($i=0;$i<sizeof($line);$i++){
        $val = ord($line[$i]);
        if($val >= 65 && $val <= 90){
            $val -= 65;
            $val = ($val + $shift) % 26;
            $val += 65;
        }
        $line[$i] = chr($val);
    }
    $line = implode('',$line);
    $new_data[] = [$shift,$line];
}

print_r($new_data);
$fp = fopen("encrypted.txt","w");
fwrite($fp,sizeof($new_data)."\n");
foreach($new_data as $key => $val){
    fwrite($fp,$val[0]."\n");
    fwrite($fp,$val[1]);
}