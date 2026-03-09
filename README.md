# Knowledge Tree Starter Kit

**AI-optimized hierarchical documentation with fractal 3-layer structure**

[![Token Efficiency](https://img.shields.io/badge/Token_Savings-97%25-brightgreen)]()
[![License](https://img.shields.io/badge/License-MIT-blue)]()

---

## 🚀 What Is This?

Knowledge Tree Starter Kit provides a **fractal documentation system** that enables token-efficient AI context loading.

**The Innovation:** 3-layer hierarchical documentation
- **Strategic** (800 tokens) → High-level architecture & decisions
- **Tactical** (3,200 tokens) → Implementation approaches & modules  
- **Implementation** (18,000 tokens) → Specific code & details

**The Impact:** 97% token savings - AI can scan 30+ projects in the same token budget as loading 1 full tree.

---

## 💡 Why Token Efficiency Matters

**Traditional approach:**
```
Load full codebase → 500,000 tokens → Can't fit in AI context
```

**Fractal approach:**
```
Load strategic layers only → 15,000 tokens → Entire codebase fits!
Need details? → Load tactical/implementation progressively
```

**Real-world benefit:** Your AI assistant can understand your entire organization's architecture in a single conversation.

---

## ⚡ Quick Start

### 1. Install

```bash
git clone https://github.com/Mxcks/KT-starter-kit.git
cd kt-starter-kit
pip install -r requirements.txt  # (no dependencies currently!)
```

### 2. Create Your First Project

```bash
# Initialize a project
python kt.py init my-first-project "Learning Knowledge Tree"

# Add nodes as you work
python kt.py add decision "Use Python for backend" --branch my-first-project \
  --reasoning "Team expertise, great libraries"

python kt.py add commit "Set up project structure" --branch my-first-project

# View your work
python kt.py tree my-first-project
```

### 3. Generate Fractal Summaries

```bash
# Generate 3-layer summaries
python branches/system-documentation/tools/kt-hierarchical-summarizer.py --branch my-first-project

# Update ISS indexes
python branches/system-documentation/tools/iss-hierarchical-indexer.py
```

### 4. Query via AI

```bash
# Search for context
python tools/kt-integration/tools/iss-query.py search "python"

# Load strategic layer (97% token savings!)
python tools/kt-integration/tools/iss-query.py layer my-first-project strategic
```

---

## 📚 What's Included

### 🎯 The Fractal Documentation System

**Location:** `branches/system-documentation/`

A complete operational branch demonstrating the 3-layer pattern:
- 8 nodes explaining the system
- 4 automation tools included
- Pre-generated ISS summaries
- **Meta:** The branch uses its own pattern to document itself!

**Tools:**
1. **kt-hierarchical-summarizer.py** - Generate 3-layer summaries
2. **iss-hierarchical-indexer.py** - Update ISS indexes
3. **kt-intelligent-loader.py** - Smart context discovery
4. **kt-tool-node-generator.py** - Tool scanning with local LLM

### 🔧 kt-integration (OpenClaw Skill)

**Location:** `tools/kt-integration/`

Query tools for OpenClaw with intelligent automation:
- Query KT index and ISS systems
- Auto-search when planning
- Auto-load strategic layers
- Configurable on/off switches

### 🗂️ Core KT System

**Coming soon:** Core KT engine, CLI, branch management
- Tree-based context management
- Branch system for distributed workspaces
- Query engine for cross-project search
- Sync system for team collaboration

---

## 🎓 How To Use

### Scenario 1: Planning a New Feature

```bash
# AI assistant searches for related work
python tools/kt-integration/tools/kt-smart.py discover --query "authentication API"

# Loads strategic layers of relevant projects
# Shows: "Found 3 related projects: auth-service, api-gateway, user-management"
# Token cost: ~2,400 tokens (vs 75,000 for full trees)
```

### Scenario 2: Code Review

```bash
# Load tactical + implementation for specific module
python tools/kt-integration/tools/iss-query.py layer my-project tactical
python tools/kt-integration/tools/iss-query.py layer my-project implementation

# Focused context on just what's being reviewed
# Token cost: ~7,000 tokens (vs 25,000 for full tree)
```

### Scenario 3: Architecture Decision

```bash
# Compare strategic layers across multiple projects
python tools/kt-integration/tools/iss-query.py search "database architecture"

# Cross-project architectural analysis
# Token cost: ~5,000 tokens for 5 projects (vs 125,000)
```

---

## 📊 Token Efficiency Examples

| Scenario | Traditional | Fractal | Savings |
|----------|-------------|---------|---------|
| Understand 1 project | 25,000 tokens | 800 tokens | **97%** |
| Scan 5 projects | 125,000 tokens | 4,000 tokens | **97%** |
| Scan entire codebase (30 projects) | 750,000 tokens | 24,000 tokens | **97%** |
| Planning + deep dive (3 projects) | 75,000 tokens | 12,000 tokens | **84%** |

---

## 🏗️ Architecture

```
KT Nodes (JSONL)
    ↓
kt-hierarchical-summarizer.py
    ↓
3-Layer Markdown Summaries
    ├── strategic.md (800 tokens)
    ├── tactical.md (3,200 tokens)
    └── implementation.md (18,000 tokens)
    ↓
iss-hierarchical-indexer.py
    ↓
ISS Indexes (fast lookups)
    ↓
kt-intelligent-loader.py
    ↓
Auto-Discovery & Context Loading
```

---

## 🎯 Use Cases

### For Solo Developers
- Manage multiple projects without losing context
- Progressive learning curve (strategic → tactical → implementation)
- Quick refreshers on old projects

### For Teams
- Onboard new members efficiently
- Share architectural decisions
- Maintain consistency across projects
- Cross-project pattern analysis

### For AI Assistants
- Understand entire codebases
- Smart context loading
- Token-efficient cross-project analysis
- Progressive detail as needed

---

## 🔧 Configuration

### Environment Variables

```bash
# Set your KT root
export KT_ROOT=/path/to/kt-starter-kit

# Optional: Custom ISS location
export ISS_ROOT=/custom/path
```

### kt-integration Settings

Edit `tools/kt-integration/config/settings.json`:

```json
{
  "auto_preload": false,              // Load context on session start
  "auto_search_on_planning": true,    // Auto-search when planning
  "auto_load_strategic": true,        // Auto-load strategic layers
  "quiet_mode": false                 // Silent queries
}
```

**Toggle features:**
```bash
# Enable smart mode
python tools/kt-integration/tools/kt-config.py smart

# Manual mode only
python tools/kt-integration/tools/kt-config.py manual
```

---

## 📖 Documentation

- **[System Documentation Branch](branches/system-documentation/README.md)** - Complete fractal docs guide
- **[kt-integration Skill](tools/kt-integration/SKILL.md)** - OpenClaw integration
- **[Publishing Guide](PUBLISHING.md)** - How to customize and publish

---

## 🚧 Roadmap

### Phase 1 (Current)
- ✅ Fractal documentation system
- ✅ system-documentation operational branch
- ✅ kt-integration OpenClaw skill
- ✅ ISS integration

### Phase 2 (Next)
- [ ] Core KT engine integration
- [ ] CLI tools (kt.py)
- [ ] Branch management system
- [ ] More operational branches (templates, examples)

### Phase 3 (Future)
- [ ] MCP server for universal AI access
- [ ] VS Code extension
- [ ] Team collaboration features
- [ ] CI/CD integrations

---

## 🤝 Contributing

Contributions welcome! Areas of interest:
- Additional operational branches (templates, patterns)
- Language-specific analyzers (Python, TypeScript, etc.)
- Custom layer definitions
- Integration with other AI tools

---

## 📝 License

MIT License - See [LICENSE](LICENSE) for details

---

## 💬 Community

- **Issues:** [GitHub Issues](https://github.com/yourusername/kt-starter-kit/issues)
- **Discord:** [Join our community](#) (coming soon)
- **Docs:** [Full documentation](#) (coming soon)

---

## 🙏 Credits

**Created by:** Max Stern  
**Inspiration:** Need for token-efficient AI context in large codebases  
**Special Thanks:** Knowledge Tree community

---

## ⭐ Star This Repo!

If you find this useful, give it a star! It helps others discover token-efficient AI context management.

---

**Ready to optimize your AI context? Clone and start with strategic layers!** 🚀

```bash
git clone https://github.com/yourusername/kt-starter-kit.git
cd kt-starter-kit
python tools/kt-integration/tools/kt-smart.py preload
```
