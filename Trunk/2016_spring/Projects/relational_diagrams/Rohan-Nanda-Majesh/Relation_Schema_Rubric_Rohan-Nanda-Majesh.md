## Relational Design Grading Rubric

Group: **Rohan-Nanda-Majesh**

----

| Criteria(weight)   | 5-Exemplary                                                                                                                                                          | 3-Satisfactory                                                                                                                      | 1-NeedsImprovement                                                                                                       | Score(Weighted)   |
|:-------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------|:------------------|
| Notation(x3)       | Document uses an appropriate notation using some diagramming tool. The notation is used correctly for all elements of the diagram.                                   | Document uses an appropriate notation using some diagramming tool. The notation is used correctly for most elements of the diagram. | Document does not use an appropriate notation or the notation is used incorrectly for most elements of the diagram.      | 1 (3)            |
| Professional(x2)   | Document presents a professional appearance. It could be shared with a `real-world` customer without changes.                                                        | Document largely presents a professional tone. It could be shared with a `real-world` customer with minor revisions.                | Document is unprofessional. Major revisions would be necessary before sharing the document with a `real-world` customer. | 5 (10)             |
| Relations(x4)      | Relation schemas captures all the necessary relationships from the requirements document.                                                                            | Relation schemas captures most of the necessary relationships from the requirements document.                                       | Relation schemas captures some to few of the necessary relationships from the requirements document.                     | 3 (12)            |
| Tables(x4)         | Organized data elements into appropriate tables in a manner to handle all foreseeable queries.                                                                       | Organized data elements into appropriate tables in a manner to handle most foreseeable queries.                                     | Organized data elements into appropriate tables in a manner to handle some foreseeable queries.                          | 3 (12)             |
| PrimaryKeys(x3)    | Diagram indicates a primary key for every relation. All primary keys are clearly unique, or explanations are offered for their uniqueness.                           | Diagram indicates a primary key for nearly all relations. Most primary keys are clearly unique.                                     | Diagram fails to indicate primary keys.                                                                                  | 5 (15)            |
| ForeignKeys(x2)    | Diagram indicates all foreign keys and shows the tables that they reference.                                                                                         | Diagram indicates most foreign keys and shows the tables that they reference.                                                       | Diagram does not indicate foreign keys.                                                                                  | 5 (10)            |
| Redundancy(x2)     | Relation schemas include no redundant data without offering an explanation of the design requirements (e.g., performance) that indicate why redundancy is desirable. | Relation schemas include some redundant data. In most cases an explanation is given for why the redundancy is desirable.            | Relation schemas include significant duplication of data. No explanation is given for why the redundancy is desirable.   | 5 (10)            |
|                    |                                                                                                                                                                      |                                                                                                                                     |                                                                                                                          | **27 (72)**           |

### Notes:

How do you represent employees of the airline who can look up passenger manifests, and change status of aircraft etc..

How do you calculate the cost of a flight? For example: `Fare = $50 + (Distance * $0.11)` But there is no place to find distance. 

How does a passenger request a window seat?

What are the data types of all your columns? I am ok with you not using one of the recommended tools to create your schema, but I'm not ok with the lack of information provided.







