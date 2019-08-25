# Library System

## Spring 2015

### Description

The objectives of the library system are to allow patrons to:

* withdraw and return books
* search the library's books
* pay overdue charges and librarians to:

    * add/delete books to/from the library's holding
    * move books from one shelf of the library to another.


### Specifications / Requirements:

1. The system shall contain information about each valid patron of the system: 
- name
- password
- address_, 
_Id_, 
unpaid _fine_s, 

the identity of each book the patron has currently withdrawn and its _due-date_. It is assumed that the information about all patrons is part of the initial state of&nbsp; the database (no interactions are needed to add or delete patrons from the system).
2. The system shall contain information about each librarian: _name, password, address_, _Id_.&nbsp; It is assumed that the information about all librarians is part of the initial state of&nbsp; the database (no interactions are needed to add or delete librarians from the system).&nbsp; Librarians can be patrons.
3. The system shall contain information about each book in the library's holdings: _isbn_ number, _title_,&nbsp;_ author_(s), _year_ (of publication), copy _number_, _shelf-Id_, __publisher, _publisher's_ city___, _current _status_ (on-loan, on-shelf, on-hold, on-loan-and-on-hold), the date on which the book entered loan and/or hold status.&nbsp; For books on loan the system shall contain the _Id_ of the patron involved.&nbsp; For books on loan and overdue the system shall contain the date on which the last reminder letter was sent.&nbsp; For books on hold the system shall contain an ordered list of _Id_s of patrons who have requested hold status.
4. _The system shall contain the year of birth of each author_.
5. The system shall contain information about each shelf in the library: s_helf-Id, capacity _(number of books that it can hold).

##

* * *

  
**_Assumptions_**

* _Author names (but not patron names) are unique_.
* _An author does not (co-) author more than one book per year_.
* _An author does not (co-) author more than one book with a particular title_.
* * *

  
**Integrity Constraints**

&gt; The database shall satisfy the following integrity constraints.

    1. _A patron can request a book that is currently withdrawn.&nbsp; This fact needs to be stored in the database, and when the book is returned it should be placed on hold status for at most 3 days _(_the count starts when the book is returned)_.&nbsp; If after removing a book from hold status as a result of this constraint, the hold list is empty, the book reverts to the on shelf status.
    2. _A patron cannot withdraw a book if his/her unpaid fines exceed $5._
    3. A patron cannot withdraw more than 2 books at any one time.
    4. The date on which the last reminder letter for an overdue book was sent cannot be more than one week old.
    5. _The number of books on a shelf cannot exceed its capacity._
    6. _A book on loan for more than one week becomes overdue._

##

* * *

##  Interactions with the System

&gt; In order to perform the following interactions with the system, a user&nbsp; must login&nbsp; first with a valid _Name_ and _password_.&nbsp; If login is successful the user's _Id_ is returned by the DBMS to the application program. All subsequent interactions are assumed to have been initiated by that user until the session completes (the user logs out) .&nbsp; Since _Id_ is used to identify the user in these interactions, the application should retain _Id_ until the end of the session, supplying it as a parameter when necessary to the DBMS.&nbsp; _The session is ended with logout, _at which point the application can discard _Id_ and the next interaction must be a new login.

**withdraw - (patron)**
:  The purpose of this interaction is to allow a patron to withdraw a book. __title _and one of the _author _names are supplied at the screen_ . The interaction fails if:

&gt; * The book is already withdrawn.
&gt; * _The book is not in the library's collection._
&gt; * The patron has already withdrawn _2_ books.
&gt; * The patron owes more than $5.
&gt; * The book is on hold and the patron is not at the head of the hold list.

**hold - (patron)**
:  The purpose of this interaction is to allow a patron to place a book that is currently withdrawn or being held (for a different patron) on hold. __title _and one of the_ author _names are supplied at the screen_. An ordered list is maintained of all patrons who have placed the book on hold. The interaction fails if

* _The patron has withdrawn and not yet returned the book_
* _The book is not in the library's collection_
* The book is on the shelf
* The patron has already withdrawn _2 _books.
* The patron owes more than $5.
  
&nbsp; :  **return - (patron)**

:  The purpose of this interaction is to allow a patron to return a book that he/she has withdrawn. _t_itle ___and_ _one of the_ author _names are supplied at the screen._ If the book is overdue, the patron's charge record is updated by an amount of $1 a day. If the book is on hold, a call is made to the patron at the head of the hold list (you can ignore the call in the transaction, but you should record the date that the call was made). The interaction fails if the book is not recorded as being withdrawn by that patron.

  
&nbsp;

**add - ( librarian)**
:  The purpose of this interaction is to allow a librarian to add a new book to the library's holding.&nbsp; __isbn, title, year, author_(s)_, _and _shelf-Id_ (of the shelf on which the book is to be stored) are supplied at the screen_. Multiple copies of the same book can exist in the library's holdings. The interaction fails&nbsp; if

&gt; * The initiator is not a librarian (one implementation of this is that your interface ensures that only a librarian can initate this interaction).
&gt; * The shelf is full.
&gt; * _The book specifications conflict with a book already in the library's collection (e.g., if there is a book in the library's collection with the same isbn number but a different author, title, or year._

**move - (librarian)**
:  The purpose of this interaction is to allow a librarian to move a book from one shelf to another. __title, _one of the _author _names_,_ and copy _number _(to identify the book) and _shelf-Id_ (to identify the new shelf) are supplied_. The interaction fails if

&gt; * The book is not in the library's holdings.
&gt; * The initiator is not a librarian.
&gt; * The shelf is full.

**remove - ( librarian)**
:  The purpose of this interaction is to allow a librarian to remove a book from the library's holding.&nbsp;&nbsp; _t_itle ___and_ _one&nbsp; of the _author _names_ _are supplied at the screen_. The interaction fails if the book is not in the library's holdings, if _the book is currently withdrawn_, or if the initiator is not a librarian.

  
&nbsp;

**search - ( patron)**
:  The purpose of this interaction is to allow a patron to search for a book in the library's holdings.&nbsp;&nbsp; _One or more of the following: _title, author, year_ are supplied at the screen_. _Either title or author must be supplied, however the title need not be complete - a substring of the title might be supplied - and only a single author can be supplied (even though books can have multiple authors).&nbsp; A range of years can be specified.&nbsp; For example, the search "list all books with the word `hiking' in the title written by Smith (there might be coauthors) between 1995 and 2000.&nbsp; The title, author and year of all books that satisfy the search criterion are&nbsp; output._

  
&nbsp;

**pay - (patron)**
:  The purpose of this interaction is to allow a patron to pay a fine.&nbsp; The amount of payment is deducted from the balance owed. _The&nbsp; amount of the payment is input at the screen_. Any excess is considered a donation to the library.&nbsp; The amount of fine remaining is displayed _on the screen_.

  
&nbsp;

**next-day - (librarian)**
:  The purpose of this interaction is to allow a librarian to record the fact that another day has passed.&nbsp; The interaction fails if the initiator is not a librarian.&nbsp; Actions which depend on the date (e.g., removing a book from hold status) should be automatically triggered by this interaction.

* * *

  
&nbsp;  