"""
User Model

Manages users, API keys, and tier-based access control.
"""

from datetime import datetime, timedelta
from sqlalchemy import Column, String, Integer, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

from app.models.base import BaseModel


class User(BaseModel):
    """
    User with API key and tier management.
    
    Attributes:
        email: User email (unique)
        password_hash: Hashed password (nullable for API-only users)
        api_key: Plain API key (format: iapi_xxxxx)
        api_key_hash: Hashed API key for secure storage
        tier: Subscription tier (free, pro, enterprise)
        stripe_customer_id: Stripe customer ID for billing
        stripe_subscription_id: Stripe subscription ID
        queries_today: Query counter for rate limiting
        queries_reset_at: Timestamp when counter resets
        last_query_at: Last query timestamp
    """
    __tablename__ = 'users'
    
    # Authentication
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255))  # Nullable for API-only users
    
    # API Key (plain for user display, hashed for validation)
    api_key = Column(String(64), unique=True, nullable=False, index=True)
    api_key_hash = Column(String(255), nullable=False)
    
    # Tier Management
    tier = Column(String(20), default='free', nullable=False, index=True)
    stripe_customer_id = Column(String(255))
    stripe_subscription_id = Column(String(255))
    
    # Rate Limiting (Invariante #3)
    queries_today = Column(Integer, default=0, nullable=False)
    queries_reset_at = Column(
        DateTime, 
        default=lambda: datetime.utcnow() + timedelta(days=1),
        nullable=False
    )
    
    # Last activity
    last_query_at = Column(DateTime)
    
    def __repr__(self):
        """String representation."""
        return f'<User {self.email} ({self.tier})>'
    
    @staticmethod
    def generate_api_key():
        """
        Generate secure API key.
        
        Returns:
            str: API key in format iapi_xxxxx (40 chars random)
        """
        random_part = secrets.token_urlsafe(30)  # ~40 chars base64
        return f'iapi_{random_part}'
    
    def set_password(self, password):
        """
        Hash and set user password.
        
        Args:
            password: Plain text password
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Verify password against hash.
        
        Args:
            password: Plain text password to verify
        
        Returns:
            bool: True if password matches
        """
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    def set_api_key(self, api_key=None):
        """
        Set API key (auto-generate if not provided).
        Stores plain key for user display and hashed version for validation.
        
        Args:
            api_key: Optional API key (auto-generated if None)
        """
        if api_key is None:
            api_key = self.generate_api_key()
        
        self.api_key = api_key
        self.api_key_hash = generate_password_hash(api_key)
    
    def verify_api_key(self, api_key):
        """
        Verify API key against hash.
        
        Args:
            api_key: Plain API key to verify
        
        Returns:
            bool: True if API key matches
        """
        return check_password_hash(self.api_key_hash, api_key)
    
    def can_query(self, config):
        """
        Check if user can make query based on tier limits.
        Implements Invariante #3: Tier enforcement.
        
        Args:
            config: Flask app config dict
        
        Returns:
            bool: True if user can make query
        """
        # Reset counter if day passed
        if datetime.utcnow() >= self.queries_reset_at:
            self.queries_today = 0
            self.queries_reset_at = datetime.utcnow() + timedelta(days=1)
        
        # Get tier limits from config
        limits = {
            'free': config.get('TIER_FREE_QUERIES_PER_DAY', 100),
            'pro': config.get('TIER_PRO_QUERIES_PER_DAY', 10000),
            'enterprise': float('inf')  # Unlimited
        }
        
        tier_limit = limits.get(self.tier, 0)
        return self.queries_today < tier_limit
    
    def increment_query_count(self):
        """
        Increment query counter and update last query timestamp.
        Call after successful query.
        """
        self.queries_today += 1
        self.last_query_at = datetime.utcnow()
    
    def get_tier_info(self, config):
        """
        Get tier information (current usage, limits, reset time).
        
        Args:
            config: Flask app config dict
        
        Returns:
            dict: Tier information
        """
        limits = {
            'free': config.get('TIER_FREE_QUERIES_PER_DAY', 100),
            'pro': config.get('TIER_PRO_QUERIES_PER_DAY', 10000),
            'enterprise': None  # Unlimited
        }
        
        return {
            'tier': self.tier,
            'queries_today': self.queries_today,
            'queries_limit': limits.get(self.tier),
            'queries_remaining': (
                limits.get(self.tier, 0) - self.queries_today
                if limits.get(self.tier) is not None
                else None  # Unlimited
            ),
            'reset_at': self.queries_reset_at.isoformat() if self.queries_reset_at else None
        }
