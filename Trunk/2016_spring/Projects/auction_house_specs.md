# Online Auction House

## Spring 2015

### Description

The basic idea behind your on-line auction house is that it will allow customers to use the web to browse/search the contents of your database (at least that part you want the customer to see) and to hold auctions over the web.

### Specifications / Requirements:

The users of your system will be:
- Customers that buy and sell at your auction house
- Customer representatives who provide customer-related services
- House manager

The data items required for the auction-house database can be classified into four categories: 
- auctions
- items
- customers
- employees

This classification does not imply any particular table arrangement. You are responsible for arranging the data items into tables, determining the relationships among tables and identifying the key attributes. 

You should include indices in your tables to speed up query processing. You should base your choice of indices on the type and expected frequency of the queries. Finally, you should specify and enforce integrity constraints on the data.

You will create your relational model using Mysql Workbench or Phpmyadmin Designer. 


![](https://s3.amazonaws.com/f.cl.ly/items/2R0q41330k2k0N1O2G31/diagram.png)

### Data / Actions

#### Auction

1. Auction ID
2. Item ID
3. Seller ID
4. Buyer ID
5. Opening Date/Time
6. Closing Date/Time
7. Minimum or Opening Bid
8. Closing Bid
9. Current Bid
10. Current High Bid
11. Reserve
12. Increment
13. Employee ID

- Each auction is for a certain item in the auction house's database.
- The Seller establishes an opening data/time and closing date/time for the auction. 
- An auctions may last 3, 5, or 7 days from the time the auction is opened.

Since this is an on-line auction house, the bidding rules governing an auction are a bit different than what you might expect. This is because bidders are obviously not expected to stay connected to the site for the duration of an auction. Instead, they are encouraged to bid the maximum amount they are willing to pay for an item, even on their first bid! Moreover, this amount is kept secret! If necessary, bids will be made on your behalf as other bidders increase the bid price, up to your maximum amount or the necessary preset bid increment to outbid other bidders.

All bidding is done in bid increments. An auction's bid increment is calculated by the system and changes with the current maximum bid. Use Google to find an increment formula.

To clarify the bidding process, let's consider an example. Suppose the opening bid on an item is $100 and the increment is $25. The seller stipulates what the opening or minimum bid is to be. Suppose now that Sarah bids $500 on the item and she is the first person to make a bid on the item. Then the current bid will be posted as $100 although the system knows that the high bid so far is $500. Suppose John comes along and bids $250. Then the current bid will now be posted as $275 and Sarah will be credited with this bid.

This is an example of a _proxy bid_, i.e., a bid made by the system on behalf of a user, and such bids are a key mechanism for making on-line auctions feasible. In this particular case, the system has outbid John by the bid increment on behalf of Sarah. John decides that enough is enough and bids $600. John has succeeded in outbidding Sarah, the current bid becomes $525, and the current maximum bid belongs to John at $600. As always, John's maximum bid is kept secret.

Auctions may also be run with reserve prices. The reserve price is the lowest price at which a seller is willing to sell an item. The reserve price is not disclosed to bidders. A seller might specify a reserve price if she is unsure of the real value of the item and would like to be able to refuse to sell the item if the market value is below a certain price. During an auction, an annotation should be displayed in the item information screen if the seller has specified a reserve price.

The seller specifies the reserve price when she lists an item. This price should be above the minimum bid price. The auction begins at the minimum bid price. When a bidder's maximum bid is equal to or greater than the reserve price, the item's current price will indicate that the reserve price has been met.

When an auction finishes, the customer who placed the current high bid becomes the buyer. You can optionally implement a scheme where at the conclusion of an auction, the buyer and seller will be notified by e-mail. The auction house receives a fixed-percentage commission of 10% on every completed auction. A customer representative from the auction house oversees each auction.


#### Items

1. Item ID
2. Item Name
3. Item Type
4. Year Manufactured
5. Copies Sold
6. Amount in Stock

- An item is the entity that is purchased or sold in an auction. 
- The types of items in your database can be whatever you like. 
- Standard items are jewelry, silverware, quilts, books, CDs, and sport memorabilia. 
- You should keep track of the number of copies of the item sold and currently up for auction.

#### Customers

1. Last Name
2. First Name
9. E-Mail Address
3. Address
4. City
5. State
6. Zip Code
7. Telephone
8. E-mail Address
8. Credit Card No.
8. Expiration month
8. Expiration year
8. CVC Code
10. Items Sold
11. Items Purchased
12. Rating

- A given customer may partake in any number of auctions, either as a buyer or as a seller. 
- The customer's rating should reflect how trustworthy and reliable the customer is, either as a buyer (pays the seller what he said he would) or as a seller (sends the buyer what he said he would).

#### Employees

1. Social Security #
9. E-Mail Address
2. Last Name
3. First Name
4. Address
5. City
6. State
7. Zip Code
8. Telephone
9. Start Date
10. Hourly Rate


### Transaction Support

#### Manager Transactions:

* Add, Edit and Delete information for an employee
* Obtain a sales report for a particular month
* Produce a comprehensive listing of all items
* Produce a list of sales by item name or by customer name
* Produce a summary listing of revenue generated by a particular item, item type, or customer
* Determine which customer representative generated most total revenue
* Determine which customer generated most total revenue
* Produce a Best-Sellers list of items

#### Customer Representative Transactions:

* Record a sale
* Add, Edit and Delete information for a customer
* Produce customer mailing lists
* Produce a list of item suggestions for a given customer (based on that customer's past purchases)

- The customer should be able to easily browse the auction house over the web and partake in auctions (as the buyer or seller). 
- While the customer will not be permitted to access the database directly, the customer should be able to retrieve the following information.

* A bid history for each auction
* A history of all current and past auctions a customer has taken part in
* Items sold by a given seller and corresponding auction info
* Items available of a particular type and corresponding auction info
* Items available with a particular keyword or set of keywords in the item name, and corresponding auction info
* Best-Seller list
* Personalized item suggestion list

- Your database system should provide controlled access to the data by distinguishing between the different types of users: manager, customer representatives, and customers.

* Customer Representatives should not be able to perform manage-level transactions, however, they should be able to read employee information, except for the hourly rate.
* Customer Representatives should be able to record the receipt of an order from a supplier.
* A customer should not be allowed to access other customers' account information, or to any employee information. Also, as discussed above, high bids and reserves are kept private.
  