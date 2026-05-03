![HIApi banner](docs/banner.png)

# HIApi — Intelligent API for LLMs with Attribution

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: planning](https://img.shields.io/badge/Status-planning-orange.svg)](#roadmap)
[![FastAPI](https://img.shields.io/badge/FastAPI-async-green.svg)](https://fastapi.tiangolo.com)
[![RAG-powered](https://img.shields.io/badge/RAG-powered-purple.svg)](#architecture)
![visitors](https://komarev.com/ghpvc/?username=drhiidden&repo=HIApi&color=00ff88&style=flat-square)

**AI ate the web. Get the traffic back.**

> An API layer that lets LLMs access your content — but enforces attribution on every response.

---

## The Problem

LLMs consume documentation, blogs and tutorials without sending traffic back to the sources.

**Real case — Tailwind CSS (2023–2025)**:
- Traffic to docs: **-40%**
- Revenue: **-80%**
- Layoffs: **75%** of the team (3 of 4 engineers gone)
- Root cause: ChatGPT and Copilot answer Tailwind questions directly — no backlink, no visit

This is not a Tailwind-specific problem. It's structural. And blocking bots only delays it.

---

## The Solution

HIApi sits between LLMs and your content. It serves the content — but **attribution is non-negotiable**.

```
LLM / AI Tool
    │
    ▼
GET /api/content?url=your-site.com/article
    │
    ▼
HIApi (RAG pipeline)
    │  → fetches, chunks, embeds your content
    │  → retrieves the most relevant fragments
    │
    ▼
{
  "content": "...",
  "attribution": {
    "source": "your-site.com",
    "title": "Article title",
    "url": "https://your-site.com/article",
    "author": "Your Name",
    "required": true          ← enforced, not optional
  }
}
```

The LLM gets the answer. Your site gets the backlink. Every time.

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│                   HIApi                         │
│                                                 │
│  ┌──────────────┐    ┌──────────────────────┐   │
│  │  Ingestion   │    │   Query Engine       │   │
│  │              │    │                      │   │
│  │ Web crawler  │    │  /api/content        │   │
│  │ RSS/Sitemap  │───▶│  RAG retrieval       │   │
│  │ Webhook push │    │  Attribution inject  │   │
│  │              │    │  Rate limiting       │   │
│  └──────────────┘    └──────────────────────┘   │
│         │                      │                │
│         ▼                      ▼                │
│  ┌──────────────────────────────────────┐       │
│  │  Vector Store (pgvector)             │       │
│  │  Embeddings + metadata + attribution │       │
│  └──────────────────────────────────────┘       │
└─────────────────────────────────────────────────┘
```

**Planned stack**:

| Layer | Technology |
|---|---|
| API | FastAPI (Python) · async |
| RAG | Custom retrieval + reranking |
| Embeddings | Ollama local (`nomic-embed-text`) or OpenAI |
| Vector store | PostgreSQL + pgvector |
| Scraping | BeautifulSoup + Playwright |
| Auth | API keys per source domain |
| Frontend | Astro (dashboard + source registration) |

---

## API Design (proposed)

### Register a source

```http
POST /api/sources
Authorization: Bearer <api_key>

{
  "domain": "your-site.com",
  "sitemap": "https://your-site.com/sitemap.xml",
  "refresh_interval_minutes": 30
}
```

### Query content

```http
GET /api/content?url=your-site.com&q=how+to+use+tailwind+flexbox&top_k=3
Authorization: Bearer <api_key>

→ 200 OK
{
  "results": [
    {
      "content": "To use flexbox in Tailwind...",
      "attribution": {
        "source": "your-site.com",
        "title": "Flexbox Guide",
        "url": "https://your-site.com/flexbox",
        "required": true
      },
      "relevance_score": 0.92
    }
  ]
}
```

### Attribution is always present

`attribution.required: true` is **not a suggestion**. The API contract requires downstream LLM integrations to include the source link in their responses. No attribution field = request rejected.

---

## Core Rules (Invariants)

These must always be true, regardless of implementation:

1. **Attribution is mandatory** — 100% of responses include `source`, `url`, and `author`
2. **Fresh content** — indexed corpus updated within 5 minutes of publication
3. **Rate limiting enforced** — free tier: 100 queries/day; pro: 10K/day
4. **API is stable** — v1 changes are additive only; breaking changes require a new version
5. **No secrets in logs** — API keys, tokens and PII are never logged

---

## Roadmap

### v0.1 — Core pipeline (current focus)
- [ ] Source registration endpoint
- [ ] Web crawler + sitemap indexer
- [ ] Chunking + embedding pipeline (Ollama)
- [ ] Basic RAG retrieval
- [ ] Attribution injection in every response
- [ ] API key auth

### v0.2 — Quality
- [ ] Reranking (ColBERT or cross-encoder)
- [ ] Webhook push indexing (real-time updates)
- [ ] Relevance score in responses
- [ ] Basic HTML dashboard

### v0.3 — Distribution
- [ ] Attribution enforcement middleware (verify downstream compliance)
- [ ] Usage analytics per source domain
- [ ] Freemium billing (Stripe)
- [ ] Public SDK (Python + JS)

### v1.0 — Stable API
- [ ] Stable API contract
- [ ] Multi-tenant source isolation
- [ ] SLA guarantees

---

## Why this matters beyond Tailwind

The EU AI Act (2024) mandates **transparency in AI-generated content sources**. HIApi is infrastructure for that: a verifiable chain from LLM response to original source.

Publishers, documentation sites, and content creators need a way to participate in the AI economy — not just be consumed by it.

---

## Status

**Planning phase.** The architecture is defined. The problem is real. No production code yet.

If you're interested in this problem — attribution economics, RAG infrastructure, or content API design — **PRs, issues and discussions are open**.

---

## Contributing

This project is in its earliest stage. The best contributions right now are:

- 💬 **Discuss**: open an issue about the problem space
- 🏗️ **Architecture feedback**: does the proposed design make sense?
- 🔧 **Prototype a module**: crawler, chunker, or the attribution enforcement logic
- 📖 **Point to prior art**: similar projects, papers, or relevant standards

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

## Methodology

Developed with [HCP (Human-Code-AI Protocol)](https://github.com/haletheia/human-code-ai-protocol) — a git-native protocol for Context Engineering.
