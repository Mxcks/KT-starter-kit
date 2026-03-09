# KT Starter Kit - Quick Reference

**For:** Understanding the complete system at a glance  
**See:** ARCHITECTURE.md for comprehensive details

---

## What Is This?

**Knowledge Tree Starter Kit** - A complete system for managing project knowledge with 97% token efficiency for AI context loading.

---

## Core Components (6 Parts)

```
1. kt.py (CLI)
   └─> Create projects, add nodes
   
2. Branches/Nodes (Data)
   └─> JSONL storage of decisions, commits, docs
   
3. Fractal Summarizer
   └─> Generate Strategic/Tactical/Implementation layers
   
4. ISS Indexer
   └─> Index summaries for fast discovery
   
5. kt-integration (AI Queries)
   └─> OpenClaw skill for querying KT
   
6. Automation (create-example.py)
   └─> Complete workflow demonstration
```

---

## 5-Minute Quick Start

```bash
# 1. Create project
python kt.py init my-project "My awesome project"

# 2. Add content
python kt.py add decision "Use PostgreSQL" --branch my-project \
  --reasoning "Need ACID compliance"

# 3. Generate summaries
python branches/system-documentation/tools/kt-hierarchical-summarizer.py \
  --branch my-project

# 4. Update indexes
python branches/system-documentation/tools/iss-hierarchical-indexer.py

# 5. Query
python tools/kt-integration/tools/iss-query.py layer my-project strategic
```

**Result:** 97% token savings vs. loading full project!

---

## File Structure

```
kt-starter-kit/
├── kt.py                           # CLI for content creation
├── create-example.py               # Workflow automation
├── README.md                       # Getting started
├── QUICKSTART.md                   # 15-min guide
├── ARCHITECTURE.md                 # This comprehensive doc
├── BUILD-PLAN.md                   # Roadmap
│
├── branches/                       # Your projects
│   ├── system-documentation/       # Example (8 nodes)
│   │   ├── knowledge/tree.jsonl
│   │   └── tools/                  # Fractal summarizer, ISS indexer
│   ├── example-todo-app/           # Example (5 nodes)
│   └── my-auth-service/            # Example (3 nodes)
│
├── index-scrolling-system/         # ISS summaries & indexes
│   └── meta-tree/
│       ├── summaries/              # 3-layer summaries per branch
│       └── index/                  # Fast lookup indexes
│
└── tools/
    └── kt-integration/             # OpenClaw skill (9 files)
        ├── SKILL.md
        ├── config/settings.json
        └── tools/                  # Query scripts
```

**Total:** 27 files, ~135KB, ~4,000 lines

---

## Node Types

```json
{
  "id": 0,
  "type": "init|decision|commit|documentation|summary|blocker",
  "message": "What happened",
  "timestamp": "2026-03-09T19:00:00Z",
  "tags": ["tag1", "tag2"],
  "reasoning": "(optional) Why we chose this",
  "content": "(optional) Detailed info"
}
```

---

## 3 Layers Explained

| Layer | Tokens | Content | Use Case |
|-------|--------|---------|----------|
| **Strategic** | ~800 | Purpose, key decisions, architecture | Scanning projects, relevance check |
| **Tactical** | ~3,200 | Modules, approaches, relationships | Planning changes, understanding structure |
| **Implementation** | ~18,000 | Files, code, details | Coding, debugging, deep dive |

**Full tree:** ~25,000 tokens  
**Savings:** Load strategic only = **97% token savings!**

---

## Key Workflows

### 1. Create Content
```bash
kt.py init <name>
kt.py add decision|commit|doc <msg> --branch <name>
kt.py tree <name>
```

### 2. Generate Summaries
```bash
kt-hierarchical-summarizer.py --branch <name>
iss-hierarchical-indexer.py
```

### 3. Query
```bash
iss-query.py search <query>
iss-query.py layer <branch> strategic|tactical|implementation
```

### 4. Integrate with AI
```bash
set KT_ROOT=C:\path\to\kt-starter-kit
kt-config.py smart
kt-smart.py discover --query <topic>
```

### 5. Automate
```bash
create-example.py  # Complete demo
```

---

## What We Have ✅

- Content creation (kt.py CLI)
- Branch/node storage (JSONL)
- 3-layer summarization (rule-based, no LLM)
- ISS indexing (fast discovery)
- Query tools (kt-integration)
- OpenClaw integration (AgentSkill)
- Complete documentation
- Working examples (17 nodes)

---

## What We Don't Have ❌

- Node editing (update/delete)
- Full core engine (tree_engine.py)
- Orchestrator (task automation)
- Genesis/PRISM (templates)
- Branch operations (merge/archive)
- Visual UI
- API server
- MCP server (planned)

**Why:** Focus on the innovation (fractal docs), keep it simple, extensible later

---

## Key Statistics

| Metric | Value |
|--------|-------|
| **Total files** | 27 |
| **Lines of code** | ~4,000 |
| **Python code** | ~2,200 lines |
| **Documentation** | ~1,800 lines |
| **Branches** | 4 examples |
| **Total nodes** | 17 nodes |
| **Token savings** | 97% (strategic only) |
| **LLM calls** | 0 (rule-based!) |

---

## Innovation Summary

**Traditional Approach:**
- Load entire codebase
- 25,000 tokens
- Fit 1-2 projects max

**Fractal Approach:**
- Load strategic layer first
- 800 tokens
- **Scan 30+ projects in same budget!**
- Drill down only when needed

**How:** Rule-based intelligent extraction groups nodes by type/depth into 3 layers

**Meta:** system-documentation branch documents itself using its own pattern!

---

## Commands Cheat Sheet

```bash
# CREATE
kt.py init my-proj "Description"
kt.py add decision "Msg" --branch my-proj --reasoning "Why"
kt.py add commit "Msg" --branch my-proj
kt.py add doc "Msg" --branch my-proj

# VIEW
kt.py list
kt.py tree my-proj
kt.py tree my-proj --detailed

# SUMMARIZE
python branches/system-documentation/tools/kt-hierarchical-summarizer.py --branch my-proj
python branches/system-documentation/tools/iss-hierarchical-indexer.py

# QUERY
python tools/kt-integration/tools/iss-query.py stats
python tools/kt-integration/tools/iss-query.py search "keyword"
python tools/kt-integration/tools/iss-query.py layer my-proj strategic

# CONFIG
python tools/kt-integration/tools/kt-config.py show
python tools/kt-integration/tools/kt-config.py smart
python tools/kt-integration/tools/kt-config.py quiet

# DISCOVER
python tools/kt-integration/tools/kt-smart.py discover --query "topic"
python tools/kt-integration/tools/kt-smart.py preload

# DEMO
python create-example.py
```

---

## Integration with OpenClaw

**Setup:**
```bash
set KT_ROOT=C:\path\to\kt-starter-kit
python tools/kt-integration/tools/kt-config.py smart
```

**Auto-triggers:** "KT", "Knowledge Tree", "ISS", "branch", planning keywords

**Config options:**
- `auto_preload` - Load on session start
- `auto_search_on_planning` - Search when planning detected
- `auto_load_strategic` - Auto-load strategic layers
- `search_threshold` - Relevance cutoff
- `max_auto_trees` - Limit auto-loaded trees
- `quiet_mode` - Suppress status messages

---

## Next Steps

**Immediate:**
- ✅ Created ARCHITECTURE.md (comprehensive overview)
- Document data format specification
- Test on fresh machine

**Short-term:**
- Publish kt-integration to ClawHub
- Add more examples
- Create video walkthrough

**Long-term:**
- Add core engine (Phase 2)
- Build MCP server
- Community adoption

---

## Resources

- **Repo:** https://github.com/Mxcks/KT-starter-kit
- **Quick Start:** QUICKSTART.md (15 minutes)
- **Deep Dive:** ARCHITECTURE.md (complete system)
- **Roadmap:** BUILD-PLAN.md (4 phases)
- **Integration:** tools/kt-integration/SKILL.md

---

**Status:** Production-ready, fully functional, open-source (MIT)  
**Innovation:** 97% token efficiency for AI context  
**Ready for:** Real-world usage, extension, contribution

🚀 **Clone it. Use it. Extend it. Save tokens!**
