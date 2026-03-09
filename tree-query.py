#!/usr/bin/env python3
"""
Tree Query Tool - Query the KT tree indexes
Simple command-line tool for searching nodes, tags, and branches
"""

import json
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any

KT_ROOT = Path(__file__).parent
INDEX_DIR = KT_ROOT / "index"

class TreeQuery:
    """Query tree indexes"""
    
    def __init__(self):
        self.index_dir = INDEX_DIR
        self.branch_index = None
        self.tag_index = None
        self.node_type_index = None
        self.search_index = None
        self.stats = None
    
    def load_indexes(self):
        """Load all indexes"""
        try:
            with open(self.index_dir / "branch-index.json") as f:
                self.branch_index = json.load(f)
            
            with open(self.index_dir / "global-tag-index.json") as f:
                self.tag_index = json.load(f)
            
            with open(self.index_dir / "node-type-index.json") as f:
                self.node_type_index = json.load(f)
            
            with open(self.index_dir / "search-index.json") as f:
                self.search_index = json.load(f)
            
            with open(self.index_dir / "statistics.json") as f:
                self.stats = json.load(f)
            
            return True
        except FileNotFoundError as e:
            print(f"[ERROR] Index not found: {e}")
            print(f"[INFO] Run 'python build-indexes.py' first")
            return False
    
    def cmd_stats(self, args):
        """Show statistics"""
        if not self.stats:
            return
        
        print("\n" + "="*60)
        print("KT Tree Statistics")
        print("="*60)
        
        summary = self.stats['summary']
        print(f"\nTotal Branches: {summary['total_branches']}")
        print(f"Total Nodes: {summary['total_nodes']}")
        print(f"Total Tags: {summary['total_tags']}")
        print(f"Node Types: {summary['total_node_types']}")
        
        print("\nBranches by Size:")
        for branch, count in list(self.stats['branches'].items())[:10]:
            print(f"  {branch:<30} {count} nodes")
        
        print("\nTop Tags:")
        for tag, count in list(self.stats['top_tags'].items())[:15]:
            print(f"  {tag:<30} {count} nodes")
        
        print("\nNode Type Distribution:")
        for node_type, count in self.stats['node_type_distribution'].items():
            print(f"  {node_type:<30} {count} nodes")
        
        print()
    
    def cmd_branches(self, args):
        """List branches"""
        if not self.branch_index:
            return
        
        branches = self.branch_index['branches']
        
        print(f"\n{len(branches)} Branches:\n")
        print(f"{'Name':<30} {'Nodes':<10} {'Tags':<40}")
        print("="*80)
        
        for name, info in sorted(branches.items()):
            tags_str = ', '.join(info['tags'][:3])
            if len(info['tags']) > 3:
                tags_str += '...'
            
            print(f"{name:<30} {info['node_count']:<10} {tags_str:<40}")
        
        print()
    
    def cmd_tags(self, args):
        """List or search tags"""
        if not self.tag_index:
            return
        
        tags = self.tag_index['tags']
        
        # Filter if search query provided
        if args.query:
            query = args.query.lower()
            tags = {
                tag: info for tag, info in tags.items()
                if query in tag.lower()
            }
        
        print(f"\n{len(tags)} Tags:\n")
        print(f"{'Tag':<30} {'Count':<10} {'Branches':<40}")
        print("="*80)
        
        for tag, info in sorted(tags.items(), key=lambda x: x[1]['count'], reverse=True):
            branches_str = ', '.join(info['branches'][:3])
            if len(info['branches']) > 3:
                branches_str += '...'
            
            print(f"{tag:<30} {info['count']:<10} {branches_str:<40}")
        
        print()
    
    def cmd_search(self, args):
        """Search nodes by text"""
        if not self.search_index:
            return
        
        query = args.query.lower()
        entries = self.search_index['entries']
        
        # Search
        matches = [
            e for e in entries
            if query in e['searchable_text']
        ]
        
        print(f"\n{len(matches)} matches for '{args.query}':\n")
        
        for match in matches[:args.limit]:
            print(f"[{match['branch']}] {match['type'].upper()}")
            print(f"  {match['message']}")
            if match['tags']:
                print(f"  Tags: {', '.join(match['tags'])}")
            print()
    
    def cmd_by_type(self, args):
        """Show nodes by type"""
        if not self.node_type_index:
            return
        
        types = self.node_type_index['types']
        
        if args.type not in types:
            print(f"[ERROR] Node type '{args.type}' not found")
            print(f"[INFO] Available types: {', '.join(types.keys())}")
            return
        
        info = types[args.type]
        nodes = info['nodes']
        
        print(f"\n{len(nodes)} {args.type} nodes:\n")
        
        for node in nodes[:args.limit]:
            print(f"[{node['branch']}] {node['message']}")
        
        print()
    
    def cmd_branch_info(self, args):
        """Show branch details"""
        if not self.branch_index:
            return
        
        branches = self.branch_index['branches']
        
        if args.branch not in branches:
            print(f"[ERROR] Branch '{args.branch}' not found")
            print(f"[INFO] Available branches: {', '.join(branches.keys())}")
            return
        
        info = branches[args.branch]
        
        print(f"\nBranch: {info['name']}")
        print("="*60)
        print(f"Description: {info['description']}")
        print(f"Nodes: {info['node_count']}")
        print(f"Created: {info['created']}")
        print(f"Path: {info['path']}")
        print(f"\nTags ({len(info['tags'])}):")
        for tag in sorted(info['tags']):
            print(f"  - {tag}")
        print(f"\nNode Types ({len(info['node_types'])}):")
        for node_type in sorted(info['node_types']):
            print(f"  - {node_type}")
        print()


def main():
    """Main entry point"""
    
    parser = argparse.ArgumentParser(
        description='Query KT tree indexes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show statistics
  python tree-query.py stats
  
  # List branches
  python tree-query.py branches
  
  # List tags
  python tree-query.py tags
  
  # Search tags
  python tree-query.py tags --query auth
  
  # Search nodes
  python tree-query.py search "authentication"
  
  # Show nodes by type
  python tree-query.py by-type decision
  
  # Branch details
  python tree-query.py branch-info system-documentation
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # stats command
    subparsers.add_parser('stats', help='Show statistics')
    
    # branches command
    subparsers.add_parser('branches', help='List branches')
    
    # tags command
    tags_parser = subparsers.add_parser('tags', help='List tags')
    tags_parser.add_argument('--query', help='Filter tags by search query')
    
    # search command
    search_parser = subparsers.add_parser('search', help='Search nodes')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--limit', type=int, default=20, help='Max results')
    
    # by-type command
    type_parser = subparsers.add_parser('by-type', help='Show nodes by type')
    type_parser.add_argument('type', help='Node type (decision, commit, etc.)')
    type_parser.add_argument('--limit', type=int, default=20, help='Max results')
    
    # branch-info command
    info_parser = subparsers.add_parser('branch-info', help='Show branch details')
    info_parser.add_argument('branch', help='Branch name')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Create query tool
    query = TreeQuery()
    
    # Load indexes
    if not query.load_indexes():
        sys.exit(1)
    
    # Execute command
    if args.command == 'stats':
        query.cmd_stats(args)
    elif args.command == 'branches':
        query.cmd_branches(args)
    elif args.command == 'tags':
        query.cmd_tags(args)
    elif args.command == 'search':
        query.cmd_search(args)
    elif args.command == 'by-type':
        query.cmd_by_type(args)
    elif args.command == 'branch-info':
        query.cmd_branch_info(args)

if __name__ == '__main__':
    main()
