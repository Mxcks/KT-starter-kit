# Lens System Guide

**Lenses provide domain-specific views of your Knowledge Tree**

---

## What Are Lenses?

Lenses are filters that help you view your branches through different perspectives:
- **Security Lens** - All security-related decisions and implementations
- **API Lens** - API endpoints, contracts, and changes
- **Architecture Lens** - Architectural decisions and patterns
- **Debugging Lens** - Known issues, workarounds, and fixes
- **Testing Lens** - Test coverage, strategies, and gaps

---

## How Lenses Work

```
All Nodes (branches/*/knowledge/tree.jsonl)
    ↓
Filter by tags, types, criteria
    ↓
Group by category
    ↓
Generate focused view
```

---

## Built-in Lenses

Located in `lenses/builtin/`:

### 1. Security Lens (`security-lens.json`)
**Filters:**
- Tags: security, auth, encryption, vulnerability
- Node types: decision, documentation

**Use cases:**
- Security audits
- Compliance reviews
- Threat modeling

**Example output:**
```markdown
# Security Decisions
- [Branch: api-gateway] Use JWT with short expiry (5 min)
- [Branch: user-service] Encrypt PII at rest with AES-256

# Security Issues
- [Branch: payment-service] Known: Rate limiting not implemented
```

---

###2. API Lens (`api-lens.json`)
**Filters:**
- Tags: api, endpoint, contract, breaking-change
- Node types: decision, commit, documentation

**Use cases:**
- API documentation
- Breaking change tracking
- Endpoint discovery

**Example output:**
```markdown
# API Endpoints
- POST /api/v1/users - Create user
- GET /api/v1/users/:id - Get user details

# Breaking Changes
- [2026-03-01] Changed authentication from cookie to header
```

---

### 3. Architecture Lens (`architecture-lens.json`)
**Filters:**
- Tags: architecture, design, pattern, decision
- Node types: decision

**Use cases:**
- Architectural review
- Design documentation
- Pattern discovery

---

### 4. Debugging Lens (`debugging-lens.json`)
**Filters:**
- Tags: bug, issue, workaround, fix, blocker
- Node types: blocker, commit, documentation

**Use cases:**
- Known issues list
- Debugging guides
- Workaround documentation

---

### 5. Testing Lens (`testing-lens.json`)
**Filters:**
- Tags: test, coverage, qa, e2e, unit
- Node types: commit, documentation

**Use cases:**
- Test coverage reports
- Testing strategy
- QA documentation

---

### 6. Performance Lens (`performance-lens.json`)
**Filters:**
- Tags: performance, optimization, caching, scaling
- Node types: decision, commit

**Use cases:**
- Performance optimization
- Scaling strategies
- Bottleneck identification

---

### 7. Onboarding Lens (`onboarding-lens.json`)
**Filters:**
- Tags: getting-started, setup, prerequisites, documentation
- Node types: documentation

**Use cases:**
- New team member onboarding
- Setup guides
- Prerequisites documentation

---

### 8. Recent Activity Lens (`recent-activity-lens.json`)
**Filters:**
- Time-based: Last 30 days
- All node types

**Use cases:**
- What's changed recently
- Active development areas
- Recent decisions

---

### 9. Project Mapping Lens (`project-mapping-lens.json`)
**Filters:**
- Groups by branch/project
- Shows relationships

**Use cases:**
- Project overview
- Cross-project dependencies
- Team coordination

---

## Creating Custom Lenses

### Step 1: Define the Lens

Create `lenses/custom/my-lens.json`:

```json
{
  "name": "My Custom Lens",
  "version": "1.0",
  "description": "Description of what this lens shows",
  
  "filters": {
    "tags": {
      "include": ["tag1", "tag2"],
      "exclude": ["exclude1"]
    },
    "node_types": {
      "include": ["decision", "commit"]
    },
    "time_range": {
      "days": 30
    }
  },
  
  "grouping": {
    "by": "branch",
    "sort": "timestamp_desc"
  },
  
  "output": {
    "format": "markdown",
    "template": "default",
    "include_metadata": true
  },
  
  "use_cases": [
    "When you need to...",
    "Helps with..."
  ]
}
```

### Step 2: Apply the Lens

**Option A: Manual filtering** (current starter kit)

```python
# Read all nodes
nodes = []
for branch in os.listdir('branches/'):
    tree_file = f'branches/{branch}/knowledge/tree.jsonl'
    if os.path.exists(tree_file):
        with open(tree_file) as f:
            for line in f:
                nodes.append(json.loads(line))

# Apply lens filters
filtered = [
    n for n in nodes
    if any(tag in n.get('tags', []) for tag in ['security', 'auth'])
    and n.get('type') in ['decision', 'documentation']
]

# Group and output
for node in sorted(filtered, key=lambda x: x.get('timestamp', '')):
    print(f"[{node['type']}] {node['message']}")
```

**Option B: Lens CLI** (future enhancement)

```bash
# Apply built-in lens
python lenses/lens_cli.py apply security --all-branches

# Apply custom lens
python lenses/lens_cli.py apply custom/my-lens --branch my-project

# List available lenses
python lenses/lens_cli.py list
```

---

## Lens Use Cases

### Security Audit
```bash
# Apply security lens across all branches
python lenses/lens_cli.py apply security --all-branches > security-audit.md

# Review all security decisions
# Identify missing encryption
# Check authentication patterns
```

### API Documentation
```bash
# Generate API documentation from nodes
python lenses/lens_cli.py apply api --branch api-gateway > api-docs.md

# Outputs:
# - All endpoints
# - Request/response formats
# - Authentication requirements
# - Breaking changes
```

### Onboarding New Developer
```bash
# Generate onboarding guide
python lenses/lens_cli.py apply onboarding --all-branches > onboarding.md

# They get:
# - Setup instructions from all projects
# - Architecture decisions
# - Getting started guides
```

### Finding Related Work
```bash
# "I'm working on authentication, what exists?"
python lenses/lens_cli.py apply security --filter auth

# Shows all auth-related nodes across all projects
```

---

## Tag Trees (Related Concept)

**Tag Trees** organize tags hierarchically for better discovery.

**Example hierarchy:**
```yaml
architecture:
  backend:
    - api
    - database
    - cache
  frontend:
    - ui
    - state-management
    - components
  infrastructure:
    - deployment
    - monitoring
    - scaling

implementation:
  features:
    - authentication
    - payments
    - notifications
  fixes:
    - bug-fix
    - hotfix
    - workaround
```

**Benefits:**
- Browse tags hierarchically
- Discover related tags
- Consistent tagging across projects
- Improved search

**Status in Starter Kit:**
❌ Not yet implemented
✅ Could be added in Phase 2/3

**Where it would live:**
- `tag-tree.yaml` - Global tag hierarchy
- Per-branch `summaries/[branch]/tag-tree.json` - Branch-specific tags

---

## Current Status in Starter Kit

**✅ What We Have:**
- 9 built-in lenses (JSON definitions)
- `lenses/builtin/` directory
- `lenses/custom/` directory for your lenses
- Lens definitions with filters, grouping, output specs

**❌ What We Don't Have Yet:**
- Lens CLI (`lens_cli.py`) - Apply lenses from command line
- Lens analyzer - Generate views automatically
- Tag trees - Hierarchical tag organization
- Lens templates - Reusable patterns

**📋 How to Use Currently:**
1. View lens definitions in `lenses/builtin/`
2. Manually filter nodes based on lens criteria
3. Use as reference for what to look for
4. Build your own scripts using lens definitions

**🔮 Future (Phase 2/3):**
1. Lens CLI tool
2. Automatic lens application
3. Tag tree system
4. Lens templates and patterns

---

## Example: Manual Lens Application

**Task:** Find all security decisions across all branches

```python
import json
import os
from pathlib import Path

# Load security lens definition
with open('lenses/builtin/security-lens.json') as f:
    lens = json.load(f)

security_tags = lens['filters']['tags']['include']
node_types = lens['filters']['node_types']['include']

# Collect matching nodes
matches = []
for branch_dir in Path('branches').iterdir():
    if not branch_dir.is_dir():
        continue
    
    tree_file = branch_dir / 'knowledge' / 'tree.jsonl'
    if not tree_file.exists():
        continue
    
    with open(tree_file) as f:
        for line in f:
            node = json.loads(line)
            
            # Apply lens filters
            node_tags = node.get('tags', [])
            if (any(tag in node_tags for tag in security_tags) and
                node.get('type') in node_types):
                
                node['_branch'] = branch_dir.name
                matches.append(node)

# Output
print(f"# Security Lens Results\n")
print(f"Found {len(matches)} matching nodes\n")

for node in sorted(matches, key=lambda x: x.get('timestamp', '')):
    print(f"## [{node['_branch']}] {node['message']}")
    if 'reasoning' in node:
        print(f"   Reasoning: {node['reasoning']}")
    print()
```

---

## Contributing

**Want to add a lens?**

1. Create `lenses/custom/your-lens.json`
2. Define filters and grouping
3. Document use cases
4. Test with your branches
5. Submit PR!

**See:** CONTRIBUTING.md for guidelines

---

## Resources

- **Lens definitions:** `lenses/builtin/*.json`
- **Custom lenses:** `lenses/custom/` (add yours here!)
- **Examples:** `branches/iss-workflow-example/README.md`
- **Architecture:** ARCHITECTURE.md

---

**Summary:** Lenses help you see your Knowledge Tree from different perspectives. Use them for audits, documentation, discovery, and focused views!
