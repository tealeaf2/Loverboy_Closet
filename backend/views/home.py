import sqlite3
from flask import Blueprint, jsonify, request, abort
from .database import get_db_connection

posts_bp = Blueprint('home', __name__)

# Helper function to convert rows to dictionaries for both SQLite and MySQL
def row_to_dict(row, cursor):
    if isinstance(row, sqlite3.Row):
        return dict(row)
    else:
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, row))


# GET all products
@posts_bp.route('/api/products', methods=['GET']) 
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    cursor.close()
    conn.close()

    product_list = [row_to_dict(product, cursor) for product in products]
    return jsonify(product_list)

# GET a single product by ID
@posts_bp.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE ProductID = ?', (product_id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()

    if product is None:
        abort(404, description="Product not found")
    return jsonify(row_to_dict(product, cursor))

# POST a new product
@posts_bp.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()
    print(data)
    required_fields = ["ProductName", "ProductBrand", "Gender", "Price", "NumImages", "Description", "PrimaryColor"]
    if not all(field in data for field in required_fields):
        abort(400, description="All fields are required")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO products (ProductName, ProductBrand, Gender, Price, NumImages, Description, PrimaryColor)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (data["ProductName"], data["ProductBrand"], data["Gender"], data["Price"], data["NumImages"], data["Description"], data["PrimaryColor"]))
    conn.commit()
    new_product_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return jsonify({"ProductID": new_product_id, **data}), 201

# PUT update a product by ID
@posts_bp.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    if not data:
        abort(400, description="Request must be in JSON format")
    valid_fields = ["ProductName", "ProductBrand", "Gender", "Price", "NumImages", "Description", "PrimaryColor"]

    update_fields = {key: value for key, value in data.items() if key in valid_fields}

    if not update_fields:
        abort(400, description="No valid fields provided to update")

    set_clause = ", ".join([f"{field} = ?" for field in update_fields])
    values = list(update_fields.values()) + [product_id]

    # Establish a database connection
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        UPDATE products SET {set_clause} WHERE ProductID = ?
    """, values)
    conn.commit()

    cursor.close()
    conn.close()
    updated_data = {**update_fields, "ProductID": product_id}
    return jsonify(updated_data)

# DELETE a product by ID
@posts_bp.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE ProductID = ?', (product_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Product deleted successfully"}), 200