"""
API Error Handlers

Centralized error handling for Flask application.
"""

from flask import jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):
    """
    Register error handlers with Flask app.
    
    Args:
        app: Flask application instance
    """
    
    @app.errorhandler(400)
    def bad_request(e):
        """Handle 400 Bad Request."""
        return jsonify({
            'error': 'bad_request',
            'message': str(e.description) if hasattr(e, 'description') else 'Bad request',
            'code': 400
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(e):
        """Handle 401 Unauthorized."""
        return jsonify({
            'error': 'unauthorized',
            'message': 'Invalid or missing API key',
            'code': 401
        }), 401
    
    @app.errorhandler(404)
    def not_found(e):
        """Handle 404 Not Found."""
        return jsonify({
            'error': 'not_found',
            'message': 'Resource not found',
            'code': 404
        }), 404
    
    @app.errorhandler(429)
    def rate_limit_exceeded(e):
        """Handle 429 Too Many Requests."""
        return jsonify({
            'error': 'rate_limit_exceeded',
            'message': str(e.description) if hasattr(e, 'description') else 'Rate limit exceeded',
            'code': 429
        }), 429
    
    @app.errorhandler(500)
    def internal_error(e):
        """Handle 500 Internal Server Error."""
        # Log error for debugging
        app.logger.error(f'Internal error: {str(e)}')
        
        return jsonify({
            'error': 'internal_error',
            'message': 'An unexpected error occurred',
            'code': 500
        }), 500
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """Handle generic HTTP exceptions."""
        return jsonify({
            'error': e.name.lower().replace(' ', '_'),
            'message': e.description,
            'code': e.code
        }), e.code
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handle uncaught exceptions."""
        # Log error for debugging
        app.logger.exception('Unhandled exception')
        
        return jsonify({
            'error': 'internal_error',
            'message': 'An unexpected error occurred',
            'code': 500
        }), 500
