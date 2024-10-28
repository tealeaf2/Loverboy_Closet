# from flask import Flask, send_from_directory, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import text
# import os

#app = Flask(__name__, static_folder='../dist')
# app = Flask(__name__)

# password = "1r1sh"
# host = "db8.cse.nd.edu"
# username = "kle2"
# db_name = username

# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@{host}:3306/{db_name}'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# app.debug=True

# # @app.route('/')
# # def serve_index():
# #     return send_from_directory(app.static_folder, 'index.html')

# # @app.route('/<path:path>')
# # def serve_static(path):
# #     return send_from_directory(app.static_folder, path)


# @app.route('/test-connection')
# def test_connection():
#     try:
#         db.session.execute(text("SELECT 1"))
#         return "Database connection is working!"
#     except Exception as e:
#         return jsonify({"success": False, "message": str(e)})

import sqlite3
from flask import Flask, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/posts', methods=['GET'])
def get_posts():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    
    posts_list = [dict(post) for post in posts]
    return jsonify(posts_list)

if __name__ == '__main__':
  app.debug=True