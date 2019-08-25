 <?php
 
 $data = json_decode(file_get_contents("allProducts.json"),true);

 $key_array = [];
 $product_keys = [];
 $market_keys = [];
 $gift_keys = [];
 $image_keys = [];

// foreach($data as $product_id=>$item_array){
//     foreach($item_array as $key => $value){
//        if(in_array($key,['bestMarketplacePrice','giftOptions','imageEntities','variants','attributes'])){
//             if($key=='bestMarketplacePrice'){
//                 foreach($value as $subkey => $subvalue){
//                     $market_keys[$subkey] = 0;
//                 }
//             }else if($key == 'giftOptions'){
//                 foreach($value as $subkey => $subvalue){
//                     $gift_keys[$subkey] = 0;
//                 }
//             }else if($key == 'imageEntities'){
//                 foreach($value as $subkey => $subvalue){
//                     foreach($subvalue as $imagekey => $imageurl){
//                         $image_keys[$imagekey] = 0;
//                     }
//                 }
//             }else if($key == 'attributes'){
//                 var_dump($value);
//             }else if($key == 'variants'){
//                 var_dump($value);
//             }
//        }else{

//             $info = typensize($value);
//             if(array_key_exists($key,$key_array)){
//                 if($key_array[$key]['size'] < $info['size']){
//                     $key_array[$key] = $info;
//                     $product_keys[$key] = $info;
//                 }
//             }else{
//                 $key_array[$key] = $info;
//             }
//        }

//     }
// }

$keys = [];

$iterator = new RecursiveIteratorIterator(new RecursiveArrayIterator($data));

foreach($iterator as $key=>$value) {
    if(gettype($key) != 'integer'){
        $info = typensize($value);
        if(!array_key_exists($key,$keys)){
            $keys[$key] = $info;
        }else{
            if($info['size'] > $keys[$key]['size']){
                $keys[$key] = $info;
            }
        }
    }
}

ksort($keys);
print_r($keys);

file_put_contents("keys.json",json_encode($keys, JSON_PRETTY_PRINT));

//recursive($data);

$allKeys = [];

$iterator = new RecursiveIteratorIterator(new RecursiveArrayIterator($data));

foreach ($iterator as $key => $value) {
    // loop through the subIterators... 
    $keys = array();
    $keys[] = $key;
    // in this case i skip the grand parent (numeric array)
    for ($i = $iterator->getDepth()-1; $i>=0; $i--) {
        $keys[] = $iterator->getSubIterator($i)->key();
    }

    //echo implode(' ',$keys).': '.$value.'\n';
    $keys = array_reverse($keys);
    //echo implode(' ',$keys)."\n";
    $allKeys[] = $keys;
}

//print_r($allKeys);

print_r($allKeys[117908]);

//print_r($data[$allKeys[117908][0]]);

$temp = &$data[$allKeys[117908][0]];

print_r($temp);

for($i=1;$i<sizeof($allKeys[117908]);$i++){
    $temp = &$temp[$allKeys[117908][$i]];
}
print_r($temp);

function typensize($value,$key=null){

    if($key){
        echo"$key\n";
    }
    return array("type"=>gettype($value),"size"=>strlen(strval($value)));
}

function recursive($array,$level=0) 
{
    foreach($array as $key=>$value)
    {
       echo str_repeat("\t",$level)."$key =>";
       if(is_array($value))
       {
          echo"\n";
          recursive($value,$level+1);
       }else{
           echo str_repeat("\t",$level)."(type=>".gettype($value).",size=>".strlen(strval($value)).")\n";
       }
    }
    
}