from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import logging

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)

    app.logger.info("Initializing application...")

    app.secret_key = os.getenv('SECRET_KEY', 'your_fallback_secret_key_here')
    app.logger.info(f"Secret key set: {'from environment' if os.getenv('SECRET_KEY') else 'using fallback'}")
    
    if os.getenv("DATABASE_URL"):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
        app.logger.info(f"Using database URL: {os.getenv('DATABASE_URL')}")
    elif os.getenv("ANSWER_FILE"):
        app.config['ANSWER_FILE'] = os.getenv("ANSWER_FILE")
        app.logger.info(f"Using answer file: {os.getenv('ANSWER_FILE')}")
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.logger.info("Using in-memory SQLite database")
    
    db.init_app(app)
    app.logger.info("SQLAlchemy initialized")
    
    with app.app_context():
        from .models import create_tables
        create_tables()
        app.logger.info("Database tables created and answer table recreated")

    from .routes import quiz_bp
    app.register_blueprint(quiz_bp)
    app.logger.info("Quiz blueprint registered")

    app.logger.info("Application initialization complete")
    return app
