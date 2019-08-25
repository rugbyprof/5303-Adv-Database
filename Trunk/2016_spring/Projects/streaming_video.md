
[Source](http://cs2.mwsu.edu/~griffin/streaming_video.html "Permalink to Description of CSE 532 Database Programming Project")

# Description of CSE 532 Database Programming Project

## Fall 2001

## The information contained within this project description is subject to change. Please check this page frequently over the next couple of weeks.

## Last Modified: 18 Sep 2001

In this project, you will design and implement an object-relational database system to support the operations of a **streaming Video on Demand (VoD) web site**. You will use HTML and Java for the user interface, DB2 for the database server, and Javascript, JDBC and SQL for connectivity between the user interface and database server. The database server is accessible from any of the sbpub machines in Room 2206, and from the PCs in the Graduate PC lab (Computer Science Building, Room 1239).

To use a machine in the Grad PC lab, you need to physically be sitting in front of the machine. Use your department account and password to log in. Regardless of where you do your development, you will need a separate account to access the DB2 server machine. Please e-mail the TA [Yan Rong][1] in order to receive your DB2 account information. Also, please see the [Project Hints Page][2] for more information about accessing the DB2 Server.

If you own a PC, you are encouraged to develop as much of the code as possible on your PC, to ease the congestion in the PC and Pub labs. As long as you use DB2 (or some similar database product supporting SQL 3 such as Oracle8i), HTML, Java/Javascript, JDBC, etc., it does not matter where your project runs. If you like, you can even bring in your own PC or laptop when it comes time to demo your project at the end of the semester. The version of DB2 running within the department is 7.1.

You can order or download a free copy of DB2 Universal Developer's Edition Version 7.1 from IBM by going to IBM's [DB2 Scholars Program web site][3] and registering for the DB2 Scholars Program.

You are to work in teams of two. Teams of any other size (including one and three) will not be allowed. Pick a partner and also choose a name for your team. Since you are expected to do a professional-looking job on this project, you can think of your team as a small hi-tech company. E-mail the names of your team members and the name of your company to [yanrong AT cs DOT sunysb DOT edu][4] as soon as possible. If you are unable to find a teammate, please let me know asap, and I will find one for you.

The TA is putting together a prototypical database system on which you can base your project. We will give you access to the code, which should help you a lot. In the meanwhile, you should start to become familiar with CGI programming, Java, JDBC, and HTML on your own. Make sure you buy the books that we have recommended -- see the course homepage.

It is recommended that you regularly check the [course homepage][5], for information on the term project. The homepage will be updated from time to time with important information on how to proceed with the project.

The basic idea behind your VoD web site is that it will allow customers to browse/search the contents of your database (at least that part you want the customer to see) and to "rent" videos by streaming downloads at date/time specified by customers. Available videos should be organized into a **classification hierarchy** much like  the way the books portion of the [amazon.com][6] web site is organized. Each video-file download will be treated as a **transaction** by your system and the user charged accordingly. Your web site will maintain MPEG video files having the .mpg file extension. See [www.mpeg.org][7] for further information about MPEG files.

Your database system must be based on the specifications and requirements that follow.

The users of your system will be the customers that download streaming videos from your web site for viewing on their PCs or laptop computers; suppliers that capture videos as MPEG files and download these to your web site; customer representatives who process customer orders and provide other customer-related services; and the store's manager. You should assume that the computer knowledge of the users is limited (say, that of a typical AOL subscriber), and thus your system must be easy to access, navigate, and operate.

The data items required for the music-store database can be classified into five categories: _videos_, _customers_, _employees_, _sales_, _suppliers_, and _orders_.

This classification does not imply any particular table arrangement. You are responsible for arranging the data items into tables, determining the relationships among tables and identifying the key attributes. In addition, you should include indices in your tables to speed up query processing. You should base your choice of indices on the type and expected frequency of the queries outlined in Section&nbsp;[3][8]. Finally, you should specify and enforce integrity constraints on the data, including referential integrity constraints.

However, before you begin thinking about your relational model (i.e. tables, indices, etc.), you should first create an E-R diagram of your VoD database system. The first project assignment, the details of which will be announced shortly, will ask you to create E-R, relational, and SQL models of your database system.

The items required for this category include:

1. Video ID
2. Title
3. Stars
4. Director
5. Year Produced
6. Motion Picture/Video Company
7. Motion Picture Association Rating
8. Video Classification Type
9. MPEG File
10. Wholesale Price
11. Download Price
12. Current Sale Price
13. Number of Rentals
14. Number of Downloads

Each video has an associated MPEG file. Your database will classify videos according to the video classification type. The classification scheme you are to implement should be tree-like. See the books section of the [amazon.com][6] for a good example of such a classification hierarchy. To implement such a hierarchy in your database system, you should use subtyping; i.e. make Video Classification Type  a user-defined data type, and subtype on that type.

As described in Section&nbsp;[3][8], you will want to create web pages that allow a customer to download a video from your VoD web site as streaming video at a specified date/time. You will also want to allow suppliers to upload video files to your web site, after having captured the video as an MPEG file.

Although a streaming download of a video should accompany every rental of a video, the number of rentals and the number of copies downloaded can be different. This can happen, for example, if you allow some video to be viewed for free as part of a promotional effort.

The items required for this category include:

1. Social Security no.
2. Last Name
3. First Name
4. Street Address
5. City
6. State
7. Zip Code
8. Credit Card no.
9. E-Mail Address
10. Videos Rented (for each rental, include date/time and rental price)
11. Videos Downloaded
12. Date of Last Rental
13. Date of Last Download
14. Outstanding Balance

The items required for this category include:

1. Social Security no.
2. Last Name
3. First Name
4. Street Address
5. City
6. State
7. Zip Code
8. Telephone
9. Start Date
10. Hourly Rate

The items required for this category include:

1. Transaction date and time
2. Requested Viewing date/time
3. Customer Representative
4. Customer
5. Videos downloaded and rental prices

You are to assign a customer representative to each transaction. This person is responsible for ensuring that the customer's order is filled properly and for answering any questions the customer may have regarding his or her transaction. You can choose any scheme you like for assigning customer representatives to transactions, as long as you document the scheme clearly. It should also be made clear during your project demo how your scheme works. One possible scheme is that the store's manager assigns a customer representative to each category of videos in your classification hierarchy. The revenue generated under a category is credited to its representative.

The items required for this category include:

1. Supplier Id
2. Company Name
3. Street Address
4. City
5. State
6. Zip Code
7. Telephone
8. Videos Supplied
9. Cost of each Video Supplied

This category of data should include the following:

1. Video Ordered
2. Supplier Id
3. Date Ordered
4. Date Received

&nbsp; A database _transaction_ can be viewed as a small program (written in the DML) that either updates or queries the database. Transactions that change the contents of the database must do so in a consistent manner. Moreover, transactions should not interfere with one another when running concurrently.

What follows is a breakdown of the user-level transactions that your database system should support.

The manager should be able to:

* Add, Edit and Delete information for an employee
* Obtain a sales report for a particular month
* Produce a comprehensive listing of all videos in stock
* Produce a list of rentals by video name or by customer name
* Produce a summary listing of revenue generated by a particular video, video type, or customer.
* Determine which film star generated most total revenue, and which customer representative generated most total revenue
* Determine which customer generated most total revenue
* Produce a Best-Sellers list of videos
* Add, Edit and Delete information for a supplier
* Place an order for videos with a supplier
* Update the database when the order is received to reflect the shipment
* Determine the least expensive supplier for a particular video

The manager is responsible for creating and maintaining the classification hierarchy of video types. When a new video is received from a supplier, the manager must decide into which category to place the video, and create a new category if necessary.

Customer Representatives should be able to:

* Add, Edit and Delete information for a customer
* Produce a customized menu for a customer
* List videos currently being offered at a special sale price
* Produce customer mailing lists
* Produce a list of video suggestions for a given customer (based on that customer's past rentals)

The customer should be able to easily browse the contents of your web site and make rentals and perform streaming downloads. While the customer will not be permitted to access the database directly, the customer should be able to retrieve the following information.

* Customer account information
* Videos currently being offered at a special sale price
* Videos by a given movie star, director, or rating value
* Videos of a particular type
* Videos with a particular keyword or set of keywords in the title
* Best-Seller list
* Personalized videos suggestion list

Customers should also be able to sample videos. That is, they should be able to download the first few seconds of any streaming video, at no charge.

Suppliers should be able to fill orders they are contracted for. To do so, they should have the capability to capture video as MPEG files and download the files to your database in order to fill an order.

Your database system should provide controlled access to the data by distinguishing between the different types of users: manager, customer representatives, and customers.

* Customer Representatives should not be able to perform manage-level transactions; however, they should be able to read employee information, except for the hourly rate.
* Customer Representatives should be able to record the receipt of an order from a supplier.
* A customer should not be allowed to access other customers' account information, or to any employee information.

HTML and its successors provide facilities for creating pop-up and pull-down menus, value lists, input/output forms, labels and customized reports. You should make use of all of these capabilities, and in the process come up with a system that caters to users with only limited computer knowledge. The information you provide to customers should look professional and inviting.

You will be required to supplement your completed database implementation  with a design document that contains information concerning your design criteria and decisions. The following is a list of some of the information you should include:

* Entity-Relationship (E-R) Diagram of the complete database scheme
* Lucid description of the relational database scheme of your web site's database including a discussion of the reasoning behind your design decisions. Make clear how your design supports efficient query processing.
* A list of all functional dependencies in the relational database scheme
* Description of integrity constraints including referential integrity

You will also be required to submit a _Users Guide_ that carefully explains how to use all aspects of the system. It should be understandable by non-computer experts. Be sure that the user interface (screen design, menu structure, etc.) is clearly explained.

You will be given assignments to produce an E-R and relational model of your system. The due dates for these assignments will be announced shortly.

All documentation should be done in HTML and be available on-line. Do not hand-in any hardcopies of anything during this course unless I explicitly ask you to.

After you have submitted the final system, you will be asked to present a short (15 minutes) demo to myself or the TA. Demos will take place on the Friday and Saturday of the last week of classes.

* * *

_Scott Smolka   
Last Modified: Tue Sep 18 11:20:11 EDT 2001_

[1]: mailto:yanrong@cs.sunysb.edu
[2]: http://www.cs.sunysb.edu/~yanrong/
[3]: http://www-4.ibm.com/software/data/highered/
[4]: /cgi-bin/nomail.cgi/yanrong/0/2
[5]: http://www.cs.sunysb.edu/~sas/courses/cse532/fall01/
[6]: http://www.amazon.com
[7]: http://www.mpeg.org/
[8]: main.html#sectxn
  