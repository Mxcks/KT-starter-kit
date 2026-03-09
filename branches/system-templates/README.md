# system-templates

**Reusable project templates for common architectures**

---

## Overview

This branch contains 6 battle-tested project templates that serve as starting points for new projects. Each template includes structure, patterns, and best practices.

## Templates

### 1. Web API Template
**Use for:** REST APIs, backend services  
**Stack:** Node.js/Express, Python/FastAPI, Go/Gin  
**Features:**
- JWT authentication
- CRUD operations
- OpenAPI/Swagger docs
- Rate limiting
- Error handling & logging

**Structure:**
```
src/
├── routes/      # API endpoints
├── models/      # Data models
├── middleware/  # Auth, validation
├── services/    # Business logic
└── utils/       # Helpers
```

---

### 2. Microservice Template
**Use for:** Distributed systems, service-oriented architecture  
**Components:**
- Service core
- Message queue (consumer/producer)
- Health checks
- Metrics/monitoring
- Service discovery

**Patterns:**
- Circuit breaker
- Retry logic
- Graceful shutdown
- Config management

---

### 3. Frontend SPA Template
**Use for:** Single-page applications  
**Stack:** React, Vue, Angular, Svelte  
**Features:**
- Routing
- State management
- API integration
- Authentication flow
- Component library
- Responsive design

**Structure:**
```
src/
├── components/  # Reusable UI
├── pages/       # Page components
├── store/       # State management
├── services/    # API clients
├── hooks/       # Custom hooks
└── styles/      # Themes
```

---

### 4. Data Pipeline Template
**Use for:** ETL/ELT, data processing  
**Components:**
- Data ingestion (batch/streaming)
- Transformation logic
- Data validation/quality
- Error handling
- Orchestration (Airflow/Prefect)
- Monitoring/alerting

**Patterns:**
- Idempotent operations
- Incremental processing
- Partitioning strategy
- Schema evolution

---

### 5. CLI Tool Template
**Use for:** Command-line applications  
**Features:**
- Subcommands (init, run, status)
- Config file support (YAML/JSON)
- Progress indicators
- Colored output
- Auto-completion
- Help text

**Structure:**
```
cli/
├── commands/    # Command implementations
├── config.py    # Config loading
├── output.py    # Formatted output
└── main.py      # Entry point
```

---

### 6. Library/Package Template
**Use for:** Reusable libraries, npm/pip packages  
**Components:**
- Public API (clean interface)
- Internal implementation
- Comprehensive tests
- API documentation
- Examples/tutorials
- Changelog

**Best Practices:**
- Semantic versioning
- Backward compatibility
- Clear deprecation policy
- Type hints/annotations
- Performance benchmarks

---

## Usage

### Using a Template

1. **Choose template:** Review templates above
2. **Copy structure:** Use as starting point for new project
3. **Customize:** Adapt to your specific needs
4. **Document:** Create KT branch for new project

### Creating Your Own Template

```bash
# Add custom template
python kt.py add doc "My Custom Template" --branch system-templates \
  --reasoning "Description and use case" \
  --tags template,custom,my-domain
```

### Example: Starting with Web API Template

```bash
# 1. Create new project branch
python kt.py init my-api "New REST API project"

# 2. Add decision to use template
python kt.py add decision "Use Web API template" --branch my-api \
  --reasoning "Standard REST API with auth and CRUD" \
  --tags architecture,template

# 3. Implement following template structure
# ... create src/routes/, src/models/, etc.

# 4. Document customizations
python kt.py add doc "Added custom authentication flow" --branch my-api
```

---

## Template Selection Guide

**Need a backend API?**
→ Web API Template (REST endpoints, CRUD)

**Building distributed system?**
→ Microservice Template (message queues, health checks)

**Need a web frontend?**
→ Frontend SPA Template (routing, state management)

**Processing data?**
→ Data Pipeline Template (ETL/ELT, orchestration)

**Creating a command-line tool?**
→ CLI Tool Template (subcommands, config)

**Building a library?**
→ Library/Package Template (clean API, documentation)

---

## Extending Templates

Templates are starting points, not rigid specifications. Common extensions:

**Web API:**
- Add WebSocket support
- Implement GraphQL
- Add caching layer
- Setup CI/CD

**Microservice:**
- Add tracing (OpenTelemetry)
- Implement CQRS pattern
- Add event sourcing
- Setup service mesh

**Frontend SPA:**
- Add SSR (Server-Side Rendering)
- Implement PWA features
- Add internationalization
- Setup micro-frontends

**Data Pipeline:**
- Add real-time streaming
- Implement data versioning
- Add ML model serving
- Setup data catalog

---

## Contributing

Have a template to share?

```bash
python kt.py add doc "Your Template Name" --branch system-templates \
  --reasoning "Template description and use case" \
  --tags template,your-domain
```

Include:
- Template name and purpose
- Recommended stack/technologies
- Key features and components
- Folder structure
- Patterns and best practices
- When to use it

---

**Status:** 6 production-ready templates  
**Last updated:** 2026-03-09
