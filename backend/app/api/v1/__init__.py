"""
API v1 Blueprint

REST API endpoints for IApi v0.1.
"""

from flask import Blueprint

# Create API v1 blueprint
api_v1 = Blueprint('api_v1', __name__)

# Import routes to register them
from app.api.v1 import health  # noqa: F401, E402
# from app.api.v1 import query  # TODO: Implement in Week 2
