"""
IApi Backend Application

Flask application factory for IApi MVP v0.1.
Stack: Flask 3.1 + LlamaIndex + pgvector + PostgreSQL
"""

from flask import Flask

from app.config import Config


def create_app(config_class=Config):
    """
    Application factory pattern.
    
    Args:
        config_class: Configuration class to use
    
    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    from app.extensions import init_extensions
    init_extensions(app)
    
    # Register blueprints
    from app.api.v1 import api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')
    
    # Register error handlers
    from app.api import errors
    errors.register_error_handlers(app)
    
    # Register attribution decorator (Invariante #1)
    from app.services.attribution import add_attribution
    app.after_request(add_attribution)
    
    return app
