import mysql.connector


# create a connection
connection = mysql.connector.connect(
    host = 'localhost',
    user = 'gargi',
    passwd = '123456Jan@'
    
)

# create a cursor object
cursor = connection.cursor()

# create the DB
cursor.execute("CREATE DATABASE gargi_db")

print("All Done!")