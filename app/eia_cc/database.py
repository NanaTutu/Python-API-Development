import mysql.connector
import time

while True:
    try:
        conn = mysql.connector.connect(host='localhost', database='eia_cc', user='root')
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(5)