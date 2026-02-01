# IApi Backend - Flask + LlamaIndex + pgvector

Backend RAG API con Flask, LlamaIndex y PostgreSQL pgvector.

## Stack Técnico

- **Framework**: Flask 3.1.2 (WSGI)
- **RAG**: LlamaIndex 0.12+ (NO LangChain)
- **Database**: PostgreSQL 16 + pgvector 0.3.6 (HNSW indexing)
- **LLMs**: OpenAI GPT-4o-mini (primary) + Anthropic Claude (fallback)
- **Rate Limiting**: Flask-Limiter
- **Billing**: Stripe (freemium tiers)
- **Observability**: Prometheus metrics

## Quick Start

### 1. Prerequisites

- Python 3.11+
- PostgreSQL 16 con extensión pgvector instalada
- OpenAI API key
- (Opcional) Redis para rate limiting distribuido

### 2. Instalación

```bash
# Crear entorno virtual
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -e .

# Instalar dependencias de desarrollo
pip install -e ".[dev]"
```

### 3. Configuración

```bash
# Copiar .env.example
cp .env.example .env

# Editar .env con tus credenciales
# - DATABASE_URL: PostgreSQL connection string
# - OPENAI_API_KEY: OpenAI API key
# - SECRET_KEY: Flask secret (generar con: python -c "import secrets; print(secrets.token_hex(32))")
```

### 4. Setup Base de Datos

```bash
# Crear extensión pgvector en PostgreSQL
psql $DATABASE_URL -c "CREATE EXTENSION IF NOT EXISTS vector;"

# Ejecutar migraciones (TODO: setup Alembic)
# flask db upgrade
```

### 5. Ejecutar Desarrollo

```bash
# Modo desarrollo (Flask dev server)
flask run --debug

# O con gunicorn (producción)
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

API disponible en: http://localhost:5000

## Estructura del Proyecto

```
backend/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration classes
│   ├── api/                 # API endpoints (Blueprints)
│   │   ├── __init__.py
│   │   ├── v1/              # API v1 routes
│   │   │   ├── query.py     # POST /api/v1/query
│   │   │   └── health.py    # GET /api/v1/health
│   │   └── errors.py        # Error handlers
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── content.py       # Content chunks con pgvector
│   │   └── user.py          # User + API keys
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── rag_service.py   # LlamaIndex RAG pipeline
│   │   ├── attribution.py   # Attribution decorator
│   │   └── billing.py       # Stripe + tier enforcement
│   └── utils/               # Helpers
│       ├── __init__.py
│       └── embeddings.py    # OpenAI embeddings utils
├── tests/                   # pytest tests
│   ├── test_api.py
│   ├── test_rag.py
│   └── test_attribution.py
├── migrations/              # Alembic migrations (TODO)
├── pyproject.toml           # Dependencies & config
├── .env.example             # Environment variables template
└── README.md                # This file
```

## API Endpoints

### POST /api/v1/query

RAG query endpoint.

**Request**:
```json
{
  "query": "¿Cómo funciona el RAG?",
  "api_key": "iapi_...your-key..."
}
```

**Response**:
```json
{
  "answer": "El RAG (Retrieval-Augmented Generation) es...",
  "sources": [
    {
      "url": "https://iapi.example.com/docs/rag-intro",
      "title": "Introducción a RAG",
      "relevance": 0.95
    }
  ],
  "attribution": {
    "powered_by": "IApi",
    "source_url": "https://iapi.example.com",
    "timestamp": "2026-02-01T20:00:00Z"
  }
}
```

### GET /api/v1/health

Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "database": "connected",
  "pgvector": "enabled"
}
```

## Testing

```bash
# Ejecutar todos los tests
pytest

# Con coverage
pytest --cov=app --cov-report=html

# Solo tests específicos
pytest tests/test_api.py -v
```

## Development

### Code Quality

```bash
# Formatear código
black app/ tests/

# Linter
ruff check app/ tests/

# Type checking
mypy app/
```

### HNSW Index Tuning (pgvector)

Defaults validados (ver ADR-003):
- `m = 16` (conexiones por layer)
- `ef_construction = 128` (calidad build)
- `ef_search = 100` (calidad query)

Para ajustar performance/recall tradeoff, modificar en `.env`:
```bash
HNSW_M=16              # Higher = mejor recall, más RAM
HNSW_EF_CONSTRUCTION=128  # Higher = mejor index quality, más lento build
HNSW_EF_SEARCH=100     # Higher = mejor recall, más latencia query
```

## Deployment (Render)

### Backend + PostgreSQL

1. **PostgreSQL**: Render PostgreSQL Pro ($20/mes)
   - Includes SSD (required for HNSW performance)
   - pgvector extension auto-installed

2. **Web Service**: Render Web Service
   - Build Command: `pip install -e .`
   - Start Command: `gunicorn -w 4 -b 0.0.0.0:$PORT "app:create_app()"`

### Environment Variables (Render)

Configurar en Render Dashboard:
- `DATABASE_URL`: Auto-configured por Render PostgreSQL
- `OPENAI_API_KEY`: OpenAI key
- `SECRET_KEY`: Generate secure key
- `FLASK_ENV`: production
- Ver `.env.example` para lista completa

## Referencias

- [ADR-003](../.procontext/planning/adrs/ADR-003-backend-stack-pivot.md): Backend Stack Decision
- [Flask + pgvector Patterns](../.procontext/snapshots/research/flask-pgvector-stack-reference.md): SQLAlchemy + pgvector examples
- [LlamaIndex Docs](https://docs.llamaindex.ai/)
- [pgvector GitHub](https://github.com/pgvector/pgvector)

## Licencia

MIT
