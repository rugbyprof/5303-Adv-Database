## First Assignment

#### Part 1 Due: Monday August 31st by Midnight
#### Part 2 Due: Wednesday September 2nd by Midnight

### Description

It seems that we discussed a lot of topics on the 26th in class, a small part of it actually pertained to DB's, so 
I think it's time to put it all together to show how it all connects. The best way to utilize everything we discussed 
in class is to actually perform tasks that require you to do so.  

### Goal

We are going to write a php script to obtain "User Information" from the web using an API called https://randomuser.me/api/. 
This API allows developers to grab "random" user information (with images and everything) for use in developing applications.
I would like you to grab information for 100 users and place it into a table in your Mysql database.

I know this isn't a php scripting class, but your in grad school so suck it up. Dont worry though, I will give you step by 
step instructions to guide you through this process. You will have to make some decisions about column names and thier data
types. The rest will be provided by me.


### Basic Overview

I will list the steps below, then explain each one further down.

#### Part1

1. Log into server and change your password to your account.
2. Create a `public_html` folder in your home directory. 
3. Create a folder called `assignment1` in your `public_html` folder.
4. Create a file called `load_db.php` in your `assignment1` folder. 
5. Log into http://cs2.mwsu.edu/phpmyadmin 
6. Create a table to hold our data called `users` 

#### Part2
7. Add php code to `load_db.php` to access the api, and load the data.
8. Add your code to github.


#### 1.

Open up a terminal (shell) and connect to our server:
```bash
ssh yourusername@cs2.mwsu.edu
password: (enter password)
```
If your using putty, just fill out the fields like you saw in class.

This is my command prompt: `user@cs2:~$`. When you see this, I'm typing commands at the terminal.

```bash
user@cs2:~$ passwd
Changing password for griffin.
(current) UNIX password: (enter current password)
Enter new UNIX password: (enter new password)
Retype new UNIX password: (again)
passwd: password updated successfully
```

---

#### 2.

```bash
user@cs2:~$ mkdir public_html
```

---

#### 3.

```bash
user@cs2:~$ cd public_html
user@cs2:~$ mkdir assignment1
```

---

#### 4.

```bash
user@cs2:~$ cd assignment1
user@cs2:~$ touch load_db.php
```

---

#### 5.

Now you have to use your brain (a little). Given the following json response from https://randomuser.me/api/ create a table in 
your mysql database to hold some of the data. I will list the items I want included in your table. Json is `javascript object
notation`, and holds information using key:value pairs. I want you to name the columns in your table using the "keys" and choose
datatype for your columns using the "values". For example:

```
gender:"female"

Column name: gender
Datatype : enum('male','female')

email:"manuela.velasco50@example.com"

Column name: email
Datatype: varchar(64)
```

```json
{
  results: [{
    user: {
      gender: "female",
      name: {
        title: "ms",
        first: "manuela",
        last: "velasco"
      },
      location: {
        street: "1969 calle de alberto aguilera",
        city: "la coruña",
        state: "asturias",
        zip: "56298"
      },
      email: "manuela.velasco50@example.com",
      username: "heavybutterfly920",
      password: "enterprise",
      salt: ">egEn6YsO",
      md5: "2dd1894ea9d19bf5479992da95713a3a",
      sha1: "ba230bc400723f470b68e9609ab7d0e6cf123b59",
      sha256: "f4f52bf8c5ad7fc759d1d4156b25a4c7b3d1e2eec6c92d80e508aa0b7946d4ba",
      registered: "1303647245",
      dob: "415458547",
      phone: "994-131-106",
      cell: "626-695-164",
      DNI: "52434048-I",
      picture: {
        large: "http://api.randomuser.me/portraits/women/39.jpg",
        medium: "http://api.randomuser.me/portraits/med/women/39.jpg",
        thumbnail: "http://api.randomuser.me/portraits/thumb/women/39.jpg",
      },
      version: "0.6"
      nationality: "ES"
    },
    seed: "graywolf"
  }]
}
```

I want your table to have the following columns:

```
  gender
  title
  first
  last
  street
  city
  state
  zip
  email
  username
  password
  dob
  phone
  picture 
```

Out of 1000 requests to the api, I found the max column lengths to be:

```
Array
(
    [gender] => 6
    [title] => 4
    [first] => 12
    [last] => 16
    [street] => 38
    [city] => 30
    [state] => 13
    [zip] => 5
    [email] => 38
    [username] => 21
    [password] => 10
    [dob] => 10
    [phone] => 14
    [medium] => 52
)
```

### Part 2

Coming Next

