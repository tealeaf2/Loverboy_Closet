import sqlite3
from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()

def get_db_connection():
    """
    Establishes a database connection based on the environment (production or development).
    Uses MySQL in production and SQLite for local development.
    """
    try:
        if os.getenv('ENV') == 'PRODUCTION':
            conn = mysql.connector.connect(
                host=os.getenv('MYSQL_HOST'),
                user=os.getenv('MYSQL_USER'),
                password=os.getenv('MYSQL_PASSWORD'),
                database=os.getenv('MYSQL_DB')
            )
        else:
            conn = sqlite3.connect('database.db')
            conn.row_factory = sqlite3.Row  # Allows access to SQLite rows as dictionaries
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None