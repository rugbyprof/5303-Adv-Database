# Products Database Creation
Due: September 12th by Classtime.

## Overview

This assignment is about creating a products database to store data found in [allProducts.json](../../walmart_data/allProducts.json). 

There will be (as of now) four tables:

- `gift_options`
- `image_entities`
- `market_place_price`
- `products`

You should use the sql files located in this folder to build your schema but you must first alter the table create statements 
to include the proper datatypes. 

I've created a file called [keys.json](./keys.json) that holds each `column name` along with its data type and max size. This was created using php so the data types aren't 1=>1 with sql. 

## Requirements

- Add a user to your database that has `root` privileges. 
- To do this:
    - login to phpmyadmin on your server
    - click on `Users` on the top menu
    - Click on `Add user` 
        - User Name: `griffin`
        - Host: `localhost`
        - Password: `2D2016!!!`
        - Global Priveleges: `Check All`
        - `GO`

- Create a database called `products`

- In `products` create 4 tables using the `sql` files provided in this directory:
    -  [gift_options.sql](./gift_options.sql)
    -  [image_entities.sql](./products.sql)
    -  [market_place_price.sql](./market_place_price.sql)
    -  [products.sql](./products.sql)

- Ensure that you alter the table create statements:
    1. Choose an appropriate data type for each column
    2. Choose an appropriate size for each column
    3. Add a primary key for each table 

## Deliverables

- A document named `homework-01.md` placed in your repository in a folder called `assignments`.
- The document should include:
    - Your Name
    - Your Ip Address
    - A link to your phpmyadmin page.
    - Your revised sql for each table.

## Example Document Format

## Homework 1

### Name:
    First Last

### Ip Address
    111.222.333.444

### Phpmyadmin Link
    http://111.222.333.444/phpmyadmin

## Table Create statements

#### gift_options.sql

```sql
CREATE TABLE IF NOT EXISTS `gift_options` (
       	`allowGiftWrap` NOT NULL,
       	`allowGiftMessage` NOT NULL,
       	`allowGiftReceipt` NOT NULL,
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

#### image_entities.sql

```sql
CREATE TABLE IF NOT EXISTS `image_entities` (
       	`thumbnailImage` NOT NULL,
       	`mediumImage` NOT NULL,
       	`largeImage` NOT NULL,
       	`entityType` NOT NULL,
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

#### market_place_price.sql

```sql
CREATE TABLE IF NOT EXISTS `market_place_price` (
       	`price` NOT NULL,
       	`sellerInfo` NOT NULL,
       	`standardShipRate` NOT NULL,
       	`twoThreeDayShippingRate` NOT NULL,
       	`availableOnline` NOT NULL,
       	`clearance` NOT NULL,
       	`offerType` NOT NULL,
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

#### products.sql

```sql
CREATE TABLE IF NOT EXISTS `products` (
       	`itemId` NOT NULL,
       	`parentItemId` NOT NULL,
       	`name` NOT NULL,
       	`salePrice` NOT NULL,
       	`upc` NOT NULL,
       	`categoryPath` NOT NULL,
       	`shortDescription` NOT NULL,
       	`longDescription` NOT NULL,
       	`brandName` NOT NULL,
       	`thumbnailImage` NOT NULL,
       	`mediumImage` NOT NULL,
       	`largeImage` NOT NULL,
       	`productTrackingUrl` NOT NULL,
       	`modelNumber` NOT NULL,
       	`productUrl` NOT NULL,
       	`categoryNode` NOT NULL,
       	`stock` NOT NULL,
       	`addToCartUrl` NOT NULL,
       	`affiliateAddToCartUrl` NOT NULL,
       	`offerType` NOT NULL,
       	`msrp` NOT NULL,
       	`standardShipRate` NOT NULL,
       	`color` NOT NULL,
       	`customerRating` NOT NULL,
       	`numReviews` NOT NULL,
       	`customerRatingImage` NOT NULL,
       	`maxItemsInOrder` NOT NULL,
       	`size` NOT NULL,
       	`sellerInfo` NOT NULL,
       	`age` NOT NULL,
       	`gender` NOT NULL,
       	`isbn` NOT NULL,
       	`preOrderShipsOn` NOT NULL,
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```