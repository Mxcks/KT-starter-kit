---
branch: system-documentation
layer: strategic
node_count: 8
token_estimate: 650
generated_at: 2026-03-09T19:03:00Z
generator: Manual-Creation-v1
node_types:
  decision: 1
  documentation: 6
  init: 1
---

# System-Documentation - Strategic Layer

**Summary:** 8 nodes covering fractal documentation system architecture and token efficiency

---

## Overview

The Fractal Documentation System provides AI-optimized hierarchical documentation using 3 layers: Strategic (macro), Tactical (mid), and Implementation (micro). Enables 97% token savings through progressive loading.

## Key Decision

**Decision:** Adopt Strategic/Tactical/Implementation hierarchy for all KT branches

**Reasoning:** Token efficiency - Strategic layer (~800 tokens) vs full tree (~25,000 tokens). AI can scan 30+ trees in same token budget as loading 1 full tree. Critical for large codebases and multi-project contexts.

## Architecture

**Three-Layer System:**
1. **Strategic Layer** - High-level architecture, major decisions (800-1,500 tokens)
2. **Tactical Layer** - Implementation approaches, module organization (2,000-5,000 tokens)
3. **Implementation Layer** - Specific code, files, utilities (10,000-25,000 tokens)

**Tools Included:**
- kt-hierarchical-summarizer.py - Generates 3-layer summaries
- iss-hierarchical-indexer.py - Updates ISS indexes
- kt-intelligent-loader.py - Auto-discovers relevant context
- kt-tool-node-generator.py - Scans Python scripts with local LLM

## Token Efficiency

**Impact:** 97% token savings (Strategic only: 800 tokens vs Full tree: 25,000 tokens)

**Enables:**
- Scan entire codebase at strategic level
- Progressive detail loading (only pay for what you need)
- Cross-project analysis with minimal token cost

## ISS Integration

Auto-generates summaries → Updates ISS indexes → Enables intelligent discovery → Progressive context loading

---

## Use Cases

1. **Planning** - Load strategic layers of related projects
2. **Code Review** - Load tactical + implementation of specific modules
3. **Architecture** - Compare strategic layers across projects
4. **Onboarding** - Progressive loading from macro to micro
5. **Cross-Project** - Scan strategic layers of entire codebase

---

**This branch demonstrates the fractal pattern by using it to document itself!**
