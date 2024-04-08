import mysql.connector

connection = mysql.connector.connect(user = 'root', database = 'example', password = 'Kimura1074!')
cursor = connection.cursor()
#welcome
print('Welcome to this real cool bank!')


#ask for Account Number
accNum= input('Please Enter Your Accout Number: ')

#ask for accout PIN for that account number
pinNum= input('Please Enter Your PIN: ')


#menu
# Check balance, withdrawl money, deposite money
print('Choose an option from this menu')




testQuery = ("SELECT Id FROM guests WHERE AccountNumber="+accNum)

 

cursor.execute(testQuery)
plsid=cursor.fetchone()

#for item in cursor:

    #print(item)

 
print(plsid[0])
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