"""
IApi Backend - Flask Application Factory
"""
from flask import Flask
from flask_cors import CORS

from app.config import Config


def create_app(config_class=Config):
    """
    Flask application factory.
    
    Args:
        config_class: Configuration class (default: Config from environment)
    
    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints (TODO: uncomment when implemented)
    # from app.api.v1 import api_v1
    # app.register_blueprint(api_v1, url_prefix='/api/v1')
    
    # Register error handlers (TODO: implement)
    # from app.api import errors
    # app.register_error_handler(404, errors.not_found)
    # app.register_error_handler(500, errors.internal_error)
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'version': '0.1.0'}, 200
    
    return app
