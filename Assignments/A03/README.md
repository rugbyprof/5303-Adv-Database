## Script Starter - Load data into Mysql w/ PHP
### Due: Monday Sep 9<sup>th</sup> by classtime.

### Overview

This is an easy assignment. You are simply going to run a php script from [here](./script.php) on the cs2 server from your home directory. It will create and load a new table called `users` with data from [here](./users.json). Its just an example of how to use a scripting language to interact with a database. 

Sounds easy but we need to get our script onto the server. This to is easy, but maybe a little confusing if you have never done it before. There are many ways to accomplish this task, but I'll cover a few. 

### SSH

- You will need to `ssh` into the server many many times this semester, so just get used to it. 
- Here are some choices (taken from slack)
  - https://www.chiark.greenend.org.uk/~sgtatham/putty/
  - https://www.cygwin.com/
  - https://git-scm.com/
- To log in to the server, open your terminal emulator and type:
  - `ssh yourusername@cs2.msutexas.edu`
- It will prompt you for your password. 
- Enter the one I gave you for mysql.
- If you have not changed your password yet:
  - Type the `passwd` command.
- Do NOT forget it!! 
- It also better not be a weak password!!

- Look in [Resources](../../Resources) for a list of necessary commands.

```

### FTP

- This is the easiest and the least cool way of doing it. No developer would use ftp if they didn't have to.
- Download an FTP client like [FileZilla](https://filezilla-project.org/) or [WinSCP](https://winscp.net/eng/download.php)
- Connect to the cs2 server:

![](https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/filezilla.png)

- Once you connect, you will see your folder (`/home/yourusername`) on the right.
- Drag your file over.

### Rsync

- This is a very cool command, but may not be available in some terminal emulators. I think gitbash doesn't have it.
- It stands for Remote SYNC, and it was created to keep two folders syncronized. It works great as a backup tool as well. If that interests you, go explore!
- Basic Command:
  - `rsync -avz source/file user@server:/location/path`
  - `rsync -avz script.php username@cs2.msutexas.edu:/home/username/5303/script.php`

