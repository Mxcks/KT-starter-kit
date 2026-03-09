# Contributing to KT Starter Kit

**Thank you for your interest in contributing!**

We welcome contributions of all kinds: bug fixes, new features, documentation improvements, examples, and more.

---

## 🌟 Ways to Contribute

### 1. **Use It & Give Feedback**
- Try the system with your projects
- Report issues or confusing documentation
- Share your use cases
- Suggest improvements

### 2. **Improve Documentation**
- Fix typos or unclear explanations
- Add examples or tutorials
- Translate documentation
- Create video walkthroughs

### 3. **Add Features**
- Extend the CLI with new commands
- Add new summarization layers
- Build integrations (VS Code, Obsidian, etc.)
- Create visualization tools

### 4. **Share Operational Branches**
- Create reusable templates
- Share example projects
- Document design patterns
- Contribute domain-specific analyzers

### 5. **Fix Bugs**
- Report issues with clear reproduction steps
- Submit fixes with tests
- Improve error handling

---

## 🚀 Getting Started

### Prerequisites

```bash
# Clone the repository
git clone https://github.com/Mxcks/KT-starter-kit.git
cd kt-starter-kit

# Python 3.8+ required
python --version

# No external dependencies currently!
pip install -r requirements.txt
```

### Understanding the System

Before contributing code:

1. **Read QUICK-REFERENCE.md** (5 min) - Understand the basics
2. **Read ARCHITECTURE.md** (30 min) - Understand the system deeply
3. **Try the QUICKSTART** (15 min) - Get hands-on experience
4. **Explore the code** - Read docstrings and comments

**Key files to understand:**
- `kt.py` - CLI and node management
- `branches/system-documentation/tools/kt-hierarchical-summarizer.py` - Summarization logic
- `branches/system-documentation/tools/iss-hierarchical-indexer.py` - Indexing logic
- `tools/kt-integration/` - OpenClaw integration

---

## 📋 Contribution Guidelines

### Code Style

**Python:**
- Follow PEP 8 style guide
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use type hints where helpful
- Write docstrings for all functions/classes

**Example:**
```python
def add_node(branch_name: str, node_type: str, message: str,
             reasoning: Optional[str] = None) -> Dict[str, Any]:
    """
    Add a node to a branch
    
    Args:
        branch_name: Branch to add to
        node_type: Type of node (decision, commit, etc.)
        message: Node message
        reasoning: Optional reasoning (for decisions)
        
    Returns:
        Created node dictionary
        
    Raises:
        ValueError: If branch doesn't exist
    """
    # Implementation here
```

**Markdown:**
- Use consistent heading levels
- Include code examples with syntax highlighting
- Keep lines under 120 characters when possible
- Use tables for structured data

**JSONL:**
- One JSON object per line
- Consistent field ordering: id, type, branch, message, timestamp, tags
- ISO 8601 timestamps with 'Z' suffix
- UTF-8 encoding

---

## 🔧 Development Workflow

### 1. Fork & Clone

```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR-USERNAME/KT-starter-kit.git
cd kt-starter-kit
git remote add upstream https://github.com/Mxcks/KT-starter-kit.git
```

### 2. Create a Branch

```bash
# Use descriptive branch names
git checkout -b feature/add-export-command
git checkout -b fix/windows-encoding-issue
git checkout -b docs/improve-quickstart
```

**Branch naming:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation only
- `refactor/` - Code improvements
- `test/` - Test additions

### 3. Make Changes

**Write clear, focused commits:**
```bash
git add file1.py file2.md
git commit -m "feat: Add export command to kt.py CLI

- Implement export_branch() method
- Add --format json|markdown option
- Update help text and documentation
- Fixes #42"
```

**Commit message format:**
```
type: Short description (50 chars max)

- Longer explanation if needed
- Bullet points for multiple changes
- Reference issues: Fixes #123, Relates to #456
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

### 4. Test Your Changes

```bash
# Test CLI commands
python kt.py init test-branch "Test branch"
python kt.py add decision "Test decision" --branch test-branch
python kt.py tree test-branch

# Test summarization
python branches/system-documentation/tools/kt-hierarchical-summarizer.py --branch test-branch

# Test queries
python tools/kt-integration/tools/iss-query.py stats
```

**Testing checklist:**
- [ ] Commands execute without errors
- [ ] Output is correct and well-formatted
- [ ] Edge cases handled (empty branches, missing files, etc.)
- [ ] Windows compatibility (if applicable)
- [ ] Documentation updated

### 5. Update Documentation

**For new features:**
- Update relevant .md files
- Add examples to QUICKSTART.md
- Update QUICK-REFERENCE.md command list
- Add to ARCHITECTURE.md if it's a major component

**For bug fixes:**
- Update documentation if behavior changed
- Add troubleshooting section if helpful

### 6. Submit Pull Request

```bash
# Sync with upstream
git fetch upstream
git rebase upstream/main

# Push to your fork
git push origin feature/add-export-command
```

**On GitHub:**
1. Create Pull Request
2. Use the template below
3. Link related issues
4. Request review

**PR Template:**
```markdown
## Description
Brief description of what this PR does

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Other (specify)

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing Done
- [ ] Tested on Windows
- [ ] Tested on macOS/Linux
- [ ] Updated documentation
- [ ] Added examples

## Related Issues
Fixes #123
Relates to #456

## Screenshots (if applicable)
```

---

## 🎯 Contribution Ideas

### Easy / Good First Issues

**Documentation:**
- [ ] Add more examples to QUICKSTART.md
- [ ] Create troubleshooting guide
- [ ] Improve error messages
- [ ] Add animated GIFs showing workflows
- [ ] Translate documentation to other languages

**Small Features:**
- [ ] Add `kt.py delete` command for removing nodes
- [ ] Add `kt.py edit` command for updating nodes
- [ ] Add `kt.py export` command (JSON, Markdown, HTML)
- [ ] Improve output formatting with colors
- [ ] Add progress indicators for long operations

### Medium Difficulty

**New Features:**
- [ ] Add tag management commands
- [ ] Implement node search within branches
- [ ] Add branch archiving/unarchiving
- [ ] Create branch templates system
- [ ] Build visualization tool (ASCII tree, HTML)
- [ ] Add batch operations (add multiple nodes from file)

**Integrations:**
- [ ] VS Code extension
- [ ] Obsidian plugin
- [ ] Notion integration
- [ ] GitHub Actions workflow
- [ ] Git hooks for auto-node creation

**Tools:**
- [ ] Web UI for browsing branches
- [ ] Dashboard for statistics
- [ ] Diff tool for comparing branches
- [ ] Merge tool for combining branches

### Advanced / Experimental

**Core Engine:**
- [ ] Add full tree_engine.py (Phase 2 from BUILD-PLAN.md)
- [ ] Implement query_engine.py for advanced searches
- [ ] Add branch_manager.py for operations
- [ ] Build sync system for team collaboration

**AI/LLM Features:**
- [ ] MCP server implementation
- [ ] Semantic search with embeddings
- [ ] Auto-tagging with LLMs
- [ ] Smart summary generation improvements
- [ ] Multi-language summarization

**Advanced Features:**
- [ ] Plugin/extension system
- [ ] REST API server
- [ ] GraphQL API
- [ ] WebSocket for real-time updates
- [ ] Distributed/federated branches

---

## 🏗️ Extension Points

### 1. Adding New Node Types

**Location:** `kt.py` line ~230

```python
# Add to the choices list
add_parser.add_argument('type', 
    choices=['decision', 'commit', 'doc', 'summary', 'blocker', 'YOUR_TYPE'],
    help='Node type')
```

**Then update summarizer to handle it:**
`branches/system-documentation/tools/kt-hierarchical-summarizer.py`

### 2. Adding New Summarization Layers

**Location:** `kt-hierarchical-summarizer.py`

```python
def generate_custom_layer(self, nodes: List[Dict]) -> str:
    """Generate your custom layer"""
    # Your logic here
    pass

# Add to generate_all_layers()
self.layers['custom'] = self.generate_custom_layer(nodes)
```

### 3. Adding New Query Commands

**Location:** `tools/kt-integration/tools/iss-query.py`

```python
def custom_query(args):
    """Your custom query logic"""
    # Implementation
    pass

# Add to main()
elif args.command == 'custom':
    custom_query(args)
```

### 4. Creating New Operational Branches

**Structure:**
```
branches/your-operational-branch/
├── README.md              # Explain the pattern
├── knowledge/
│   └── tree.jsonl         # Example nodes
└── tools/                 # Optional automation scripts
    └── your-tool.py
```

**Then:**
1. Generate summaries for your branch
2. Add to system catalog
3. Document in ARCHITECTURE.md
4. Submit as PR

### 5. Building Integrations

**kt-integration as example:**
```python
# Your integration structure
your-integration/
├── SKILL.md               # How to use
├── config/
│   └── settings.json      # Configuration
└── tools/
    ├── tool1.py
    └── tool2.py
```

---

## 🧪 Testing Guidelines

### Manual Testing

**Before submitting PR:**
1. Test on your target platform (Windows/macOS/Linux)
2. Test with fresh repository clone
3. Test with example branches
4. Test error cases (missing files, invalid input)
5. Test with large branches (100+ nodes)

### Test Cases to Cover

**CLI commands:**
- Create branch with valid/invalid names
- Add nodes with all combinations of optional fields
- List branches when empty/populated
- View tree with 0/1/many nodes
- Handle special characters in messages
- Handle very long messages

**Summarization:**
- Branches with 0/1/few/many nodes
- All node types
- Missing optional fields
- Unicode/emoji in content
- Very large content fields

**Queries:**
- Empty indexes
- Single result
- Many results
- No matches
- Special characters in search

### Future: Automated Tests

We plan to add pytest-based tests. Structure:
```
tests/
├── test_cli.py
├── test_summarizer.py
├── test_indexer.py
└── test_queries.py
```

Contributions adding tests are very welcome!

---

## 📝 Documentation Standards

### Writing Style

- **Clear and concise** - Avoid jargon
- **Action-oriented** - Use imperative mood ("Do this" not "You can do this")
- **Examples first** - Show, then explain
- **Progressive detail** - Simple overview → detailed explanation
- **Beginner-friendly** - Don't assume expert knowledge

### Documentation Types

**README.md** - Marketing + quick start  
**QUICKSTART.md** - Hands-on tutorial  
**ARCHITECTURE.md** - Deep technical details  
**QUICK-REFERENCE.md** - Fast lookup  
**CONTRIBUTING.md** - This file!

### Adding Examples

**Good example format:**
```markdown
### Task: Export a Branch

**Command:**
\`\`\`bash
python kt.py export my-branch --format json > my-branch.json
\`\`\`

**Result:**
\`\`\`json
{
  "branch": "my-branch",
  "nodes": [...]
}
\`\`\`

**Use case:** Backup branches or share with team
```

---

## 🤝 Community Guidelines

### Code of Conduct

**Be respectful:**
- Treat everyone with respect and kindness
- Welcome newcomers and help them learn
- Assume good intentions
- Give constructive feedback

**Be collaborative:**
- Share knowledge generously
- Credit others' work
- Ask questions when unsure
- Accept feedback gracefully

**Be professional:**
- Stay on topic
- Use inclusive language
- Avoid inflammatory comments
- Focus on the work, not the person

### Communication Channels

**GitHub Issues:**
- Bug reports
- Feature requests
- Questions about usage
- Design discussions

**Pull Requests:**
- Code contributions
- Documentation improvements
- Review and feedback

**Discussions (future):**
- General questions
- Show your projects
- Ideas and brainstorming

---

## 🎁 Recognition

**Contributors will be:**
- Listed in CONTRIBUTORS.md (coming soon)
- Credited in release notes
- Mentioned in documentation where applicable
- Given commit access after consistent contributions

**Types of contributions we recognize:**
- Code contributions (features, fixes)
- Documentation improvements
- Bug reports with reproduction steps
- Helpful issue/PR reviews
- Community support
- Example branches/templates
- Integrations and extensions

---

## 📦 Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR** version: Breaking changes
- **MINOR** version: New features (backward compatible)
- **PATCH** version: Bug fixes

**Current version:** 0.1.0 (pre-release)

### Release Checklist

1. Update version numbers
2. Update CHANGELOG.md
3. Test on all platforms
4. Update documentation
5. Tag release on GitHub
6. Write release notes

---

## ❓ Questions?

**Before opening an issue:**
1. Check existing issues
2. Read documentation (especially ARCHITECTURE.md)
3. Try the QUICKSTART guide
4. Search discussions (when available)

**When opening an issue:**
- Use a clear, descriptive title
- Include reproduction steps for bugs
- Provide system information (OS, Python version)
- Include error messages and logs
- Suggest potential solutions if you have ideas

**Where to ask:**
- **Bugs:** Open a GitHub issue
- **Features:** Open a GitHub issue with [Feature] tag
- **Usage:** Check docs first, then open issue with [Question] tag
- **Discussion:** Wait for GitHub Discussions to be enabled

---

## 🙏 Thank You!

Every contribution makes this project better. Whether you're fixing a typo, adding a feature, or sharing your use case, **thank you for being part of the KT Starter Kit community!**

**Happy contributing!** 🚀

---

## Quick Links

- [QUICK-REFERENCE.md](QUICK-REFERENCE.md) - Command reference
- [QUICKSTART.md](QUICKSTART.md) - Getting started
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [BUILD-PLAN.md](BUILD-PLAN.md) - Development roadmap
- [Issues](https://github.com/Mxcks/KT-starter-kit/issues) - Report bugs
- [Pull Requests](https://github.com/Mxcks/KT-starter-kit/pulls) - Submit changes

---

**License:** MIT - See [LICENSE](LICENSE) for details
