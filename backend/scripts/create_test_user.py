"""
Create Test User Script

Creates a test user for development with API key.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models.user import User


def create_test_user(email='test@iapi.dev', tier='free'):
    """
    Create a test user with API key.
    
    Args:
        email: User email
        tier: User tier (free, pro, enterprise)
    """
    app = create_app()
    
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f'❌ User {email} already exists')
            print(f'📧 Email: {existing_user.email}')
            print(f'🔑 API Key: {existing_user.api_key}')
            print(f'🎫 Tier: {existing_user.tier}')
            return
        
        # Create new user
        user = User(email=email, tier=tier)
        user.set_api_key()  # Auto-generate API key
        
        db.session.add(user)
        db.session.commit()
        
        print('✅ Test user created successfully!')
        print(f'📧 Email: {user.email}')
        print(f'🔑 API Key: {user.api_key}')
        print(f'🎫 Tier: {user.tier}')
        print(f'📊 Queries Limit: {100 if tier == "free" else (10000 if tier == "pro" else "Unlimited")}')
        print()
        print('💡 Test with:')
        print(f'   curl -H "Authorization: Bearer {user.api_key}" http://localhost:5000/api/v1/health')


if __name__ == '__main__':
    tier = sys.argv[1] if len(sys.argv) > 1 else 'free'
    email = sys.argv[2] if len(sys.argv) > 2 else 'test@iapi.dev'
    
    create_test_user(email=email, tier=tier)
