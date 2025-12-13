# app/__init__.py
from flask import Flask
from src.logging_setup import logger

def create_app():
    logger.info("Creating Flask application")

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'

    from .routes import main_bp, crud_bp   # 👈 import BOTH
    app.register_blueprint(main_bp)
    app.register_blueprint(crud_bp)        # 👈 REGISTER CRUD

    logger.info("Flask application created and routes registered")
    return app
