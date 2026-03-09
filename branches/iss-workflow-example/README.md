# ISS Workflow Example Branch

**Purpose:** Demonstrate the complete workflow using Branches, Nodes, and ISS

---

## What This Branch Demonstrates

This branch shows how to use the KT Starter Kit's core systems:

1. **Branch System** - Project organization
2. **Node System** - Knowledge capture
3. **ISS (Index Scrolling System)** - Progressive context loading
4. **Query Tools** - Efficient discovery

---

## The Complete Workflow

### Step 1: Create a Branch

```bash
python kt.py init my-project "My project description"
```

**What happens:**
- Creates `branches/my-project/` directory
- Creates `branches/my-project/knowledge/` subdirectory
- Creates initial `tree.jsonl` file with node 0 (init node)

---

### Step 2: Add Nodes as You Work

```bash
# Document a decision
python kt.py add decision "Use PostgreSQL for database" \
  --branch my-project \
  --reasoning "Need ACID compliance and complex queries" \
  --tags "architecture,database"

# Track a milestone
python kt.py add commit "Set up database schema" \
  --branch my-project \
  --tags "database,milestone"

# Add documentation
python kt.py add doc "Database connection uses connection pooling (max 20 connections)" \
  --branch my-project \
  --tags "database,implementation"
```

**What happens:**
- Each command appends a new node to `tree.jsonl`
- Nodes get auto-incremented IDs
- Tags make nodes discoverable

---

### Step 3: Generate ISS Summaries

```bash
cd branches/system-documentation/tools
python kt-hierarchical-summarizer.py --branch my-project
```

**What happens:**
- Analyzes all nodes in the branch
- Groups nodes by type and depth
- Generates 3 markdown files:
  - `strategic.md` (~800 tokens) - High-level overview
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

### Step 4: Update ISS Indexes

```bash
python iss-hierarchical-indexer.py
```

**What happens:**
- Scans all summary directories
- Creates fast-lookup indexes:
  - `hierarchical-summaries.json` - All summaries by tree
  - `by-layer.json` - Grouped by layer
  - `quick-access.json` - Fast lookups by tree
  - `stats.json` - Statistics

**Output location:**
```
index-scrolling-system/meta-tree/index/
```

---

### Step 5: Query via ISS

```bash
cd ../../../  # Back to root

# Search for relevant branches
python tools/kt-integration/tools/iss-query.py search "database"

# Load strategic layer (cheap!)
python tools/kt-integration/tools/iss-query.py layer my-project strategic

# If relevant, load tactical
python tools/kt-integration/tools/iss-query.py layer my-project tactical

# If coding, load implementation
python tools/kt-integration/tools/iss-query.py layer my-project implementation
```

**Result:**
- Progressive loading saves tokens
- Load only what you need
- Scan many projects cheaply

---

## Understanding the Layers

### Strategic Layer (~800 tokens)
**Content:**
- Branch purpose
- Key architectural decisions
- Major technologies chosen
- High-level patterns

**Use case:**
- "Is this project relevant?"
- Scanning 30+ projects
- Architectural review
- Initial discovery

**Example:**
```markdown
# My-Project - Strategic Layer

**Purpose:** Web application for task management

**Key Decisions:**
- Use PostgreSQL for database (ACID compliance needed)
- ...

**Architecture:**
- REST API backend
- React frontend
- ...
```

---

### Tactical Layer (~3,200 tokens)
**Content:**
- Module organization
- Implementation strategies
- Component relationships
- Technical approaches

**Use case:**
- "How is it structured?"
- Planning changes
- Understanding architecture
- Design review

**Example:**
```markdown
# My-Project - Tactical Layer

**Modules:**
- Database layer: Connection pooling (max 20)
- API layer: Express.js with JWT auth
- ...

**Implementation Approach:**
- Database schema migrations via Knex
- ...
```

---

### Implementation Layer (~18,000 tokens)
**Content:**
- Specific files and paths
- Code snippets
- Detailed utilities
- Edge cases and gotchas

**Use case:**
- "Show me the code"
- Actual coding
- Debugging issues
- Deep dive

**Example:**
```markdown
# My-Project - Implementation Layer

**Database Files:**
- `src/db/connection.js` - Connection pool setup
- `src/db/migrations/` - Schema migrations
- ...

**Code Details:**
- Connection pool config: min 5, max 20, idle timeout 10s
- ...
```

---

## Token Efficiency Math

**Traditional approach:**
```
Load full project → 25,000 tokens
Fit in context: 1-2 projects max (with 200K token limit)
```

**ISS approach:**
```
Load strategic only → 800 tokens per project
Fit in context: 30+ projects!
Drill down only if relevant → Load tactical (3,200) or implementation (18,000)
```

**Example scenario:**
You have 50 projects and need to find all authentication-related code.

**Traditional:** Can't load all 50 (50 × 25k = 1.25M tokens)
**ISS:** Load all 50 strategic layers (50 × 800 = 40K tokens)
- Find 3 relevant projects
- Load tactical for those 3 (3 × 3,200 = 9,600 tokens)
- Total: 49,600 tokens vs. 1,250,000 tokens
- **Savings: 96%**

---

## What We DON'T Have (Yet)

### Lens System ❌
**What it is:**
Domain-specific views of the tree (security, API, architecture, debugging, testing, etc.)

**Example lens (security-lens.json):**
```json
{
  "name": "Security Review",
  "filters": {
    "tags": ["security", "auth", "encryption"],
    "node_types": ["decision", "documentation"]
  },
  "grouping": "by_tag",
  "output": "security-review.md"
}
```

**What it does:**
- Filters nodes by criteria
- Groups related nodes
- Generates focused views
- Helps with code review, onboarding, debugging

**Status:** Not in starter kit (could be added in Phase 2)

---

### Tag Trees ❌
**What it is:**
Hierarchical organization of tags

**Example (tag-tree.yaml):**
```yaml
architecture:
  - backend:
    - api
    - database
    - cache
  - frontend:
    - ui
    - state-management
  - infrastructure:
    - deployment
    - monitoring
```

**What it does:**
- Organizes tags hierarchically
- Enables tag inheritance
- Improves discoverability
- Creates tag-based navigation

**Status:** Not in starter kit (could be added in Phase 2)

---

### Core Engine ❌
**What it is:**
Full tree management system

**Components:**
- `tree_engine.py` - CRUD operations on nodes
- `branch_manager.py` - Branch lifecycle management
- `query_engine.py` - Advanced search capabilities

**What it does:**
- Update/delete nodes (we only have create)
- Complex queries (AND/OR/NOT conditions)
- Cross-branch searches
- Node relationships/linking

**Status:** Not in starter kit (Phase 2 in BUILD-PLAN.md)

---

### Orchestrator ❌
**What it is:**
Task automation and execution layer

**What it does:**
- Queries KT for priority tasks
- Executes automated workflows
- Tracks manual tasks
- Scrum/sprint management

**Status:** Not in starter kit (Phase 3+)

---

## What We DO Have ✅

### 1. Branch System
- Organize projects as branches
- Each branch has `knowledge/tree.jsonl`
- Create via `kt.py init`

### 2. Node System
- Capture knowledge as nodes
- Types: init, decision, commit, documentation, summary, blocker
- Create via `kt.py add`
- JSONL format (one JSON per line)

### 3. ISS (Index Scrolling System)
- Generate 3-layer summaries
- Progressive context loading
- Fast discovery via indexes
- 97% token savings

### 4. Query Tools (kt-integration)
- Search across branches
- Load specific layers
- Statistics and discovery
- OpenClaw integration

### 5. CLI (kt.py)
- Create branches: `kt init`
- Add nodes: `kt add`
- View branches: `kt list`
- View nodes: `kt tree`

---

## Example Use Cases

### Use Case 1: Starting a New Project

```bash
# Create branch
python kt.py init payment-service "Payment processing microservice"

# Document initial decisions
python kt.py add decision "Use Stripe for payment processing" \
  --branch payment-service \
  --reasoning "PCI compliance handled, good API, popular" \
  --tags "architecture,payments,third-party"

python kt.py add decision "Use PostgreSQL with row-level security" \
  --branch payment-service \
  --reasoning "ACID transactions critical for payments" \
  --tags "architecture,database,security"

# Track progress
python kt.py add commit "Set up Stripe integration" \
  --branch payment-service \
  --tags "payments,milestone"

# Generate summaries when ready
cd branches/system-documentation/tools
python kt-hierarchical-summarizer.py --branch payment-service
python iss-hierarchical-indexer.py
```

---

### Use Case 2: Finding Related Work

```bash
# You're working on authentication
# Find all auth-related projects

# Search ISS
python tools/kt-integration/tools/iss-query.py search "authentication"

# Returns list of branches with auth work
# Load strategic layers to see if relevant
python tools/kt-integration/tools/iss-query.py layer user-service strategic
python tools/kt-integration/tools/iss-query.py layer api-gateway strategic

# Found relevant project? Load more detail
python tools/kt-integration/tools/iss-query.py layer user-service tactical
```

---

### Use Case 3: Onboarding New Team Member

```bash
# They need to understand the architecture

# Get overview of all projects (cheap!)
for branch in $(python kt.py list | tail -n +3 | awk '{print $1}'); do
  python tools/kt-integration/tools/iss-query.py layer $branch strategic
done

# Total tokens: ~800 per project
# Can understand 20+ projects in one read!

# Want details on specific project?
python tools/kt-integration/tools/iss-query.py layer core-api tactical
```

---

## Next Steps

### Try It Yourself

1. **Create your own branch:**
   ```bash
   python kt.py init my-test-project "Testing the workflow"
   ```

2. **Add some nodes:**
   ```bash
   python kt.py add decision "Your decision" --branch my-test-project
   python kt.py add commit "Your milestone" --branch my-test-project
   ```

3. **Generate summaries:**
   ```bash
   cd branches/system-documentation/tools
   python kt-hierarchical-summarizer.py --branch my-test-project
   python iss-hierarchical-indexer.py
   ```

4. **Query it:**
   ```bash
   cd ../../..
   python tools/kt-integration/tools/iss-query.py layer my-test-project strategic
   ```

### Learn More

- **QUICKSTART.md** - Step-by-step tutorial
- **ARCHITECTURE.md** - Complete system documentation
- **CONTRIBUTING.md** - Extend the system
- **BUILD-PLAN.md** - Future roadmap (lenses, tag-trees, core engine)

---

## Summary

**What this branch taught you:**

✅ How branches organize projects  
✅ How nodes capture knowledge  
✅ How ISS generates summaries  
✅ How progressive loading works  
✅ How queries discover context  
✅ What's missing (lenses, tag-trees, core engine)  
✅ Real workflow from start to finish  

**The innovation:**
97% token savings through 3-layer progressive loading!

**Next:** Create your own branches and see the benefits! 🚀
