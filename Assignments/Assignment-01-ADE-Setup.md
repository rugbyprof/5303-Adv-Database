## Assignment 1 - Setting up Develepment Environment
#### Due: Wednesday Aug 31st by classtime.

## ADE - Academic Development Environment

Typically a `development environment` is:
>A set of processes and programming tools used to create the program or software product. 

This usually consists of a local code editor, with the libraries / frameworks downloaded and installed for your particular type of coding. In addition a local server to run code on might be necessary. What is absolutely necessary is the initial code base that your going to be working with. This is usually kept in some type of repository managed with Git or Subversion (version control software).
Ultimately you will NOT work until your environment is set up! For us in class it's similar and no less important!  

### Intructors Note:
>As you read below (and no TL;DR excuses) it will seem like overkill for this level of programming. Some of the terminology and software components will be confusing, but only at first. After your initial setup (all of the components below are installed), there will be a repetative series of steps used to write, edit, and save (commit) your code. It will be so repetative that it will become second nature. I guarantee that you will learn to appreciate and probably start to prefer the power of the command line and gaining more control over your dev environment.
>
>This is an important step to getting your semester off on the right foot. **It's so important that:**
>- If you don't complete it, drop the course because you will fail.
>- If you complete it late, you will lose 1 letter grade off of your final grade.
>- If you complete it wrong, you will lose 1/2 of one letter grade off of your final grade.
>- Having said that, feel free to get help from me at anytime.
>- And no I will not penalize you if there are configuration problems or other issues that present themselves after each thing is installed. I only want you to get this done as soon as possible, so don't wait.
>


### Step 1: Team Chat
---

![](https://d17oy1vhnax1f7.cloudfront.net/items/1J3A0f36402p2r1K1u0L/slack-2014.hG65.png)

The first step in doing well in any of my courses is establishing a base of communication. Why? Not everything can be done while we are in class. 

Otherwise: 

1. I would lecture
2. give an assignment
3. you would complete said assignment
4. then you would go home
5. communication not necessary

That's so highschool. Assignments will (and should) be challenging. Therefore you will need help from me and your classmates. Since the labs are only open 9-5 with limited help, we need to alleviate that problem. So we will use a chat client built for developers called [Slack](https://slack.com)<sup>2</sup>. You should have gotten an invite already from me. Accept it. If you didn't, ask me for another invite. [Here](https://get.slack.help/hc/en-us/articles/218080037-Getting-started-for-new-users) is a getting started guide to help you use slack. 

#### Slack provides:

- Team chat (class members and myself).
- Code highlighting for snippets so we can share code and read it better.
- File sharing simply by dragging and dropping.
- Private channels so you can discuss things without everyone seeing (even I can't see).
- Polls so we can vote on things (mainly for me).

So, **NO email!** Unless I specifically ask. Slack is your communication conduit for this class.


Now that we have our communication client set up, we probably need to start getting the actual programming environment ready! We will be doing many things from the command line this semester. Windows is not know for it's 
command line prowess, so we need to give it some assistance.


### Step 2: Command Line Interface (Telnet Client)
---

#### Gitbash
![](https://d17oy1vhnax1f7.cloudfront.net/items/160M141x29360Y0f0T0l/gwindows_logo_72.hF1V.png)

From Gitbash's website:

>Git for Windows provides a BASH emulation used to run Git from the command line. *NIX users should feel right at home, as the BASH emulation behaves just like the "git" command in LINUX and UNIX environments.

This tells us two things: 

1. We're getting a command line (`bash`) emulator.
2. We will be using `Git`! ?? 

Don't worry about `Git` just yet. Simply install Git for windows. 

Download Gitbash from [here](https://git-for-windows.github.io/). This page also gives a little more information about what your installing. 

#### Putty
![](https://d3vv6lp55qjaqc.cloudfront.net/items/433k3t2F1R2Q0s1E3K0K/putty.png?X-CloudApp-Visitor-Id=1094421)

PuTTY is an SSH and telnet client, developed originally by Simon Tatham for the Windows platform. PuTTY is open source software that is available with source code and is developed and supported by a group of volunteers.

It doesn't provide a "linux" or "bash" type interface, it simply offers an interface to a server that allows remote logins.

#### Bitvise

![](https://d3vv6lp55qjaqc.cloudfront.net/items/2K2L232m1Q1n173B1I2X/Screen%20Shot%202016-08-29%20at%203.51.00%20PM.png?X-CloudApp-Visitor-Id=1094421)

Bitvise SSH Client is an SSH and SFTP client for Windows. It is developed and supported professionally by Bitvise. The SSH Client is robust, easy to install, easy to use, and supports all features supported by PuTTY, as well as the following:

- graphical SFTP file transfer;
- single-click Remote Desktop tunneling;
- auto-reconnecting capability;
- dynamic port forwarding through an integrated proxy;
- an FTP-to-SFTP protocol bridge.

Download [here](https://www.bitvise.com/ssh-client-download)

### Step 3: Digital Ocean

-----
![](https://d3vv6lp55qjaqc.cloudfront.net/items/2J0S130Y0Y0F3D393g07/Digital-Ocean-Logo1.png?X-CloudApp-Visitor-Id=1094421)

>Follow the steps below to create your own server. If these steps aren't clear enough, you can 
view an online tutorial [here](https://www.digitalocean.com/community/tutorials/how-to-create-your-first-digitalocean-droplet-virtual-server).

-----

#### A. [Sign up](https://cloud.digitalocean.com/registrations/new) for Digital Ocean.

This will cost you around $5.00 + tax for the entire month.

Use the code __`DROPLET10`__ for a $10 dollar credit for "new" users.

-----


#### B. [Create a new Droplet](https://cloud.digitalocean.com/droplets/new)

### Create Droplets
#### Choose an image:
- Click on the tab "One-click Apps" and choose:

![](https://s3.amazonaws.com/f.cl.ly/items/0Y0v0G3G031C0T2a2I1t/Screen%20Shot%202016-06-05%20at%209.19.17%20PM.png)

#### Choose a size

![](https://s3.amazonaws.com/f.cl.ly/items/3I3W2y1b0r2h2o3f1N2Z/Screen%20Shot%202016-06-05%20at%209.20.04%20PM.png)

#### Choose a datacenter region
> Default of New York is fine.

#### Select additional options
> Don't choose any (unless you want to)

#### Add your SSH keys
> Skip, we will address ssh keys later.

#### Finalize and create
- How many Droplets?
> Only need 1 droplet

- Choose a hostname
> Your hostname is the name of your server and it's what you see when you log in. This is not a domain name!

-----

#### C. IP Address & Password

- The IP address that is assigned to your "droplet", is your only connection to your server.
- The root password will be emailed to you.
- You need both IP address & password to access your new server.

#### D. Accessing Your Server

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
    - Set my password as `2D2016!!!`, I will change it as necessary.
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

#### E. Basic necessary packages:

```bash
# update the package repositories
$ sudo apt-get update

# actually update any out of data packages
$ sudo apt-get upgrade

# install git a distributed version control system  
$ sudo apt-get install git

```

#### F. Testing Your Server

- Go to http://your.ip.address/ and see if the apache default page shows up.




### Step 4: Revision Control
---

![](https://d17oy1vhnax1f7.cloudfront.net/items/1J3p2j221s2q2q1G100T/elmah.io.apps.github.hGP6.png)


In addition to our team chat, our code editor, and our new terminal environment we need a place where we can store / retreive our code base. A `code base` is a collection of source code that is used to build a particular software system. Where `software system` in the context of class is basically our programs. Github is where you will get all of your starter code (code base) for each of your assignments, and it's also where you will store all of your assignments when completed. 


#### What is Git?

>Git is a distributed revision control and source code management (SCM) system with an emphasis on speed,data integrity,and support for distributed, non-linear workflows. Git was initially designed and developed by Linus Torvalds for Linux kernel development in 2005, and has since become the most widely adopted version control system for software development.<br><br>
As with most other distributed revision control systems, and unlike most client–server systems, every Git working directory is a full-fledged repository with complete history and full version-tracking capabilities, independent of network access or a central server. Like the Linux kernel, Git is free software distributed under the terms of the GNU General Public License  [[1]](http://en.wikipedia.org/wiki/Git_(software)).

`Git != Github`

`Github` is a social site that allows programmers to share code with other programmers. It's also a great place to discover projects to work on, discover code to use in your own projects, and a great place to start a portfolio. Whereas `Git` is simply the revision control system that can be installed anywhere, and only used locally if that's the users choice. 

#### Why github for this course?

We will be using github this semester as a means of communicating, storing documents (assignments and programs), as well as 
a means to push your files to a central repository. So if your using a lab or personal machine, there's a centralized location that we both have access to.

---

#### Create a Github account. 
- When you create a Github account, you must choose a `username`. 
- This is very important to remember, because you will update the class roster with this username so I know where to find all your assignments.
- Create a repository named:
    - `5303-AdvDB-yourlastname`
    - replace the `yourlastname` with your last name to make it unique.
- Check the box that says: "Add a README.md file"

#### Edit the README.md 

- Edit the readme file on github and place your contact information inside along with a picture of YOU. NOT an avatar. NOT a thumbnail. But an easily identifiable picture of you.
- Your readme should include:
    - Your image
    - Your first and last name
    - Your email address
    - Your website (if you have one)

#### Make me a contributer:

- Go to your repo settings and add `rugbyprof` as a collaborater.

- You can do this in the settings of your repository. 
- This is vital as I need access to your files with edit permissions.

### Step 5: Class Roster
---

![](https://d3vv6lp55qjaqc.cloudfront.net/items/2Y3p3e0B3t362M1Z020X/Apps-Google-Drive-Sheets-icon.png?X-CloudApp-Visitor-Id=1094421)
#### Update the Class Roster:

- Here is a link to our class roster on google docs: https://docs.google.com/spreadsheets/d/1Ryb4wiL9mQjTCPeLLASosfHuUi3YnZ6AlEXQChcUCQw/edit?usp=sharing

- Update the roster by adding your information to it. 

Add:

1. Your name (last, first)
2. Your email
3. Your github username<sup>*</sup>
4. A link to your 5303-AdvDB repository<sup>*</sup>
5. Ip address of your server

*Your repository name and your github username are NOT the same thing.

---

#### Rules for emailing me:

Every email must have a minimum of two items included:

- The course number and title in the subject:
    - `5303-AdvDBs`
- Your name

I can't promise an answer if you don't provide those two pieces of information.


Sources:
- <sub>[1] http://en.wikipedia.org/wiki/Git_(software)</sub>
- <sub>[2] https://slack.com</sub>
- <sub>[3] http://www.openbookproject.net/courses/webappdev/units/softwaredesign/resources/install_python_win7.html </sub>
- <sub>[4] https://code.visualstudio.com/</sub>
- <sub>[5] https://git-for-windows.github.io/</sub>
- <sub>[6] https://www.python.org/</sub>

[1]:  http://cs.mwsu.edu/~griffin/Free-file-icons/24px/folder2.png
[2]:  http://cs.mwsu.edu/~griffin/Free-file-icons/24px/php.png
[3]:  http://cs.mwsu.edu/~griffin/Free-file-icons/24px/html.png
[4]:  http://cs.mwsu.edu/~griffin/Free-file-icons/24px/css.png
[5]:  http://cs.mwsu.edu/~griffin/Free-file-icons/24px/js.png
[6]:  http://cs.mwsu.edu/~griffin/Free-file-icons/24px/json.png
[7]:  http://cs.mwsu.edu/~griffin/Free-file-icons/24px/xml.png
[8]:  http://cs.mwsu.edu/~griffin/Free-file-icons/24px/csv.png
[9]:  http://cs.mwsu.edu/~griffin/Free-file-icons/24px/md2.png
[10]: http://cs.mwsu.edu/~griffin/Free-file-icons/24px/sql.png
[11]: http://cs.mwsu.edu/~griffin/Free-file-icons/24px/yml.png
[12]: http://cs.mwsu.edu/~griffin/Free-file-icons/24px/json.png
