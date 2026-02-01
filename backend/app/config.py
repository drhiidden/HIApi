"""
Flask Configuration Classes
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
basedir = Path(__file__).resolve().parent.parent
load_dotenv(basedir / '.env')


class Config:
    """Base configuration."""
    
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    FLASK_APP = 'app:create_app'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://user:password@localhost:5432/iapi_dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # pgvector Configuration
    PGVECTOR_DIMENSION = int(os.environ.get('PGVECTOR_DIMENSION', 1536))  # OpenAI default
    HNSW_M = int(os.environ.get('HNSW_M', 16))
    HNSW_EF_CONSTRUCTION = int(os.environ.get('HNSW_EF_CONSTRUCTION', 128))
    HNSW_EF_SEARCH = int(os.environ.get('HNSW_EF_SEARCH', 100))
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-4o-mini')
    OPENAI_EMBEDDING_MODEL = os.environ.get('OPENAI_EMBEDDING_MODEL', 'text-embedding-3-small')
    
    # Anthropic Claude (Fallback)
    ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
    ANTHROPIC_MODEL = os.environ.get('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022')
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = os.environ.get('RATELIMIT_STORAGE_URL')  # Redis URL (optional)
    TIER_FREE_QUERIES_PER_DAY = int(os.environ.get('TIER_FREE_QUERIES_PER_DAY', 100))
    TIER_PRO_QUERIES_PER_DAY = int(os.environ.get('TIER_PRO_QUERIES_PER_DAY', 10000))
    
    # Stripe Configuration
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
    STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
    STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')
    
    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:4321').split(',')
    
    # Monitoring
    PROMETHEUS_PORT = int(os.environ.get('PROMETHEUS_PORT', 9090))
    SENTRY_DSN = os.environ.get('SENTRY_DSN')
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = os.environ.get('LOG_FORMAT', 'text')  # json | text


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    FLASK_ENV = 'development'
    SQLALCHEMY_ECHO = True  # Log SQL queries in development


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    FLASK_ENV = 'production'
    SQLALCHEMY_ECHO = False
    
    # Override with stricter settings
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 20
    SQLALCHEMY_POOL_TIMEOUT = 30


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    FLASK_ENV = 'testing'
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost:5432/iapi_test'
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
