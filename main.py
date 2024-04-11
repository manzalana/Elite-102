import mysql.connector
import os
import random
from time import sleep

connection = mysql.connector.connect(user = 'root', database = 'example', password = 'Kimura1074!')
cursor = connection.cursor()
#welcome

def resetTable():
    sql_defalt_code=["TRUNCATE TABLE guests","INSERT INTO guests(AccountNumber, Id, LastName, FirstName, Balance) VALUES(1000,111,\'manzanares\',\'alana\', 100.00)",
                     "INSERT INTO guests(AccountNumber, Id, LastName, FirstName, Balance) VALUES(1001,333,\'lopez\',\'tracy\', 100.00)"
                     ,
                     "INSERT INTO guests(AccountNumber, Id, LastName, FirstName, Balance) VALUES(1002,222,\'martinex\',\'jaime\', 100.00)"]
    for code in sql_defalt_code:
        
        cursor.execute(code)
        connection.commit()


def Display_Clear():
    sleep(1)
    os.system('cls')

def Display_Seperator():
    print()
    print('------------------')
    print()
#should probably ask if they have an account already or if they want to make a new account, then it can run
def Initial_Menu():
    Display_Seperator()
    print('Welcome to this real cool bank!')
    print()
    print('Do you have an account with us?')

    #lists possible options
    choices=['1','2','3']

    #gets user input
    user_choice= input('1. Yes\n2. I want to Create an Account!\n3. Exit\n')

    #data validation
    if Input_Validation(user_choice,choices):
        if user_choice =='1':
            getAccountNumber()
            Display_Clear()
        elif user_choice=='2' :
            Create_Account()
        else:
            print('Good Bye!')
            quit()
    else:
        print('Invalid Input')
        #sleeps for 1 second, then clears the screen
        
        Display_Clear()
        Initial_Menu()
    
#if the user has an account, this functions is meant to find their account
def getAccountNumber():
    Display_Clear()
    Display_Seperator()
    print('Log Into your Bank Account')
    Display_Seperator()
    #ask for Account Number
    accNum= input('Please Enter Your Accout Number: ')
    accFound=False

    #get all account numbers, then loop through them to see if this is valid. if not then uhoh
    accNumValidationQuery=("SELECT AccountNumber FROM guests")
    cursor.execute(accNumValidationQuery)
    allAccNum=cursor.fetchall()
    

    #gets the account numbers
    choices=[]
    for accounts in allAccNum:
        choices.append(f"{accounts[0]}")
    

    if Input_Validation(accNum,choices):
        print('Account Found!')
        
    else:
        print('Account not found. Please Try Again')
        
        getAccountNumber()
    

    #ask for the pin number
    pinNum= input('Please Enter Your PIN: ')
    #get the correct PIN number
    pinQuery= ("SELECT Id FROM guests WHERE AccountNumber="+accNum)
    cursor.execute(pinQuery)
    userPin=cursor.fetchone()
   
    #see if the PIN's match up

    if(int(pinNum)==int(userPin[0])):
        print('PIN Correct')

        
    else:
        #if PIN is Incorrect, this will run
        print('Incorrect PIN. Please re-enter your Account Number')
        getAccountNumber()
    
    #Gets all of the Account Information for the account the user is accessing
    accountInformationQuery=("SELECT * FROM guests WHERE AccountNumber="+accNum)
    cursor.execute(accountInformationQuery)
    accountInformation=cursor.fetchone()
    #menu
    Actions_Menu(accountInformation)
                 

def Actions_Menu(account_info):
    
    userChoice=0
    choices=['1','2','3','4','5']
    #should be a while loop so like while user doesnt choose 4 this will run
    while userChoice !=5:
        Display_Clear()
        Display_Seperator()
        print('Action Menu')
        Display_Seperator()
        #gets the information from the table and updates it
        accountInformationQuery=(f"SELECT * FROM guests WHERE AccountNumber={account_info[0]}")
        cursor.execute(accountInformationQuery)
        accountInformation=cursor.fetchone()
        print(f"Hello, {accountInformation[3]} {accountInformation[2]}" )
        
        userChoice=input('1: Check Balance \n2: Deposit Money\n3: Withdrawl Money\n4: Edit Account Information\n5: Back to Main Menu\n')
        #data validation

        #if data validation returns true, run the menu code and all of that, if false, ask user for input again
        if Input_Validation(userChoice, choices):
            userChoice=int(userChoice)

        #menu from which the user will choose from
            match userChoice:
                case 1:
                    Check_Balance(accountInformation)
                case 2:
                    Deposit_Money(accountInformation)
                case 3:
                    Withdraw_Money(accountInformation)
                case 4:
                    Edit_Account_Info(accountInformation)
                case 5:
                    Display_Clear()
                    Initial_Menu()
            
            #updates the user's information in the script after every loop to account for changes made
            
        else:
            print('Input Invalid')
            
        




    #for item in cursor:

        #print(item)

#checks the balance of the user's account
def Check_Balance(account_info):
    Display_Clear()
    Display_Seperator()
    print('Balance')
    Display_Seperator()
    print(f"{account_info[3]} {account_info[2]}, your balance is currently ${account_info[4]}")
    sleep(4)

#Withdraws money from their account
def Withdraw_Money(account_info):
    
    #data validation to check if user is entering an Integer
    dataValid=False
    
    while(dataValid==False):
        Display_Clear()
        Display_Seperator()
        print('Withdraw Money')
        Display_Seperator()
        #each time this loops data valid is set to true
        dataValid=True
    #data validation
        try:
            #asks user how much they want to withdraw, tries to convert it to a positive float value with 2 decimal places
            withdraw_amount=abs(round(float(input('How much money do you want to withdraw? $')),2))
            
        except ValueError:
            print('Invalid Input. Please Input a number value')
            #will continue to loop if data isnt valid
            dataValid=False
    
    #gets the amount currently in their account
    amount_avaliable=float(account_info[4])
    print(f"Balance: ${account_info[4]}")
    #place holder value for the final value after they withdraw
    amount_final=0
    
    #if the amount they want to withdraw is more than their balance, they will have to choose a new amount to withdraw
    if withdraw_amount>amount_avaliable:
        print(f"You do not have the funds in your account to withdraw ${withdraw_amount}. Please input another amount.")
        Withdraw_Money(account_info)

        #sets amount_final to the difference between amount avalible and the amount they are taking out
    else:
        print(f"Withdrawing: ${withdraw_amount}")
        amount_final=amount_avaliable-withdraw_amount
        
        #updates the sql table with the new amount in their balance
        withdrawQuery=f"UPDATE guests SET Balance = {round(amount_final,2)} WHERE AccountNumber={account_info[0]}"

        #executes the command
        cursor.execute(withdrawQuery)

        #commits the changes to the table
        connection.commit()
        print(f"Your balance is now ${amount_final}")
        
#deposits money into their account
def Deposit_Money(account_info):
    #gets the amount of money the user wants to deposit
    dataValid=False
    while dataValid==False:
        dataValid=True
        Display_Clear()
        Display_Seperator()
        print('Deposit Money')
        Display_Seperator()
        try:
            #tries to take user input as a float, rounds it to 2 decimal places then takes the absolute value of it
            deposit_amount=abs(round(float(input('How much money do you want to deposit into your account?')),2))
        except ValueError:
            print('Invalid Input. Please try again')

            dataValid=False

    #gets the ammount of money currently in the account
    initial_amount=float(account_info[4])

    #gets the amount after depositing
    final_amount=deposit_amount+initial_amount

    #the sql query to update the balance with the new balance
    depositQuery=f"UPDATE guests SET Balance= {final_amount} WHERE AccountNumber={account_info[0]}"

    #executes the command
    cursor.execute(depositQuery)
    #commits the command
    connection.commit()

    print(f"Your balance is now {final_amount}")
    sleep(3)

def Edit_Account_Info(account_info):
    Display_Clear()
    Display_Seperator()
    print('Edit Account Information')
    Display_Seperator()
    print('What part of your account do you wish to edit?')
    
    user_choice=input('1. PIN\n2. Name\n3. Exit to Menu')
    choices=['1','2','3']

    #data validation
    if Input_Validation(user_choice,choices):
    
        match user_choice:
            case '1':
                while not_valid_data:
                    not_valid_data=False
                    try:
                        pin=int(input('Please enter a 3 digit PIN: '))
                    except ValueError:
                        print('Invalid Input')
                        not_valid_data=True
                    if (len(str(pin)) !=3):
                            print('Please enter a 3 digit PIN!')
                            Display_Clear()
                            not_valid_data=True
                    newPinQuery=f"UPDATE guests SET Id= {pin} WHERE AccountNumber={account_info[0]}"
                    cursor.execute(newPinQuery)
                    connection.commit()
            case '2':

                #gets new first name
                first_name=input('Please Enter your new First Name\n')
                #gets new last name
                last_name=input('Please Enter your new Last Name\n ')
                #queries
                newFNameQuery='UPDATE guests SET FirstName= \''+first_name+f"\' WHERE AccountNumber={account_info[0]}"
                newLNameQuery='UPDATE guests SET LastName= \''+last_name+f"\' WHERE AccountNumber={account_info[0]}"
                
                print(newFNameQuery)
                cursor.execute(newFNameQuery)
                cursor.execute(newLNameQuery)
                connection.commit()
            case '3':
                Actions_Menu(account_info)

def Input_Validation(input, choices):
    if input in choices:
        return True
    else:
        return False
     
def Create_Account():
    Display_Clear()
    Display_Seperator()
    print('Creating an Account')
    Display_Seperator()
    print('We are glad you\'ve decided to open an account with us!')
    first_name=input('What is your first name?: ')
    last_name=input('What is your last name?: ')
    not_valid_data=True
    #generates new user's account number
    newAccNum= random.randint(1003,9999)
    pin=0
    #validates the new user's PIN information
    
    while not_valid_data:
        Display_Clear()
        Display_Seperator()
        print('Creating an Account')
        Display_Seperator()
        not_valid_data=False
        try:
            pin=int(input('Please enter a 3 digit PIN: '))
        except ValueError:
            print('Invalid Input')
            not_valid_data=True
        if (len(str(pin)) !=3):
                print('Please enter a 3 digit PIN!')
                not_valid_data=True
    #creates account for new user
    addUserQuery=f"INSERT INTO guests(AccountNumber, Id, LastName, FirstName, Balance) VALUES({newAccNum},{pin},'"+last_name+"','"+first_name+"', 0.00)"
    cursor.execute(addUserQuery)
    connection.commit()
    print(f"Your Account Number is {newAccNum}")
    sleep(2)
    Initial_Menu()

resetTable()
Display_Clear()
Initial_Menu()

cursor.close()
connection.close()



#addData=("INSERT INTO guests (Name,Age,Height) VALUES (1001,18,5.0)")
#cursor.execute(addData)
#connection.commit()



#In this project you will create an online banking program. 
#Users need to have an account number and PIN to identify themselves 
#as owners of an account. Once users get into the system they will have 
#standard options: check balance, deposit, and withdraw. Additionally, a 
#new user or bank administrator can also create a new account, close 
#account, and modify an account (such as edit name, PIN, or any other 
#personal identification required to open an account).
#
#