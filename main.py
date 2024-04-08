import mysql.connector

connection = mysql.connector.connect(user = 'root', database = 'example', password = 'Kimura1074!')
cursor = connection.cursor()

addData=("INSERT INTO guests (Name,Age,Height) VALUES (1001,18,5.0)")
cursor.execute(addData)
connection.commit()
cursor.close()

connection.close()