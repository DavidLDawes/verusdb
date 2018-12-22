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

## Python
The utility runs in python and wraps the SQL code in pyodbc wrapping ODBC for mySQL.

### Requirements: python 2.7
This was written for python 2.7. Should mostly workj with 3.x, except maybe the prints? Possibly the execs?

### Requirements: ODBC
You will need to get mySQL's ODBC client installed and working.

### Requirements: pyodbc
You will need to get the pyodbc Python ODBC package installed using pip.

### Requirements: Create Tables
You can use the createTables() method to get the block and tx tables in the verus database created properly. Once created you can comment the createTables() call out.
