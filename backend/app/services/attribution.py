"""
Attribution Service

Implements Invariante #1: Attribution Obligatoria
All API responses MUST include attribution metadata.
"""

from flask import request, jsonify
from datetime import datetime
import hashlib
import json


def generate_signature(data: dict) -> str:
    """
    Generate verification signature for response data.
    
    Args:
        data: Response data to sign
    
    Returns:
        str: SHA-256 signature
    """
    content = json.dumps(data, sort_keys=True)
    return hashlib.sha256(content.encode()).hexdigest()


def add_attribution(response):
    """
    Add attribution metadata to JSON responses.
    Applied globally via @after_request decorator.
    
    Implements Invariante #1: Attribution Obligatoria
    
    Args:
        response: Flask response object
    
    Returns:
        response: Modified response with attribution
    """
    # Only process JSON responses from /api/v1/query
    if (response.content_type == 'application/json' and 
        request.path.startswith('/api/v1/query') and 
        response.status_code == 200):
        
        try:
            data = response.get_json()
            
            # Add attribution metadata (Invariante #1)
            data['attribution'] = {
                'powered_by': 'IApi',
                'source_url': request.host_url.rstrip('/'),
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'signature': generate_signature({
                    'answer': data.get('answer', ''),
                    'sources': data.get('sources', [])
                })
            }
            
            # Update response data
            response.set_data(json.dumps(data))
            
        except Exception as e:
            # Log error but don't break response
            # (attribution failure should not break API)
            print(f'Attribution error: {str(e)}')
    
    return response
