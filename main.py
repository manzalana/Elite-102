import mysql.connector

connection = mysql.connector.connect(user = 'root', database = 'example', password = 'Kimura1074!')
cursor = connection.cursor()
#welcome
print('Welcome to this real cool bank!')

#should probably ask if they have an account already or if they want to make a new account, then it can run

def getAccountNumber():
    #ask for Account Number
    accNum= input('Please Enter Your Accout Number: ')
    accFound=False

    #get all account numbers, then loop through them to see if this is valid. if not then uhoh
    accNumValidationQuery=("SELECT AccountNumber FROM guests")
    cursor.execute(accNumValidationQuery)
    allAccNum=cursor.fetchall()
    for accounts  in allAccNum:
        
        #checks if the account number entered is in the system
        if int(accounts[0]) ==int(accNum):
            print(accounts[0])
            #if it is found then this will run
            accFound=True
    #if there isnt an account found, the userLogin function will loop
    if (accFound==False):
        print('Account not Found. Please Try Again')
        getAccountNumber()
    
    print('Account Found!')
    

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
    print(accountInformation)
    #menu
    # Check balance, withdrawl money, deposite money
    print('Choose an option from this menu')
    print('1: Check Balance \n2: Deposit Money\n3: Withdrawl Money\n4: Exit')
    userChoice=int(input())
    print(userChoice)
    #should be a while loop so like while user doesnt choose 4 this will run
    while userChoice !=4:
        match userChoice:
            case 1:
                print('this is a placeholder el o el')
            case 2:
                print('choice 2')
            case 3:
                print ('choice 3')
            case 4:
                print('choice 4')
        userChoice=int(input())
            



    #for item in cursor:

        #print(item)

#checks the balance of the user's account
def Check_Balance(account_info):
    
    pass

#Withdraws money from their account
def Withdraw_Money(account_info):
    pass

#deposits money into their account
def Deposit_Money(account_info):
    pass
    
   
    


getAccountNumber()

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