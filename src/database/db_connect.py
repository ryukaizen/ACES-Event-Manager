import os
import mysql.connector
import time

from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

while True:
    try:
        cnx = mysql.connector.connect(
            host=HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
    except mysql.connector.Error as err:
        print(err)
        print("[*] Trying to connect again... (Press Ctrl + C to exit.)\n")
        time.sleep(5)
        continue
    else:
        print("[*] MySQL connection established successfully!\n--- Host: {} | Database: {}\n".format(HOST, DB_NAME))    
        break
    
cursor = cnx.cursor()