# Tag Tree Example

**Hierarchical organization of tags across the Knowledge Tree**

---

## What Is A Tag Tree?

A tag tree shows how tags are organized hierarchically, making it easy to:
- Browse related tags
- Understand tag relationships
- Discover tag patterns
- Navigate by category

---

## Example: Starter Kit Tag Tree

```
Knowledge Tree (40 tags)
│
├── 📐 architecture (5 nodes)
│   ├── backend
│   │   ├── api (1 node)
│   │   ├── database (1 node)
│   │   └── auth (2 nodes)
│   │
│   ├── frontend
│   │   ├── ui (1 node)
│   │   └── components
│   │
│   └── patterns
│       ├── fractal (2 nodes)
│       └── layer-system (3 nodes)
│
├── 📚 documentation (4 nodes)
│   ├── overview
│   ├── getting-started
│   ├── details (1 node)
│   └── roadmap (1 node)
│
├── 🔧 implementation (3 nodes)
│   ├── feature (2 nodes)
│   ├── crud (1 node)
│   ├── workflow (2 nodes)
│   └── automation (1 node)
│
├── 🔒 security (2 nodes)
│   ├── auth (2 nodes)
│   ├── encryption
│   └── vulnerability
│
├── 🧪 testing
│   ├── unit
│   ├── integration
│   └── e2e
│
├── 📊 performance
│   ├── optimization
│   ├── caching
│   └── scaling
│
├── 🎯 workflow (2 nodes)
│   ├── summarization (1 node)
│   ├── indexing (1 node)
│   └── discovery (1 node)
│
├── 🏷️ metadata
│   ├── init (3 nodes)
│   ├── example (1 node)
│   ├── simple (1 node)
│   └── ai-optimized (1 node)
│
└── 🔍 discovery
    ├── iss (4 nodes)
    ├── token-efficiency (2 nodes)
    └── missing-features (1 node)
```

---

## Tag Hierarchy By Branch

### system-documentation
```
system-documentation (8 nodes)
├── architecture
│   ├── fractal (2 nodes)
│   └── layer-system (3 nodes)
├── documentation (3 nodes)
├── iss (2 nodes)
├── ai-optimized (1 node)
└── token-efficiency (1 node)
```

### my-auth-service
```
my-auth-service (3 nodes)
├── architecture (1 node)
│   └── auth (1 node)
├── security (2 nodes)
│   └── auth (1 node)
└── implementation (1 node)
```

### iss-workflow-example
```
iss-workflow-example (8 nodes)
├── iss (2 nodes)
├── documentation (4 nodes)
├── architecture (1 node)
├── workflow (2 nodes)
├── discovery (1 node)
└── roadmap (1 node)
```

### example-todo-app
```
example-todo-app (5 nodes)
├── example (1 node)
├── simple (1 node)
├── architecture (1 node)
├── storage (1 node)
├── feature (2 nodes)
├── crud (1 node)
└── ui (1 node)
```

---

## Tag Relationships

### Parent-Child Relationships

**architecture** (parent)
- backend (child)
  - api (grandchild)
  - database (grandchild)
  - auth (grandchild)
- frontend (child)
  - ui (grandchild)
- patterns (child)
  - fractal (grandchild)

**security** (parent)
- auth (child)
- encryption (child)
- vulnerability (child)

**workflow** (parent)
- summarization (child)
- indexing (child)
- discovery (child)

---

## Tag Usage Statistics

```
Tag                    Count  Branches
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
architecture           5      system-documentation, my-auth-service, iss-workflow-example
iss                    4      system-documentation, iss-workflow-example
documentation          4      system-documentation, iss-workflow-example
init                   3      All branches (initialization nodes)
implementation         3      system-documentation, my-auth-service
layer-system           3      system-documentation
feature                2      example-todo-app
token-efficiency       2      system-documentation, iss-workflow-example
workflow               2      iss-workflow-example
security               2      my-auth-service
fractal                2      system-documentation
```

---

## How To Use Tag Trees

### 1. Browse By Category
```bash
# Find all architecture-related work
python tree-query.py tags --query architecture

# Output: Shows all architecture tags and usage
```

### 2. Discover Related Tags
```
Looking at: "authentication"
Related tags in hierarchy:
  - security (parent)
  - auth (sibling)
  - encryption (sibling)
```

### 3. Navigate By Tag
```bash
# Start with broad category
python tree-query.py search "architecture"

# Narrow down to specific area
python tree-query.py search "architecture auth"

# Get specific branch
python tree-query.py branch-info my-auth-service
```

### 4. Tag Consistency Check
```
Common variations found:
  - "auth" vs "authentication" vs "authorize"
  
Recommendation: Standardize on "auth"
Update nodes: [list of nodes to update]
```

---

## Tag Tree Configuration

**File:** `tag-tree.yaml` (example)

```yaml
# Tag hierarchy definition
hierarchy:
  architecture:
    description: "Architectural decisions and patterns"
    children:
      - backend
      - frontend
      - patterns
    
    backend:
      children:
        - api
        - database
        - auth
    
    frontend:
      children:
        - ui
        - components
  
  security:
    description: "Security-related work"
    children:
      - auth
      - encryption
      - vulnerability
    
  implementation:
    description: "Implementation milestones"
    children:
      - feature
      - bugfix
      - optimization

# Tag aliases (for search)
aliases:
  authentication: auth
  authorize: auth
  backend-api: api
  user-interface: ui

# Tag colors (for visualization)
colors:
  architecture: "#3498db"
  security: "#e74c3c"
  implementation: "#2ecc71"
  documentation: "#f39c12"
```

---

## Building Tag Trees

**Automatic generation:**
```bash
# Analyze all branches and generate tag tree
python build-tag-tree.py

# Output: tag-tree.json with hierarchy
```

**Manual definition:**
```yaml
# Create custom tag hierarchy
# File: custom-tag-tree.yaml

my-project-tags:
  features:
    - authentication
    - payments
    - notifications
  
  infrastructure:
    - deployment
    - monitoring
    - scaling
```

---

## Tag Tree Benefits

✅ **Discoverability** - Browse by category instead of searching  
✅ **Consistency** - Standard tag hierarchy enforces consistent tagging  
✅ **Navigation** - Natural hierarchical exploration  
✅ **Relationships** - See how tags relate to each other  
✅ **Aliases** - Multiple ways to find the same thing  
✅ **Visual** - Tree structure is intuitive  

---

## Example Queries Using Tag Tree

**"Show me all backend work"**
```
Query: "backend" (includes children)
Results:
  - backend (direct)
  - api (child of backend)
  - database (child of backend)
  - auth (child of backend)

Total: 5 nodes across 3 branches
```

**"What security work have we done?"**
```
Query: "security" (includes children)
Results:
  - security (direct): 2 nodes
  - auth (child): 2 nodes
  - encryption (child): 0 nodes
  - vulnerability (child): 0 nodes

Total: 4 nodes across 2 branches
```

**"Find all architectural patterns"**
```
Query: "architecture.patterns" (specific path)
Results:
  - fractal: 2 nodes (system-documentation)
  - layer-system: 3 nodes (system-documentation)

Total: 5 nodes in 1 branch
```

---

## Interactive Tag Tree (Future)

**Web UI concept:**
```
[ ] architecture (5)
  [ ] backend (3)
    [✓] api (1) ← expanded
      📄 Define REST API endpoints
    [ ] database (1)
    [✓] auth (2) ← expanded
      📄 Use JWT for authentication
      📄 Implement OAuth2 flow
  [ ] frontend (1)
  [✓] patterns (5) ← expanded
```

Click to expand/collapse branches  
Number shows node count  
Click node to view details

---

**Status:** Tag tree concept documented, awaiting implementation in Phase 2/3

**See also:**
- TREE-INDEX-GUIDE.md - Query existing tags
- LENSES-GUIDE.md - Filter by tags
- BUILD-PLAN.md - Phase 2 includes tag trees
