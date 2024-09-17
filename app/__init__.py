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
    
    # Check if any of the required database environment variables are missing
    required_db_vars = ["DB_USERNAME", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]
    missing_vars = [var for var in required_db_vars if not os.getenv(var)]
    
    if missing_vars:
        app.logger.warning(f"Missing database environment variables: {', '.join(missing_vars)}")
        app.logger.info("Using in-memory SQLite database due to missing database configuration")

    # Check if all required environment variables for database connection are set
    if os.getenv("DB_USERNAME") and os.getenv("DB_PASSWORD") and os.getenv("DB_HOST") and os.getenv("DB_PORT") and os.getenv("DB_NAME"):
        db_url = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url
        app.logger.info(f"Using database URL: postgresql://*******@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}")
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
        app.logger.info("Database tables created")

    from .routes import quiz_bp
    app.register_blueprint(quiz_bp)
    app.logger.info("Quiz blueprint registered")

    app.logger.info("Application initialization complete")
    return app
