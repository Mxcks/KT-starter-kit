"""
Query Engine - Search and filter nodes across branches
Simplified version for KT Starter Kit
"""

import re
from typing import Dict, List, Optional, Any
from pathlib import Path
import json


class QueryEngine:
    """Query and search engine for knowledge tree"""
    
    def __init__(self, tree_engine):
        """
        Initialize query engine
        
        Args:
            tree_engine: TreeEngine instance
        """
        self.tree = tree_engine
    
    def query(
        self,
        branch: Optional[str] = None,
        node_type: Optional[str] = None,
        tags: Optional[List[str]] = None,
        text: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Query nodes with multiple filters
        
        Args:
            branch: Filter by branch name (None = all branches)
            node_type: Filter by node type
            tags: Filter by tags (nodes must have ALL tags)
            text: Search in message/reasoning/content (case-insensitive)
            date_from: Filter by timestamp >= date (ISO format)
            date_to: Filter by timestamp <= date (ISO format)
            limit: Maximum results to return
        
        Returns:
            List of matching nodes (with _branch field added)
        """
        results = self.tree.query_nodes(
            branch_name=branch,
            node_type=node_type,
            tags=tags,
            text=text
        )
        
        # Date filtering
        if date_from or date_to:
            filtered = []
            for node in results:
                timestamp = node.get("timestamp", "")
                
                if date_from and timestamp < date_from:
                    continue
                if date_to and timestamp > date_to:
                    continue
                
                filtered.append(node)
            
            results = filtered
        
        # Apply limit
        if limit:
            results = results[:limit]
        
        return results
    
    def search_text(self, query: str, branch: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Simple text search across nodes
        
        Args:
            query: Search query
            branch: Optional branch filter
            limit: Max results
        
        Returns:
            Matching nodes
        """
        return self.query(branch=branch, text=query, limit=limit)
    
    def find_by_type(self, node_type: str, branch: Optional[str] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Find nodes by type
        
        Args:
            node_type: Node type to find
            branch: Optional branch filter
            limit: Optional limit
        
        Returns:
            Matching nodes
        """
        return self.query(branch=branch, node_type=node_type, limit=limit)
    
    def find_by_tags(self, tags: List[str], branch: Optional[str] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Find nodes with specific tags
        
        Args:
            tags: Tags to search for (nodes must have ALL)
            branch: Optional branch filter
            limit: Optional limit
        
        Returns:
            Matching nodes
        """
        return self.query(branch=branch, tags=tags, limit=limit)
    
    def find_recent(self, days: int = 7, branch: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Find recent nodes
        
        Args:
            days: Number of days to look back
            branch: Optional branch filter
            limit: Max results
        
        Returns:
            Recent nodes (sorted by timestamp desc)
        """
        from datetime import datetime, timedelta
        
        date_from = (datetime.utcnow() - timedelta(days=days)).isoformat() + "Z"
        
        results = self.query(branch=branch, date_from=date_from, limit=limit)
        
        # Sort by timestamp descending
        return sorted(results, key=lambda x: x.get("timestamp", ""), reverse=True)
    
    def get_related_nodes(self, branch: str, node_id: str, max_distance: int = 2) -> List[Dict[str, Any]]:
        """
        Get nodes related to a specific node (by proximity in tree)
        
        Args:
            branch: Branch name
            node_id: Node ID
            max_distance: Maximum distance in tree (IDs away)
        
        Returns:
            Related nodes
        """
        nodes = self.tree.load_nodes(branch)
        
        # Find target node index
        target_idx = None
        for i, node in enumerate(nodes):
            if str(node.get("id")) == str(node_id):
                target_idx = i
                break
        
        if target_idx is None:
            return []
        
        # Get nodes within distance
        start_idx = max(0, target_idx - max_distance)
        end_idx = min(len(nodes), target_idx + max_distance + 1)
        
        related = []
        for i in range(start_idx, end_idx):
            if i != target_idx:  # Exclude the target node itself
                node = nodes[i].copy()
                node["_branch"] = branch
                node["_distance"] = abs(i - target_idx)
                related.append(node)
        
        return related
    
    def aggregate_tags(self, branch: Optional[str] = None) -> Dict[str, int]:
        """
        Aggregate tags across nodes
        
        Args:
            branch: Optional branch filter
        
        Returns:
            Dict of tag -> count
        """
        nodes = self.tree.query_nodes(branch_name=branch)
        
        tags = {}
        for node in nodes:
            for tag in node.get("tags", []):
                tags[tag] = tags.get(tag, 0) + 1
        
        return dict(sorted(tags.items(), key=lambda x: x[1], reverse=True))
    
    def aggregate_types(self, branch: Optional[str] = None) -> Dict[str, int]:
        """
        Aggregate node types across nodes
        
        Args:
            branch: Optional branch filter
        
        Returns:
            Dict of type -> count
        """
        nodes = self.tree.query_nodes(branch_name=branch)
        
        types = {}
        for node in nodes:
            node_type = node.get("type", "unknown")
            types[node_type] = types.get(node_type, 0) + 1
        
        return dict(sorted(types.items(), key=lambda x: x[1], reverse=True))


def main():
    """Example usage"""
    import sys
    from tree_engine import TreeEngine
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python query_engine.py search <query> [--branch <name>]")
        print("  python query_engine.py type <type> [--branch <name>]")
        print("  python query_engine.py tags <tag1> [tag2...] [--branch <name>]")
        print("  python query_engine.py recent [--days <n>] [--branch <name>]")
        print("  python query_engine.py agg-tags [--branch <name>]")
        print("  python query_engine.py agg-types [--branch <name>]")
        sys.exit(1)
    
    tree = TreeEngine()
    query_engine = QueryEngine(tree)
    
    command = sys.argv[1]
    
    # Parse common args
    branch = None
    if "--branch" in sys.argv:
        idx = sys.argv.index("--branch")
        if idx + 1 < len(sys.argv):
            branch = sys.argv[idx + 1]
    
    if command == "search":
        if len(sys.argv) < 3:
            print("Error: Search query required")
            sys.exit(1)
        
        query = sys.argv[2]
        results = query_engine.search_text(query, branch=branch)
        
        print(f"\n{len(results)} results for '{query}':\n")
        for node in results:
            print(f"[{node['_branch']}] {node['type'].upper()}: {node['message']}")
            if node.get("tags"):
                print(f"  Tags: {', '.join(node['tags'])}")
            print()
    
    elif command == "type":
        if len(sys.argv) < 3:
            print("Error: Node type required")
            sys.exit(1)
        
        node_type = sys.argv[2]
        results = query_engine.find_by_type(node_type, branch=branch)
        
        print(f"\n{len(results)} {node_type} nodes:\n")
        for node in results:
            print(f"[{node['_branch']}] {node['message']}")
    
    elif command == "tags":
        if len(sys.argv) < 3:
            print("Error: At least one tag required")
            sys.exit(1)
        
        tags = []
        for arg in sys.argv[2:]:
            if arg.startswith("--"):
                break
            tags.append(arg)
        
        results = query_engine.find_by_tags(tags, branch=branch)
        
        print(f"\n{len(results)} nodes with tags {tags}:\n")
        for node in results:
            print(f"[{node['_branch']}] {node['type'].upper()}: {node['message']}")
            print(f"  Tags: {', '.join(node['tags'])}")
            print()
    
    elif command == "recent":
        days = 7
        if "--days" in sys.argv:
            idx = sys.argv.index("--days")
            if idx + 1 < len(sys.argv):
                days = int(sys.argv[idx + 1])
        
        results = query_engine.find_recent(days=days, branch=branch)
        
        print(f"\n{len(results)} nodes from last {days} days:\n")
        for node in results:
            print(f"[{node['_branch']}] {node['timestamp'][:10]} - {node['type'].upper()}: {node['message']}")
    
    elif command == "agg-tags":
        tags = query_engine.aggregate_tags(branch=branch)
        
        print(f"\n{len(tags)} unique tags:\n")
        print(f"{'Tag':<30} {'Count':<10}")
        print("=" * 40)
        for tag, count in list(tags.items())[:20]:
            print(f"{tag:<30} {count:<10}")
    
    elif command == "agg-types":
        types = query_engine.aggregate_types(branch=branch)
        
        print(f"\n{len(types)} node types:\n")
        print(f"{'Type':<30} {'Count':<10}")
        print("=" * 40)
        for node_type, count in types.items():
            print(f"{node_type:<30} {count:<10}")


if __name__ == "__main__":
    main()
