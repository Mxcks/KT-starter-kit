#!/usr/bin/env python3
"""
Create system-templates branch with reusable project templates
"""

import json
from pathlib import Path
from datetime import datetime

# Create branch structure
branch_dir = Path("branches/system-templates")
knowledge_dir = branch_dir / "knowledge"
knowledge_dir.mkdir(parents=True, exist_ok=True)

# Template definitions
templates = [
    {
        "id": "0",
        "type": "init",
        "message": "Project Templates - Reusable starting points",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "tags": ["templates", "system", "init"]
    },
    {
        "id": "1",
        "type": "documentation",
        "message": "Web API Template",
        "reasoning": "Standard REST API structure with authentication, CRUD endpoints, and documentation",
        "tags": ["template", "api", "backend"],
        "content": {
            "template_name": "web-api",
            "stack": ["Node.js/Express", "Python/FastAPI", "Go/Gin"],
            "features": [
                "JWT authentication",
                "CRUD operations",
                "OpenAPI/Swagger docs",
                "Rate limiting",
                "Error handling",
                "Logging"
            ],
            "structure": {
                "src/": {
                    "routes/": "API endpoints",
                    "models/": "Data models",
                    "middleware/": "Auth, validation, etc.",
                    "services/": "Business logic",
                    "utils/": "Helper functions"
                },
                "tests/": "Unit and integration tests",
                "docs/": "API documentation",
                "config/": "Configuration files"
            }
        }
    },
    {
        "id": "2",
        "type": "documentation",
        "message": "Microservice Template",
        "reasoning": "Independent service with message queue, health checks, and observability",
        "tags": ["template", "microservice", "backend"],
        "content": {
            "template_name": "microservice",
            "components": [
                "Service core",
                "Message queue consumer/producer",
                "Health check endpoints",
                "Metrics/monitoring",
                "Service discovery"
            ],
            "patterns": [
                "Circuit breaker",
                "Retry logic",
                "Graceful shutdown",
                "Config management"
            ]
        }
    },
    {
        "id": "3",
        "type": "documentation",
        "message": "Frontend SPA Template",
        "reasoning": "Single-page application with routing, state management, and component library",
        "tags": ["template", "frontend", "spa"],
        "content": {
            "template_name": "frontend-spa",
            "stack": ["React", "Vue", "Angular", "Svelte"],
            "features": [
                "Routing",
                "State management (Redux/Vuex/etc.)",
                "API integration",
                "Authentication flow",
                "Component library",
                "Responsive design"
            ],
            "structure": {
                "src/": {
                    "components/": "Reusable UI components",
                    "pages/": "Page-level components",
                    "store/": "State management",
                    "services/": "API clients",
                    "hooks/": "Custom hooks/composables",
                    "styles/": "Global styles/themes"
                },
                "public/": "Static assets"
            }
        }
    },
    {
        "id": "4",
        "type": "documentation",
        "message": "Data Pipeline Template",
        "reasoning": "ETL/ELT pipeline with orchestration, monitoring, and data quality checks",
        "tags": ["template", "data", "pipeline"],
        "content": {
            "template_name": "data-pipeline",
            "components": [
                "Data ingestion (batch/streaming)",
                "Transformation logic",
                "Data validation/quality",
                "Error handling/retry",
                "Orchestration (Airflow/Prefect)",
                "Monitoring/alerting"
            ],
            "patterns": [
                "Idempotent operations",
                "Incremental processing",
                "Partitioning strategy",
                "Schema evolution"
            ]
        }
    },
    {
        "id": "5",
        "type": "documentation",
        "message": "CLI Tool Template",
        "reasoning": "Command-line tool with subcommands, config, and user-friendly output",
        "tags": ["template", "cli", "tool"],
        "content": {
            "template_name": "cli-tool",
            "features": [
                "Subcommands (init, run, status, etc.)",
                "Config file support (YAML/JSON)",
                "Progress indicators",
                "Colored output",
                "Auto-completion",
                "Help text/documentation"
            ],
            "structure": {
                "cli/": {
                    "commands/": "Command implementations",
                    "config.py": "Config loading/saving",
                    "output.py": "Formatted output helpers",
                    "main.py": "Entry point"
                }
            }
        }
    },
    {
        "id": "6",
        "type": "documentation",
        "message": "Library/Package Template",
        "reasoning": "Reusable library with clean API, documentation, and testing",
        "tags": ["template", "library", "package"],
        "content": {
            "template_name": "library-package",
            "components": [
                "Public API (clean interface)",
                "Internal implementation",
                "Comprehensive tests",
                "API documentation",
                "Examples/tutorials",
                "Changelog"
            ],
            "best_practices": [
                "Semantic versioning",
                "Backward compatibility",
                "Clear deprecation policy",
                "Type hints/annotations",
                "Performance benchmarks"
            ]
        }
    }
]

# Write nodes to tree.jsonl
tree_file = knowledge_dir / "tree.jsonl"
with open(tree_file, 'w', encoding='utf-8') as f:
    for node in templates:
        f.write(json.dumps(node) + '\n')

# Create README
readme = branch_dir / "README.md"
readme_content = """# system-templates

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
python kt.py add doc "My Custom Template" --branch system-templates \\
  --reasoning "Description and use case" \\
  --tags template,custom,my-domain
```

### Example: Starting with Web API Template

```bash
# 1. Create new project branch
python kt.py init my-api "New REST API project"

# 2. Add decision to use template
python kt.py add decision "Use Web API template" --branch my-api \\
  --reasoning "Standard REST API with auth and CRUD" \\
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
python kt.py add doc "Your Template Name" --branch system-templates \\
  --reasoning "Template description and use case" \\
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
"""

with open(readme, 'w', encoding='utf-8') as f:
    f.write(readme_content)

print("[OK] Created system-templates branch")
print(f"     Location: {branch_dir}")
print(f"     Templates: {len(templates)}")
print(f"     README: {readme}")
