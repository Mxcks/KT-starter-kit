# KT Integration AgentSkill

**Version:** 1.0.0  
**Author:** Max Stern  
**Created:** 2026-03-09

## Overview

Query Knowledge Tree index and ISS systems with intelligent context discovery and configurable automation.

## Quick Start

### View Current Settings
```bash
python tools/kt-config.py show
```

### Toggle Features
```bash
# Enable smart features
python tools/kt-config.py smart

# Manual mode only
python tools/kt-config.py manual

# Quiet mode (background queries)
python tools/kt-config.py quiet
```

### Manual Queries
```bash
# KT statistics
python tools/kt-index.py stats

# List branches
python tools/kt-index.py list --status active

# ISS statistics
python tools/iss-query.py stats

# Search summaries
python tools/iss-query.py search "authentication"

# Get strategic layer
python tools/iss-query.py layer ui-builder-mcp strategic
```

### Smart Context Discovery
```bash
# Discover related context
python tools/kt-smart.py discover --query "authentication system"

# Suggest context for task
python tools/kt-smart.py suggest --task "Build new API"

# Compare trees
python tools/kt-smart.py compare ui-builder-mcp research-lab

# Preload session context
python tools/kt-smart.py preload
```

## Configuration

Edit `config/settings.json`:

| Setting | Default | Description |
|---------|---------|-------------|
| `auto_preload` | `false` | Load context on session start |
| `auto_search_on_planning` | `true` | Auto-search when planning |
| `auto_load_strategic` | `true` | Auto-load strategic layers |
| `auto_load_tactical` | `false` | Auto-load tactical layers |
| `auto_load_implementation` | `false` | Auto-load implementation layers |
| `search_threshold` | `0.7` | Relevance threshold |
| `max_auto_trees` | `3` | Max trees to auto-load |
| `quiet_mode` | `false` | Silent background queries |

## Tools

| Tool | Purpose |
|------|---------|
| `kt-index.py` | Query main KT index |
| `iss-query.py` | Query ISS system |
| `kt-smart.py` | Intelligent context discovery |
| `kt-config.py` | Configure features |

## Documentation

See `SKILL.md` for complete documentation.

## Paths

- **KT Root:** `C:\dev\KT`
- **ISS:** `C:\dev\KT\index-scrolling-system`
- **Skill:** `C:\Users\maxrs\.openclaw\workspace\kt-integration`

## Permissions

- ✅ **Read:** Query KT/ISS anytime
- ✅ **Execute:** Run tools automatically
- ❌ **Write:** Cannot modify branches/nodes
- ❌ **Network:** No external API calls

## Integration with OpenClaw

This skill is loaded when:
- User mentions "KT", "Knowledge Tree", branch names
- Planning new work (if `auto_search_on_planning` enabled)
- Session starts (if `auto_preload` enabled)

OpenClaw will automatically use these tools to provide better context.

## Publishing

To publish to ClawHub:
```bash
cd kt-integration/
clawhub publish
```

## License

MIT
