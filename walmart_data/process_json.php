<?php

$path = 'jsonData/';
$dir = scandir($path);

$outputFile = 'jsonData/allProducts.json';

array_shift($dir);
array_shift($dir);

$products = [];

$f = @fopen($outputFile, "r+");
if ($f !== false) {
    ftruncate($f, 0);
    fclose($f);
}

foreach($dir as $file){
    $json = json_decode(file_get_contents($path.$file),true);

    if(array_key_exists('items',$json)){
        $items = $json['items'];

        foreach($items as $item){
            $products[$item['itemId']] = $item;
        }
    }

}

echo sizeof($products)."\n";

file_put_contents($outputFile,json_encode($products, JSON_PRETTY_PRINT));