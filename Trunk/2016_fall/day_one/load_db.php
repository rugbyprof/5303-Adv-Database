
<?php

include('dbconnect.php');

$data = json_decode(file_get_contents('products_big.json'),true);

$i = 0;
foreach($data as $row){
    $id = $i;
    $category = $row['category'];
    $description = $row['h2'];
    $price = substr($row['price'],1)*1;

    $sql = "INSERT INTO products VALUES ('{$id}','{$category}','{$description}','{$price}')";
    $conn->query($sql);
    echo $sql."\n";
    $i++;
}
