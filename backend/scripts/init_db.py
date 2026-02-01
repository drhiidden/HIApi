"""
Initialize Database Script

Creates all tables and runs migrations.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db


def init_database():
    """Initialize database with all tables."""
    app = create_app()
    
    with app.app_context():
        print('🔧 Creating database tables...')
        
        # Create all tables
        db.create_all()
        
        print('✅ Database initialized successfully!')
        print()
        print('📊 Tables created:')
        print('   - content_chunks (with HNSW index)')
        print('   - users')
        print('   - query_logs')
        print()
        print('💡 Next steps:')
        print('   1. Run: python scripts/create_test_user.py')
        print('   2. Start server: flask run')


if __name__ == '__main__':
    init_database()
