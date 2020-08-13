import mysql.connector
import mysql.connector as mysql
# enter your server IP address/domain name
HOST = "onlinetnpsc.com" # or "domain.com"
# database name, if you want just to connect to MySQL server, leave it empty
DATABASE = "u852023448_khhWy"
# this is the user you create
USER = "u852023448_5LMAu"
# user password
PASSWORD = "fz9jYGhBtY"
try:
   db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD,connection_timeout=6000)
   print("Connected to:", db_connection.get_server_info())
   mycursor = db_connection.cursor()


except mysql.Error as err:
    print(err)
    print("Error Code:", err.errno)
    print("SQLSTATE", err.sqlstate)
    print("Message", err.msg)
