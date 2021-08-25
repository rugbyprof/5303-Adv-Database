### Assignment 2 - Create your own server.
#### Due: August 31<sup>st</sup> by 2359 hours (1 minute before midnight).

-----

>Follow the steps below to create your own server. If these steps aren't clear enough, you can 
view an online tutorial [here](https://www.digitalocean.com/community/tutorials/how-to-create-your-first-digitalocean-droplet-virtual-server).

-----

#### 1. [Sign up](https://cloud.digitalocean.com/registrations/new) for Digital Ocean.

This will cost you around $5.00 + tax for the entire month. 

-----

#### 2. [Create a new Droplet](https://cloud.digitalocean.com/droplets/new)

- Droplet Hostname
> Pick a name for your computer. This is NOT a domain name that will be DNS resolvable.

- Select Size
> 512MB / 1 CPU<br>
20GB SSD DISK<br>
1TB TRANSFER<br>

- Select Region
> Pick the closest region to Texas.

- Select Image
> Ubuntu 14.04 x64

- Select Applications (Tab over from image)
> LAMP on Ubuntu 14.04

- Add optional SSH Keys
> Skip, we will address ssh keys later.

- Settings
> Leave default settings, and don't worry about backups (unless you want to pay).

-----

#### 3. IP Address & Password

- The IP address that is assigned to your "droplet", is your only connection to your server.
- The root password will be emailed to you.
- You need both IP address & password to access your new server.

#### 4. Accessing Your Server

- Open some type of "terminal" (like [putty](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html)) application and log into your server using:
    - The IP address given to you
    - The password emailed to you
- Change your root password!
    - Run the following command (note: the dollar `$` sign just implies "command line", don't use it in the command):
    - `$ passwd`
    - Follow the prompts.
- Add yourself as a user:
    - `$ adduser your-new-username`
    - Follow the prompts.
    - Stay root for now, but as soon as you add 'your-new-username' to `sudoers`, you should change to your new user:
    - `$ su your-new-username`
- Add me as a user:
    - `$ adduser griffin`
    - Set my password as `BigData2014!`, I will change it as necessary.
- Now we need to edit the `sudoers` file. `Sudoers` is a file that allows regular users to run commands as "root" as long as an entry is placed correctly in the file. 
- "Your-new-user" and "griffin" both need to be added:
    - A comprehensive tutorial about sudoers is available [Here](https://help.ubuntu.com/community/Sudoers).
    - Shortcut version:
        - (As root) $ nano /etc/sudoers
        - Edit sudoers and add two lines using the following example:

```txt
# User privilege specification
root	            ALL=(ALL:ALL) ALL

# Add yourself:
your-new-username 	ALL=(ALL:ALL) ALL

# Add me:
griffin 	        ALL=(ALL:ALL) ALL
```

#### 5. Basic necessary packages:

```bash
# update the package repositories
$ sudo apt-get update

# actually update any out of data packages
$ sudo apt-get upgrade

# install git a distributed version control system  
$ sudo apt-get install git

```

#### 6. Testing Your Server

- Go to http://your.ip.address/ and see if the apache default page shows up.


#### 7. Github

- Create a folder called `BigData` in your `/var/www/html` directory.
- Change into that folder: `cd BigData`
- Run the following: `git init`.
- If you get an error from the previous command, most likely `git` is not installed, so run:

```
sudo apt-get install git
```
- Then try `git init` again.

- If you succesfully ran the previous command, then great! You should see a folder: `.git` in your `BigData` folder now.
- Go [HERE](https://help.github.com/articles/generating-ssh-keys/) and follow this Github tutorial to generate ssh keys to allow you to "push" files from your server to Github.
- Now go [HERE](https://help.github.com/articles/adding-an-existing-project-to-github-using-the-command-line/) to add this `.git` repo to the one you created in your first assignment.

#### 8. Commit Your First File to Github

- Create a folder called `BigData` in `/var/www/html/`
- Create a file called `README.md` in `/var/www/html/BigData`
- The `README.md` file shows up when someone browses to your repository!

- In your `README.md` file, place the following info (using nice markdown):

-----

### Name

Your name

### Github Username

Your github username

### Server IP

http://111.222.333.444

-----

When your all done, you should have a directory structure like:

-----
- ![1] /var/www/html
    - ![1] BigData
         - ![9] README.md 

-----

___Now commit your new "repo" to Github!___

```
git add .
git commit -m "My first commit"
git push origin master
```

If it doesn't work, then your ssh keys, or your upstream remote wasn't set correctly. 
Come get help from me, because from here on out, everything gets pushed to Github.


[1]:  https://cs.mwsu.edu/~griffin/icons/icons8-folder-24.png
[2]:  https://cs.mwsu.edu/~griffin/Free-file-icons/24px/php.png
[3]:  http://cs.mwsu.edu/~griffin/Free-file-icons/24px/html.png
[4]:  http://cs.mwsu.edu/~griffin/Free-file-icons/24px/css.png
[5]:  http://cs.mwsu.edu/~griffin/Free-file-icons/24px/js.png
[6]:  http://cs.mwsu.edu/~griffin/Free-file-icons/24px/json.png
[7]:  http://cs.mwsu.edu/~griffin/Free-file-icons/24px/xml.png
[8]:  http://cs.mwsu.edu/~griffin/Free-file-icons/24px/csv.png
[9]:  https://cs.mwsu.edu/~griffin/icons/icons8-markdown-24.png
[10]: http://cs.mwsu.edu/~griffin/Free-file-icons/24px/sql.png
[11]: http://cs.mwsu.edu/~griffin/Free-file-icons/24px/yml.png
[12]: http://cs.mwsu.edu/~griffin/Free-file-icons/24px/json.png
