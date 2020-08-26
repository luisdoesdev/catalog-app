# Catalog APP

This app was part of my fullstack program at Udacity.co
The goal of the app is to handle CRUD and User oauth with google
User will be able to perform CRUD commands if they sign up with their google accounts but with the limitiations of the inputs they add to the database, for example if User A creates item X user B will not be able to manipulate that input.

In the latest version I am updating the app with modern stack and practices. To see the changes look at the [changelog]('changelog.md') or the `git log --oneline`. A blog and video series explaining how it was made from scratch is on the work. Stay tuned.

# Getting Started


## pre-requisites
 Install latest version fof [Vagrant](https://www.vagrantup.com/) and  [Virtual Box](https://www.virtualbox.org/)   

## Installing
 
 Just clone this repo: `git clone https://github.com/letorruella/catalog-app`

### Setup Server

 Start vagrant `vagrant up`
 
 Shh into it `vagrant ssh`

 If you want to nuke the box `vagrant destroy`

 ### Setup App
 
 Once that's done install the dependencies: `pip install -r requirements.txt `
 
 Setup the database `python project/models.py` 
 
 Add some data `python project/modelstemplate.py`    
 
 ### Run
 run the app `python run.py`, it should look like this:
 
 

# Tech Stack(all organized in requirements.txt)
Checkout the [Vagrantfile](Vagrantfile) and the [requirements.txt](requirements.txt) for more info

   
    cachetools
    certifi
    chardet
    click
    FLask
    Flask-HTTPAuth
    Flask-SQLAlchemy
    google-auth
    html5lib
    httplib2
    dna
    itsdangerous
    Jinja2
    MarkupSafe
    oauth2client
    packaging
    passlib
    psycopg2
    pyasn1
    pyasn1-modules
    pyparsing
    requests
    rsa
    six
    SQLAlchemy
    urllib3
    webencodings
    Werkzeug



# Overview 

The app is organize in very easy to nagivate folders, I looked at how other professionals organize their flask folders structures and applied to my own

* Root folder '/'   
    * .gitgnore you all know what this is 
    * run.py this is basic script that allows you to start the app just type 'python run.py' in the terminal and voila
    * This README.md file that is basically explaining what is happening
    * requirements.txt that has all the libraries that are used to composed the entire aplication
    * the Vagrantfile, this project was built using Vagrant as virtual enviroments to sepparte the libraries from my local pc see https://www.vagrantup.com/ for more information on it, the configuration for this enviroment was provided by Udacity

* project folder '/'
    * static holds the css folders where all the styles are located, nothing special here, oh and a cheesy logo I made for favicon placeholder
    * Holds all the 
    *  -___init__-.py' to make sure all folders are treated as packages
    * models.py creates the database and its relationships
    * modelstemplate.py has a couple dummy descriptions to populate the database
    * routes.py has, weell, all the apps routes and functionalities

## Functionalities

The user has the ability to browse thru the app without logging in, in order to access CRUD operations, he/she will have to login using a google account

## TODO
 * ~~[*]    Upgrade to  Python3~~
 * ~~[*]    Update Bento~~
 * ~~[*]    Sudo issue on Machine~~
 * [ ]  Update Design
 * [ ]  Fix Sign Issues
 * [ ]  Add a Cart
 * [ ]  Add a Blog
 * [ ]  Automate the creation of the DB
 * [ ]  Add PGAdmin
 * [ ]  Add Search Feature
 * ~~[*] Add React~~
 * [ ]  Add Recomendation System
 * [ ] Add User Managment
 * [ ] [Config React's WebPack for Vagrant reload](https://dev.to/nodewarrior/override-cra-and-add-webpack-config-without-ejecting-2f3n )
 

---
## Design

[LINK]: https://www.figma.com/file/l79JiT9r4T49zr1hKIq0BC/Catalog-App?node-id=0%3A1
![design](screenshot.png)

