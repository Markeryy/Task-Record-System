from re import A
import mysql.connector as mariadb
from datetime import datetime
import os

# MEMBERS:
# Damalerio, Mark Lewis
# Makiling, Michael Jay
# Sorinio, Nicole Angela

# DATABASE NAME: final_project

# TASK CHECKER:
# Add/Create Task - Kael (Done), updated
# Edit Task - Kael (Done)
# Delete Task - Nicole (Done)
# View Task:
#       By Date - Kael(Done)
#       By Month - Nicole (Done)
#       View All - Nicole (Done)
# Mark Task as Done - Nicole (Done)
# Add Category - Kael (Done), updated
# Edit Category - Mark (Done)
# Delete Category - Mark (Done)
# View Category - Mark (Done)
# Add Task to Category - Mark (Done)


# --------------ACCESSING--------------------

#           1st TIME CONNECTION
#mariadb_connection = mariadb.connect(user="root", password="____", host="localhost", port="3306")

#           2ND TIME CONNECTION 
#mariadb_connection = mariadb.connect(user="root", password="____", host="localhost", database="final_project", port="3306")

#               CONNECTION
#create_cursor = mariadb_connection.cursor()

# -------------CREATING DATABASE--------------------
#create_cursor.execute("CREATE DATABASE IF NOT EXISTS final_project")

# -------------CREATING TABLES--------------------
#create_cursor.execute("CREATE TABLE IF NOT EXISTS category(categoryid INT(2) PRIMARY KEY AUTO_INCREMENT, categorytitle VARCHAR(30) NOT NULL, description VARCHAR(280));")
#create_cursor.execute("CREATE TABLE IF NOT EXISTS task(taskid INT PRIMARY KEY AUTO_INCREMENT, tasktitle VARCHAR(30) NOT NULL, description VARCHAR(280), deadline DATE, isdone BOOLEAN DEFAULT 0, categoryid INT(2), FOREIGN KEY(categoryid) REFERENCES category(categoryid));")

# -------------DELETING--------------------
#create_cursor.execute("DROP DATABASE final_project")
#create_cursor.execute("DROP TABLE task")



# Purpose: Checks if a table is empty
# Returns: True/False

# Purpose: Clears the console window


def clear():
    # Clear console for Windows; for Linux replace 'cls' with 'clear'
    os.system('cls')

# Purpose: Pauses the execution of the next line of code until the user presses ENTER


def pause():
    input('\nPress ENTER to continue...')

# Purpose: Check if table is empty


def isEmpty(table):
    create_cursor.execute("SELECT * FROM " + table)
    checker = create_cursor.fetchall()
    if not checker:
        return False
    return True

# Purpose: Creates/Adds Task in table task. (Automated ID)


def add_createTaskAlt():
    clear()
    print("---Adding/Creating Task---")
    tasktitle = input("Task Title: ")
    while tasktitle == "":
        print("Task title cannot be empty.")
        tasktitle = input("Task Title: ")
    description = input("Description: ")

    # Checks if date format is acceptable---
    while 1:
        deadline = input("Deadline (mm/dd/yy): ")
        deadlineIsValid = True
        try:
            final_deadline = datetime.strptime(deadline, "%m/%d/%y").date()
            today = datetime.today()

            # check if deadline date is already done
            if (today.date() > final_deadline):
                print("\nDeadline is already done!")
                continue

        except ValueError:
            deadlineIsValid = False

        if(deadlineIsValid):
            break
        else:
            print("\nDeadline Invalid Format/Input!\n")

    # Inserting task to table -------------
    query = "INSERT INTO task (tasktitle, description, deadline) VALUES (%s, %s, %s)"
    create_cursor.execute(
        query, (tasktitle, description, final_deadline))
    mariadb_connection.commit()
    print("---Successfully Added Task---")
    pause()

# Purpose: Edit task's id, category id, title, description and deadline.
# Limitations:
#       - Can edit if table is not empty.
#       - Category can be editted if category table is not empty.


def editTask():
    clear()
    notEmpty = isEmpty("task")
    if (notEmpty):
        isFound = False

        # Printing of possible task to edit ----------
        create_cursor.execute("SELECT taskid,tasktitle FROM task")
        task_tupleList = create_cursor.fetchall()
        task_array = [item for item in task_tupleList]

        print("--- List of Task ---")
        for j in range(len(task_array)):
            print("\t>> " + "Task ID: " +
                  str(task_array[j][0]) + " - Task Title: " + task_array[j][1])

        taskid = input("Task Id (dd): ")

        # Check if Task Id Exist ---------------------
        for i in range(len(task_array)):
            if taskid == str(task_array[i][0]):
                isFound = True
                break

        # If found, continue to take user input -------
        if (isFound):
            tasktitle = input("New Task Title: ")
            description = input("New Description: ")

            # Checks if date format is acceptable---
            while 1:
                deadline = input("New Deadline (mm/dd/yy): ")
                deadlineIsValid = True
                try:
                    final_deadline = datetime.strptime(
                        deadline, "%m/%d/%y").date()
                except ValueError:
                    deadlineIsValid = False
                if(deadlineIsValid):
                    break
                else:
                    print("\nDeadline Invalide Format/Input!\n")

            # Updating Chosen Task -------------
            query = "UPDATE task SET tasktitle = %s, description = %s, deadline = %s WHERE taskid = %s"
            create_cursor.execute(
                query, (tasktitle, description, final_deadline, taskid))
            mariadb_connection.commit()

            # If category table is not empty, the user can edit the category id
            notEmpty = isEmpty("category")
            if (notEmpty):
                while 1:
                    choice = input(
                        "\nWould you like to change its Category?\n\t[1] Yes\n\t[2] NO\n\tChoice: ")
                    if choice == "1":

                        # Printing of possible categoryid to choose ----------
                        create_cursor.execute(
                            "SELECT categoryid,categorytitle FROM category")
                        category_tupleList = create_cursor.fetchall()
                        category_array = [item for item in category_tupleList]

                        for j in range(len(category_array)):
                            print("\t>> " + "Category ID: " +
                                  str(category_array[j][0]) + " - Category Title: " + category_array[j][1])

                        categoryid = input("Enter Categoryid: ")

                        isFound = False

                        # Check if Category Id Exist ---------------------
                        for i in range(len(category_array)):
                            if categoryid == str(category_array[i][0]):
                                isFound = True
                                break

                        # If found, update the task's category id ---------
                        if (isFound):
                            query = "UPDATE task SET categoryid = %s WHERE taskid = %s"
                            create_cursor.execute(query, (categoryid, taskid))
                            mariadb_connection.commit()
                            break
                        else:
                            print("Categoryid not found!")

                    elif choice == "2":
                        break
                    else:
                        print("Invalid Input!")

            print("---Successfully Updated Task---")
            pause()
        else:
            print("Task not Found!")
    else:
        print("---No Task Available---")
        pause()

# Purpose: Delete task

def deleteTask():
    clear()
    notEmpty = isEmpty("task")
    if (notEmpty):
        choice = input(
            "---Deleting Task---\n\t[1] Delete One\n\t[2] Delete All\n\tChoice: ")
        if choice == "1":
            deleteOneTask()
        elif choice == "2":
            deleteAllTask()
        else:
            print("Invalid Input!")
            pause()
    else:
        print("---No Task Available---")
        pause()

def deleteOneTask():
    clear()
    notEmpty = isEmpty("task")
    if (notEmpty):
        viewall()

        # Printing of possible taskid to choose ----------
        create_cursor.execute(
            "SELECT taskid FROM task")
        task_tupleList = create_cursor.fetchall()
        task_array = [item for item in task_tupleList]

        taskId = input("Task Id (dd): ")

        isFound = False

        # Check if Task Id Exist ---------------------
        for i in range(len(task_array)):
            if taskId == str(task_array[i][0]):
                isFound = True
                break

        # If found, delete the task through its task id ---------
        if (isFound):
            query = "DELETE FROM task WHERE taskid = " + taskId
            create_cursor.execute(query)
            mariadb_connection.commit()
            print("---Successfully Deleted Task---")
        else:
            print("Task ID not found!")

        pause()
    else:
        print("---No Task Available---")
        pause()

def deleteAllTask():
    clear()
    notEmpty = isEmpty("task")
    if (notEmpty):
        query = "DELETE FROM task"
        create_cursor.execute(query)
        mariadb_connection.commit()
        print("Successfully deleted all tasks.\n")
    else:
        print("---No Task Available---")
    
    pause()


# --------------------VIEWING---------------------------

# Purpose: Remove duplicates in a list


def removeDups(x):
    return list(dict.fromkeys(x))


def viewbydate():
    clear()
    print("---Viewing Tasks by Date---")
    notEmpty = isEmpty("task")
    if (notEmpty):
        monthsInYear = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE",
                        "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]

        create_cursor.execute(
            "SELECT * FROM task")
        task_tupleList = create_cursor.fetchall()
        task_array = [item for item in task_tupleList]

        # Get only available months in the task
        availableMonths = []

        for i in range(len(task_array)):
            availableMonths.append(int(task_array[i][3].strftime("%m"))-1)

        availableMonths = removeDups(availableMonths)
        availableMonths.sort()

        # check if there is a task for every month of the year
        for a in range(len(availableMonths)):
            print("\n***** " + monthsInYear[availableMonths[a]] + " *****")

            dayList = []
            tasks = []

            for b in range(len(task_array)):
                # convert the string month into an int to compare it to the index of the month being checked (-1)
                month = int(task_array[b][3].strftime("%m"))-1

                # Get only available days and tasks in the month
                for i in range(len(task_array)):
                    if (month == availableMonths[a]):
                        dayList.append(task_array[b][3].strftime("%d"))
                        tasks.append(task_array[b])

                dayList = removeDups(dayList)
                tasks = removeDups(tasks)
                dayList.sort()

            for i in range(len(dayList)):
                print(
                    "\n\t--- DEADLINE: " + monthsInYear[availableMonths[a]] + " " + dayList[i] + " ---")

                for j in range(len(tasks)):
                    # if the day of the task being checked and the index a of the dayList are the same, print the task
                    if (tasks[j][3].strftime("%d") == dayList[i]):
                        # Converting the int value of isdone from task into "Done" or "Not Done"
                        status = "Not Done"
                        if (task_array[j][4]):
                            status = "Done"

                        # Getting the category name of the tasks
                        if (task_array[j][5] != None):
                            categoryId = str(task_array[j][5])
                            create_cursor.execute(
                                "SELECT categorytitle FROM category WHERE categoryid = " + categoryId)
                            # first element of tuple
                            categoryName = create_cursor.fetchone()[0]
                        else:
                            categoryName = "None"

                        print("\t>> " + "Task ID: " + str(task_array[j][0]) +
                              "\n\t\t Task Title: " + str(task_array[j][1]) +
                              "\n\t\t Description: " + str(task_array[j][2]) +
                              "\n\t\t Status: " + str(status) +
                              "\n\t\t Category: " + str(categoryName))
    pause()

# Purpose: View tasks by month


def viewbymonth():
    clear()
    print("---Viewing Tasks by Month---")
    notEmpty = isEmpty("task")
    if (notEmpty):
        monthsInYear = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE",
                        "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]

        create_cursor.execute(
            "SELECT * FROM task")
        task_tupleList = create_cursor.fetchall()
        task_array = [item for item in task_tupleList]

        # Get only available months in the task
        availableMonths = []

        for i in range(len(task_array)):
            availableMonths.append(int(task_array[i][3].strftime("%m"))-1)

        availableMonths = removeDups(availableMonths)
        availableMonths.sort()

        # check if there is a task for every month of the year
        for a in range(len(availableMonths)):
            print("\n***** " + monthsInYear[availableMonths[a]] + " *****")

            # check if there are tasks belonging to a month in index a of the monthsInYear
            for b in range(len(task_array)):
                # convert the string month into an int to compare it to the index of the month being checked (-1)
                month = int(task_array[b][3].strftime("%m"))-1

                # if the month of the task being checked and the index a of the availableMonths are the same, print the task
                if (month == availableMonths[a]):
                    # Converting datetime to string
                    deadline = task_array[b][3].strftime("%b %d, %Y -> %a")

                    # Converting the int value of isdone from task into "Done" or "Not Done"
                    status = "Not Done"
                    if (task_array[b][4]):
                        status = "Done"

                    # Getting the category name of the tasks
                    if (task_array[b][5] != None):
                        categoryId = str(task_array[b][5])
                        create_cursor.execute(
                            "SELECT categorytitle FROM category WHERE categoryid = " + categoryId)
                        # first element of tuple
                        categoryName = create_cursor.fetchone()[0]
                    else:
                        categoryName = "None"

                    print("\t>> " + "Task ID: " + str(task_array[b][0]) +
                          "\n\t\t Task Title: " + str(task_array[b][1]) +
                          "\n\t\t Description: " + str(task_array[b][2]) +
                          "\n\t\t Deadline: " + str(deadline) +
                          "\n\t\t Status: " + str(status) +
                          "\n\t\t Category: " + str(categoryName))
    pause()

# Purpose: View all tasks


def viewall():
    clear()
    print("---Viewing All Task---")

    notEmpty = isEmpty("task")
    if (notEmpty):

        create_cursor.execute(
            "SELECT * FROM task")
        task_tupleList = create_cursor.fetchall()
        task_array = [item for item in task_tupleList]

        for j in range(len(task_array)):
            # Converting datetime to string
            deadline = task_array[j][3].strftime("%b %d, %Y -> %a")

            # Converting the int value of isdone from task into "Done" or "Not Done"
            status = "Not Done"
            if (task_array[j][4]):
                status = "Done"

            # Getting the category name of the tasks
            if (task_array[j][5] != None):
                categoryId = str(task_array[j][5])
                create_cursor.execute(
                    "SELECT categorytitle FROM category WHERE categoryid = " + categoryId)
                # first element of tuple
                categoryName = create_cursor.fetchone()[0]
            else:
                categoryName = "None"

            print("\t>> " + "Task ID: " + str(task_array[j][0]) +
                  "\n\t\t Task Title: " + str(task_array[j][1]) +
                  "\n\t\t Description: " + str(task_array[j][2]) +
                  "\n\t\t Deadline: " + str(deadline) +
                  "\n\t\t Status: " + str(status) +
                  "\n\t\t Category: " + str(categoryName))

    pause()

# Purpose: Provide options on viewing tasks


def viewAllTask():
    clear()
    notEmpty = isEmpty("task")
    if (notEmpty):
        choice = input(
            "---Viewing Task---\n\t[1] By Date\n\t[2] By Month\n\t[3] View All\n\tChoice: ")
        if choice == "1":
            viewbydate()
        elif choice == "2":
            viewbymonth()
        elif choice == "3":
            viewall()
        else:
            print("Invalid Input!")
            pause()
    else:
        print("---No Task Available---")
        pause()

# Purpose: Mark task as done


def markTask():
    clear()
    notEmpty = isEmpty("task")
    if (notEmpty):

        viewall()

        # Printing of possible taskid to choose ----------
        create_cursor.execute(
            "SELECT taskid FROM task WHERE isdone = false")
        task_tupleList = create_cursor.fetchall()
        task_array = [item for item in task_tupleList]

        taskId = input("Task Id (dd): ")

        isFound = False

        # Check if Task Id Exist ---------------------
        for i in range(len(task_array)):
            if taskId == str(task_array[i][0]):
                isFound = True
                break

        # If found, update the task through its task id ---------
        if (isFound):
            query = "UPDATE task SET isdone = true WHERE taskid = " + \
                str(taskId)
            create_cursor.execute(query)
            mariadb_connection.commit()
            print("---Successfully Marked Task as Done---")
        else:
            print("Task ID not found or task is already done!")

        pause()
    else:
        print("---No Task Available---")
        pause()

# Purpose: Creates/Adds Category in category table.


def addCategoryAlt():
    clear()
    categorytitle = input("Category Title: ")
    while categorytitle == "":
        print("Category title cannot be empty.")
        categorytitle = input("Category Title: ")
    description = input("Category Description: ")

    query = "INSERT INTO category (categorytitle, description) VALUES (%s, %s)"
    create_cursor.execute(query, (categorytitle, description))
    mariadb_connection.commit()
    print("---Successfully Added Category---")
    pause()


def addCategory():
    clear()
    alreadyTaken = False
    categoryid = input("Category Id (dd): ")

    # Checks if task id is already taken---
    create_cursor.execute("SELECT categoryid FROM category")
    categoryid_tupleList = create_cursor.fetchall()
    categoryid_array = [str(item[0]) for item in categoryid_tupleList]

    for i in range(len(categoryid_array)):
        if categoryid == categoryid_array[i]:
            alreadyTaken = True
            break

    # If not taken, continue to take user inputs
    if (not alreadyTaken):
        categorytitle = input("Category Title: ")
        description = input("Category Description: ")

        query = "INSERT INTO category VALUES (%s, %s, %s)"
        create_cursor.execute(
            query, (categoryid, categorytitle, description))
        mariadb_connection.commit()
        print("---Successfully Added Category---")
        pause()
    else:
        print("Category Id already taken. It must be unique.")
        pause()

# Purpose: Edit a category, changes will be reflected in tasks having the selected categoryid as their foreign key


def editCategory():
    clear()
    notEmpty = isEmpty("category")
    if (notEmpty):
        # Printing of categories to choose from
        create_cursor.execute("SELECT categoryid,categorytitle FROM category")
        category_tupleList = create_cursor.fetchall()
        category_array = [item for item in category_tupleList]
        print("--- List of Categories ---")
        for j in range(len(category_array)):
            print("\t>> " + "Category ID: " +
                  str(category_array[j][0]) + " - Category Title: " + category_array[j][1])

        # Find if category exists
        categoryId = input("Category Id (dd): ")
        categoryFound = False
        for i in range(len(category_array)):
            if categoryId == str(category_array[i][0]):
                categoryFound = True
                break

        # If there is a category, update category
        # Task with this category will automatically be updated since it has its foreign key
        if categoryFound:
            categoryTitle = input("New Category Title: ")
            description = input("New Category Description: ")
            query = "UPDATE category SET categorytitle=%s, description=%s WHERE categoryid=%s"
            create_cursor.execute(
                query, (categoryTitle, description, categoryId))
            mariadb_connection.commit()
            print("---Successfully Updated Category---")
        else:
            print("Category ID not found!")
    else:
        print("---No Category Available---")
    pause()

# Purpose: Delete a category, also clears the category of tasks having the selected categoryid


def deleteCategory():
    clear()
    notEmpty = isEmpty("category")
    if (notEmpty):
        choice = input(
            "---Deleting Category---\n\t[1] Delete One\n\t[2] Delete All\n\tChoice: ")
        if choice == "1":
            deleteOneCategory()
        elif choice == "2":
            deleteAllCategory()
        else:
            print("Invalid Input!")
            pause()
    else:
        print("---No Category Available---")
        pause()


def deleteOneCategory():
    clear()

    # Printing of categories to choose from
    create_cursor.execute("SELECT categoryid,categorytitle FROM category")
    category_tupleList = create_cursor.fetchall()
    category_array = [item for item in category_tupleList]
    print("--- List of Categories ---")
    for j in range(len(category_array)):
        print("\t>> " + "Category ID: " +
                str(category_array[j][0]) + " - Category Title: " + category_array[j][1])

    # Find if category exists
    categoryId = input("Category Id (dd): ")
    categoryFound = False
    for i in range(len(category_array)):
        if categoryId == str(category_array[i][0]):
            categoryFound = True
            break

    # If there is a category, update the affected tasks and delete the category
    if categoryFound:
        updateTasksQuery = "UPDATE task SET categoryid=NULL WHERE categoryid=%s"
        create_cursor.execute(updateTasksQuery, (categoryId,))
        mariadb_connection.commit()

        deleteQuery = "DELETE FROM category WHERE categoryid=%s"
        create_cursor.execute(deleteQuery, (categoryId,))
        mariadb_connection.commit()
        print("---Successfully Deleted Category---")
    else:
        print("Category ID not found!")

    pause()


def deleteAllCategory():
    clear()

    # Check if there are tasks, all their categoryid will be NULL
    notEmpty = isEmpty("task")
    if (notEmpty):
        updateTasksQuery = "UPDATE task SET categoryid=NULL"
        create_cursor.execute(updateTasksQuery)
        mariadb_connection.commit()
    
    # Delete all categories
    deleteQuery = "DELETE FROM category"
    create_cursor.execute(deleteQuery)
    mariadb_connection.commit()
    print("---Successfully Deleted All Categories---")
    pause()

# Purpose: View a category


def viewCategory():
    clear()
    notEmpty = isEmpty("category")
    if (notEmpty):
        print("---Viewing All Categories---")

        create_cursor.execute("SELECT * FROM category")
        category_tupleList = create_cursor.fetchall()
        category_array = [item for item in category_tupleList]

        for i in range(len(category_array)):
            print("\t>> " + "Category ID: " + str(category_array[i][0]) +
                  "\n\t\t Category Title: " + category_array[i][1] +
                  "\n\t\t Description: " + category_array[i][2])

        pause()
    else:
        print("---No Category Available---")
        pause()

# Purpose: Add task to a category


def addTaskToCategory():
    clear()
    taskNotEmpty = isEmpty("task")
    categoryNotEmpty = isEmpty("category")

    # Check if task and category is not empty
    if not taskNotEmpty:
        print("There are no tasks yet.")
        pause()
        return
    if not categoryNotEmpty:
        print("There are no categories yet.")
        pause()
        return

    # Printing of possible task to update
    create_cursor.execute("SELECT taskid,tasktitle FROM task")
    task_tupleList = create_cursor.fetchall()
    task_array = [item for item in task_tupleList]
    print("--- List of Tasks ---")
    for j in range(len(task_array)):
        print("\t>> " + "Task ID: " +
              str(task_array[j][0]) + " - Task Title: " + task_array[j][1])

    print("Enter task id to insert to a category")
    taskId = input("Task Id (dd): ")

    # Check if taskid exists
    create_cursor.execute(
        "SELECT taskid FROM task")
    task_tupleList = create_cursor.fetchall()
    task_array = [item for item in task_tupleList]
    taskIsFound = False
    for i in range(len(task_array)):
        if taskId == str(task_array[i][0]):
            taskIsFound = True
            break

    # If found, check if category id exists
    if (taskIsFound):

        # Printing of categories to choose from
        create_cursor.execute("SELECT categoryid,categorytitle FROM category")
        category_tupleList = create_cursor.fetchall()
        category_array = [item for item in category_tupleList]
        print("--- List of Categories ---")
        for j in range(len(category_array)):
            print("\t>> " + "Category ID: " +
                  str(category_array[j][0]) + " - Category Title: " + category_array[j][1])

        # Find if category exists
        categoryId = input("Category Id (dd): ")
        categoryFound = False
        for i in range(len(category_array)):
            if categoryId == str(category_array[i][0]):
                categoryFound = True
                break

        # If there is a category, update the task
        if categoryFound:
            query = "UPDATE task SET categoryid=%s WHERE taskid=%s"
            create_cursor.execute(query, (categoryId, taskId))
            mariadb_connection.commit()
            print("---Successfuly Added Task to Category---")
        else:
            print("Category ID not found!")
    else:
        print("Task ID not found!")

    pause()

# Purpose: Provide main menu for the users


def main_menu():
    print("---Welcome to TaskIT---")
    # Loops the program until the user terminates it ---
    while 1:
        choice = input(
            "\nMain Menu:\n\t[1] Add/Create Task\n\t[2] Edit Task\n\t[3] Delete Task\n\t[4] View Task\n\t[5] Mark Task as Done\n\t[6] Add Category\n\t[7] Edit Category\n\t[8] Delete Category\n\t[9] View Category\n\t[10] Add Task to Category\n\t[0] Exit\n\tChoice: ")

        # Checks if the input is valid, and is one of the options
        try:
            if int(choice) >= 0 and int(choice) <= 10:
                if choice == "1":
                    add_createTaskAlt()
                elif choice == "2":
                    editTask()
                elif choice == "3":
                    deleteTask()
                elif choice == "4":
                    viewAllTask()
                elif choice == "5":
                    markTask()
                elif choice == "6":
                    addCategoryAlt()
                elif choice == "7":
                    editCategory()
                elif choice == "8":
                    deleteCategory()
                elif choice == "9":
                    viewCategory()
                elif choice == "10":
                    addTaskToCategory()
                if choice == "0":
                    break
            else:
                print("Invalid Input. Please pick from numbers 0-10 only\n")
                pause()
        except:
            print("Invalid Input.\n")
            pause()
            
        
        clear()
    print("\n---CLOSING PROGRAM---")


main_menu()
mariadb_connection.close()
