import sqlite3
import os
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error
from views.database import get_db_connection
import csv
import re

load_dotenv()

env = os.getenv('ENV')

def init_db(connection):
    with open('sqlite3.sql') as f:
        cursor = connection.cursor()
        if env == 'DEVELOPMENT':
            cursor.executescript(f.read())
        elif env == 'PRODUCTION':
            for statement in f.read().split(';'):
                if statement.strip():
                    cursor.execute(statement)
        cursor.close()

    insert_posts(connection)
    insert_data_from_csv(connection, 'clothes.csv', env)


def insert_posts(connection):
    cursor = connection.cursor()
    insert_query = "INSERT INTO posts (title, content) VALUES (?, ?)"
    cursor.execute(insert_query, ('First Post', 'Content for the first post'))
    cursor.execute(insert_query, ('Second Post', 'Content for the second post'))
    connection.commit()
    cursor.close()


def insert_data_from_csv(connection, csv_file_path, env='PRODUCTION'):
    cursor = connection.cursor()
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        # Define keyword categories with their respective regex patterns
        keyword_categories = {
            "Shirts": [r'\b\w*shirt\w*\b', r'\b\w*top\w*\b'],
            "Pants": [r'\b\w*short\w*\b', r'\b\w*jean\w*\b', r'\b\w*pant\w*\b', r'\b\w*trunk\w*\b', r'\b\w*jogger\w*\b', r'\b\w*trouser\w*\b', r'\b\w*chino\w*\b', r'\b\w*cargo\w*\b'],
            "Accessories": [r'\b\w*bag\w*\b', r'\b\w*necklace\w*\b', r'\b\w*jewelry\w*\b', r'\b\w*ring\w*\b', r'\b\w*cufflink\w*\b', r'\b\w*sunglass\w*\b', r'\b\w*belt\w*\b'],
            "Shoes": [r'\b\w*loafer\w*\b', r'\b\w*sneaker\w*\b', r'\b\w*shoe\w*\b', r'\b\w*sandal\w*\b', r'\b\w*slipper\w*\b'],
            "Outerwear": [r'\b\w*jacket\w*\b', r'\b\w*hoodie\w*\b', r'\b\w*sweater\w*\b', r'\b\w*cardigan\w*\b'],
            "Dresses": [r'\b\w*dress\w*\b'],
            "Formals": [r'\b\w*suit\w*\b', r'\b\w*blazer\w*\b']
        }

        # Choose the appropriate placeholder based on environment
        placeholder = '%s' if env == 'PRODUCTION' else '?'
        insert_queries = {
            category: f"INSERT INTO {category.lower()} VALUES ({', '.join([placeholder] * 8)})"
            for category in keyword_categories
        }

        # Function to identify the category based on keywords
        def get_category(row):
            for category, patterns in keyword_categories.items():
                for pattern in patterns:
                    if any(re.search(pattern, field, re.IGNORECASE) for field in row):
                        return category
            return None

        # Insert each row into the appropriate category table
        for row in reader:
            category = get_category(row)
            if category:
                cursor.execute(insert_queries[category], row)

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
