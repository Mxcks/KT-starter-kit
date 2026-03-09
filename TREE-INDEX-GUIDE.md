# Tree/Index System Guide

**The tree/index system enables fast cross-branch queries and discovery**

---

## What Is The Tree/Index System?

The tree/index system provides searchable indexes across all your branches, enabling:
- **Cross-branch searches** - Find nodes across all projects
- **Tag discovery** - See all tags and where they're used
- **Node type filtering** - Find all decisions, commits, etc.
- **Statistics** - Understanding your knowledge tree
- **Fast queries** - Pre-built indexes for instant results

---

## How It Works

```
Branches (tree.jsonl files)
    ↓
build-indexes.py (scans all branches)
    ↓
Indexes (JSON files in index/)
    ↓
tree-query.py (query tool)
    ↓
Fast Results!
```

---

## The 5 Indexes

Located in `index/`:

### 1. branch-index.json
**What:** Complete branch catalog  
**Contains:**
- Branch name, path, description
- Node counts
- Tags per branch
- Node types per branch
- Creation timestamps

**Use cases:**
- "What branches do I have?"
- "Which branch has the most nodes?"
- "What tags does this branch use?"

---

### 2. global-tag-index.json
**What:** All tags across all branches  
**Contains:**
- Tag name
- Usage count
- Which branches use this tag
- All nodes with this tag

**Use cases:**
- "Where is 'authentication' mentioned?"
- "What are the most common tags?"
- "Which branches use 'security' tags?"

---

### 3. node-type-index.json
**What:** Nodes organized by type  
**Contains:**
- Node types (decision, commit, documentation, etc.)
- Counts per type
- Which branches have each type
- All nodes of each type

**Use cases:**
- "Show me all architectural decisions"
- "List all commits across projects"
- "Which branches have blockers?"

---

### 4. search-index.json
**What:** Full-text searchable index  
**Contains:**
- All node content
- Searchable text (message + reasoning + content + tags)
- Branch and node metadata

**Use cases:**
- "Find nodes mentioning 'PostgreSQL'"
- "Search for 'authentication' across all projects"
- "Where did we discuss caching?"

---

### 5. statistics.json
**What:** Tree statistics and metrics  
**Contains:**
- Total branches, nodes, tags, types
- Top tags by usage
- Branches by size
- Node type distribution

**Use cases:**
- "How big is my knowledge tree?"
- "What are the most common tags?"
- "Which branches are largest?"

---

## Building Indexes

**Command:**
```bash
python build-indexes.py
```

**What it does:**
1. Scans all branches in `branches/`
2. Loads all `tree.jsonl` files
3. Extracts tags, types, metadata
4. Builds 5 index files
5. Generates statistics

**When to run:**
- After creating new branches
- After adding many nodes
- Before querying
- Periodically (daily/weekly)

**Output:**
```
index/
├── branch-index.json
├── global-tag-index.json
├── node-type-index.json
├── search-index.json
└── statistics.json
```

**Performance:**
- Very fast (processes 100s of nodes in seconds)
- No dependencies
- Pure Python

---

## Querying Indexes

**Command:**
```bash
python tree-query.py <command> [options]
```

### Available Commands

#### 1. stats - Show Statistics
```bash
python tree-query.py stats
```

**Output:**
```
Total Branches: 5
Total Nodes: 25
Total Tags: 40
Node Types: 5

Branches by Size:
  system-documentation    8 nodes
  example-todo-app        5 nodes
  ...

Top Tags:
  architecture            5 nodes
  documentation           4 nodes
  ...
```

---

#### 2. branches - List Branches
```bash
python tree-query.py branches
```

**Output:**
```
Name                  Nodes      Tags
=========================================
system-documentation  8          fractal, iss, documentation...
example-todo-app      5          example, simple, crud...
```

---

#### 3. tags - List/Search Tags
```bash
# List all tags
python tree-query.py tags

# Search tags
python tree-query.py tags --query auth
```

**Output:**
```
Tag                   Count      Branches
============================================
architecture          5          system-documentation, my-auth...
auth                  2          my-auth-service, example...
```

---

#### 4. search - Full-Text Search
```bash
python tree-query.py search "authentication"
python tree-query.py search "PostgreSQL"
python tree-query.py search "caching" --limit 10
```

**Output:**
```
2 matches for 'authentication':

[my-auth-service] DECISION
  Use JWT for authentication
  Tags: architecture, auth, security

[example-api] COMMIT
  Implement JWT authentication
  Tags: security, milestone
```

---

#### 5. by-type - Filter by Node Type
```bash
python tree-query.py by-type decision
python tree-query.py by-type commit --limit 10
```

**Output:**
```
4 decision nodes:

[system-documentation] Use fractal 3-layer structure
[my-auth-service] Use JWT for authentication
[example-todo-app] Use localStorage for persistence
...
```

---

#### 6. branch-info - Branch Details
```bash
python tree-query.py branch-info system-documentation
```

**Output:**
```
Branch: system-documentation
===============================
Description: Fractal Documentation System
Nodes: 8
Created: 2026-03-09T...
Path: branches/system-documentation

Tags (12):
  - architecture
  - documentation
  - fractal
  ...

Node Types (4):
  - decision
  - documentation
  - init
  - summary
```

---

## Use Cases

### Use Case 1: Finding Related Work

**Scenario:** You're working on authentication. What have we done before?

```bash
# Search for auth-related nodes
python tree-query.py search "authentication"

# Check auth tag
python tree-query.py tags --query auth

# See all security decisions
python tree-query.py by-type decision | grep -i security
```

**Result:** Find all auth work across all projects

---

### Use Case 2: Architectural Review

**Scenario:** Review all architectural decisions

```bash
# Get all decisions
python tree-query.py by-type decision

# Filter by architecture tag
python tree-query.py tags --query architecture

# Check specific branches
python tree-query.py branch-info api-gateway
python tree-query.py branch-info user-service
```

**Result:** Complete architectural decision log

---

### Use Case 3: Tag Audit

**Scenario:** Are we tagging consistently?

```bash
# See all tags
python tree-query.py tags

# Check statistics
python tree-query.py stats

# Find rarely-used tags
# (tags with count=1 might be typos or need consolidation)
```

**Result:** Identify tagging patterns and inconsistencies

---

### Use Case 4: Project Discovery

**Scenario:** New team member wants overview

```bash
# Show all branches
python tree-query.py branches

# Get statistics
python tree-query.py stats

# Review each branch
python tree-query.py branch-info <branch-name>
```

**Result:** Quick understanding of all projects

---

### Use Case 5: Find Blockers

**Scenario:** What's blocking us across all projects?

```bash
# Find all blocker nodes
python tree-query.py by-type blocker

# Search for "blocked" or "issue"
python tree-query.py search "blocked"
python tree-query.py search "issue"
```

**Result:** Cross-project blocker list

---

## Automation

### Auto-Rebuild on Changes

**Option 1: Git Hook**
```bash
# .git/hooks/post-commit
#!/bin/bash
python build-indexes.py
```

**Option 2: Cron Job**
```bash
# Rebuild daily at 2am
0 2 * * * cd /path/to/kt-starter-kit && python build-indexes.py
```

**Option 3: Watch Script**
```bash
# Rebuild on file changes (requires watchdog)
python watch-and-rebuild.py
```

---

## Integration

### With OpenClaw (kt-integration)

The kt-integration skill can query these indexes:

```python
# In kt-integration tools
import json
from pathlib import Path

# Load indexes
with open('index/search-index.json') as f:
    search_idx = json.load(f)

# Query
matches = [
    e for e in search_idx['entries']
    if query.lower() in e['searchable_text']
]
```

### With ISS

Combine tree indexes with ISS summaries:

```python
# 1. Search tree index for relevant branches
matches = tree_query.search("authentication")
branches = [m['branch'] for m in matches]

# 2. Load ISS strategic summaries for those branches
for branch in branches:
    load_iss_summary(branch, layer='strategic')
```

**Result:** Find + summarize in one workflow

---

## Current Limitations

**What it doesn't do:**
- ❌ Node relationships/links (future)
- ❌ Cross-branch dependencies (future)
- ❌ Historical queries (time-based) (future)
- ❌ Semantic search (embeddings) (future)
- ❌ Real-time updates (need to rebuild)

**What it does well:**
- ✅ Fast keyword search
- ✅ Tag-based discovery
- ✅ Type filtering
- ✅ Branch overview
- ✅ Statistics

---

## Extending The System

### Adding Custom Indexes

Create your own index builder:

```python
# custom-index-builder.py
import json
from pathlib import Path

def build_custom_index():
    # Your logic here
    
    # Load branches
    branches_dir = Path('branches')
    
    # Build your index
    custom_index = {
        "your_data": []
    }
    
    # Save
    with open('index/custom-index.json', 'w') as f:
        json.dump(custom_index, f, indent=2)

if __name__ == '__main__':
    build_custom_index()
```

### Adding Custom Queries

Extend tree-query.py:

```python
def cmd_custom(self, args):
    """Your custom query"""
    # Load your index
    with open(self.index_dir / 'custom-index.json') as f:
        data = json.load(f)
    
    # Query logic
    # ...
    
    # Output
    print(results)
```

---

## Example: Current Starter Kit Indexes

**Generated from 5 example branches:**

```
Statistics:
  Branches: 5
  Nodes: 25
  Tags: 40
  Node Types: 5

Top Tags:
  architecture (5 nodes)
  iss (4 nodes)
  documentation (4 nodes)
  
Node Types:
  documentation (10 nodes)
  init (5 nodes)
  commit (5 nodes)
  decision (4 nodes)
  summary (1 node)
```

**Try it yourself:**
```bash
python build-indexes.py
python tree-query.py stats
```

---

## Resources

- **Index builder:** `build-indexes.py`
- **Query tool:** `tree-query.py`
- **Indexes:** `index/*.json`
- **ISS integration:** `tools/kt-integration/`
- **Architecture:** `ARCHITECTURE.md`

---

**Summary:** The tree/index system enables fast cross-branch queries and discovery. Build indexes with `build-indexes.py`, query with `tree-query.py`, integrate with ISS for complete knowledge management!
