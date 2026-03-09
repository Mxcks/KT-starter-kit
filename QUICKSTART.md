# Quick Start Guide - KT Starter Kit

**From zero to 97% token savings in 15 minutes**

---

## What You'll Learn

1. How to create a branch with nodes
2. How to generate fractal summaries (Strategic/Tactical/Implementation)
3. How ISS indexes summaries for fast discovery
4. How to query and load context
5. **Most importantly:** See the 97% token savings in action!

---

## Prerequisites

```bash
# Clone the repo
git clone https://github.com/Mxcks/KT-starter-kit.git
cd KT-starter-kit

# Python 3.8+ (no external dependencies needed!)
python --version
```

---

## The 5-Step Workflow

### Step 1: Create a Branch with Nodes (2 min)

**Option A: Use the automation script**
```bash
python create-example.py
```

This creates `example-todo-app` branch with 5 nodes demonstrating a simple todo application.

**Option B: Create manually**
```bash
# Create branch structure
mkdir -p branches/my-project/knowledge

# Create nodes file
cat > branches/my-project/knowledge/tree.jsonl << 'EOF'
{"id":0,"type":"init","branch":"my-project","message":"My Awesome Project","timestamp":"2026-03-09T19:00:00Z","tags":["example"]}
{"id":1,"type":"decision","message":"Use React for frontend","reasoning":"Component-based, large ecosystem","decision":"React 18+ with TypeScript","tags":["architecture","frontend"],"timestamp":"2026-03-09T19:05:00Z"}
{"id":2,"type":"commit","message":"Set up project structure","content":"Created src/, tests/, docs/ directories","tags":["setup"],"timestamp":"2026-03-09T19:10:00Z"}
EOF
```

**What you created:**
- A **branch** = A project or subsystem
- **Nodes** = Decision points, commits, summaries, documentation

---

### Step 2: Generate Fractal Summaries (1 min)

```bash
cd branches/system-documentation/tools
python kt-hierarchical-summarizer.py --branch my-project
```

**What happens:**
- Analyzes your nodes
- Groups by depth/type
- Generates 3 markdown files:
  - `strategic.md` (~800 tokens) - High-level architecture
  - `tactical.md` (~3,200 tokens) - Implementation approach
  - `implementation.md` (~18,000 tokens) - Detailed code

**Output location:**
```
index-scrolling-system/meta-tree/summaries/my-project/
├── strategic.md
├── tactical.md
├── implementation.md
└── index.json
```

---

### Step 3: Update ISS Indexes (30 sec)

```bash
python iss-hierarchical-indexer.py
```

**What happens:**
- Scans all summaries
- Creates fast-lookup indexes:
  - `hierarchical-summaries.json` - All summaries
  - `by-layer.json` - Grouped by layer
  - `quick-access.json` - Fast lookups
  - `stats.json` - Statistics

**Output location:**
```
index-scrolling-system/meta-tree/index/
```

---

### Step 4: Query for Context (10 sec)

```bash
cd ../../..  # Back to root
python tools/kt-integration/tools/iss-query.py search "react"
```

**Result:**
```json
[
  {
    "tree_id": "my-project",
    "layer": "strategic",
    "path": "..."
  }
]
```

**Load a layer:**
```bash
python tools/kt-integration/tools/iss-query.py layer my-project strategic
```

**Result:**
```markdown
---
branch: my-project
layer: strategic
node_count: 3
token_estimate: 450
---

# My-Project - Strategic Layer

**Purpose:** My Awesome Project

**Key Decisions:**
- Use React 18+ with TypeScript for frontend

**Architecture:**
- Component-based structure
...
```

---

### Step 5: See Token Efficiency (Visual!)

```bash
python create-example.py  # Runs with built-in demo
```

**Output:**
```
[STEP 5] Token Efficiency Demonstration

Layer                Tokens     % of Full Tree
=============================================
Strategic            450        98.2% savings
+ Tactical           1,200      95.2% savings
+ Implementation     3,800      84.8% savings
=============================================
Full Tree (est.)     25,000     0% savings

[INSIGHT] Loading strategic only saves 98% tokens!
```

**What this means:**
- **Traditional:** Load full codebase = 25,000 tokens
- **Strategic only:** 450 tokens = **98% savings!**
- **Strategic + Tactical:** 1,650 tokens = 93% savings
- **All layers:** 5,450 tokens = 78% savings

---

## Real-World Usage

### Scenario 1: "Show me all authentication-related work"

```bash
# Search across all branches
python tools/kt-integration/tools/iss-query.py search "authentication"

# Load strategic layers only
python tools/kt-integration/tools/kt-smart.py discover --query "authentication"
```

**Token cost:** ~2,000 tokens for 5 projects (vs 125,000 for full trees)

---

### Scenario 2: "I need to understand the API module"

```bash
# Load tactical layer (mid-level detail)
python tools/kt-integration/tools/iss-query.py layer my-api-project tactical
```

**Token cost:** ~3,500 tokens (vs 25,000 for full tree)

---

### Scenario 3: "I'm coding the auth service"

```bash
# Load implementation layer (all details)
python tools/kt-integration/tools/iss-query.py layer my-api-project implementation
```

**Token cost:** ~18,000 tokens (still better than loading ALL projects)

---

## Understanding the Layers

### 🎯 Strategic Layer (Macro)
**When:** First pass - "Is this relevant?"
**Contains:**
- Branch purpose
- Major architectural decisions
- High-level patterns
- Key technologies chosen

**Size:** 800-1,500 tokens  
**Use case:** Scanning many projects, architectural review

---

### ⚙️ Tactical Layer (Mid)
**When:** Second pass - "How is it built?"
**Contains:**
- Module organization
- Implementation strategies
- Component relationships
- Technical approaches

**Size:** 2,000-5,000 tokens  
**Use case:** Planning changes, understanding structure

---

### 🔧 Implementation Layer (Micro)
**When:** Deep dive - "Show me the code"
**Contains:**
- Specific files and paths
- Code snippets
- Detailed utilities
- Edge cases and gotchas

**Size:** 10,000-25,000 tokens  
**Use case:** Coding, debugging, detailed analysis

---

## Tips & Tricks

### Tip 1: Start Strategic, Drill Down
```bash
# 1. Load all strategic layers (cheap!)
python tools/kt-integration/tools/kt-smart.py preload

# 2. Identify relevant project
python tools/kt-integration/tools/iss-query.py search "your-topic"

# 3. Load tactical for that project
python tools/kt-integration/tools/iss-query.py layer relevant-project tactical

# 4. Load implementation only if needed
python tools/kt-integration/tools/iss-query.py layer relevant-project implementation
```

### Tip 2: Automate with OpenClaw
```bash
# Set KT root
export KT_ROOT=/path/to/kt-starter-kit

# Configure kt-integration for auto-loading
python tools/kt-integration/tools/kt-config.py smart

# Now OpenClaw auto-loads strategic layers when planning!
```

### Tip 3: Regenerate Summaries After Changes
```bash
# After adding nodes to a branch
cd branches/system-documentation/tools
python kt-hierarchical-summarizer.py --branch my-project
python iss-hierarchical-indexer.py
```

---

## What You Just Learned

✅ How to create branches and nodes  
✅ How to generate fractal summaries  
✅ How ISS indexes for discovery  
✅ How to query and load context  
✅ **Why 97% token savings matters!**

---

## Next Steps

### For Your Own Projects

1. **Create a branch** for your project
2. **Add nodes** as you make decisions/commits
3. **Generate summaries** periodically
4. **Query via AI** and enjoy token savings!

### For Teams

1. **Create operational branches** for common patterns
2. **Share via Git** - everyone gets the summaries
3. **Use as templates** for new projects
4. **Establish conventions** for what goes in each layer

### For Advanced Users

1. **Extend the summarizer** with custom layers
2. **Build MCP server** for universal AI access
3. **Integrate with CI/CD** to auto-generate summaries
4. **Create domain-specific analyzers** (Python, TypeScript, etc.)

---

## Troubleshooting

**"No module found"**
→ Make sure you're in the right directory when running scripts

**"No summaries generated"**
→ Check that your branch has nodes in `knowledge/tree.jsonl`

**"ISS indexes empty"**
→ Run the hierarchical summarizer first

**"Query returns nothing"**
→ Update ISS indexes with `iss-hierarchical-indexer.py`

---

## Get Help

- **Issues:** https://github.com/Mxcks/KT-starter-kit/issues
- **Examples:** See `branches/system-documentation/`
- **Docs:** `BUILD-PLAN.md` for architecture details

---

**You're ready! Start creating branches and enjoying 97% token savings!** 🚀

```bash
# Create your first real branch
mkdir -p branches/my-first-project/knowledge
echo '{"id":0,"type":"init","branch":"my-first-project","message":"My First KT Project","timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","tags":["learning"]}' > branches/my-first-project/knowledge/tree.jsonl

# Generate summaries
cd branches/system-documentation/tools
python kt-hierarchical-summarizer.py --branch my-first-project

# Query it
cd ../../..
python tools/kt-integration/tools/iss-query.py layer my-first-project strategic
```

**Welcome to token-efficient AI context management!**
