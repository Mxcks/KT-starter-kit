#!/usr/bin/env python3
"""
Knowledge Tree CLI - Simple node and branch management
Enables the complete workflow: Create → Summarize → Index → Query
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

# Default KT root (can be overridden by KT_ROOT env var)
import os
KT_ROOT = Path(os.environ.get('KT_ROOT', Path(__file__).parent))

class KnowledgeTree:
    """Simple Knowledge Tree manager"""
    
    def __init__(self, root: Path = KT_ROOT):
        self.root = root
        self.branches_dir = root / "branches"
        self.branches_dir.mkdir(exist_ok=True)
    
    def init_branch(self, branch_name: str, description: str = "") -> Path:
        """
        Initialize a new branch (project)
        
        Args:
            branch_name: Name of the branch
            description: Optional description
            
        Returns:
            Path to created branch
        """
        # Create branch directory
        branch_dir = self.branches_dir / branch_name
        if branch_dir.exists():
            print(f"[ERROR] Branch '{branch_name}' already exists")
            sys.exit(1)
        
        branch_dir.mkdir(parents=True)
        knowledge_dir = branch_dir / "knowledge"
        knowledge_dir.mkdir()
        
        # Create initial node
        init_node = {
            "id": 0,
            "type": "init",
            "branch": branch_name,
            "message": description or f"{branch_name.replace('-', ' ').title()}",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "tags": ["init"]
        }
        
        tree_file = knowledge_dir / "tree.jsonl"
        with open(tree_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(init_node) + '\n')
        
        print(f"[OK] Initialized branch: {branch_name}")
        print(f"     Location: {branch_dir}")
        print(f"     Nodes: {tree_file}")
        
        return branch_dir
    
    def add_node(self, branch_name: str, node_type: str, message: str, 
                 reasoning: Optional[str] = None, content: Optional[str] = None,
                 tags: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Add a node to a branch
        
        Args:
            branch_name: Branch to add to
            node_type: Type of node (decision, commit, documentation, etc.)
            message: Node message
            reasoning: Optional reasoning (for decisions)
            content: Optional detailed content
            tags: Optional tags
            
        Returns:
            Created node
        """
        branch_dir = self.branches_dir / branch_name
        tree_file = branch_dir / "knowledge" / "tree.jsonl"
        
        if not tree_file.exists():
            print(f"[ERROR] Branch '{branch_name}' not found")
            print(f"  Initialize it first: kt init {branch_name}")
            sys.exit(1)
        
        # Get next node ID
        nodes = self._load_nodes(tree_file)
        next_id = max([n.get('id', 0) for n in nodes]) + 1 if nodes else 1
        
        # Create node
        node = {
            "id": next_id,
            "type": node_type,
            "message": message,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "tags": tags or []
        }
        
        # Add optional fields
        if reasoning:
            node["reasoning"] = reasoning
        if content:
            node["content"] = content
        
        # For decisions, add decision field
        if node_type == "decision" and reasoning:
            node["decision"] = message
        
        # Append to tree
        with open(tree_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(node) + '\n')
        
        print(f"[OK] Added {node_type} node #{next_id} to {branch_name}")
        print(f"     Message: {message}")
        if reasoning:
            print(f"     Reasoning: {reasoning}")
        
        return node
    
    def list_branches(self) -> List[Dict[str, Any]]:
        """List all branches"""
        branches = []
        
        for branch_dir in self.branches_dir.iterdir():
            if not branch_dir.is_dir():
                continue
            
            tree_file = branch_dir / "knowledge" / "tree.jsonl"
            if not tree_file.exists():
                continue
            
            nodes = self._load_nodes(tree_file)
            init_node = nodes[0] if nodes else {}
            
            branches.append({
                "name": branch_dir.name,
                "path": str(branch_dir),
                "nodes": len(nodes),
                "description": init_node.get("message", ""),
                "created": init_node.get("timestamp", "")
            })
        
        return branches
    
    def show_tree(self, branch_name: str, detailed: bool = False):
        """Show nodes in a branch"""
        branch_dir = self.branches_dir / branch_name
        tree_file = branch_dir / "knowledge" / "tree.jsonl"
        
        if not tree_file.exists():
            print(f"[ERROR] Branch '{branch_name}' not found")
            sys.exit(1)
        
        nodes = self._load_nodes(tree_file)
        
        print(f"\n{branch_name} ({len(nodes)} nodes)")
        print("=" * 60)
        
        for node in nodes:
            node_id = node.get('id', '?')
            node_type = node.get('type', 'unknown')
            message = node.get('message', '')
            tags = node.get('tags', [])
            
            print(f"\n[{node_id}] {node_type.upper()}")
            print(f"    {message}")
            
            if tags:
                print(f"    Tags: {', '.join(tags)}")
            
            if detailed:
                if 'reasoning' in node:
                    print(f"    Reasoning: {node['reasoning']}")
                if 'content' in node:
                    content = node['content']
                    if isinstance(content, str):
                        print(f"    Content: {content[:100]}...")
                if 'decision' in node:
                    print(f"    Decision: {node['decision']}")
    
    def _load_nodes(self, tree_file: Path) -> List[Dict[str, Any]]:
        """Load nodes from JSONL file"""
        nodes = []
        
        with open(tree_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        nodes.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        
        return nodes


def main():
    """Main CLI entry point"""
    
    parser = argparse.ArgumentParser(
        description='Knowledge Tree - Simple node and branch management',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Initialize a new project
  kt init my-project "My awesome project"
  
  # Add nodes
  kt add decision "Use PostgreSQL" --reasoning "Need ACID compliance"
  kt add commit "Set up authentication"
  kt add doc "API follows REST principles"
  
  # View branches and nodes
  kt list
  kt tree my-project
  
  # Generate summaries (after adding nodes)
  python branches/system-documentation/tools/kt-hierarchical-summarizer.py --branch my-project
  
  # Update ISS indexes
  python branches/system-documentation/tools/iss-hierarchical-indexer.py
  
  # Query via AI
  python tools/kt-integration/tools/iss-query.py search "postgresql"
        """
    )
    
    parser.add_argument('--root', help='KT root directory (default: current directory or $KT_ROOT)')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # init command
    init_parser = subparsers.add_parser('init', help='Initialize a new branch')
    init_parser.add_argument('branch', help='Branch name')
    init_parser.add_argument('description', nargs='?', default='', help='Branch description')
    
    # add command
    add_parser = subparsers.add_parser('add', help='Add a node to a branch')
    add_parser.add_argument('type', choices=['decision', 'commit', 'doc', 'summary', 'blocker'], 
                           help='Node type')
    add_parser.add_argument('message', help='Node message')
    add_parser.add_argument('--branch', required=True, help='Branch name')
    add_parser.add_argument('--reasoning', help='Reasoning (for decisions)')
    add_parser.add_argument('--content', help='Detailed content')
    add_parser.add_argument('--tags', help='Comma-separated tags')
    
    # list command
    subparsers.add_parser('list', help='List all branches')
    
    # tree command
    tree_parser = subparsers.add_parser('tree', help='Show nodes in a branch')
    tree_parser.add_argument('branch', help='Branch name')
    tree_parser.add_argument('--detailed', action='store_true', help='Show detailed info')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize KT
    kt_root = Path(args.root) if args.root else KT_ROOT
    kt = KnowledgeTree(kt_root)
    
    # Execute command
    if args.command == 'init':
        kt.init_branch(args.branch, args.description)
        
    elif args.command == 'add':
        # Parse tags
        tags = args.tags.split(',') if args.tags else []
        
        # Map doc to documentation
        node_type = 'documentation' if args.type == 'doc' else args.type
        
        kt.add_node(
            branch_name=args.branch,
            node_type=node_type,
            message=args.message,
            reasoning=args.reasoning,
            content=args.content,
            tags=tags
        )
        
    elif args.command == 'list':
        branches = kt.list_branches()
        
        if not branches:
            print("No branches found. Initialize one with: kt init <name>")
            sys.exit(0)
        
        print(f"\nFound {len(branches)} branches:\n")
        print(f"{'Name':<30} {'Nodes':<10} {'Description':<40}")
        print("=" * 80)
        
        for branch in branches:
            name = branch['name'][:28]
            nodes = str(branch['nodes'])
            desc = branch['description'][:38]
            print(f"{name:<30} {nodes:<10} {desc:<40}")
        
    elif args.command == 'tree':
        kt.show_tree(args.branch, detailed=args.detailed)


if __name__ == '__main__':
    main()
