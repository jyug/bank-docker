import mysql.connector

mydb = mysql.connector.python.connect(
    host="localhost",
    user="root",
    passwd="CMPE202",
    auth_plugin='mysql_native_password',
)

my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE users")
my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)