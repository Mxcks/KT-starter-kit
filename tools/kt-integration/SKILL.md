# KT Integration AgentSkill

Query Knowledge Tree index and ISS for intelligent context discovery.

## Use When

- User mentions KT, Knowledge Tree, or specific branch names
- Questions about projects, branches, or tree structure
- Need context about existing work/systems
- Searching for prior decisions or documentation
- Planning work that might relate to existing projects

## NOT for

- Direct file editing (use OpenClaw file tools)
- Git operations (use github skill)
- Creating/modifying branches (requires approval)

## Installation

This skill is already in your workspace:
```
C:\Users\maxrs\.openclaw\workspace\kt-integration\
```

## Configuration

Edit `config/settings.json` to control behavior:

```json
{
  "auto_preload": false,          // Automatically load context on session start
  "auto_search_on_planning": true, // Search ISS when planning new work
  "auto_load_strategic": true,    // Load strategic layers automatically
  "auto_load_tactical": false,    // Load tactical layers (more tokens)
  "auto_load_implementation": false, // Load implementation layers (heavy)
  "search_threshold": 0.7,        // Relevance threshold for auto-loading
  "max_auto_trees": 3,            // Max trees to auto-load
  "quiet_mode": false             // Don't announce when querying KT
}
```

**Toggle intelligent features:**
```bash
# Turn on session preloading
python tools/kt-config.py --set auto_preload true

# Turn off auto-search (manual only)
python tools/kt-config.py --set auto_search_on_planning false

# Enable quiet mode (query silently)
python tools/kt-config.py --set quiet_mode true
```

## Commands

### Manual Queries

**Query Main Index:**
```bash
# Get KT statistics
python tools/kt-index.py stats

# List all branches
python tools/kt-index.py list

# List by status
python tools/kt-index.py list --status active
python tools/kt-index.py list --status archived

# List by type
python tools/kt-index.py list --type project
python tools/kt-index.py list --type research

# Get specific branch info
python tools/kt-index.py info <branch-id>

# Query tags
python tools/kt-index.py tags
python tools/kt-index.py tags --tag <tag-name>
```

**Query ISS:**
```bash
# Get ISS statistics
python tools/iss-query.py stats

# List all tree summaries
python tools/iss-query.py list

# Get full tree summary
python tools/iss-query.py summary <tree-id>

# Get specific layer
python tools/iss-query.py layer <tree-id> strategic
python tools/iss-query.py layer <tree-id> tactical
python tools/iss-query.py layer <tree-id> implementation

# Search summaries
python tools/iss-query.py search <keyword>

# Get all indexes
python tools/iss-query.py indexes
```

**Intelligent Helper:**
```bash
# Smart context discovery
python tools/kt-smart.py discover --query "authentication system"

# Compare trees
python tools/kt-smart.py compare <tree-id-1> <tree-id-2>

# Suggest related context
python tools/kt-smart.py suggest --task "Build new API"

# Session preload (what auto_preload does)
python tools/kt-smart.py preload
```

## Automatic Behaviors

When enabled via config:

### auto_preload (Session Start)
- Checks focus tree for today's priorities
- Loads relevant strategic layers
- Shows summary of available context

### auto_search_on_planning (Planning Trigger)
- Detects planning keywords: "build", "create", "design", "implement"
- Searches ISS for related trees
- Loads strategic layers if relevance > threshold
- Suggests: "I found related work in [trees]..."

### auto_load_strategic (Context Discovery)
- When tree mentioned, auto-loads strategic layer
- Provides immediate context without asking

### quiet_mode (Silent Queries)
- Queries run in background
- Only speaks up if finds something relevant
- Reduces noise in conversation

## Triggers (What Makes Me Use This)

**Direct mentions:**
- "KT", "Knowledge Tree", "branch"
- Branch names: ui-builder-mcp, research-lab, etc.
- "ISS", "index", "catalog", "tree summary"

**Contextual cues:**
- "Have we worked on X before?"
- "What projects exist?"
- "Show me existing [domain] work"
- Planning new features/systems

**Planning keywords:**
- "build", "create", "design", "implement"
- "new project", "start work on"
- "architecture for", "system for"

## Permission Model

**✅ Automatic (No approval needed):**
- Query KT/ISS anytime
- Load summaries/layers
- Search for keywords
- Read strategic/tactical/implementation context
- Compare trees
- Suggest related work

**❌ Requires approval:**
- Creating/modifying branches
- Deleting nodes
- Sharing KT data externally
- Modifying index/ISS files

## Examples

### Example 1: Manual Query
```
User: "What KT branches are active?"
Macks: <runs: python tools/kt-index.py list --status active>
Response: "1 active branch: test-prism-fix (6 nodes)"
```

### Example 2: Auto-Search (Enabled)
```
User: "Let's build an authentication system"
Macks: <auto-searches ISS for "authentication">
Response: "I found related work in security-patterns tree. Want me to load it?"
```

### Example 3: Auto-Load Strategic (Enabled)
```
User: "Tell me about ui-builder-mcp"
Macks: <auto-loads strategic layer>
Response: "ui-builder-mcp is focused on [strategic summary]..."
```

### Example 4: Quiet Mode (Enabled)
```
User: "Let's work on the API"
Macks: <silently checks ISS for "api">
Macks: <finds api tree, loads strategic layer>
Response: "I see we have existing API architecture. [context]..."
```

## Paths

**Tools location:** `C:\Users\maxrs\.openclaw\workspace\kt-integration\tools\`
**Config location:** `C:\Users\maxrs\.openclaw\workspace\kt-integration\config\`
**KT root:** `C:\dev\KT`
**ISS location:** `C:\dev\KT\index-scrolling-system`

## Version

**Version:** 1.0.0  
**Author:** Max Stern  
**Created:** 2026-03-09
