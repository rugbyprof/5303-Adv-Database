### Assignment 2 - Create your own server.
#### Due: 08-30-2021 (Monday @ 5:00 p.m.)



-----

#### DIGITAL OCEAN TUTORIALS:

<a href="https://www.digitalocean.com/community/tutorials"><img src="https://upload.wikimedia.org/wikipedia/commons/f/ff/DigitalOcean_logo.svg" width="100"></a>


#### 1. [Sign up](https://cloud.digitalocean.com/registrations/new) for Digital Ocean.

This will cost you around $5.00 + tax for the entire month. 

-----

#### 2. SSH Keys HowTo

- [Windows Tutorial](https://docs.digitalocean.com/products/droplets/how-to/add-ssh-keys/create-with-putty/)
- [Linux/Mac Tutorial](https://www.digitalocean.com/community/tutorials/how-to-create-ssh-keys-with-openssh-on-macos-or-linux)

-----

#### 3. Creating a new Droplet

[Droplet Tutorial](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-ubuntu-20-04-server-on-a-digitalocean-droplet).

- The IP address that is assigned to your "droplet", is your only connection to your server.
- The root password will be emailed to you.
- You need both IP address & password to access your new server.

-----

#### 4. Server Setup

[Initial Server Setup](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-20-04)

- Logging in as root
- Creating Users
- Privileges
- Firewall

-----

#### 5. SSHing Into Your Server

[SSH Tutorial](https://docs.digitalocean.com/products/droplets/how-to/connect-with-ssh/)
- This tutorial is about connecting to your server with console.

[SSH Keys Tutorial](https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-on-ubuntu-20-04)
- This tutorial is more about generating ssh keys to help secure logins.
-----

#### 6. Me Accessing Your Server

Add my public key to: `authorized_users` in the `/root/.ssh` folder.

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINnp5TGdQdQ+p4j6MAa2S2xWeoQCFmLd9H10S/UPBYed terry.griffin@msutexas.edu
```


#### 7. Package Management:

```bash
# update the package repositories
$ sudo apt-get update

# actually update any out of data packages
$ sudo apt-get upgrade

# install git a distributed version control system  
$ sudo apt-get install git

```

#### 8. Testing Your Server

- Go to http://your.ip.address/ and see if the apache or nginx default page shows up.


# STOP HERE

#### 7. Using Git

- Create a folder called `DataBase` in your `/var/www/html` directory.
- Change into that folder: `cd DataBase`
- Run the following: `git init`.
- If you get an error from the previous command, most likely `git` is not installed, so run:

```
sudo apt-get install git
```
- Then try `git init` again.

- If you successfully ran the previous command, then great! You should see a folder: `.git` in your `DataBase` folder now.
- Go [HERE](https://help.github.com/articles/generating-ssh-keys/) and follow this Github tutorial to generate ssh keys to allow you to "push" files from your server to Github.
- Now go [HERE](https://help.github.com/articles/adding-an-existing-project-to-github-using-the-command-line/) to add this `.git` repo to the one you created in your first assignment.

#### 8. Commit Your First File to Github

- Create a folder called `DataBase` in `/var/www/html/`
- Create a file called `README.md` in `/var/www/html/DataBase`
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
- <img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/icons8-folder-24.png" width="24"> /var/www/html
    - <img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/icons8-folder-24.png" width="24"> DataBase
         - <img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/icons8-markdown-24.png" width="24"> README.md 

-----


___Now commit your new "repo" to Github!___

```
git add .
git commit -m "My first commit"
git push origin master
```

If it doesn't work, then your ssh keys, or your upstream remote wasn't set correctly. 
Come get help from me, because from here on out, everything gets pushed to Github.


[1]:  ../../Resources/01-icons/icons8-folder-24.png
[2]: ../../Resources/01-icons/DigitalOcean_logo.png
[9]:  ../../Resources/01-icons/icons8-markdown-24.png


