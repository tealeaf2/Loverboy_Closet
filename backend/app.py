import os
from flask import Flask
from flask_cors import CORS
from views.home import posts_bp
from dotenv import load_dotenv

load_dotenv()
os.environ['ENV'] = 'PRODUCTION'

app = Flask(__name__)
CORS(app)

app.register_blueprint(posts_bp)

if __name__ == '__main__':
  app.debug=True
  host = '127.0.0.1'
  port = 5000
  os.environ['ENV'] = 'DEVELOPMENT'
  app.run(host=host, port=port)