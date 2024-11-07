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

# GET all posts
@posts_bp.route('/api/posts', methods=['GET'])
def get_posts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts')
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    
    posts_list = [row_to_dict(post, cursor) for post in posts]
    return jsonify(posts_list)

# GET a single post by ID
@posts_bp.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
    post = cursor.fetchone()
    cursor.close()
    conn.close()

    if post is None:
        abort(404, description="Post not found")
    return jsonify(row_to_dict(post, cursor))

# POST a new post
@posts_bp.route('/api/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    if 'title' not in data or 'content' not in data:
        abort(400, description="Title and content are required")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (data['title'], data['content']))
    conn.commit()
    new_post_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return jsonify({"id": new_post_id, "title": data['title'], "content": data['content']}), 201

# PUT update a post by ID
@posts_bp.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (data['title'], data['content'], post_id))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"id": post_id, "title": data['title'], "content": data['content']})

# DELETE a post by ID
@posts_bp.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Post deleted successfully"}), 200

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
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE products SET ProductName = ?, ProductBrand = ?, Gender = ?, Price = ?, NumImages = ?, Description = ?, PrimaryColor = ?
        WHERE ProductID = ?
    """, (data["ProductName"], data["ProductBrand"], data["Gender"], data["Price"], data["NumImages"], data["Description"], data["PrimaryColor"], product_id))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"ProductID": product_id, **data})

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