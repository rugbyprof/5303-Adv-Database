<?php



$major_categories = ['Electronics','Cell Phones','Video Games'];

$json = json_decode(file_get_contents("taxonomy.json"),true);

$json = $json['categories'];

print_r(array_keys($json));

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