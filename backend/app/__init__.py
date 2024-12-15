from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config.from_object('app.config.Config')
    jwt = JWTManager(app)
    db.init_app(app)

    with app.app_context():
        from .routes.auth import auth_bp
        from .routes.closet import closet_bp
        from .routes.recommend import recommend_bp
        from .routes.outfits import outfits_bp

        db.create_all()
        CORS(app, resources={r"/api/*": {"origins": "*"}})
        app.register_blueprint(auth_bp)
        app.register_blueprint(closet_bp)
        app.register_blueprint(recommend_bp)
        app.register_blueprint(outfits_bp)

    return app