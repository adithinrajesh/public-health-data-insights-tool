# app/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'  # Needed for forms/session

    # Import and register routes
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
