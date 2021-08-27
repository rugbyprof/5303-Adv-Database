## Linux Commands

Not a whole lot of order, I just put commands in this file as I saw them in the `history` or as I thought of them.

### Adding Users

- `useradd` is native binary compiled with the system. (only adds the user with nothing else!) 
- `adduser` is more user friendly and interactive than its back-end useradd. 


- `adduser` : adds a new user to your server as well as:
    -   creates a directory for them in `/home`
    -   prompts for a password
    -   copies some files into the home directory to allow:
        -   a history to be kept (`.bash_history`)
        -   and a file to place aliases in so they are remembered the next time you log in (`.bashrc`).

- `userdel -r username` removes a user along with thier home directory.

### Package Management

- `apt update` : updates the repos for the package manager
- `apt upgrade` : actually installs the new packages
- Run both `apt update && apt upgrade -y` (-y is a flag that auto answers yes when prompted)
- `apt search keyword` finds a package that contains "keyword"
- `apt install packageName` installs a package
- `apt remove packageName` removes a package

### Moving Around FileSystem

>NOTE: In linux the `.` by itself refers to the "current folder", and the `..` references the previous directory.

- `cd` change to your home directory (`/home/username` OR `/root` if you are root)
- `cd /directory/subdirectory` changes into  /directory/subdirectory
- `cd ..` move back (or up) 1 folder
- `cd ../../..` move back (or up) 3 folders
- `cd /var/www/html` change into web roots folder
- `cd .` means change into "this" folder :) You wont do it, but its valid.
- `./runme` this says execute the file called `runme` located in "this" folder


### Make or Remove Directorys and Files

- `touch fileName` - creates an empty file called "fileName"
- `rm fileName` - deletes the file called "fileName"
- `mv fileName newName` - renames "fileName"=>"newName"
- `mv fileName ..` - moves file back one folder keeping same name
- `mv fileName ../newName` - moves file back one folder renaming to "newName"
- `mv /var/www/html/file1 /home/griffin/` moves file1 to a new location keeping same name
- `mv /var/www/html/file1 /home/griffin/newFileName1` same as previous,but renames "file1"=>"newFileName1"
- `mkdir dirname` - creates a directory
- `mkdir ../dirname` - creates a directory in your parent folder
- `mkdir /var/www/html/website1/images` - would create the folder `images` if all the previous folders exist. If they don't you should use the `-p` flag that says to "create parent folders" if they dont exist.
- `rmdir` removes a directory (if its empty)
- `rm -rf folderName` - deletes a folder with files in it. `-r` = recurse into file `-f` = force ( don't prompt me if I'm sure just do it).


### Some Notable Directories

- `/home` - where all user dirs are
- `/var/www/html` - root web folder (for Apache)
- `/etc` - Another folder where lots of system software is located
- `/usr/bin` - Executable (binary) files are here. Most of the commands you use exist in this folder.
- `/usr/local/bin` - A place to store your own executables if you want to write them.
- `/usr/share` - Folder where some extra software is installed (like phpmyadmin)
- `/root/.ssh` or `/home/user/.ssh` The folder where your ssh keys live.



### Git Commands

- Add username and email so git knows who is running commands
  - `git config --global user.name username`
  - `git config --global user.email youremail@gmail.com`
- `git init` - Run inside a folder you want to turn into a repository.
- `git status` - Check to see if you need to commit anything.
- `git add .` - Add all new files in folder to be tracked.
- `git commit -m "commit message"` - Commit any changes made for git to track.

### Misc

- `nano fileName` opens terminal editor allowing you to edit "fileName".
- `passwd` - lets you change your passwd
- `passwd user` lets root change passwd of user

### ssh

- `ssh-keygen -t ed25519 -C "terry.griffin@msutexas.edu"` generate an ssh key
- `authorized_keys` file in .ssh folder where you put your public keys to allow passwordless login
- `known_hosts` all machines that have connected put thier key in this file 