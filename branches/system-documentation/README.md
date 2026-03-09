# Fractal Documentation System

**AI-optimized hierarchical documentation for Knowledge Tree**

---

## Overview

The Fractal Documentation System provides a 3-layer hierarchical approach to documenting projects, enabling token-efficient AI context loading.

## The Three Layers

### 🎯 Strategic Layer (Macro)
- **What:** High-level architecture, major decisions, branch purpose
- **Size:** 800-1,500 tokens
- **When:** First pass - understanding if this tree is relevant
- **Contains:** README-level information, architectural decisions, macro patterns

### ⚙️ Tactical Layer (Mid)
- **What:** Implementation approaches, module organization, component patterns
- **Size:** 2,000-5,000 tokens
- **When:** Second pass - planning changes or understanding structure
- **Contains:** How systems are built, module relationships, technical strategies

### 🔧 Implementation Layer (Micro)
- **What:** Specific code, files, utilities, edge cases
- **Size:** 10,000-25,000 tokens
- **When:** Deep dive - coding, debugging, or detailed analysis
- **Contains:** Code snippets, specific file paths, detailed implementations

---

## Token Efficiency

**Comparison:**

| Approach | Tokens | Savings |
|----------|--------|---------|
| Full tree | 25,000 | 0% |
| Strategic only | 800 | **97%** |
| Strategic + Tactical | 4,000 | **84%** |
| Strategic + Tactical + Selective Implementation | 7,000 | **72%** |

**Impact:**
- Scan **30+ trees** in same token budget as 1 full tree
- AI can search entire codebase at strategic level
- Progressive detail loading - only pay for what you need

---

## Tools Included

### 1. kt-hierarchical-summarizer.py
Generates 3-layer markdown summaries from KT nodes.

**Usage:**
```bash
python tools/kt-hierarchical-summarizer.py --branch my-branch
```

**Output:**
- `strategic.md` - High-level summary
- `tactical.md` - Mid-level summary
- `implementation.md` - Detailed summary
- `index.json` - Metadata

### 2. iss-hierarchical-indexer.py
Updates ISS indexes for fast discovery.

**Usage:**
```bash
python tools/iss-hierarchical-indexer.py
```

**Creates:**
- `hierarchical-summaries.json` - All summaries
- `by-layer.json` - Grouped by layer
- `quick-access.json` - Fast lookups
- `stats.json` - Statistics

### 3. kt-intelligent-loader.py
Auto-discovers and loads relevant context.

**Usage:**
```bash
python tools/kt-intelligent-loader.py --query "authentication"
```

**Features:**
- Semantic search across trees
- Auto-ranking by relevance
- Progressive loading (strategic first)
- System map generation

### 4. kt-tool-node-generator.py
Scans Python scripts and generates tool nodes.

**Usage:**
```bash
python tools/kt-tool-node-generator.py --limit 10
```

**Features:**
- Uses local Ollama (zero API cost)
- Extracts purpose, dependencies, usage
- Generates tool nodes in KT format
- Batch processing for large codebases

---

## ISS Integration

The system integrates with Knowledge Tree's Index Scrolling System:

```
KT Nodes (JSONL)
    ↓
kt-hierarchical-summarizer.py
    ↓
3-Layer Markdown Summaries (with YAML frontmatter)
    ↓
iss-hierarchical-indexer.py
    ↓
ISS Indexes (fast lookups)
    ↓
kt-intelligent-loader.py
    ↓
Auto-Discovery & Context Loading
```

---

## Use Cases

### 1. Planning New Features
```bash
# Load strategic layers of related projects
python tools/kt-intelligent-loader.py --query "authentication api"
```

**Benefit:** See high-level patterns across multiple projects without token overload

### 2. Code Review
```bash
# Load tactical + implementation of specific module
python tools/kt-intelligent-loader.py --branch my-project --layers tactical,implementation --path src/auth/
```

**Benefit:** Focused context on just what's being reviewed

### 3. Architecture Decisions
```bash
# Compare strategic layers across projects
python tools/kt-intelligent-loader.py --query "database architecture" --layer strategic
```

**Benefit:** Cross-project architectural analysis at macro level

### 4. Onboarding
```bash
# Progressive loading for new team members
# Day 1: Strategic layer (understand architecture)
# Week 1: Tactical layer (understand modules)
# Month 1: Implementation layer (understand code)
```

**Benefit:** Gradual learning curve from macro to micro

### 5. Cross-Project Analysis
```bash
# Scan strategic layers of entire codebase
python tools/kt-intelligent-loader.py --all-branches --layer strategic
```

**Benefit:** Codebase-wide patterns visible in <10k tokens

---

## Example: Generated Summary

**Branch:** `ui-builder-mcp`

### strategic.md (450 tokens)
```markdown
---
branch: ui-builder-mcp
layer: strategic
node_count: 12
token_estimate: 450
---

# UI Builder MCP - Strategic Layer

**Purpose:** MCP server for UI component generation and management

**Key Decisions:**
- Use Model Context Protocol for AI integration
- Component-based architecture
- TypeScript for type safety

**Architecture:**
- MCP tools for component CRUD
- Template system for common patterns
- Integration with VS Code
```

### tactical.md (1,200 tokens)
```markdown
---
branch: ui-builder-mcp
layer: tactical
node_count: 12
token_estimate: 1200
---

# UI Builder MCP - Tactical Layer

**Module Organization:**
1. Tools layer (MCP tool definitions)
2. Template engine (Component generation)
3. VS Code integration (Extension setup)

**Implementation Approach:**
- TypeScript SDK from MCP
- Stdio transport for communication
- Resource-based component access

**Key Patterns:**
- Tool registration via setRequestHandler
- Resource URIs: `ui://components/{name}`
- Template variables with Handlebars
```

### implementation.md (3,500 tokens)
```markdown
---
branch: ui-builder-mcp
layer: implementation
node_count: 12
token_estimate: 3500
---

# UI Builder MCP - Implementation Layer

**Files:**
- `src/index.ts` - MCP server entry
- `src/tools/` - Tool definitions
- `src/templates/` - Component templates
- `src/resources/` - Resource handlers

**Key Code:**
```typescript
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === 'create_component') {
    // Component creation logic
  }
});
```

**Edge Cases:**
- Handle missing template files
- Validate component names
- Error recovery for malformed requests
```

---

## Installation

These tools are included in the `system-documentation` branch:

```bash
cd C:\dev\KT\branches\system-documentation\tools

# Generate summaries for a branch
python kt-hierarchical-summarizer.py --branch my-branch

# Update ISS indexes
python iss-hierarchical-indexer.py

# Discover related context
python kt-intelligent-loader.py --query "my search"
```

---

## Configuration

No configuration needed! Tools auto-detect:
- KT root location
- ISS directory
- Branch paths

All outputs use standard KT/ISS structure.

---

## Performance

**Benchmarks (175 nodes across 5 branches):**
- Summary generation: ~2 minutes
- ISS indexing: ~5 seconds
- Context discovery: <1 second

**Token efficiency:**
- Total nodes: 175
- Total summaries: 9 (3 layers × 3 branches)
- Total tokens: 10,562
- Average: ~2,112 tokens/branch
- vs Full trees: ~25,000 tokens/branch
- **Efficiency: 92% token savings**

---

## Extending the System

### Add Custom Layers

Define your own layers in the summarizer:

```python
CUSTOM_LAYERS = {
    "overview": lambda nodes: filter_by_depth(nodes, 1-2),
    "architecture": lambda nodes: filter_by_type(nodes, "decision"),
    "code": lambda nodes: filter_by_depth(nodes, 5+)
}
```

### Add Custom Filters

Filter nodes by tags, types, or custom logic:

```python
def custom_filter(node):
    return "security" in node.get("tags", [])
```

### Integrate with CI/CD

Auto-generate summaries on commit:

```yaml
# .github/workflows/generate-summaries.yml
on: [push]
jobs:
  summarize:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: python tools/kt-hierarchical-summarizer.py --all
      - run: python tools/iss-hierarchical-indexer.py
```

---

## Credits

**Created by:** Max Stern  
**Date:** 2026-03-09  
**License:** MIT  
**Part of:** Knowledge Tree Starter Kit

**Inspiration:** Need for token-efficient AI context in large codebases

---

## Learn More

- [Knowledge Tree System](../../README.md)
- [ISS Documentation](../../index-scrolling-system/INDEX.md)
- [Examples](examples/)

---

**Ready to optimize your AI context? Start with strategic layers!** 🚀
