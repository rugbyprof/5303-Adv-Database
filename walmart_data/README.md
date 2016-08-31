## Data Files

### allProducts.json

This file contains a json object / array with ~ 6000 products and their information.

### taxonomy.json

This file contains a list of all walmarts categories and their associated id numbers.
It also contains a "path" field which is like a breadcrumb trail of parent categories.

## my_categories.json

This file is a list of categories that I used to search the walmart api. I'm not sure
if it will be necessary, but I kept it here.


## Php Files

## read_taxonomy.php

This file simply opens the taxonomy.json file and pulls out all the categories that are
children of a major category that I am interested in (['Electronics','Cell Phones','Video Games']).

I then clean them up a bit and build a list that was used to query the walmart api for products.
I left this file in here just as an example of php reading json.
