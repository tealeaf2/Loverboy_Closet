from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config.from_object('app.config.Config')

    db.init_app(app)

    with app.app_context():
        from .routes.home import home_bp
        from .routes.closet import closet_bp
        from .routes.recommend import recommend_bp
        db.create_all()
        CORS(app)
        app.register_blueprint(home_bp)
        app.register_blueprint(closet_bp)
        app.register_blueprint(recommend_bp)

    return app