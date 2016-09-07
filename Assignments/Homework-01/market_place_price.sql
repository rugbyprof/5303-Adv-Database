CREATE TABLE IF NOT EXISTS `market_place_price` (
       	`price` NOT NULL,
       	`sellerInfo` NOT NULL,
       	`standardShipRate` NOT NULL,
       	`twoThreeDayShippingRate` NOT NULL,
       	`availableOnline` NOT NULL,
       	`clearance` NOT NULL,
       	`offerType` NOT NULL,
) ENGINE=InnoDB DEFAULT CHARSET=latin1;