<?php

// The major categories in the taxonomy that we want to deal with
$major_categories = ['Electronics','Cell Phones','Video Games'];

// Read in the taxonomy json file
$json = json_decode(file_get_contents("taxonomy.json"),true);

// Move down one level in the array
$json = $json['categories'];

//loop through and create clean sub categories to do data lookups with the walmart api
$i=0;
foreach($json as $category){
    if(in_array($category['name'],$major_categories)){
        foreach($category['children'] as $subcat){
            $i++;
            $subcat_name = str_replace(" & "," ",$subcat['name']);
            $subcat_name = str_replace(" - "," ",$subcat_name);
            $subcat_name = str_replace(" ","+",$subcat_name);
            echo "\"".$subcat_name."\",\n";
        }
    }
}

echo $i."\n";