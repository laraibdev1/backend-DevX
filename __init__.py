# __init__.py
import os
from flask import Flask
from flask_cors import CORS
from models import db
from dotenv import load_dotenv
from services.courses import courses_bp  # Ensure the blueprint is named correctly

def create_app():
    # Load environment variables from .env file
    load_dotenv()

    app = Flask(__name__)

    # CORS configuration: Allow requests from your frontend origin
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    # Flask application configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')  # Use a default if not set
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite')  # Default to SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoid warning about deprecated behavior

    # Initialize the database
    db.init_app(app)

    # YouTube API key retrieval from environment variables
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
    if not YOUTUBE_API_KEY:
        raise ValueError("YOUTUBE_API_KEY not set in environment variables")

    # Register blueprints
    app.register_blueprint(courses_bp, url_prefix='/api/courses')  # Ensure correct import
    from services.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # Create database tables (only for development)
    with app.app_context():
        db.create_all()

    return app
