 <?php
 
$data = json_decode(file_get_contents("allProducts.json"),true);

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


for($i=0;$i<sizeof($allKeys);$i++){
    $temp = [];
    $temp = &$data[$allKeys[$i][0]];
    $keystring = "";
    for($j=1;$j<sizeof($allKeys[$i]);$j++){
        echo $allKeys[$i][$j]."\n";
        $temp = &$temp[$allKeys[$i][$j]];
    }
    print_r(typensize($temp));
}


function typensize($value,$key=null){

    if($key){
        echo"$key\n";
    }
    return array("type"=>gettype($value),"size"=>strlen(strval($value)));
}
