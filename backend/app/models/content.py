"""
Content Model

Stores content chunks with vector embeddings for RAG.
Uses pgvector extension for vector similarity search.
"""

from sqlalchemy import Column, String, Text, JSON, Index, text
from pgvector.sqlalchemy import Vector

from app.models.base import BaseModel
from app.extensions import db


class ContentChunk(BaseModel):
    """
    Content chunk with vector embedding.
    
    Attributes:
        content: Full text content of the chunk
        title: Title/heading of the content
        url: Source URL (public IApi URL)
        embedding: Vector embedding (1536 dimensions for text-embedding-3-small)
        metadata: Additional metadata (author, tags, etc.) as JSON
    """
    __tablename__ = 'content_chunks'
    
    # Content fields
    content = Column(Text, nullable=False)
    title = Column(String(500), nullable=False)
    url = Column(String(1000), nullable=False, index=True)
    
    # Vector embedding (1536 dimensions for OpenAI text-embedding-3-small)
    embedding = Column(Vector(1536), nullable=False)
    
    # Metadata JSON
    metadata = Column(JSON, default=dict)
    
    def __repr__(self):
        """String representation."""
        return f'<ContentChunk {self.id}: {self.title[:50]}>'
    
    @classmethod
    def similarity_search(cls, query_embedding, limit=5, ef_search=100):
        """
        Perform vector similarity search using HNSW index.
        
        Args:
            query_embedding: Query vector (1536 dimensions)
            limit: Number of results to return (default 5)
            ef_search: HNSW search parameter (higher = better recall, slower)
                      Default: 100 (validated in ADR-007)
        
        Returns:
            List of tuples: [(ContentChunk, distance), ...]
            Distance is cosine distance (lower = more similar)
        """
        # Set ef_search parameter for this query
        db.session.execute(text(f'SET hnsw.ef_search = {ef_search}'))
        
        # Vector similarity search using <=> operator (cosine distance)
        results = db.session.query(
            cls,
            cls.embedding.cosine_distance(query_embedding).label('distance')
        ).order_by('distance').limit(limit).all()
        
        return results
    
    @classmethod
    def similarity_search_with_threshold(cls, query_embedding, threshold=0.5, limit=10, ef_search=100):
        """
        Similarity search with distance threshold.
        
        Args:
            query_embedding: Query vector (1536 dimensions)
            threshold: Maximum distance threshold (0.0 = identical, 1.0 = opposite)
            limit: Maximum results to return
            ef_search: HNSW search parameter
        
        Returns:
            List of tuples: [(ContentChunk, distance), ...]
        """
        # Set ef_search
        db.session.execute(text(f'SET hnsw.ef_search = {ef_search}'))
        
        # Search with threshold filter
        results = db.session.query(
            cls,
            cls.embedding.cosine_distance(query_embedding).label('distance')
        ).filter(
            cls.embedding.cosine_distance(query_embedding) < threshold
        ).order_by('distance').limit(limit).all()
        
        return results


# HNSW Index (created via Alembic migration)
# CREATE INDEX content_chunks_embedding_idx ON content_chunks
# USING hnsw (embedding vector_cosine_ops)
# WITH (m = 16, ef_construction = 128);

# Note: Index creation is handled in Alembic migration to ensure proper setup
# Parameters validated in ADR-007:
# - m = 16 (connections per layer)
# - ef_construction = 128 (build quality)
# - ef_search = 100 (runtime search quality, adjustable)
