# Title: IS 6713 Homework #1
# Author: Kalea Sebesta
# Date: Oct. 20, 2017
# Due Date: Oct 31, 2017

'''
Program Discription: Purpose is to maintian company info
for a small business. (first and last name, position, department,
and salary of each employee) The program continuously read input
from the user, output data, or quit the program depending on the
option the user selects. Menu items: the input of the company can
only be entered once, can input department, add employee, change
employee name, promote employee, output list of all current empl-
oyee and their info, output whether an employee exists (by name)
if not can add employee, or quit the program.
'''

# ---------------------------------------------------------
# FUNCTION DEFINITIONS
# ---------------------------------------------------------
# Function Name: Menu function
# Inputs: None
# Output: Returns the option the user input (str)
# Purpose: Displays menu and prompts for user input
# ---------------------------------------------------------
def Menu():
    # Prompts the user for input
    option = input('Choose one of the Following Options:\n'
                   'a. Input Company Name\n'
                   'b. Input Department Name\n'
                   'c. Add Employee\n'
                   'd. Change Employee Name\n'
                   'e. Promote Employee to New Position\n'
                   'f. Give Employee Raise\n'
                   'g. Current Employees and Info\n'
                   'h. Check Employee Existence\n'
                   'i. End Program\n')
    return option
# ----------------------------------------------------------
# Name: addEmployee function
# Input: Dictionary
# Output: Dictionary
# Purpose: Takes in a global dictionary and prompts the user
#          for an employees information and then adds the emp
#          to the dictionary if the emp doesnt already exists
# -----------------------------------------------------------
def addEmployee(dictionary):
    try:
        lname = str(input('Enter last name:'))
        fname= str(input('Enter first name:'))
        pos = str(input('Enter position: '))
        dept = str(input('Enter department: '))
        sal = int(input('Enter annual salary: '))

    except:
        # put a try or except to inform the user to enter the
        # salary as numeric value
        print('Please try again, the salary must include only numeric values')
        sal = int(input('Enter annual salary: '))

    # takes values inputted by user and saves them in the employee
    # dictionary and returns it. it also creates a new key called
    # full name that combines first and last names
    dictionary[dept] = {'lname': lname,
                         'fname': fname,
                         'fullName': fname + " " + lname,
                         'Position': pos,
                         'Department': dept,
                         'Salary': sal}
    return dictionary
# ------------------------------------------------------------
# Name: display_emp_counts
# Input: Two Lists and an index
# Output: Void (print statement
# Purpose: Takes the department list that contains the depart-
#          ment names and the list that contains the dictionaries
#          of the employees and the index that contains the
#          desired department in the department list. It then loops
#          through the employee list comparing the department in
#          the employee dictionary to the desired department, if
#          they are the same then the counter is increased (the
#          counter is counting how many employees are in that
#          department. Then the department name and number of emp
#          is printed out.
# -------------------------------------------------------------
def display_emp_counts(dept_lst, dept_emp_lst, index):
    # initializing variables
    count = 0
    size = len(dept_emp_lst)

    # printing the department
    print('The Below Employee List for Department:', dept_lst[index])

    for i in range(0, size, 1):
        # HELP HERE MY LOOP IS REPEATING LAST PERSON AND NOT PUTTING
        # IT IN THE CORRECT DEPARTMENT IF THE DEPARTMENT HAS ALREADY
        # BEEN ENTERED PREVIOUSLY
        # printing each employees info on one line prettily who is in
        # desired dept
        if dept_emp_lst[i]['Department'] == dept_lst[index]:
            print(dept_emp_lst[i]['fullName'],
                  dept_emp_lst[i]['Department'],
                  dept_emp_lst[i]['Position'],
                  "$"+'{:,}'.format(dept_emp_lst[i]['Salary']))
            count = count + 1

    # printing the department and total employee count
    print('The', dept_lst[index], 'department has', count, 'employee(s)\n')
# ----------------------------------------------------------------
# MAIN PROGRAM
# ----------------------------------------------------------------
# initialize variables
counter = 0
dept = tuple()
optionList = ['a','b','c','d','e','f','g','h','i']
count = 0
dept_emp_lst = []
global_emp = dict()

# Display Menu (start while loop)
while True:
    choice = Menu()

    # ----------------------------------------------------------

    # a. Input Company Name
    # if option a. is selected more than once an error message is
    # displayed and prompts the user to choose another option

    if choice == 'a' or choice == 'A' and counter == 0:
        comName = str(input('Enter the name of the company: '))
        counter = counter + 1

    elif choice == 'a' or choice == 'A' and counter > 0:
        # entering same company name results in error message
        comName = str(input('Enter the name of the company: '))
        print('Please choose another option (b-i) ', comName, 'already exists')
    # ----------------------------------------------------------

    # b. Input Department Name
    # prompts the user for a department name and checks to see
    # if it exists, if it doesnt it adds it to the dept tuple
    # if it does exists an error message is displayed

    elif choice == 'b' or choice == 'B' and counter > 0:
        deptName = input('Enter department name: ')
        if deptName not in dept:
            dept += (deptName,)
        else:
            print('Department Already Exists')
    # ----------------------------------------------------------

    # c. Add Employee
    # HOW CAN I CHECK AND IF EMPLOYEE ALREADY EXISTS DELETE DUPLICATES
    # add employee to the global dictionary and checks to see if
    # department is in department list, if it isn't it adds it to the
    # department tuple

    elif choice == 'c' or choice == 'C' and counter > 0:
            addEmployee(global_emp)
            for key in global_emp:
                if global_emp[key]["Department"] not in dept:
                    print("department not found")
                    print("adding to dept tuple")
                    dept += (global_emp[key]["Department"],)
            dept_emp_lst.append(global_emp[key])
    # ----------------------------------------------------------

    # d. Change Employee's Name
    # prompts user for the employee's name to change, if it is
    # in the system, it prompts the employee for the new name, if
    # it is not in the system it informs the user that the employee
    # isn't in the system

    elif choice == 'd' or choice == 'D' and counter > 0:
        # prompt user for original name
        oName = input('Enter original name:')

        if oName in global_emp[key]['fullName']:
            # prompt user for new name
            nName = input('Enter new name: ')

            # loop through employees in dept and find the original name
            # replace old name with new name in the empInfo
            for oName in global_emp[key]['fullName']:
                global_emp[key]['fullName'] = nName
        else:
            print('That employee does not exist')
    # ----------------------------------------------------------

    # e. Promote Employee to New Position
    # prompts the user for the employee that will be given a new
    # position, if the employee is in the system it prompts the
    # user for the new position title and replaces the old position
    # with the new position, if employee is not found in the system
    # the user is informed

    elif choice == 'e' or choice == 'E' and counter > 0:
        # prompt user for employee
        name = input('Enter name of employee that is changing positions: ')

        if name in global_emp[key]['fullName']:
            # prompt user for new position
            newPos = input('Enter the title of the new position: ')

            # change position in dictionary
            for name in global_emp[key]['fullName']:
                global_emp[key]['Position'] = newPos
        else:
            print('That employee does not exist')
    # ----------------------------------------------------------

    # f. Give Employee Raise
    # prompts the user for the employee that will be getting the
    # raise, if the employee is in the system it then prompts the
    # user for the percentage raise and calculates the new salary
    # with the new raise and replaces the old salary with the new
    # salary in the employee's dictionary

    elif choice == 'f' or choice == 'F' and counter > 0:
        # prompt user for employee
        name = input('Enter name of employee that is getting a raise: ')

        # checks to verify name is in the dictionary, if the employee is
        # in the dictionary then the user is prompt for the percentage raise
        # then calculate the raise and applies it to salary. if employee
        # is not in the system the user is notified
        if name in global_emp[key]['fullName']:
            percR = float(input('Enter the %raise: '))
            newSal = round((1 + (percR / 100)) * global_emp[key]['Salary'], 2)
            global_emp[key]['Salary'] = newSal
        else:
            print('That employee does not exist')
    # ---------------------------------------------------------

    # g. Current Employees and Info
    # for each department the employees info are printed out and
    # the total count for each department is also displayed
# ERRORS HERE WHEN A EMPLOYEE IT IT SALES MARKETING IT (THE LAST IT
# IS PRINTED AS A DUPLICATE OF THE MARKETING EMPLOYEE) LOGIC OF MY
# LOOP IS INCORRECT

    elif choice == 'g' or choice == 'G' and counter > 0:
        size = len(dept_emp_lst)
        for index in range(0, size, 1):
            display_emp_counts(dept, dept_emp_lst, index)
    # ---------------------------------------------------------

    # h. Does Employee Exist?
    # prompts the user for the name of the employee and checks it
    # against the names in the global employee dictionary, if emp-
    # loyee is already in the system the user is notified, if it
    # is not, it prompts the user to add the new employee

    elif choice == 'h' or choice == 'H' and counter > 0:
        # prompt user for original name
        name = input('Enter name of employee: ')
        # if yes display info
        if name in global_emp[key]['fullName']:
            print(name, 'is already an employee in the system')

        # if not then prompt to add to employee
        else:
            print('Employee not found, please add to system')
            addEmployee(global_emp)
            for key in global_emp:
                if global_emp[key]["Department"] not in dept:
                    print("department not found")
                    print("adding to dept tuple")
                    dept += (global_emp[key]["Department"],)
            dept_emp_lst.append(global_emp[key])
    # ---------------------------------------------------------

    # if the user inputs invalid option
    # if the user tries to input any information before entering
    # company name the user is notified and loops back to the menu

    elif (choice != 'a' or choice != 'A') and counter == 0:
        print('Company Name Must be Entered First')

    # if user enters a string instead of a value from the option
    # list the user is notified and loops back to the menu
    elif choice not in optionList:
        print('Not a valid option, please choose again')
    # --------------------------------------------------------

    # i. End Program
    # by ending the program an output file is written and the
    # title of the file is displayed to the user

    elif choice == 'i' or choice == 'I':
        # create output file
        # open and write
        fout = open('sebesta_HW1_output.txt', 'w')

        # prints company name and total number of employees
        fout.write('Company Name: %s\nNumber of Employees: %d\n\n' %
                   (comName, len(dept_emp_lst)))

        # prints out each employee and info in department
        # prints out alphabetically by department and last name
        # packages and imports
        from operator import itemgetter
        import operator
        newlst = sorted(dept_emp_lst,
                        key=operator.itemgetter('Department','lname'),
                        reverse=False)

        # calculates the number of employees for each department and
        # writes it to the file
        for i in dept:
            fout.write('The %s department has %d employees\n' %
                       (i, sum(x.get('Department') == i for x in newlst)))
        fout.write('\n')

        # LOGIC ERROR OCCURING HERE WHEN, IT IT Sales Marketing IT, IS ENTERED
        fout.write('\n'.join(d['fullName'] + ", " +
                             d['Department'] + ", " +
                             d['Position'] + ", $" +
                             '{:,}'.format(d['Salary'])for d in newlst))

        # print output file name
        print("The output file is: 'sebesta_HW1_output.txt' ")

        # close file
        fout.close()
        break
    # ---------------------------------------------------------