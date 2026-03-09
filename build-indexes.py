#!/usr/bin/env python3
"""
Index Builder - Build tree indexes from example branches
Demonstrates the KT index system using only starter kit data
"""

import json
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Any

KT_ROOT = Path(__file__).parent
BRANCHES_DIR = KT_ROOT / "branches"
INDEX_DIR = KT_ROOT / "index"

class IndexBuilder:
    """Build tree indexes from branches"""
    
    def __init__(self):
        self.branches_dir = BRANCHES_DIR
        self.index_dir = INDEX_DIR
        self.index_dir.mkdir(exist_ok=True)
        
        self.branches = []
        self.all_nodes = []
        self.all_tags = defaultdict(list)
        self.node_types = defaultdict(list)
    
    def load_all_branches(self):
        """Load all branches and their nodes"""
        print("\n[STEP 1] Loading branches...")
        
        for branch_dir in self.branches_dir.iterdir():
            if not branch_dir.is_dir():
                continue
            
            tree_file = branch_dir / "knowledge" / "tree.jsonl"
            if not tree_file.exists():
                continue
            
            # Load nodes
            nodes = []
            with open(tree_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            node = json.loads(line)
                            node['_branch'] = branch_dir.name
                            nodes.append(node)
                            self.all_nodes.append(node)
                        except json.JSONDecodeError:
                            continue
            
            # Branch metadata
            init_node = nodes[0] if nodes else {}
            branch_info = {
                "name": branch_dir.name,
                "path": str(branch_dir),
                "node_count": len(nodes),
                "description": init_node.get("message", ""),
                "created": init_node.get("timestamp", ""),
                "nodes": nodes
            }
            
            self.branches.append(branch_info)
            
            # Collect tags
            for node in nodes:
                for tag in node.get("tags", []):
                    self.all_tags[tag].append({
                        "branch": branch_dir.name,
                        "node_id": node.get("id"),
                        "message": node.get("message", "")
                    })
            
            # Collect node types
            for node in nodes:
                node_type = node.get("type", "unknown")
                self.node_types[node_type].append({
                    "branch": branch_dir.name,
                    "node_id": node.get("id"),
                    "message": node.get("message", "")
                })
            
            print(f"  [OK] Loaded {branch_dir.name}: {len(nodes)} nodes")
        
        print(f"\n[OK] Loaded {len(self.branches)} branches, {len(self.all_nodes)} total nodes")
    
    def build_branch_index(self):
        """Build branch-index.json"""
        print("\n[STEP 2] Building branch index...")
        
        index = {
            "generated": datetime.utcnow().isoformat() + "Z",
            "total_branches": len(self.branches),
            "total_nodes": len(self.all_nodes),
            "branches": {}
        }
        
        for branch in self.branches:
            index["branches"][branch["name"]] = {
                "name": branch["name"],
                "path": branch["path"],
                "node_count": branch["node_count"],
                "description": branch["description"],
                "created": branch["created"],
                "tags": list(set(
                    tag for node in branch["nodes"]
                    for tag in node.get("tags", [])
                )),
                "node_types": list(set(
                    node.get("type") for node in branch["nodes"]
                ))
            }
        
        output_file = self.index_dir / "branch-index.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)
        
        print(f"[OK] Created {output_file}")
        return index
    
    def build_tag_index(self):
        """Build global-tag-index.json"""
        print("\n[STEP 3] Building tag index...")
        
        index = {
            "generated": datetime.utcnow().isoformat() + "Z",
            "total_tags": len(self.all_tags),
            "total_tagged_nodes": sum(len(nodes) for nodes in self.all_tags.values()),
            "tags": {}
        }
        
        for tag, nodes in sorted(self.all_tags.items()):
            index["tags"][tag] = {
                "tag": tag,
                "count": len(nodes),
                "branches": list(set(n["branch"] for n in nodes)),
                "nodes": nodes
            }
        
        output_file = self.index_dir / "global-tag-index.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)
        
        print(f"[OK] Created {output_file}")
        print(f"     Tags: {', '.join(sorted(self.all_tags.keys())[:10])}...")
        return index
    
    def build_node_type_index(self):
        """Build node-type-index.json"""
        print("\n[STEP 4] Building node type index...")
        
        index = {
            "generated": datetime.utcnow().isoformat() + "Z",
            "total_types": len(self.node_types),
            "total_nodes": len(self.all_nodes),
            "types": {}
        }
        
        for node_type, nodes in sorted(self.node_types.items()):
            index["types"][node_type] = {
                "type": node_type,
                "count": len(nodes),
                "branches": list(set(n["branch"] for n in nodes)),
                "nodes": nodes
            }
        
        output_file = self.index_dir / "node-type-index.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)
        
        print(f"[OK] Created {output_file}")
        print(f"     Types: {', '.join(sorted(self.node_types.keys()))}")
        return index
    
    def build_search_index(self):
        """Build searchable index"""
        print("\n[STEP 5] Building search index...")
        
        # Create searchable entries
        search_entries = []
        
        for node in self.all_nodes:
            entry = {
                "branch": node.get("_branch"),
                "node_id": node.get("id"),
                "type": node.get("type"),
                "message": node.get("message", ""),
                "tags": node.get("tags", []),
                "timestamp": node.get("timestamp", ""),
                "searchable_text": " ".join([
                    node.get("message", ""),
                    node.get("reasoning", ""),
                    str(node.get("content", "")),
                    " ".join(node.get("tags", []))
                ]).lower()
            }
            search_entries.append(entry)
        
        index = {
            "generated": datetime.utcnow().isoformat() + "Z",
            "total_entries": len(search_entries),
            "entries": search_entries
        }
        
        output_file = self.index_dir / "search-index.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)
        
        print(f"[OK] Created {output_file}")
        return index
    
    def build_statistics(self):
        """Build statistics"""
        print("\n[STEP 6] Building statistics...")
        
        stats = {
            "generated": datetime.utcnow().isoformat() + "Z",
            "summary": {
                "total_branches": len(self.branches),
                "total_nodes": len(self.all_nodes),
                "total_tags": len(self.all_tags),
                "total_node_types": len(self.node_types)
            },
            "branches": {
                b["name"]: b["node_count"]
                for b in sorted(self.branches, key=lambda x: x["node_count"], reverse=True)
            },
            "top_tags": {
                tag: len(nodes)
                for tag, nodes in sorted(self.all_tags.items(), key=lambda x: len(x[1]), reverse=True)[:20]
            },
            "node_type_distribution": {
                node_type: len(nodes)
                for node_type, nodes in sorted(self.node_types.items(), key=lambda x: len(x[1]), reverse=True)
            }
        }
        
        output_file = self.index_dir / "statistics.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)
        
        print(f"[OK] Created {output_file}")
        print(f"\n{'='*60}")
        print(f"Statistics Summary:")
        print(f"  Branches: {stats['summary']['total_branches']}")
        print(f"  Nodes: {stats['summary']['total_nodes']}")
        print(f"  Tags: {stats['summary']['total_tags']}")
        print(f"  Node Types: {stats['summary']['total_node_types']}")
        print(f"{'='*60}")
        
        return stats
    
    def build_all(self):
        """Build all indexes"""
        print("="*60)
        print("KT Index Builder")
        print("="*60)
        
        self.load_all_branches()
        self.build_branch_index()
        self.build_tag_index()
        self.build_node_type_index()
        self.build_search_index()
        self.build_statistics()
        
        print(f"\n{'='*60}")
        print(f"All indexes built successfully!")
        print(f"Location: {self.index_dir}")
        print(f"{'='*60}\n")

def main():
    """Main entry point"""
    builder = IndexBuilder()
    builder.build_all()

if __name__ == "__main__":
    main()
