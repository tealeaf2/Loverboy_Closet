from flask import Blueprint, jsonify
from .database import get_db_connection

posts_bp = Blueprint('home', __name__)

@posts_bp.route('/api/posts', methods=['GET'])
def get_posts():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM posts')
    # cursor.execute('SELECT 1')
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    
    posts_list = [dict(post) for post in posts]
    return jsonify(posts_list)