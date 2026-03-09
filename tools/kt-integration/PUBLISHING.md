# Publishing kt-integration to ClawHub

## What Gets Published

```
kt-integration/
├── SKILL.md              ✅ Main documentation (required)
├── skill.json            ✅ Metadata (required)
├── README.md             ✅ Quick start (recommended)
├── LICENSE               ⚠️ Need to add
├── .gitignore            ⚠️ Need to add
├── config/
│   └── settings.json     ✅ Default config
├── tools/
│   ├── kt-index.py       ⚠️ Need to fix hardcoded paths
│   ├── iss-query.py      ⚠️ Need to fix hardcoded paths
│   ├── kt-smart.py       ✅ Already good
│   └── kt-config.py      ✅ Already good
└── examples/             ⚠️ Should add
    └── usage-examples.md

```

## Issues to Fix Before Publishing

### 1. Hardcoded Paths
**Current problem:** `C:\dev\KT` is hardcoded

**Fix:** Use environment variable or config file
```python
# Instead of:
KT_ROOT = Path("C:/dev/KT")

# Do this:
KT_ROOT = Path(os.environ.get('KT_ROOT', 'C:/dev/KT'))
```

### 2. Installation Instructions
Need to add setup steps for new users:
```markdown
## Installation

1. Install skill:
   ```bash
   clawhub install kt-integration
   ```

2. Set your KT path:
   ```bash
   # Windows
   set KT_ROOT=C:\your\path\to\KT
   
   # Linux/Mac
   export KT_ROOT=/your/path/to/KT
   ```

3. Verify:
   ```bash
   python tools/kt-index.py stats
   ```
```

### 3. Add License
Choose a license (MIT recommended for open source):
```
MIT License

Copyright (c) 2026 Max Stern

Permission is hereby granted...
```

### 4. Add .gitignore
Exclude user-specific files:
```
# User config
config/settings.json

# Python
__pycache__/
*.pyc

# OS
.DS_Store
Thumbs.db
```

### 5. Add Examples
Real usage examples help users understand:
```markdown
## Examples

### Find all active projects
\`\`\`bash
python tools/kt-index.py list --status active
\`\`\`

### Search for authentication work
\`\`\`bash
python tools/iss-query.py search "authentication"
\`\`\`
```

## Publishing Process

### Option 1: Via ClawHub CLI
```bash
cd C:\Users\maxrs\.openclaw\workspace\kt-integration

# Login to ClawHub
clawhub login

# Publish
clawhub publish

# Or update existing
clawhub publish --update
```

### Option 2: Via GitHub + ClawHub
```bash
# 1. Create GitHub repo
git init
git add .
git commit -m "Initial kt-integration skill"
git remote add origin https://github.com/yourusername/kt-integration.git
git push -u origin main

# 2. Register on ClawHub
clawhub register --github yourusername/kt-integration
```

### Option 3: Manual (if ClawHub CLI not available)
1. Create account on clawhub.com
2. Click "Publish Skill"
3. Upload skill folder as .zip
4. Fill in metadata form
5. Submit for review

## Skill Metadata (skill.json)

Update for public consumption:
```json
{
  "name": "kt-integration",
  "version": "1.0.0",
  "description": "Query Knowledge Tree index and ISS systems with intelligent context discovery",
  "author": "Max Stern",
  "license": "MIT",
  "homepage": "https://github.com/yourusername/kt-integration",
  "repository": "https://github.com/yourusername/kt-integration",
  "keywords": ["knowledge-tree", "context", "index", "iss", "discovery"],
  "triggers": ["kt", "knowledge tree", "iss", "tree summary", "branch"],
  "dependencies": [],
  "min_openclaw_version": "0.1.0",
  "paths": {
    "kt_root": "${KT_ROOT:-C:/dev/KT}",
    "tools_dir": "tools",
    "config_dir": "config"
  }
}
```

## What Users Will See

On ClawHub, your skill page shows:
- **Name & Description** from skill.json
- **README.md** as main content
- **Installation instructions**
- **Tags/keywords** for search
- **Version history**
- **Download/install button**

## Files NOT to Publish

❌ Don't include:
- Your personal `config/settings.json` with your settings
- Cache files or logs
- `.env` files with credentials
- IDE-specific files (.vscode/, .idea/)
- Your specific KT data

## Recommended: Test Installation Flow

Before publishing, test the install experience:

1. **Create fresh test directory:**
   ```bash
   mkdir C:\temp\skill-test
   cd C:\temp\skill-test
   ```

2. **Copy skill (simulate install):**
   ```bash
   xcopy C:\Users\maxrs\.openclaw\workspace\kt-integration .\kt-integration\ /E
   ```

3. **Try as new user:**
   ```bash
   set KT_ROOT=C:\dev\KT
   python kt-integration\tools\kt-index.py stats
   ```

4. **Fix any issues found**

## Marketing Your Skill

Add to README.md:

**Features:**
- 🔍 Query KT index and ISS systems
- 🤖 Automatic context discovery
- ⚙️ Configurable automation (on/off switches)
- 📊 Smart preloading and suggestions
- 🎯 Works with 80+ project trees

**Use Cases:**
- Find existing work before starting new projects
- Load strategic context automatically
- Search for related decisions/patterns
- Compare multiple project trees

**Perfect for:**
- Teams using Knowledge Tree
- Solo developers with multiple projects
- Anyone wanting AI that knows their codebase

## Version Strategy

**v1.0.0 - Initial Release**
- Core query functionality
- Basic automation
- Configuration system

**Future versions:**
- v1.1.0 - Add semantic search
- v1.2.0 - Add tree comparison features
- v2.0.0 - Add MCP server support

## Next Steps

1. ✅ Fix hardcoded paths
2. ✅ Add LICENSE file
3. ✅ Add .gitignore
4. ✅ Add examples
5. ✅ Test install flow
6. ✅ Publish to ClawHub
7. ✅ Share on Discord/community

Want me to fix the hardcoded paths and prepare it for publishing?
