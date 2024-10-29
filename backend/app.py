from flask import Flask
from flask_cors import CORS
from views.home import posts_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(posts_bp)

if __name__ == '__main__':
  app.debug=True