<?php

// /$file = file("http://www.tutorialspoint.com/sql/sql-syntax.htm");
// $file = file("http://www.tutorialspoint.com/sql/index.htm");
// <!-- PRINTING STARTS HERE -->
// <!-- PRINTING ENDS HERE -->

// Array
// (
//     [0] => http://www.tutorialspoint.com/sql/index.htm
//     [1] => http://www.tutorialspoint.com/sql/sql-overview.htm
//     [2] => http://www.tutorialspoint.com/sql/sql-rdbms-concepts.htm
//     [3] => http://www.tutorialspoint.com/sql/sql-databases.htm
//     [4] => http://www.tutorialspoint.com/sql/sql-syntax.htm
//     [5] => http://www.tutorialspoint.com/sql/sql-data-types.htm
//     [6] => http://www.tutorialspoint.com/sql/sql-operators.htm
//     [7] => http://www.tutorialspoint.com/sql/sql-expressions.htm
//     [8] => http://www.tutorialspoint.com/sql/sql-create-database.htm
//     [9] => http://www.tutorialspoint.com/sql/sql-drop-database.htm
//     [10] => http://www.tutorialspoint.com/sql/sql-select-database.htm
//     [11] => http://www.tutorialspoint.com/sql/sql-create-table.htm
//     [12] => http://www.tutorialspoint.com/sql/sql-drop-table.htm
//     [13] => http://www.tutorialspoint.com/sql/sql-insert-query.htm
//     [14] => http://www.tutorialspoint.com/sql/sql-select-query.htm
//     [15] => http://www.tutorialspoint.com/sql/sql-where-clause.htm
//     [16] => http://www.tutorialspoint.com/sql/sql-and-or-clauses.htm
//     [17] => http://www.tutorialspoint.com/sql/sql-update-query.htm
//     [18] => http://www.tutorialspoint.com/sql/sql-delete-query.htm
//     [19] => http://www.tutorialspoint.com/sql/sql-like-clause.htm
//     [20] => http://www.tutorialspoint.com/sql/sql-top-clause.htm
//     [21] => http://www.tutorialspoint.com/sql/sql-order-by.htm
//     [22] => http://www.tutorialspoint.com/sql/sql-group-by.htm
//     [23] => http://www.tutorialspoint.com/sql/sql-distinct-keyword.htm
//     [24] => http://www.tutorialspoint.com/sql/sql-sorting-results.htm
//     [25] => http://www.tutorialspoint.com/sql/sql-constraints.htm
//     [26] => http://www.tutorialspoint.com/sql/sql-using-joins.htm
//     [27] => http://www.tutorialspoint.com/sql/sql-unions-clause.htm
//     [28] => http://www.tutorialspoint.com/sql/sql-null-values.htm
//     [29] => http://www.tutorialspoint.com/sql/sql-alias-syntax.htm
//     [30] => http://www.tutorialspoint.com/sql/sql-indexes.htm
//     [31] => http://www.tutorialspoint.com/sql/sql-alter-command.htm
//     [32] => http://www.tutorialspoint.com/sql/sql-truncate-table.htm
//     [33] => http://www.tutorialspoint.com/sql/sql-using-views.htm
//     [34] => http://www.tutorialspoint.com/sql/sql-having-clause.htm
//     [35] => http://www.tutorialspoint.com/sql/sql-transactions.htm
//     [36] => http://www.tutorialspoint.com/sql/sql-wildcards.htm
//     [37] => http://www.tutorialspoint.com/sql/sql-date-functions.htm
//     [38] => http://www.tutorialspoint.com/sql/sql-temporary-tables.htm
//     [39] => http://www.tutorialspoint.com/sql/sql-clone-tables.htm
//     [40] => http://www.tutorialspoint.com/sql/sql-sub-queries.htm
//     [41] => http://www.tutorialspoint.com/sql/sql-using-sequences.htm
//     [42] => http://www.tutorialspoint.com/sql/sql-handling-duplicates.htm
//     [43] => http://www.tutorialspoint.com/sql/sql-injection.htm
//     [44] => http://www.tutorialspoint.com/sql/sql-database-tuning.htm
//     [45] => http://www.tutorialspoint.com/sql/sql_questions_answers.htm
//     [46] => http://www.tutorialspoint.com/sql/sql-quick-guide.htm
//     [47] => http://www.tutorialspoint.com/sql/sql-useful-functions.htm
//     [48] => http://www.tutorialspoint.com/sql/sql-useful-resources.htm
//     [49] => http://www.tutorialspoint.com/sql/sql-discussion.htm
// )

$base = "http://www.tutorialspoint.com";
$next = "/sql/index.htm";

$links = array();

while(!in_array($base.$next,$links)){
    $links[] = $base.$next;
    $next = getNextLink($base.$next);
}

print_r($links);

//print_r(getContent("http://www.tutorialspoint.com/sql/sql-useful-resources.htm"));

function getNextLink($url){
    $file = file_get_contents($url);
    $regex = '#<div class="nxt-btn">(.*?)</div>#s';
    $tag = preg_match($regex, $file, $match);
    $tag = $match[1];
    $parts = explode('"',$tag);
    return $parts[1];
}

function getContent($url){
    // <!-- PRINTING STARTS HERE -->
    // <!-- PRINTING ENDS HERE -->
    $file = file_get_contents($url);

    $regex = '/<!-- OPTIONAL --> (.*?) <!-- OPTIONAL END -->/s';
    $html = preg_match($regex, $file, $match);
    return $match;
}
