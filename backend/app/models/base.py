"""
Base SQLAlchemy Model

Provides common fields and methods for all models.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import declared_attr

from app.extensions import db


class BaseModel(db.Model):
    """
    Base model with common fields.
    
    All models inherit from this to get:
    - id (primary key)
    - created_at (timestamp)
    - updated_at (auto-updating timestamp)
    """
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow, 
        nullable=False
    )
    
    @declared_attr
    def __tablename__(cls):
        """
        Auto-generate table name from class name.
        Example: ContentChunk -> content_chunk
        """
        import re
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
    
    def to_dict(self):
        """
        Convert model to dictionary.
        
        Returns:
            dict: Model data as dictionary
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def __repr__(self):
        """String representation of model."""
        return f'<{self.__class__.__name__} {self.id}>'
