# Core Engines

**The core engines provide programmatic access to the KT system**

---

## What Are The Core Engines?

The core engines are Python modules that power the KT system:

1. **tree_engine.py** - Node storage and retrieval
2. **branch_manager.py** - Branch creation and management  
3. **query_engine.py** - Search and filtering

These engines can be imported and used in your own scripts, tools, and integrations.

---

## Quick Start

### Using TreeEngine

```python
from core.tree_engine import TreeEngine

# Initialize
tree = TreeEngine()

# List branches
branches = tree.list_branches()
for branch in branches:
    print(f"{branch['name']}: {branch['node_count']} nodes")

# Load nodes from a branch
nodes = tree.load_nodes("my-project")

# Add a node
tree.add_node(
    branch_name="my-project",
    node_type="decision",
    message="Use PostgreSQL for storage",
    tags=["architecture", "database"],
    reasoning="PostgreSQL offers best balance of features and performance"
)

# Query nodes
results = tree.query_nodes(
    node_type="decision",
    tags=["architecture"]
)
```

### Using BranchManager

```python
from core.branch_manager import BranchManager

# Initialize
manager = BranchManager()

# Create a branch
manager.create_branch(
    name="my-new-project",
    description="A new project for testing",
    tags=["example", "test"]
)

# List branches
branches = manager.list_branches()

# Get branch info
info = manager.get_branch_info("my-new-project")
print(f"Branch has {info['node_count']} nodes")

# Rename branch
manager.rename_branch("old-name", "new-name")
```

### Using QueryEngine

```python
from core.tree_engine import TreeEngine
from core.query_engine import QueryEngine

# Initialize
tree = TreeEngine()
query = QueryEngine(tree)

# Text search
results = query.search_text("authentication")

# Find by type
decisions = query.find_by_type("decision")

# Find by tags
security_nodes = query.find_by_tags(["security", "auth"])

# Find recent nodes
recent = query.find_recent(days=7)

# Aggregate tags
tag_counts = query.aggregate_tags()
print(f"Most common tag: {list(tag_counts.keys())[0]}")
```

---

## Core Engine APIs

### TreeEngine

**Methods:**

- `list_branches()` - List all branches
- `load_nodes(branch_name)` - Load all nodes from branch
- `add_node(branch_name, node_type, message, ...)` - Add node
- `get_node(branch_name, node_id)` - Get specific node
- `query_nodes(branch_name, node_type, tags, text)` - Query with filters
- `get_branch_stats(branch_name)` - Get branch statistics

**Example:**
```python
tree = TreeEngine()
stats = tree.get_branch_stats("my-project")
print(f"Types: {stats['types']}")
print(f"Tags: {stats['tags']}")
```

---

### BranchManager

**Methods:**

- `create_branch(name, description, tags)` - Create new branch
- `delete_branch(name, confirm=True)` - Delete branch (requires confirmation)
- `rename_branch(old_name, new_name)` - Rename branch
- `list_branches()` - List all branches
- `get_branch_info(name)` - Get detailed branch info

**Example:**
```python
manager = BranchManager()

# Create
manager.create_branch("test-project", "Test description")

# Rename
manager.rename_branch("test-project", "production-api")

# Delete (careful!)
manager.delete_branch("old-project", confirm=True)
```

---

### QueryEngine

**Methods:**

- `query(branch, node_type, tags, text, date_from, date_to, limit)` - General query
- `search_text(query, branch, limit)` - Simple text search
- `find_by_type(node_type, branch, limit)` - Find nodes by type
- `find_by_tags(tags, branch, limit)` - Find nodes with tags
- `find_recent(days, branch, limit)` - Find recent nodes
- `get_related_nodes(branch, node_id, max_distance)` - Get nearby nodes
- `aggregate_tags(branch)` - Count tag usage
- `aggregate_types(branch)` - Count node types

**Example:**
```python
query = QueryEngine(tree)

# Complex query
results = query.query(
    branch="my-project",
    node_type="decision",
    tags=["architecture"],
    text="database",
    limit=10
)

# Aggregation
tags = query.aggregate_tags(branch="my-project")
for tag, count in list(tags.items())[:5]:
    print(f"{tag}: {count} nodes")
```

---

## Command-Line Usage

Each engine can be run standalone:

### tree_engine.py

```bash
# List branches
python core/tree_engine.py list

# Branch info
python core/tree_engine.py info my-project

# Query
python core/tree_engine.py query --branch my-project --type decision
python core/tree_engine.py query --text "authentication"
```

### branch_manager.py

```bash
# List branches
python core/branch_manager.py list

# Create branch
python core/branch_manager.py create my-new-project "Project description"

# Branch info
python core/branch_manager.py info my-project

# Rename
python core/branch_manager.py rename old-name new-name
```

### query_engine.py

```bash
# Text search
python core/query_engine.py search "authentication" --branch my-project

# Find by type
python core/query_engine.py type decision

# Find by tags
python core/query_engine.py tags architecture database

# Recent nodes
python core/query_engine.py recent --days 7

# Aggregate tags
python core/query_engine.py agg-tags

# Aggregate types
python core/query_engine.py agg-types
```

---

## Building Custom Tools

### Example: Export to JSON

```python
#!/usr/bin/env python3
"""Export branch to JSON"""

import json
import sys
from core.tree_engine import TreeEngine

def export_branch(branch_name, output_file):
    tree = TreeEngine()
    nodes = tree.load_nodes(branch_name)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(nodes, f, indent=2)
    
    print(f"Exported {len(nodes)} nodes to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: export-branch.py <branch> <output.json>")
        sys.exit(1)
    
    export_branch(sys.argv[1], sys.argv[2])
```

### Example: Tag Report

```python
#!/usr/bin/env python3
"""Generate tag usage report"""

from core.tree_engine import TreeEngine
from core.query_engine import QueryEngine

def tag_report():
    tree = TreeEngine()
    query = QueryEngine(tree)
    
    # Get all tags
    all_tags = query.aggregate_tags()
    
    print(f"\nTag Usage Report")
    print(f"=" * 40)
    print(f"Total unique tags: {len(all_tags)}\n")
    
    print(f"{'Tag':<25} {'Count':<10} {'Branches'}")
    print(f"-" * 50)
    
    for tag, count in list(all_tags.items())[:20]:
        # Find which branches use this tag
        results = query.find_by_tags([tag])
        branches = set(n['_branch'] for n in results)
        
        branches_str = ', '.join(list(branches)[:3])
        if len(branches) > 3:
            branches_str += '...'
        
        print(f"{tag:<25} {count:<10} {branches_str}")

if __name__ == "__main__":
    tag_report()
```

### Example: Decision Log

```python
#!/usr/bin/env python3
"""Extract all architectural decisions"""

from core.tree_engine import TreeEngine
from core.query_engine import QueryEngine

def decision_log():
    tree = TreeEngine()
    query = QueryEngine(tree)
    
    # Find all decisions
    decisions = query.find_by_type("decision")
    
    # Group by branch
    by_branch = {}
    for node in decisions:
        branch = node['_branch']
        if branch not in by_branch:
            by_branch[branch] = []
        by_branch[branch].append(node)
    
    print(f"\nArchitectural Decision Log")
    print(f"=" * 60)
    print(f"Total decisions: {len(decisions)}\n")
    
    for branch, branch_decisions in sorted(by_branch.items()):
        print(f"\n## {branch} ({len(branch_decisions)} decisions)\n")
        
        for i, node in enumerate(branch_decisions, 1):
            print(f"{i}. {node['message']}")
            if node.get('reasoning'):
                print(f"   Reasoning: {node['reasoning']}")
            if node.get('tags'):
                print(f"   Tags: {', '.join(node['tags'])}")
            print()

if __name__ == "__main__":
    decision_log()
```

---

## Integration Examples

### With ISS

```python
# Find relevant branches, then load ISS summaries
from core.query_engine import QueryEngine
from core.tree_engine import TreeEngine

tree = TreeEngine()
query = QueryEngine(tree)

# Search for branches with authentication
results = query.search_text("authentication")
branches = set(n['_branch'] for n in results)

# Load strategic summaries for relevant branches
for branch in branches:
    summary_file = f"index-scrolling-system/meta-tree/summaries/{branch}/strategic.md"
    # ... load and process summary
```

### With build-indexes.py

```python
# The index builder uses core engines internally
from core.tree_engine import TreeEngine

tree = TreeEngine()
branches = tree.list_branches()

for branch_info in branches:
    nodes = tree.load_nodes(branch_info['name'])
    # ... build indexes from nodes
```

### With kt-integration

```python
# OpenClaw skill uses core engines for queries
from core.tree_engine import TreeEngine
from core.query_engine import QueryEngine

def kt_smart_search(user_query):
    tree = TreeEngine()
    query = QueryEngine(tree)
    
    # Search
    results = query.search_text(user_query, limit=10)
    
    # Get relevant branches
    branches = list(set(n['_branch'] for n in results))
    
    # Load summaries for context
    # ...
```

---

## Architecture

```
Core Engines
│
├── tree_engine.py
│   ├── Manages JSONL storage
│   ├── Node CRUD operations
│   ├── Basic queries
│   └── Branch statistics
│
├── branch_manager.py
│   ├── Branch creation/deletion
│   ├── Branch renaming
│   ├── README generation
│   └── Branch registry
│
└── query_engine.py
    ├── Advanced queries
    ├── Text search
    ├── Tag/type filtering
    ├── Date filtering
    ├── Aggregations
    └── Related nodes

Used by:
  ↓
├── kt.py (CLI)
├── build-indexes.py
├── tree-query.py
├── kt-integration/ (OpenClaw)
└── Your custom tools!
```

---

## Best Practices

**1. Always use TreeEngine for node access**
```python
# Good
tree = TreeEngine()
nodes = tree.load_nodes("my-branch")

# Avoid
# Directly reading tree.jsonl files
```

**2. Use QueryEngine for searches**
```python
# Good
query = QueryEngine(tree)
results = query.search_text("auth")

# Less efficient
# Manually filtering nodes in a loop
```

**3. Let BranchManager handle branches**
```python
# Good
manager = BranchManager()
manager.create_branch("test", "Description")

# Avoid
# Manually creating directories and files
```

**4. Handle errors gracefully**
```python
try:
    nodes = tree.load_nodes("nonexistent-branch")
except Exception as e:
    print(f"Error: {e}")
```

---

## Next Steps

- See **ARCHITECTURE.md** for system overview
- See **kt.py** for CLI usage
- See **tools/kt-integration/** for OpenClaw integration
- Build custom tools using these engines!

---

**Status:** Core engines complete and ready for use!
