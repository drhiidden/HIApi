"""
Custom Flask Decorators

Provides authentication and authorization decorators.
"""

from functools import wraps
from flask import request, jsonify, g

from app.models.user import User
from app.extensions import db


def require_api_key(f):
    """
    Decorator to require valid API key.
    
    Usage:
        @api_v1.route('/query', methods=['POST'])
        @require_api_key
        def query():
            user = g.current_user
            ...
    
    Returns:
        401 if API key missing or invalid
        403 if API key valid but user cannot perform action
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Extract API key from Authorization header
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return jsonify({
                'error': 'unauthorized',
                'message': 'Missing or invalid Authorization header. Use: Bearer <api_key>'
            }), 401
        
        api_key = auth[7:].strip()
        
        if not api_key:
            return jsonify({
                'error': 'unauthorized',
                'message': 'API key cannot be empty'
            }), 401
        
        # Find user by API key (plain, not hashed - for faster lookup)
        user = db.session.query(User).filter_by(api_key=api_key).first()
        
        if not user:
            return jsonify({
                'error': 'unauthorized',
                'message': 'Invalid API key'
            }), 401
        
        # Store user in Flask g object (request context)
        g.current_user = user
        
        return f(*args, **kwargs)
    
    return decorated_function


def get_current_user():
    """
    Get current authenticated user from request context.
    
    Returns:
        User: Current user or None if not authenticated
    """
    return g.get('current_user', None)


def require_tier(*allowed_tiers):
    """
    Decorator to require specific tier(s).
    Must be used after @require_api_key.
    
    Args:
        *allowed_tiers: Tier names (e.g., 'pro', 'enterprise')
    
    Usage:
        @api_v1.route('/premium', methods=['POST'])
        @require_api_key
        @require_tier('pro', 'enterprise')
        def premium_endpoint():
            ...
    
    Returns:
        403 if user tier not in allowed_tiers
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            
            if not user:
                return jsonify({
                    'error': 'unauthorized',
                    'message': 'Authentication required'
                }), 401
            
            if user.tier not in allowed_tiers:
                return jsonify({
                    'error': 'forbidden',
                    'message': f'This endpoint requires {" or ".join(allowed_tiers)} tier',
                    'current_tier': user.tier
                }), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator
