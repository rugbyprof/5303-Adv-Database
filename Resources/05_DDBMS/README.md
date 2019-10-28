## What is ACID Compliance?

The presence of four components — atomicity, consistency, isolation and durability — can ensure that a database transaction is completed in a timely manner. When databases possess these components, they are said to be ACID-compliant. But just what is ACID compliance, and why should you care? Let’s take a look:

**Atomicity:** Database transactions, like atoms, can be broken down into smaller parts. When it comes to your database, atomicity refers to the integrity of the entire database transaction, not just a component of it. In other words, if one part of a transaction doesn’t work like it’s supposed to, the other will fail as a result—and vice versa. For example, if you’re shopping on an e-commerce site, you must have an item in your cart in order to pay for it. What you can’t do is pay for something that’s not in your cart. (You can add something into your cart and not pay for it, but that database transaction won’t be complete, and thus not ‘atomic’, until you pay for it).

**Consistency:** For any database to operate as it’s intended to operate, it must follow the appropriate data validation rules. Thus, consistency means that only data which follows those rules is permitted to be written to the database. If a transaction occurs and results in data that does not follow the rules of the database, it will be ‘rolled back’ to a previous iteration of itself (or ‘state’) which complies with the rules. On the other hand, following a successful transaction, new data will be added to the database and the resulting state will be consistent with existing rules.

**Isolation:** It’s safe to say that at any given time on Amazon, there is far more than one transaction occurring on the platform. In fact, an incredibly huge amount of database transactions are occurring simultaneously. For a database, isolation refers to the ability to concurrently process multiple transactions in a way that one does not affect another. So, imagine you and your neighbor are both trying to buy something from the same e-commerce platform at the same time. There are 10 items for sale: your neighbor wants five and you want six. Isolation means that one of those transactions would be completed ahead of the other one. In other words, if your neighbor clicked first, they will get five items, and only five items will be remaining in stock. So you will only get to buy five items. If you clicked first, you will get the six items you want, and they will only get four. Thus, isolation ensures that eleven items aren’t sold when only ten exist.

**Durability:** All technology fails from time to time… the goal is to make those failures invisible to the end-user. In databases that possess durability, data is saved once a transaction is completed, even if a power outage or system failure occurs. Imagine you’re buying in-demand concert tickets on a site similar to Ticketmaster.com. Right when tickets go on sale, you’re ready to make a purchase. After being stuck in the digital waiting room for some time, you’re finally able to add those tickets to your cart. You then make the purchase and get your confirmation. However if that database lacks durability, even after your ticket purchase was confirmed, if the database suffers a failure incident your transaction would still be lost! As you might expect, this is a really bad thing to happen for an online e-commerce site, so transaction durability is a must-have.

<sup>Source: https://www.clustrix.com/bettersql/acid-compliance-means-care/ </sup>

### Mirroring / Replication

1. **Mirroring** involves the duplication of a database stored at different machines where original database is known as primary database and copied database is known as a mirror. On the other hand, **replication** is the duplication of data and database objects stored at the different location to improve the performance of the distribution database.
2. **Mirroring** is performed on the database while **replication** is implemented on data and database objects.
3. The mirror database can usually be found in the different machine from its primary database. 4. The **replicated** data and database objects are stored in another database.
5. The **mirroring** of a database costs higher than replication of data.
6. **Mirroring** doesn’t support distributed environment whereas **replication** was devised for the distributed database.

<sup>Source:https://techdifferences.com/difference-between-mirroring-and-replication.html</sup>

### Sharding / Partitioning

- **Partitioning** is a general term used to describe the act of breaking up your logical data elements into multiple entities for the purpose of performance, availability, or maintainability. 

- **Sharding** is the equivalent of **horizontal partitioning**.  When you shard a database, you create replica's of the schema, and then divide what data is stored in each shard based on a shard key.  For example, I might shard my customer database using CustomerId as a shard key - I'd store ranges 0-10000 in one shard and 10001-20000 in a different shard.  When choosing a shard key, the DBA will typically look at data-access patterns and space issues to ensure that they are distributing load and space across shards evenly. 

- **Vertical partitioning** is the act of splitting up the data stored in one entity into multiple entities - again for space and performance reasons.  For example, a customer might only have one billing address, yet I might choose to put the billing address information into a separate table with a CustomerId reference so that I have the flexibility to move that information into a separate database, or different security context, etc.   

- **To summarize**
    - **partitioning** is a generic term that just means dividing your **logical entities** into different **physical entities** for performance, availability, or some other purpose.  
    - **Horizontal partitioning**, or **sharding**, is replicating the schema, and then dividing the data based on a shard key.  
    - **Vertical partitioning** involves dividing up the schema (and the data goes along for the ride).

<sup>Source:https://www.quora.com/Whats-the-difference-between-sharding-DB-tables-and-partitioning-them</sup>