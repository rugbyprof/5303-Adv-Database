## Relational Design Grading Rubric

Group: **Ramesh, Naveen, Vaisali**

----

| Criteria(weight)   | 5-Exemplary                                                                                                                                                          | 3-Satisfactory                                                                                                                      | 1-NeedsImprovement                                                                                                       | Score(Weighted)   |
|:-------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------|:------------------|
| Notation(x3)       | Document uses an appropriate notation using some diagramming tool. The notation is used correctly for all elements of the diagram.                                   | Document uses an appropriate notation using some diagramming tool. The notation is used correctly for most elements of the diagram. | Document does not use an appropriate notation or the notation is used incorrectly for most elements of the diagram.      | 5 (15)            |
| Professional(x2)   | Document presents a professional appearance. It could be shared with a `real-world` customer without changes.                                                        | Document largely presents a professional tone. It could be shared with a `real-world` customer with minor revisions.                | Document is unprofessional. Major revisions would be necessary before sharing the document with a `real-world` customer. | 3 (6)             |
| Relations(x4)      | Relation schemas captures all the necessary relationships from the requirements document.                                                                            | Relation schemas captures most of the necessary relationships from the requirements document.                                       | Relation schemas captures some to few of the necessary relationships from the requirements document.                     | 3 (12)            |
| Tables(x4)         | Organized data elements into appropriate tables in a manner to handle all foreseeable queries.                                                                       | Organized data elements into appropriate tables in a manner to handle most foreseeable queries.                                     | Organized data elements into appropriate tables in a manner to handle some foreseeable queries.                          | 1 (4)             |
| PrimaryKeys(x3)    | Diagram indicates a primary key for every relation. All primary keys are clearly unique, or explanations are offered for their uniqueness.                           | Diagram indicates a primary key for nearly all relations. Most primary keys are clearly unique.                                     | Diagram fails to indicate primary keys.                                                                                  | 5 (15)            |
| ForeignKeys(x2)    | Diagram indicates all foreign keys and shows the tables that they reference.                                                                                         | Diagram indicates most foreign keys and shows the tables that they reference.                                                       | Diagram does not indicate foreign keys.                                                                                  | 5 (10)            |
| Redundancy(x2)     | Relation schemas include no redundant data without offering an explanation of the design requirements (e.g., performance) that indicate why redundancy is desirable. | Relation schemas include some redundant data. In most cases an explanation is given for why the redundancy is desirable.            | Relation schemas include significant duplication of data. No explanation is given for why the redundancy is desirable.   | 5 (10)            |
|                    |                                                                                                                                                                      |                                                                                                                                     |                                                                                                                          | **27 (72)**           |

### Notes:

I can see by the lack of tables that there wasn't much creativity put into the schema design. You will see that when you attempt to implement some of the queries, that it will be difficult, or impossible. For example, flights are supposed to be priced based on distance flown `e.g. Fare = $50 + (Distance * $0.11)`. How do you calculate distance?

The popularity of databases in general was driven by business, and every business wants to know how they are performing from month to month, quarter to quarter and year to year. Is your group confident that they can calculate monthly earning statements? Find out how much money was lost due to empty seats? Or empty Isle or Window seats?

Also someone must work at the airline. Where is their information and credentials stored?

What do you do with flights that are completed? Do you delete them, leave them, move them? 






