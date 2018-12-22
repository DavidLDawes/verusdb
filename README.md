# verusdb
Fiddling with Verus chain details in a mySQL DB.

## mySQL
I found it simplest to get mySQL 5.7 from hub.docker.com, specifically https://hub.docker.com/_/mysql which also has useful advice about running the container. 

### Docker run parameters
You'll need at least the following settings to run properly:
**mySQL 5.7**
```
-d mysql:5.7
```

**Set the root password**
```
-e MYSQL_ROOT_PASSWORD=my-secret-pw
```

**Map conainer DB files**
Create the direcory ```mkdir ~/mysql.data```
Then use the directory in the docker volume setting:
```
-v ~/mysql.data:/var/lib/mysql
```

**Map the TCP port**
```
-p 3306:3306
```
So you end up with something like:
```
docker run --name mysql -v ~/sql.data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:5.7 -p 3306:3306
```

### Setup Databases
If all that works, bring up mySQL in the container so we can create the database and user and give access.

First get into the mySQL client. Enter the password you created in the docker run step above in response to the password prompt.
```
docker exec -it mysql /bin/bash
mysql -u root -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 48
Server version: 5.7.24 MySQL Community Server (GPL)

Copyright (c) 2000, 2018, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

We need to create the verus database, then create a user and password pair and allow that user to access the database. The following commands are from inside of the mysql client, as indicated by the mysql> prompt.
#### Create Database & Grant Privileges
```
mysql>  CREATE DATABASE `verus1` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
Query OK, 1 row affected (0.00 sec)
GRANT ALL PRIVILEGES ON verus.* TO 'vrscusr'@'localhost' IDENTIFIED BY 'vrscusrpassword';

```

#### Note On Privileges
The above gant privileges is generous for the verus DB as long as vrscusr is on localhost. For the more general case (i.e. this continer provides DB resources via ODBC to a python script, as in our case) then you will need to open things up a bit more. **This is too open, so I'd recommend not using this:**
```
GRANT ALL PRIVILEGES ON verus.* TO 'vrscusr'@'*' IDENTIFIED BY 'vrscusrpassword';
```

Rather use the original example and when the python attempt to access fails, check the IP address in the error. Use that in the GRANT and all is well. For example, of the error said something about vrscusr@172.10.1.14 being unable to connect, use that IP address in the GRANT:
The above gant privileges is generous for the verus DB as long as vrscusr is on localhost. For the mnore general case (i.e. this continer provides DB resources via ODBC to a python script, as in our case) then you will need to open things up a bit more. **This is too open, so I'd recommend not using this:**
```
GRANT ALL PRIVILEGES ON verus.* TO 'vrscusr'@'172.10.1.14' IDENTIFIED BY 'vrscusrpassword';
```

## Python App
The utility runs in python and wraps the SQL code in pyodbc wrapping ODBC for mySQL. It executes assorted verus commands which are passed to the komodod daemon, with the responses process by the Python code and persisted in the database as block and tx records.

### Requirements: python 2.7
This was written for python 2.7. Should mostly workj with 3.x, except maybe the prints? Possibly the execs?

### Requirements: ODBC
You will need to get mySQL's ODBC client installed and working.

### Requirements: pyodbc
You will need to get the pyodbc Python ODBC package installed using pip.

### Requirements: Create Tables
You can use the createTables() method to get the block and tx tables in the verus database created properly. Once created you can comment the createTables() call out.

### Requirements: verusd/komodod Running
The Verus enhanced komodod daemon must be running and it must have caught up with processing the current chain so that it responds to komodo-cli commands (which are wrapped in the verus bash shell script) properly.

### Requirements: verusd/komodod Location
The exec command uses an explicit path to the verus shell command. You are likely to need to edit that so that it points to where you've installed the verus and komodod files.

This should all work under Windows with a bit of fiddling; I have not tried. Directories change and exec details might as well.
# Gather Data
When you run the python scipt
```
python read-chain.py
```
It will attempt to get the total number of blocks from komodod via a verus command line. If it gets a successful result it shows the block height returned (we are currently above 300,000) and goes into silent loop getting blocks one at a time, writing the blocks and their transaction details to the block and tx tables respectively.

This is a slow process, so leave it running over night and it should be done the next morning (at least as of Winter 2018, anyway).

# Missing Features
Sure needs work

## Incremental Input
Need to check the highest height in the DB and only update new data by default.

## Quality Control
Not terribly robust, it most likely has bugs. It still has POST oriented code that is useless without the Spring boot stuff it was built for and so on. Could use cleaning and commenting.

## Wallet Details
Adding wallet details, we can have the tool include the details of where your transactions tie in and how much changed hands in those transactions.

## Naive User Management
User account and password for the SQL client is checked in. Needs to be manually replaced for each use.

# The Usual Heads Up
This software is not warrantied or even well tested, so use it at your own risk. This software is not supported in any manner other than the whim of it's creator. Feel free to use it for anything you want, but don't blame me if it has problems. I warned you!
