## Relational Design Grading Rubric

Group: **Sahaja, Vasantha**

----

| Criteria(weight)   | 5-Exemplary                                                                                                                                                          | 3-Satisfactory                                                                                                                      | 1-NeedsImprovement                                                                                                       | Score(Weighted)   |
|:-------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------|:------------------|
| Notation(x3)       | Document uses an appropriate notation using some diagramming tool. The notation is used correctly for all elements of the diagram.                                   | Document uses an appropriate notation using some diagramming tool. The notation is used correctly for most elements of the diagram. | Document does not use an appropriate notation or the notation is used incorrectly for most elements of the diagram.      | 5 (15)            |
| Professional(x2)   | Document presents a professional appearance. It could be shared with a `real-world` customer without changes.                                                        | Document largely presents a professional tone. It could be shared with a `real-world` customer with minor revisions.                | Document is unprofessional. Major revisions would be necessary before sharing the document with a `real-world` customer. | 5 (10)            |
| Relations(x4)      | Relation schemas captures all the necessary relationships from the requirements document.                                                                            | Relation schemas captures most of the necessary relationships from the requirements document.                                       | Relation schemas captures some to few of the necessary relationships from the requirements document.                     | 3 (12)            |
| Tables(x4)         | Organized data elements into appropriate tables in a manner to handle all foreseeable queries.                                                                       | Organized data elements into appropriate tables in a manner to handle most foreseeable queries.                                     | Organized data elements into appropriate tables in a manner to handle some foreseeable queries.                          | 3 (12)            |
| PrimaryKeys(x3)    | Diagram indicates a primary key for every relation. All primary keys are clearly unique, or explanations are offered for their uniqueness.                           | Diagram indicates a primary key for nearly all relations. Most primary keys are clearly unique.                                     | Diagram fails to indicate primary keys.                                                                                  | 5 (15)            |
| ForeignKeys(x2)    | Diagram indicates all foreign keys and shows the tables that they reference.                                                                                         | Diagram indicates most foreign keys and shows the tables that they reference.                                                       | Diagram does not indicate foreign keys.                                                                                  | 3 (6)             |
| Redundancy(x2)     | Relation schemas include no redundant data without offering an explanation of the design requirements (e.g., performance) that indicate why redundancy is desirable. | Relation schemas include some redundant data. In most cases an explanation is given for why the redundancy is desirable.            | Relation schemas include significant duplication of data. No explanation is given for why the redundancy is desirable.   | 3 (6)             |  
|                    |                                                                                                                                                                      |                                                                                                                                   |  -5 bad data types                                                                                                                        | ***29 (79)***     |

### Notes:

Job seekers and employees should share the same table (or a portion of one since there is so much redundant data). Employees should not have a relationship with the "Company" table, that table is for companies that post jobs.

Table creation and organization could have been better. We can discuss that in person as well. 

The foreign key situation is confusing, we need to discuss what your group is trying to represent. Why does a job seeker have a direct relationship with a company? Not saying it's wrong, but it needs explained.

Why would you use `Text` for city, state, first, last? Text holds up to 2<sup>16</sup> bytes or ~ 64000!! Even though varchar can hold that much as well, it indexes much better than a text field. Then you turn around and only give 30 characters for a companies name and street address ? 


I don't even have something in the rubric to handle a blatant misuse of data types because I couldn't imagine someone using text for a state (two chars).



