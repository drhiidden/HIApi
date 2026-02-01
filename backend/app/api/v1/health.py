"""
Health Check Endpoint

Provides system health status and connectivity checks.
"""

from flask import jsonify, current_app
from sqlalchemy import text

from app.api.v1 import api_v1
from app.extensions import db


@api_v1.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint.
    
    Checks:
    - Application status
    - Database connectivity
    - pgvector extension availability
    
    Returns:
        JSON response with health status
    """
    status = 'healthy'
    errors = []
    
    # Check database connectivity
    db_status = 'disconnected'
    pgvector_enabled = False
    
    try:
        # Test database connection
        db.session.execute(text('SELECT 1'))
        db_status = 'connected'
        
        # Check pgvector extension
        result = db.session.execute(text(
            "SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname = 'vector')"
        ))
        pgvector_enabled = result.scalar()
        
        if not pgvector_enabled:
            errors.append('pgvector extension not enabled')
            status = 'degraded'
            
    except Exception as e:
        db_status = 'error'
        errors.append(f'Database connection failed: {str(e)}')
        status = 'unhealthy'
    
    # Check LLM availability (basic check)
    llm_status = {
        'openai': 'configured' if current_app.config.get('OPENAI_API_KEY') else 'not_configured',
        'claude': 'configured' if current_app.config.get('ANTHROPIC_API_KEY') else 'not_configured'
    }
    
    if llm_status['openai'] == 'not_configured':
        errors.append('OpenAI API key not configured')
        status = 'degraded'
    
    # Build response
    response = {
        'status': status,
        'version': '0.1.0',
        'database': {
            'status': db_status,
            'pgvector_enabled': pgvector_enabled
        },
        'llm': llm_status
    }
    
    if errors:
        response['errors'] = errors
    
    # Return appropriate HTTP status code
    http_status = 200 if status == 'healthy' else (503 if status == 'unhealthy' else 200)
    
    return jsonify(response), http_status
