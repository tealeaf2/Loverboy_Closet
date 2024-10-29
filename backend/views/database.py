import sqlite3
from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()

def get_db_connection():
    if os.getenv('ENV') == 'PRODUCTION':
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DB')
        )
    else:
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
    return conn