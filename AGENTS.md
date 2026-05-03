# AGENTS.md — HIApi

---

## Identidad

| Campo | Valor |
|---|---|
| Nombre | **HIApi** (Intelligent API) |
| Repo GitHub | `drhiidden/HIApi` |
| Tagline | *AI ate the web. Get the traffic back.* |
| Licencia | MIT |
| Estado | Planning phase — diseño en progreso |

---

## Problema que resuelve

Los LLMs consumen contenido de webs (docs, blogs, artículos) sin generar tráfico de retorno. Caso real: Tailwind CSS perdió -40% de tráfico y -80% de revenue cuando ChatGPT y Copilot empezaron a responder preguntas sobre Tailwind directamente.

HIApi propone una solución: una API RAG-powered que intermedie entre LLMs y el contenido web, **forzando attribution** (backlinks) como condición para servir el contenido.

---

## Arquitectura planeada

```
LLM / AI Tool
    ↓ GET /api/content?url=...
HIApi (FastAPI)
    ↓ RAG: chunking + embedding + retrieval
Contenido origen (web scraping / RSS / sitemap)
    ↓ response con attribution obligatoria
{
  "content": "...",
  "attribution": {
    "source": "original-site.com",
    "backlink": "https://...",
    "required": true   ← no se puede omitir
  }
}
```

---

## Stack planeado

| Capa | Tecnología |
|---|---|
| API | FastAPI (async) |
| RAG | LangChain / llama-index o custom |
| Embeddings | Ollama local (nomic-embed-text) |
| Vector DB | ChromaDB o pgvector |
| Scraping | BeautifulSoup + Playwright |
| Auth | API keys (simple) |

---

## Estado actual

- [ ] Diseño de API (endpoints, contrato)
- [ ] Modelo de datos (sources, attribution)
- [ ] Prototipo de scraping + RAG
- [ ] Enforcement de attribution
- [ ] Tests

**No hay código funcional todavía.** Este repo documenta el diseño y acepta PRs de quien quiera co-implementar.

---

## Reglas críticas

1. **Attribution es obligatoria** — nunca devolver contenido sin el campo `attribution.backlink`
2. **Respetar robots.txt** — el scraper debe verificar permisos antes de indexar
3. **Rate limiting** — proteger las fuentes de origin de sobrecargas
4. **No cachear indefinidamente** — TTL configurable por dominio

---

## Metodología

Desarrollado con [HCP (Human-Code-AI Protocol)](https://github.com/haletheia/human-code-ai-protocol).
