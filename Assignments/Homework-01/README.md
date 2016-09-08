# NOT COMPLETE DO NOT START UNTIL THIS MESSAGE IS GONE

# Products Database Creation
Due: September 12th by Classtime.

## Overview

This assignment is about creating a products database representing data found in [allProducts.json](../../walmart_data/allProducts.json). 

There will be (as of now) four tables:

- `gift_options`
- `image_entities`
- `market_place_price`
- `products`

You should use the sql files located in this folder to build your schema but you must first alter the table create statements 
to include the proper datatypes. 

I've created a file called [keys.json](./keys.json) that holds each `column name` along with its data type and max size. This was created using php so the data types aren't 1=>1 with sql. 

## Requirements

- Create a database called `products`

- In `products` create 4 tables using the `sql` files provided in this directory:
    -  [gift_options.sql](./gift_options.sql)
    -  [image_entities.sql](./products.sql)
    -  [market_place_price.sql](./market_place_price.sql)
    -  [products.sql](./products.sql)

- Ensure that you alter the table create statements:
    - Choose an appropriate data type for each column
    - Choose an appropriate size for each column
    - Add a primary key for each table 


