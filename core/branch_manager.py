"""
Branch Manager - Handles branch creation and management
Simplified version for KT Starter Kit
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class BranchManager:
    """Manages branches in the knowledge tree"""
    
    def __init__(self, root_path: str = "."):
        """
        Initialize branch manager
        
        Args:
            root_path: Path to KT root (default: current directory)
        """
        self.root_path = Path(root_path).resolve()
        self.branches_dir = self.root_path / "branches"
        self.branches_dir.mkdir(parents=True, exist_ok=True)
    
    def create_branch(
        self,
        name: str,
        description: str = "",
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create new branch
        
        Args:
            name: Branch name (must be unique, use kebab-case)
            description: Branch description
            tags: Initial tags for branch
        
        Returns:
            Branch configuration
        """
        branch_dir = self.branches_dir / name
        
        if branch_dir.exists():
            raise ValueError(f"Branch '{name}' already exists")
        
        # Create directory structure
        knowledge_dir = branch_dir / "knowledge"
        knowledge_dir.mkdir(parents=True, exist_ok=True)
        
        # Create init node
        init_node = {
            "id": "0",
            "type": "init",
            "message": description or f"Initialize {name}",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "tags": tags or ["init"]
        }
        
        # Write tree.jsonl
        tree_file = knowledge_dir / "tree.jsonl"
        with open(tree_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(init_node) + '\n')
        
        # Create README
        readme_file = branch_dir / "README.md"
        readme_content = f"""# {name}

{description or 'Project description goes here'}

## Quick Info

- **Created:** {datetime.utcnow().strftime('%Y-%m-%d')}
- **Nodes:** 1 (init)
- **Tags:** {', '.join(tags or ['init'])}

## Structure

```
{name}/
├── knowledge/
│   └── tree.jsonl       # Node storage
├── tools/               # Optional: project-specific tools
└── README.md            # This file
```

## Getting Started

Add nodes to this branch:

```bash
# Add a decision
python kt.py add decision "Your decision here" --branch {name}

# Add a commit
python kt.py add commit "Implementation milestone" --branch {name}

# Add documentation
python kt.py add doc "Documentation entry" --branch {name}
```

Generate summaries:

```bash
python branches/system-documentation/tools/kt-hierarchical-summarizer.py --branch {name}
```

Query:

```bash
python tree-query.py branch-info {name}
python tree-query.py search "your query" --branch {name}
```

## Tags

{chr(10).join(f'- {tag}' for tag in (tags or ['init']))}

---

For more info, see the main [README](../../README.md) and [QUICKSTART](../../QUICKSTART.md).
"""
        
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        return {
            "name": name,
            "path": str(branch_dir),
            "description": description,
            "created": datetime.utcnow().isoformat() + "Z",
            "node_count": 1,
            "tags": tags or ["init"]
        }
    
    def delete_branch(self, name: str, confirm: bool = False):
        """
        Delete a branch (requires confirmation)
        
        Args:
            name: Branch name
            confirm: Must be True to actually delete
        
        Raises:
            ValueError: If branch doesn't exist or confirmation not given
        """
        if not confirm:
            raise ValueError(
                "Must pass confirm=True to delete branch. "
                "This operation cannot be undone!"
            )
        
        branch_dir = self.branches_dir / name
        
        if not branch_dir.exists():
            raise ValueError(f"Branch '{name}' does not exist")
        
        # Delete the branch directory
        import shutil
        shutil.rmtree(branch_dir)
    
    def rename_branch(self, old_name: str, new_name: str):
        """
        Rename a branch
        
        Args:
            old_name: Current branch name
            new_name: New branch name
        
        Raises:
            ValueError: If old branch doesn't exist or new name already exists
        """
        old_dir = self.branches_dir / old_name
        new_dir = self.branches_dir / new_name
        
        if not old_dir.exists():
            raise ValueError(f"Branch '{old_name}' does not exist")
        
        if new_dir.exists():
            raise ValueError(f"Branch '{new_name}' already exists")
        
        # Rename directory
        old_dir.rename(new_dir)
        
        # Update README
        readme_file = new_dir / "README.md"
        if readme_file.exists():
            content = readme_file.read_text(encoding='utf-8')
            content = content.replace(f"# {old_name}", f"# {new_name}")
            content = content.replace(f"--branch {old_name}", f"--branch {new_name}")
            content = content.replace(f"{old_name}/", f"{new_name}/")
            readme_file.write_text(content, encoding='utf-8')
    
    def list_branches(self) -> List[Dict[str, Any]]:
        """
        List all branches
        
        Returns:
            List of branch info dicts
        """
        branches = []
        
        if not self.branches_dir.exists():
            return branches
        
        for branch_dir in self.branches_dir.iterdir():
            if not branch_dir.is_dir():
                continue
            
            tree_file = branch_dir / "knowledge" / "tree.jsonl"
            if not tree_file.exists():
                continue
            
            # Count nodes
            node_count = 0
            with open(tree_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        node_count += 1
            
            # Load init node for info
            init_node = {}
            with open(tree_file, 'r', encoding='utf-8') as f:
                first_line = f.readline()
                if first_line:
                    try:
                        init_node = json.loads(first_line)
                    except json.JSONDecodeError:
                        pass
            
            branch_info = {
                "name": branch_dir.name,
                "path": str(branch_dir),
                "node_count": node_count,
                "description": init_node.get("message", ""),
                "created": init_node.get("timestamp", ""),
                "tags": init_node.get("tags", [])
            }
            
            branches.append(branch_info)
        
        return sorted(branches, key=lambda x: x["name"])
    
    def get_branch_info(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get info about a specific branch
        
        Args:
            name: Branch name
        
        Returns:
            Branch info dict or None if not found
        """
        branch_dir = self.branches_dir / name
        tree_file = branch_dir / "knowledge" / "tree.jsonl"
        
        if not tree_file.exists():
            return None
        
        # Count nodes and collect tags
        node_count = 0
        all_tags = set()
        node_types = {}
        
        with open(tree_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    node_count += 1
                    try:
                        node = json.loads(line)
                        all_tags.update(node.get("tags", []))
                        
                        node_type = node.get("type", "unknown")
                        node_types[node_type] = node_types.get(node_type, 0) + 1
                    except json.JSONDecodeError:
                        continue
        
        # Load init node
        init_node = {}
        with open(tree_file, 'r', encoding='utf-8') as f:
            first_line = f.readline()
            if first_line:
                try:
                    init_node = json.loads(first_line)
                except json.JSONDecodeError:
                    pass
        
        return {
            "name": name,
            "path": str(branch_dir),
            "node_count": node_count,
            "description": init_node.get("message", ""),
            "created": init_node.get("timestamp", ""),
            "tags": sorted(all_tags),
            "node_types": node_types
        }


def main():
    """Example usage"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python branch_manager.py list")
        print("  python branch_manager.py create <name> [description]")
        print("  python branch_manager.py info <name>")
        print("  python branch_manager.py rename <old> <new>")
        sys.exit(1)
    
    manager = BranchManager()
    command = sys.argv[1]
    
    if command == "list":
        branches = manager.list_branches()
        print(f"\n{len(branches)} branches:\n")
        print(f"{'Name':<30} {'Nodes':<10} {'Description':<50}")
        print("=" * 90)
        for branch in branches:
            desc = branch['description'][:47] + "..." if len(branch['description']) > 50 else branch['description']
            print(f"{branch['name']:<30} {branch['node_count']:<10} {desc:<50}")
    
    elif command == "create":
        if len(sys.argv) < 3:
            print("Error: Branch name required")
            sys.exit(1)
        
        name = sys.argv[2]
        description = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""
        
        result = manager.create_branch(name, description)
        print(f"\n[OK] Created branch '{name}'")
        print(f"     Path: {result['path']}")
        print(f"     Nodes: {result['node_count']}")
    
    elif command == "info":
        if len(sys.argv) < 3:
            print("Error: Branch name required")
            sys.exit(1)
        
        name = sys.argv[2]
        info = manager.get_branch_info(name)
        
        if not info:
            print(f"Error: Branch '{name}' not found")
            sys.exit(1)
        
        print(f"\nBranch: {info['name']}")
        print(f"Path: {info['path']}")
        print(f"Description: {info['description']}")
        print(f"Nodes: {info['node_count']}")
        print(f"Created: {info['created']}")
        print(f"\nTags ({len(info['tags'])}):")
        for tag in info['tags']:
            print(f"  - {tag}")
        print(f"\nNode Types:")
        for node_type, count in info['node_types'].items():
            print(f"  - {node_type}: {count}")
    
    elif command == "rename":
        if len(sys.argv) < 4:
            print("Error: Old and new branch names required")
            sys.exit(1)
        
        old_name = sys.argv[2]
        new_name = sys.argv[3]
        
        manager.rename_branch(old_name, new_name)
        print(f"\n[OK] Renamed '{old_name}' to '{new_name}'")


if __name__ == "__main__":
    main()
