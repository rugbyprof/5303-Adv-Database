<?php

$site = "http://codular.com/php-mysqli";

$html = file_get_contents($site);

$code = everything_in_tags($html,'code');

print_r($code);

function everything_in_tags($string, $tagname)
{
    $pattern = "#<\s*?$tagname\b[^>]*>(.*?)</$tagname\b[^>]*>#s";
    preg_match($pattern, $string, $matches);
    return $matches;
}
