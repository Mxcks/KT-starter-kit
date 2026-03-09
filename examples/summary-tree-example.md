# Summary Tree Example

**ISS hierarchical summary structure visualization**

---

## What Is A Summary Tree?

A summary tree shows the 3-layer fractal structure of ISS summaries:
- **Strategic** - High-level overview (~800 tokens)
- **Tactical** - Mid-level detail (~3,200 tokens)
- **Implementation** - Full detail (~18,000 tokens)

---

## Example: system-documentation Summary Tree

```
system-documentation
│
├── 📊 Strategic Layer (800 tokens)
│   │
│   ├── Purpose
│   │   └── "Fractal Documentation System - AI-optimized navigation"
│   │
│   ├── Key Decisions
│   │   ├── [Node 1] Use fractal 3-layer structure
│   │   └── [Node 4] Progressive context loading
│   │
│   ├── Architecture
│   │   ├── Strategic (macro view)
│   │   ├── Tactical (mid-level)
│   │   └── Implementation (micro details)
│   │
│   └── Technologies
│       ├── Python (rule-based summarization)
│       ├── JSONL (node storage)
│       └── Markdown (summary format)
│
├── ⚙️ Tactical Layer (3,200 tokens)
│   │
│   ├── Module Organization
│   │   ├── kt-hierarchical-summarizer.py
│   │   ├── iss-hierarchical-indexer.py
│   │   ├── kt-intelligent-loader.py
│   │   └── kt-tool-node-generator.py
│   │
│   ├── Implementation Approach
│   │   ├── Rule-based extraction (no LLM)
│   │   ├── Group by node type and depth
│   │   ├── Generate 3 markdown files
│   │   └── Create JSON indexes
│   │
│   ├── Data Flow
│   │   ├── 1. Read nodes from tree.jsonl
│   │   ├── 2. Analyze and group
│   │   ├── 3. Generate summaries
│   │   ├── 4. Write to ISS
│   │   └── 5. Build indexes
│   │
│   └── Integration Points
│       ├── ISS (summaries output)
│       ├── kt-integration (queries)
│       └── OpenClaw (AI access)
│
└── 🔧 Implementation Layer (18,000 tokens)
    │
    ├── File Structure
    │   ├── branches/system-documentation/
    │   │   ├── knowledge/tree.jsonl (8 nodes)
    │   │   ├── tools/kt-hierarchical-summarizer.py (12KB)
    │   │   ├── tools/iss-hierarchical-indexer.py (10KB)
    │   │   ├── tools/kt-intelligent-loader.py (12KB)
    │   │   └── tools/kt-tool-node-generator.py (9KB)
    │   │
    │   └── index-scrolling-system/meta-tree/summaries/
    │       └── system-documentation/
    │           ├── strategic.md
    │           ├── tactical.md
    │           ├── implementation.md
    │           └── index.json
    │
    ├── Code Details
    │   ├── kt-hierarchical-summarizer.py
    │   │   ├── Class: HierarchicalSummarizer
    │   │   ├── Methods:
    │   │   │   ├── load_nodes()
    │   │   │   ├── analyze_nodes()
    │   │   │   ├── generate_strategic()
    │   │   │   ├── generate_tactical()
    │   │   │   ├── generate_implementation()
    │   │   │   └── save_summaries()
    │   │   └── Algorithm: Group by type → Extract by depth → Format
    │   │
    │   ├── iss-hierarchical-indexer.py
    │   │   ├── Scans summaries/ directory
    │   │   ├── Builds 4 indexes
    │   │   └── Writes to meta-tree/index/
    │   │
    │   └── kt-intelligent-loader.py
    │       ├── Auto-discovery logic
    │       ├── Relevance scoring
    │       └── Progressive loading
    │
    ├── Node Examples
    │   ├── [0] init: "Fractal Documentation System"
    │   ├── [1] decision: "Use fractal 3-layer structure"
    │   ├── [2] documentation: "Strategic layer (macro)"
    │   ├── [3] documentation: "Tactical layer (mid)"
    │   ├── [4] documentation: "Implementation layer (micro)"
    │   ├── [5] documentation: "ISS integration"
    │   ├── [6] documentation: "Token efficiency (97% savings)"
    │   └── [7] documentation: "Usage examples"
    │
    └── Edge Cases
        ├── Empty branches (skip)
        ├── Single-node branches (minimal summary)
        ├── Unicode in Windows (handle cp1252)
        └── Missing fields (graceful defaults)
```

---

## Token Distribution Visualization

```
Full Tree (25,000 tokens)
│
├─────────────────────────────────────────────────────────────── 100%
│
└── After Fractal Summarization:
    │
    ├── Strategic (~800 tokens) ─────── 3.2%
    │   │
    │   ├─── 800 tokens ───┐
    │   │                  │  Quick scan:
    │   └─────────────────┘  "Is this relevant?"
    │
    ├── Tactical (~3,200 tokens) ────── 12.8%
    │   │
    │   ├──── 3,200 tokens ────┐
    │   │                       │  Mid-level:
    │   └──────────────────────┘  "How is it built?"
    │
    └── Implementation (~18,000 tokens) ── 72%
        │
        ├──────── 18,000 tokens ──────┐
        │                              │  Deep dive:
        └─────────────────────────────┘  "Show me the code"
```

**Savings:**
- Load Strategic only: 97% token savings
- Load Strategic + Tactical: 84% token savings
- Load all layers: Still organized and selective

---

## Example: Multiple Branches Comparison

```
Project Landscape (5 branches)
│
├── system-documentation (8 nodes)
│   ├── Strategic: 850 tokens
│   ├── Tactical: 3,400 tokens
│   └── Implementation: 19,000 tokens
│
├── iss-workflow-example (8 nodes)
│   ├── Strategic: 900 tokens
│   ├── Tactical: 3,600 tokens
│   └── Implementation: 20,000 tokens
│
├── example-todo-app (5 nodes)
│   ├── Strategic: 600 tokens
│   ├── Tactical: 2,400 tokens
│   └── Implementation: 12,000 tokens
│
├── my-auth-service (3 nodes)
│   ├── Strategic: 450 tokens
│   ├── Tactical: 1,800 tokens
│   └── Implementation: 9,000 tokens
│
└── test-api (1 node)
    ├── Strategic: 200 tokens
    ├── Tactical: 400 tokens
    └── Implementation: 1,000 tokens

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Totals:
  Strategic: 3,000 tokens (scan all 5 projects!)
  Tactical: 11,600 tokens (mid-level for all)
  Implementation: 61,000 tokens (full detail)
  
vs. Loading full trees: 125,000 tokens

Savings: 98% (strategic only) | 91% (strategic + tactical)
```

---

## Summary Tree By Use Case

### Use Case 1: "Which project has authentication?"

```
Query: "authentication"
│
└── Load Strategic Layers (3,000 tokens)
    │
    ├── system-documentation
    │   └── ❌ No auth mentioned
    │
    ├── iss-workflow-example
    │   └── ❌ No auth mentioned
    │
    ├── example-todo-app
    │   └── ❌ No auth mentioned
    │
    ├── my-auth-service
    │   └── ✅ "JWT authentication" ← FOUND!
    │
    └── test-api
        └── ❌ No auth mentioned

Result: Found in 1/5 branches
Tokens used: 3,000 (vs 125,000 for full trees)
```

### Use Case 2: "How is auth implemented?"

```
Found: my-auth-service
│
└── Load Tactical Layer (+1,800 tokens)
    │
    ├── Module: authentication
    │   ├── JWT token generation
    │   ├── Refresh token pattern
    │   └── Token validation
    │
    ├── Integration:
    │   ├── Express.js middleware
    │   └── Protected routes
    │
    └── Dependencies:
        └── jsonwebtoken library

Total tokens: 450 (strategic) + 1,800 (tactical) = 2,250
Enough detail to understand approach
```

### Use Case 3: "Show me the JWT code"

```
my-auth-service → Tactical shows approach
│
└── Load Implementation Layer (+9,000 tokens)
    │
    ├── Files:
    │   ├── src/auth/jwt.js
    │   ├── src/middleware/auth.js
    │   └── tests/auth.test.js
    │
    ├── Code Snippets:
    │   ├── generateToken() function
    │   ├── verifyToken() function
    │   └── refreshToken() function
    │
    ├── Configuration:
    │   ├── JWT_SECRET from env
    │   ├── Expiry: 5 minutes
    │   └── Refresh: 7 days
    │
    └── Edge Cases:
        ├── Expired tokens → 401
        ├── Invalid signature → 401
        └── Missing token → 401

Total tokens: 11,250 (strategic + tactical + implementation)
Complete code-level detail
```

---

## Progressive Loading Pattern

```
1. Start Broad (Load Strategic - 800 tokens)
   │
   ├── Relevant? → YES → Continue
   │           └─→ NO → Skip, try next branch
   │
2. Get Mid-Detail (Load Tactical - 3,200 tokens)
   │
   ├── Enough? → YES → Stop here
   │          └─→ NO → Continue
   │
3. Full Detail (Load Implementation - 18,000 tokens)
   │
   └── Complete code-level information

Total loaded: Depends on need
  - Just scanning: 800 tokens
  - Planning: 4,000 tokens (strategic + tactical)
  - Coding: 22,000 tokens (all layers)
```

---

## Summary Tree Generation Process

```
Input: Branch with nodes
│
├── Step 1: Load nodes from tree.jsonl
│   └── Parse JSON, validate structure
│
├── Step 2: Analyze & Group
│   ├── Group by node type (decision, commit, doc)
│   ├── Group by depth (0-2 = strategic, 3-5 = tactical, 6+ = implementation)
│   └── Extract key information
│
├── Step 3: Generate Strategic
│   ├── Purpose (from init node)
│   ├── Key decisions (decision nodes)
│   ├── Architecture (patterns from tags)
│   └── Technologies (from content)
│   │
│   └── Output: strategic.md (~800 tokens)
│
├── Step 4: Generate Tactical
│   ├── Module organization (from structure)
│   ├── Implementation approaches (from commits)
│   ├── Component relationships (from references)
│   └── Technical approaches (from decisions)
│   │
│   └── Output: tactical.md (~3,200 tokens)
│
├── Step 5: Generate Implementation
│   ├── File structure (all files mentioned)
│   ├── Code details (snippets from content)
│   ├── Specific utilities (helper functions)
│   └── Edge cases (blockers, issues)
│   │
│   └── Output: implementation.md (~18,000 tokens)
│
└── Step 6: Create Index
    ├── Metadata (node counts, tags, timestamps)
    ├── Token estimates
    └── Layer relationships
    │
    └── Output: index.json
```

---

## Visualization: Token Efficiency

```
Traditional Approach:
┌─────────────────────────────────────────────────────────────┐
│  Full Project Context (25,000 tokens)                        │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Load everything: files, code, docs, history            │ │
│  │ Can fit: 1-2 projects in 200K context window           │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘

Fractal Approach:
┌─────────────────────────────────────────────────────────────┐
│  Strategic Layers (800 tokens × 30 projects = 24,000 tokens) │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ...         │
│  │ P1   │ │ P2   │ │ P3   │ │ P4   │ │ P5   │ × 30        │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘              │
│  Can fit: 30+ projects in same context!                     │
│                                                              │
│  Then drill down to relevant projects:                       │
│  ┌─────────────────────┐                                    │
│  │ P4 Tactical (3,200) │                                    │
│  └─────────────────────┘                                    │
│  ┌─────────────────────────────────┐                        │
│  │ P4 Implementation (18,000)      │                        │
│  └─────────────────────────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Real Example: system-documentation

**File:** `index-scrolling-system/meta-tree/summaries/system-documentation/strategic.md`

```markdown
---
branch: system-documentation
layer: strategic
node_count: 8
token_estimate: 850
generated: 2026-03-09T19:15:00Z
---

# System-Documentation - Strategic Layer

**Purpose:** Fractal Documentation System for AI-optimized knowledge navigation

**Key Decisions:**
- [Node 1] Use fractal 3-layer structure (Strategic/Tactical/Implementation)
  - Reasoning: Enables progressive context loading with 97% token savings

**Architecture:**
- 3-layer hierarchical structure
- Strategic: ~800 tokens (macro view)
- Tactical: ~3,200 tokens (mid-level)  
- Implementation: ~18,000 tokens (micro details)

**Technologies:**
- Python for summarization
- JSONL for node storage
- Markdown for summaries
- Rule-based extraction (no LLM required)

**Token Efficiency:**
- Full tree: 25,000 tokens
- Strategic only: 800 tokens (97% savings)
- Enables scanning 30+ projects vs 1 full project
```

---

**Status:** Summary trees fully implemented and documented

**Try it:**
```bash
# Generate summaries for a branch
python branches/system-documentation/tools/kt-hierarchical-summarizer.py --branch my-project

# View summaries
cat index-scrolling-system/meta-tree/summaries/my-project/strategic.md
```

**See also:**
- QUICKSTART.md - Step-by-step summary generation
- ARCHITECTURE.md - Complete system overview
- iss-workflow-example/README.md - Detailed workflow
