### Assignment 3 - Create your own server.
#### Due: 09-03-2021 (Friday @ 5:00 p.m.)


## DIGITAL OCEAN TUTORIALS:

### LAMP Stack

- LAMP = Linux Apache Mysql Php
- The following tutorial will help you install all of the items we discussed in a single tutorial.
- [Digital Ocean LAMP Tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-linux-apache-mysql-php-lamp-stack-on-ubuntu-20-04)

### PhpMyAdmin 

- PhpMyAdmin is the graphical component we will use to interact with our Mysql DB.
- [Digital Ocean PhpMyAdmin Tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-phpmyadmin-on-ubuntu-20-04)

### Introduction To Sql

- Optional tutorial on querying Mysql
- [Digital Ocean MySql Sql Tutorial](https://www.digitalocean.com/community/tutorials/introduction-to-queries-mysql)



### Copying Your Repo 

- After you install apache, you will have a root web folder here: `/var/www/html`
- Change to the `/var/www/html` directory and clone your `5303-your-repo-name` course repo to the web root:
  - `git clone 5303-your-repo-name`
- Rename your `5303-your-repo-name` repo folder to `DataBase`
- It will act the same as it did before.
- If you want to push new content:
  
  ```bash
    cd DataBase
    git add .
    git commit -m "commit message"
    git push origin main
  ```

- To get content:

```bash
    cd DataBase
    git pull
```

### Security

- There are security issues exposing a `.git` folder in the "web-root" of your server.
- Don't put anything with passwords or sensitive info right now. I will show you how to secure it on Wednesday.
- If your interested in getting started here are a couple of methods securing your .git repos

**1)**  Directory Match
 
- Tells server to not let anyone access any .git folder
- This tutorial uses `vi` to edit files. Replace `vi` with `nano` OR use Vscode (if your logged in as root) to do your editing. 
- https://www.serverlab.ca/tutorials/linux/web-servers-linux/protect-git-folders-in-apache/

**2)**  Alter web Root

- This changes the servers web root to be a sub folder in your repo thereby placing the .git folder one level back not giving the web access.
- https://stackoverflow.com/questions/7818537/using-a-git-repository-as-a-website-root-folder

