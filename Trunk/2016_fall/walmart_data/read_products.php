<?php

$data = json_decode(file_get_contents('allProducts.json'),true);

print_r(sizeof($data));