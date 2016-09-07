 <?php
 
 $data = json_decode(file_get_contents("allProducts.json"),true);

 $key_array = [];
 $product_keys = [];
 $market_keys = [];
 $gift_keys = [];
 $image_keys = [];

foreach($data as $product_id=>$item_array){
    foreach($item_array as $key => $value){
       if(in_array($key,['bestMarketplacePrice','giftOptions','imageEntities'])){
            if($key=='bestMarketplacePrice'){
                foreach($value as $subkey => $subvalue){
                    $market_keys[$subkey] = 0;
                }
            }else if($key == 'giftOptions'){
                foreach($value as $subkey => $subvalue){
                    $gift_keys[$subkey] = 0;
                }
            }else{
                foreach($value as $subkey => $subvalue){
                    foreach($subvalue as $imagekey => $imageurl){
                        $image_keys[$imagekey] = 0;
                    }
                }
            }
       }else{
            //echo "{$key}=>{$value}\n";
            //if(gettype($value)){
                echo gettype($value)."\n";
            //}
            if(array_key_exists($key,$key_array)){
                if(strlen($key_array[$key]) < strlen($value)){
                    $key_array[$key] = strlen($value);
                    $product_keys[$key] = 0;
                }
            }else{
                $key_array[$key] = strlen($value);
            }
       }

    }
}
