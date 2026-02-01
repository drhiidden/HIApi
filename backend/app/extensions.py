"""
Flask Extensions Configuration

Centralized extension initialization for Flask app.
Extensions are created here and initialized in the app factory.
"""

from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """SQLAlchemy declarative base class."""
    pass


# Initialize extensions (without app binding)
cors = CORS()
db = SQLAlchemy(model_class=Base)


def get_api_key_or_ip():
    """
    Extract API key from Authorization header for rate limiting.
    Falls back to IP address if no API key present.
    
    Returns:
        str: API key or IP address
    """
    from flask import request
    
    # Try Authorization header
    auth = request.headers.get('Authorization', '')
    if auth.startswith('Bearer '):
        api_key = auth[7:].strip()
        if api_key:
            return api_key
    
    # Fallback to IP address
    return get_remote_address()


# Flask-Limiter with custom key function
limiter = Limiter(
    key_func=get_api_key_or_ip,
    default_limits=[],  # No global limits, define per-route
    storage_uri="memory://",  # In-memory for MVP, Redis for production
    strategy="fixed-window"
)


def init_extensions(app):
    """
    Initialize all Flask extensions with app instance.
    
    Args:
        app: Flask application instance
    """
    # CORS
    cors.init_app(
        app,
        origins=app.config.get('CORS_ORIGINS', '*'),
        allow_headers=['Content-Type', 'Authorization'],
        methods=['GET', 'POST', 'OPTIONS']
    )
    
    # SQLAlchemy
    db.init_app(app)
    
    # Flask-Limiter
    limiter.init_app(app)
    
    # Create tables if they don't exist (for development)
    with app.app_context():
        # Import models to register them with SQLAlchemy
        from app.models import content, user  # noqa: F401
        
        # Only create tables in development/testing
        if app.config.get('ENV') in ['development', 'testing']:
            db.create_all()
