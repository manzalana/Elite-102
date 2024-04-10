import mysql.connector
import os
from time import sleep

connection = mysql.connector.connect(user = 'root', database = 'example', password = 'Kimura1074!')
cursor = connection.cursor()
#welcome


def Display_Clear():
    sleep(1)
    print(' THIS IS WHERE A CLEAR WOULD BE!!!')
    print()
    #os.system('cls')

def Display_Seperator():
    print()
    print('------------------')
    print()
#should probably ask if they have an account already or if they want to make a new account, then it can run
def Initial_Menu():
    print('Welcome to this real cool bank!')
    print()
    print('Do you have an account with us?')

    #lists possible options
    choices=['1','2']

    #gets user input
    user_choice= input('1. Yes\n2. No\n')

    #data validation
    if Input_Validation(user_choice,choices):
        if user_choice =='1':
            getAccountNumber()
            Display_Clear()
        else :
            pass
    else:
        print('Invalid Input')
        #sleeps for 1 second, then clears the screen
        
        Display_Clear()
        Initial_Menu()
    
#if the user has an account, this functions is meant to find their account
def getAccountNumber():
    Display_Clear()
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
        Display_Seperator()
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
        print('Choose an option from this menu')
        Display_Seperator()
        accountInformationQuery=(f"SELECT * FROM guests WHERE AccountNumber={account_info[0]}")
        cursor.execute(accountInformationQuery)
        accountInformation=cursor.fetchone()
        print(accountInformation)
        
        userChoice=input('1: Check Balance \n2: Deposit Money\n3: Withdrawl Money\n4: Edit Account Information\n5: Finished\n')
        #data validation

        #if data validation returns true, run the menu code and all of that, if false, ask user for input again
        if Input_Validation(userChoice, choices):
            userChoice=int(userChoice)

        #menu from which the user will choose from
            match userChoice:
                case 1:
                    Check_Balance(account_info)
                case 2:
                    Deposit_Money(account_info)
                case 3:
                    Withdraw_Money(account_info)
                case 4:
                    Edit_Account_Info(account_info)
                case 5:
                    print('Quit')
            
            #updates the user's information in the script after every loop to account for changes made
            
        else:
            print('Input Invalid')
            
        




    #for item in cursor:

        #print(item)

#checks the balance of the user's account
def Check_Balance(account_info):
    Display_Clear()
    print(f"{account_info[3]} {account_info[2]}, your balance is currently ${account_info[4]}")
    sleep(4)

#Withdraws money from their account
def Withdraw_Money(account_info):
    
    #data validation to check if user is entering an Integer
    dataValid=False
    
    while(dataValid==False):
        Display_Clear()
        #each time this loops data valid is set to true
        dataValid=True
    #data validation
        try:
            #asks user how much they want to withdraw
            withdraw_amount=round(float(input('How much money do you want to withdraw? $')),2)
            
        except ValueError:
            print('Invalid Input. Please Input a number value')
            #will continue to loop if data isnt valid
            dataValid=False
    
    #gets the amount currently in their account
    amount_avaliable=float(account_info[4])
    #place holder value for the final value after they withdraw
    amount_final=0
    
    #if the amount they want to withdraw is more than their balance, they will have to choose a new amount to withdraw
    if withdraw_amount>amount_avaliable:
        print(f"You do not have the funds in your account to withdraw ${withdraw_amount}. Please input another amount.")
        Withdraw_Money(account_info)

        #sets amount_final to the difference between amount avalible and the amount they are taking out
    else:
        amount_final=amount_avaliable-withdraw_amount
        
        #updates the sql table with the new amount in their balance
        withdrawQuery=f"UPDATE guests SET Balance = {amount_final} WHERE AccountNumber={account_info[0]}"

        #executes the command
        cursor.execute(withdrawQuery)

        #commits the changes to the table
        connection.commit()
        print(f"Your balance is now {amount_final}")
        
#deposits money into their account
def Deposit_Money(account_info):
    Display_Clear()
    #gets the amount of money the user wants to deposit
    dataValid=False
    while dataValid==False:
        dataValid=True
        Display_Clear()
        try:
            deposit_amount=round(float(input('How much money do you want to depoit into your account?')),2)
        except ValueError:
            print('You did nto enter a valid amount. Please try again')
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

def Edit_Account_Info(account_info):
    Display_Clear()
    print('What part of your account do you wish to edit?')
    
    user_choice=input('1. PIN\n2. Name\n3. Exit to Menu')
    choices=['1','2','3']

    #data validation
    if Input_Validation(user_choice,choices):
    
        match user_choice:
            case '1':
                pass
                
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