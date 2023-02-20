
# Task Record System

CMSC 127: File Processing and Database Systems

This project demonstrates the use of a database, implemented in python

## Authors
 - [Damalerio, Mark Lewis](https://www.facebook.com/Markeryy/)
 - [Makiling, Michael Jay](https://www.facebook.com/profile.php?id=100077660842286)
 - [Sorinio, Nicole Angela](https://www.facebook.com/nicoleeayyy)

## Features

| Feature          | Description                                                             |
| ----------------- | ------------------------------------------------------------------ |
| Add Task | Add a task to the database |
| Edit a Task | Edit the task from the database |
| Delete a Task | Delete a task from the database |
| Delete All Tasks | Delete all tasks from the database |
| View Tasks (By Date) | View tasks by date |
| View Tasks (By Month) | View tasks by month |
| View All Tasks | View all tasks |
| Mark Task as Done | Mark task as done |
| Add Category | Add a category to the database |
| Edit Category | Edit a category from the database |
| Delete a Category | Delete a category from the database |
| Delete All Categories | Delete all categories from the database |
| View Categories | View all categories |
| Add Task to Category | Add a task to a category |


## Instructions
edit password argument for both 1st time connection and 2nd time connection

```python
#edit the password argument
#mariadb_connection = mariadb.connect(user="root", password="mypassword", host="localhost", port="3306")
#mariadb_connection = mariadb.connect(user="root", password="mypassword", host="localhost", database="final_project", port="3306")
```

uncomment the first time connection, the connection (cursor), and create database

```python
#uncomment the following lines:
mariadb_connection = mariadb.connect(user="root", password="mypassword", host="localhost", port="3306")
create_cursor = mariadb_connection.cursor()
create_cursor.execute("CREATE DATABASE IF NOT EXISTS final_project")
```

run and terminate the program

```bash
python CMSC127_FinalProject.py
```

comment out the 1st time connection

```python
#comment out the following line:
#mariadb_connection = mariadb.connect(user="root", password="mypassword", host="localhost", port="3306")
```

uncomment 2nd time connection and all create tables

```python
#uncomment the following lines:
mariadb_connection = mariadb.connect(user="root", password="mypassword", host="localhost", database="final_project", port="3306")
create_cursor.execute("CREATE TABLE IF NOT EXISTS category(categoryid INT(2) PRIMARY KEY AUTO_INCREMENT, categorytitle VARCHAR(30) NOT NULL, description VARCHAR(280));")
create_cursor.execute("CREATE TABLE IF NOT EXISTS task(taskid INT PRIMARY KEY AUTO_INCREMENT, tasktitle VARCHAR(30) NOT NULL, description VARCHAR(280), deadline DATE, isdone BOOLEAN DEFAULT 0, categoryid INT(2), FOREIGN KEY(categoryid) REFERENCES category(categoryid));")
```

run the program

```bash
python CMSC127_FinalProject.py
```