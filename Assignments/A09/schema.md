## DB Chat Client Schema

### Possible Schema

I found a schema here: https://github.com/yoosuf/Messenger that handles many possibilities, however, for our experiment / simulation we would have to write very intricate code to populate and simulate real time transactions for a schema so robust. 

<a href="https://github.com/yoosuf/Messenger"><img src="https://raw.githubusercontent.com/yoosuf/Messenger/master/Messenger.png" width="300"></a>

Therefore we should create a manageable schema that will be easier to populate and easier to gemerate simulated transactions. 

### Managable Schema 

This smaller schema has 4 tables: 

- Users
- Messages
- Message_Users

My thinking was to keep messages as seperate entities, with simply an `id`, `message body`, and `creation time`. Not worrying about "deleted messages", or "channels" or anything that would complicate our simulation. Having messages in a seperate table, will hopefully help in generating and inserting fake message traffic.  

The **`Users`** table is pretty straight forward easily populated using https://mockaroo.com. If everyone downloads 10 x 1000 users (using the same definition) we can easily create 100000 users.

The **`Message_Users`** table is how we "connect" messages to users. I thought keeping this seperate from the messages table would also help in generating and inserting fake message traffic. 

Lastly, the **`User_Connections`** table exists to help (again) with generating fake message traffic. If we can pre-populate the `User_Connections` table, this will help us generate messages between two existing "friends" more easily (or that's the idea).


<img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/chat_client_mini3.png" width="300">

```sql

CREATE SCHEMA IF NOT EXISTS `chat_client` DEFAULT CHARACTER SET utf8 ;
USE `chat_client` ;

-- -----------------------------------------------------
-- Table `chat_client`.`Users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chat_client`.`Users` (
  `user_id` INT NOT NULL,
  `username` VARCHAR(16) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `password` VARCHAR(32) NOT NULL,
  `create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `last_update` TIMESTAMP NULL,
  PRIMARY KEY (`user_id`));

-- -----------------------------------------------------
-- Table `chat_client`.`User_Connections`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chat_client`.`User_Connections` (
  `user_id` INT NOT NULL,
  `friend_id` INT NOT NULL,
  INDEX `friend_id_fk_idx` (`friend_id` ASC) VISIBLE,
  PRIMARY KEY (`user_id`, `friend_id`)

-- -----------------------------------------------------
-- Table `chat_client`.`Messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chat_client`.`Messages` (
  `message_id` INT NOT NULL,
  `message` TEXT NOT NULL,
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`message_id`));


-- -----------------------------------------------------
-- Table `chat_client`.`Message_Users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chat_client`.`Message_Users` (
  `message_id` INT NOT NULL,
  `from_id` INT NOT NULL,
  `to_id` INT NOT NULL,
  PRIMARY KEY (`message_id`, `from_id`, `to_id`),
);
```

 