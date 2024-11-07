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

    #insert_posts(connection)
    insert_data_from_csv(connection, 'clothes.csv')


def insert_data_from_csv(connection, csv_file_path):
    cursor = connection.cursor()
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        # Define keyword categories with regex patterns
        keyword_categories = {
            "shirts": [r'\b\w*shirt\w*\b', r'\b\w*top\w*\b'],
            "pants": [r'\b\w*short\w*\b', r'\b\w*jean\w*\b', r'\b\w*pant\w*\b', r'\b\w*trunk\w*\b', r'\b\w*jogger\w*\b', r'\b\w*trouser\w*\b', r'\b\w*chino\w*\b', r'\b\w*cargo\w*\b'],
            "accessories": [r'\b\w*bag\w*\b', r'\b\w*necklace\w*\b', r'\b\w*jewelry\w*\b', r'\b\w*ring\w*\b', r'\b\w*cufflink\w*\b', r'\b\w*sunglass\w*\b', r'\b\w*belt\w*\b'],
            "shoes": [r'\b\w*loafer\w*\b', r'\b\w*sneaker\w*\b', r'\b\w*shoe\w*\b', r'\b\w*sandal\w*\b', r'\b\w*slipper\w*\b'],
            "outerwear": [r'\b\w*jacket\w*\b', r'\b\w*hoodie\w*\b', r'\b\w*sweater\w*\b', r'\b\w*cardigan\w*\b'],
            "dresses": [r'\b\w*dress\w*\b'],
            "formals": [r'\b\w*suit\w*\b', r'\b\w*blazer\w*\b']
        }

        # Placeholder based on environment
        placeholder = '%s' if env == 'PRODUCTION' else '?'

        # Insert query for products table
        product_insert_query = f"""
            INSERT INTO products (ProductName, ProductBrand, Gender, Price, NumImages, Description, PrimaryColor)
            VALUES ({', '.join([placeholder] * 7)})
        """

        # Insert queries for category tables, only inserting ProductID
        insert_queries = {
            category: f"INSERT INTO {category} (ProductID) VALUES ({placeholder})"
            for category in keyword_categories
        }

        # Function to determine product category based on keywords
        def get_category(row):
            for category, patterns in keyword_categories.items():
                for pattern in patterns:
                    if any(re.search(pattern, field, re.IGNORECASE) for field in row):
                        return category
            return None

        # Insert each row into the database
        for row in reader:
            # Insert into products table first
            cursor.execute(product_insert_query, row[1:])  # Skip ProductID if present
            product_id = cursor.lastrowid  # Get the generated ProductID

            # Determine the category and insert into category table
            category = get_category(row)
            if category:
                cursor.execute(insert_queries[category], (product_id,))

    connection.commit()
    cursor.close()

def print_table_data(connection, table_name):
    cursor = connection.cursor()
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    rows = cursor.fetchall()

    print(f"\nData in {table_name} table:")
    for row in rows:
        print(row)

    cursor.close()

if __name__ == "__main__":
    if env == 'DEVELOPMENT':
        try:
            connection = sqlite3.connect('database.db')
            init_db(connection)
            # Print data from each table after initializing the database
            print_table_data(connection, 'shirts_view')
            print_table_data(connection, 'pants_view')
            print_table_data(connection, 'accessories_view')
            print_table_data(connection, 'shoes_view')
            print_table_data(connection, 'outerwear_view')
            print_table_data(connection, 'dresses_view')
            print_table_data(connection, 'formals_view')
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
    