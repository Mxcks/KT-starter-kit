"""
Tree Engine - Core node storage and management for Knowledge Tree
Simplified version for KT Starter Kit - handles JSONL storage and node operations
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class TreeEngine:
    """Core tree engine for managing nodes in branches"""
    
    def __init__(self, root_path: str = "."):
        """
        Initialize tree engine
        
        Args:
            root_path: Path to KT root (default: current directory)
        """
        self.root_path = Path(root_path).resolve()
        self.branches_dir = self.root_path / "branches"
        self.index_dir = self.root_path / "index"
        
        # Ensure directories exist
        self.branches_dir.mkdir(parents=True, exist_ok=True)
        self.index_dir.mkdir(parents=True, exist_ok=True)
    
    def get_branch_path(self, branch_name: str) -> Path:
        """Get path to branch directory"""
        return self.branches_dir / branch_name
    
    def get_tree_file(self, branch_name: str) -> Path:
        """Get path to branch's tree.jsonl file"""
        return self.get_branch_path(branch_name) / "knowledge" / "tree.jsonl"
    
    def branch_exists(self, branch_name: str) -> bool:
        """Check if branch exists"""
        return self.get_tree_file(branch_name).exists()
    
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
            
            # Load nodes to get info
            nodes = self.load_nodes(branch_dir.name)
            
            # Get init node for description
            init_node = nodes[0] if nodes else {}
            
            branch_info = {
                "name": branch_dir.name,
                "path": str(branch_dir),
                "node_count": len(nodes),
                "description": init_node.get("message", ""),
                "created": init_node.get("timestamp", "")
            }
            
            branches.append(branch_info)
        
        return sorted(branches, key=lambda x: x["name"])
    
    def load_nodes(self, branch_name: str) -> List[Dict[str, Any]]:
        """
        Load all nodes from a branch
        
        Args:
            branch_name: Name of branch
        
        Returns:
            List of nodes (in order)
        """
        tree_file = self.get_tree_file(branch_name)
        
        if not tree_file.exists():
            return []
        
        nodes = []
        with open(tree_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        node = json.loads(line)
                        nodes.append(node)
                    except json.JSONDecodeError:
                        continue
        
        return nodes
    
    def add_node(
        self,
        branch_name: str,
        node_type: str,
        message: str,
        tags: Optional[List[str]] = None,
        reasoning: Optional[str] = None,
        content: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Add node to branch
        
        Args:
            branch_name: Branch name
            node_type: Node type (decision, commit, documentation, etc.)
            message: Node message
            tags: Optional list of tags
            reasoning: Optional reasoning text
            content: Optional additional content
        
        Returns:
            Created node
        """
        if not self.branch_exists(branch_name):
            raise ValueError(f"Branch '{branch_name}' does not exist")
        
        # Load existing nodes to determine next ID
        nodes = self.load_nodes(branch_name)
        next_id = len(nodes)
        
        # Create node
        node = {
            "id": str(next_id),
            "type": node_type,
            "message": message,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "tags": tags or []
        }
        
        if reasoning:
            node["reasoning"] = reasoning
        
        if content is not None:
            node["content"] = content
        
        # Append to tree file
        tree_file = self.get_tree_file(branch_name)
        with open(tree_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(node) + '\n')
        
        return node
    
    def get_node(self, branch_name: str, node_id: str) -> Optional[Dict[str, Any]]:
        """
        Get specific node by ID
        
        Args:
            branch_name: Branch name
            node_id: Node ID
        
        Returns:
            Node dict or None if not found
        """
        nodes = self.load_nodes(branch_name)
        
        for node in nodes:
            if str(node.get("id")) == str(node_id):
                return node
        
        return None
    
    def query_nodes(
        self,
        branch_name: Optional[str] = None,
        node_type: Optional[str] = None,
        tags: Optional[List[str]] = None,
        text: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Query nodes with filters
        
        Args:
            branch_name: Filter by branch (None = all branches)
            node_type: Filter by node type
            tags: Filter by tags (nodes must have all tags)
            text: Search in message/reasoning/content (case-insensitive)
        
        Returns:
            List of matching nodes (with branch name added)
        """
        results = []
        
        # Determine which branches to search
        if branch_name:
            branches = [branch_name]
        else:
            branch_infos = self.list_branches()
            branches = [b["name"] for b in branch_infos]
        
        # Search each branch
        for branch in branches:
            nodes = self.load_nodes(branch)
            
            for node in nodes:
                # Type filter
                if node_type and node.get("type") != node_type:
                    continue
                
                # Tags filter (must have ALL specified tags)
                if tags:
                    node_tags = set(node.get("tags", []))
                    if not all(tag in node_tags for tag in tags):
                        continue
                
                # Text search
                if text:
                    text_lower = text.lower()
                    searchable = " ".join([
                        node.get("message", ""),
                        node.get("reasoning", ""),
                        str(node.get("content", ""))
                    ]).lower()
                    
                    if text_lower not in searchable:
                        continue
                
                # Add branch name to result
                result = node.copy()
                result["_branch"] = branch
                results.append(result)
        
        return results
    
    def get_branch_stats(self, branch_name: str) -> Dict[str, Any]:
        """
        Get statistics for a branch
        
        Args:
            branch_name: Branch name
        
        Returns:
            Statistics dict
        """
        nodes = self.load_nodes(branch_name)
        
        if not nodes:
            return {
                "node_count": 0,
                "types": {},
                "tags": {},
                "created": None
            }
        
        # Count types
        types = {}
        for node in nodes:
            node_type = node.get("type", "unknown")
            types[node_type] = types.get(node_type, 0) + 1
        
        # Count tags
        tags = {}
        for node in nodes:
            for tag in node.get("tags", []):
                tags[tag] = tags.get(tag, 0) + 1
        
        return {
            "node_count": len(nodes),
            "types": types,
            "tags": tags,
            "created": nodes[0].get("timestamp")
        }


def main():
    """Example usage"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python tree_engine.py list")
        print("  python tree_engine.py info <branch>")
        print("  python tree_engine.py query [--branch <name>] [--type <type>] [--text <query>]")
        sys.exit(1)
    
    tree = TreeEngine()
    command = sys.argv[1]
    
    if command == "list":
        branches = tree.list_branches()
        print(f"\n{len(branches)} branches:\n")
        for branch in branches:
            print(f"{branch['name']:<30} {branch['node_count']} nodes")
    
    elif command == "info":
        if len(sys.argv) < 3:
            print("Error: Branch name required")
            sys.exit(1)
        
        branch_name = sys.argv[2]
        stats = tree.get_branch_stats(branch_name)
        
        print(f"\nBranch: {branch_name}")
        print(f"Nodes: {stats['node_count']}")
        print(f"Created: {stats['created']}")
        print(f"\nNode Types:")
        for node_type, count in stats['types'].items():
            print(f"  {node_type}: {count}")
        print(f"\nTags:")
        for tag, count in sorted(stats['tags'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {tag}: {count}")
    
    elif command == "query":
        # Parse query args
        args = {}
        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--branch":
                args["branch_name"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--type":
                args["node_type"] = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--text":
                args["text"] = sys.argv[i + 1]
                i += 2
            else:
                i += 1
        
        results = tree.query_nodes(**args)
        print(f"\n{len(results)} results:\n")
        for node in results:
            print(f"[{node['_branch']}] {node['type'].upper()}")
            print(f"  {node['message']}")
            if node.get("tags"):
                print(f"  Tags: {', '.join(node['tags'])}")
            print()


if __name__ == "__main__":
    main()
