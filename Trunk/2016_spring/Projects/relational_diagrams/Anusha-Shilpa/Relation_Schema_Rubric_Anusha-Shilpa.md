## Relational Design Grading Rubric

Group: **Anusha , Shilpa**

----

| Criteria(weight)   | 5-Exemplary                                                                                                                                                          | 3-Satisfactory                                                                                                                      | 1-NeedsImprovement                                                                                                       | Score(Weighted)   |
|:-------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------|:------------------|
| Notation(x3)       | Document uses an appropriate notation using some diagramming tool. The notation is used correctly for all elements of the diagram.                                   | Document uses an appropriate notation using some diagramming tool. The notation is used correctly for most elements of the diagram. | Document does not use an appropriate notation or the notation is used incorrectly for most elements of the diagram.      | 5 (15)            |
| Professional(x2)   | Document presents a professional appearance. It could be shared with a `real-world` customer without changes.                                                        | Document largely presents a professional tone. It could be shared with a `real-world` customer with minor revisions.                | Document is unprofessional. Major revisions would be necessary before sharing the document with a `real-world` customer. | 5 (10)             |
| Relations(x4)      | Relation schemas captures all the necessary relationships from the requirements document.                                                                            | Relation schemas captures most of the necessary relationships from the requirements document.                                       | Relation schemas captures some to few of the necessary relationships from the requirements document.                     | 3 (12)            |
| Tables(x4)         | Organized data elements into appropriate tables in a manner to handle all foreseeable queries.                                                                       | Organized data elements into appropriate tables in a manner to handle most foreseeable queries.                                     | Organized data elements into appropriate tables in a manner to handle some foreseeable queries.                          | 1 (4)             |
| PrimaryKeys(x3)    | Diagram indicates a primary key for every relation. All primary keys are clearly unique, or explanations are offered for their uniqueness.                           | Diagram indicates a primary key for nearly all relations. Most primary keys are clearly unique.                                     | Diagram fails to indicate primary keys.                                                                                  | 5 (15)            |
| ForeignKeys(x2)    | Diagram indicates all foreign keys and shows the tables that they reference.                                                                                         | Diagram indicates most foreign keys and shows the tables that they reference.                                                       | Diagram does not indicate foreign keys.                                                                                  | 5 (10)            |
| Redundancy(x2)     | Relation schemas include no redundant data without offering an explanation of the design requirements (e.g., performance) that indicate why redundancy is desirable. | Relation schemas include some redundant data. In most cases an explanation is given for why the redundancy is desirable.            | Relation schemas include significant duplication of data. No explanation is given for why the redundancy is desirable.   | 5 (10)            |
|                    |                                                                                                                                                                      |                                                                                                                                     |                                                                                                                          | **29 (76)**           |

### Notes:

How does a user search for a job? There is no jobs table. There is job seekers, companies, and interviews, but no jobs. 

Why is the employees table in relation to the companies table? They aren't employed by any of the companies that post jobs.

Why are there spaces in your column names? How can you query a column with spaces in a column name? It's possible, but it's not common practice and frowned upon.


