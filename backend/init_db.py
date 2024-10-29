import sqlite3
import os
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error
from views.database import get_db_connection

load_dotenv()

env = os.getenv('ENV')

def init_db(connection):
    with open('sqlite3.sql') as f:
        if env == 'DEVELOPMENT':
            cursor = connection.cursor()
            cursor.executescript(f.read())
            cursor.close()
        elif env == 'PRODUCTION':
            cursor = connection.cursor()
            for statement in f.read().split(';'):
                if statement.strip():
                    cursor.execute(statement)
            cursor.close()

    insert_posts(connection)


def insert_posts(connection):
    cursor = connection.cursor()
    insert_query = "INSERT INTO posts (title, content) VALUES (%s, %s)"
    cursor.execute(insert_query, ('First Post', 'Content for the first post'))
    cursor.execute(insert_query, ('Second Post', 'Content for the second post'))
    connection.commit()
    cursor.close()


if __name__ == "__main__":
    if env == 'DEVELOPMENT':
        try:
            connection = sqlite3.connect('database.db')
            init_db(connection)
        except sqlite3.Error as e:
            print(f"The error '{e}' occurred")
        finally:
            connection.close()

    elif env == 'PRODUCTION':
        try:
            connection = get_db_connection()
            init_db(connection)
        except Error as e:
            print(f"The error '{e}' occurred")
        finally:
            if connection.is_connected():
                connection.close()