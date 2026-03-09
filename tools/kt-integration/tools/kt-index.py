#!/usr/bin/env python3
"""
KT Index Query Tool - OpenClaw Integration
Provides CLI access to KT index system
"""

import json
import sys
import argparse
from pathlib import Path

# KT paths
KT_ROOT = Path("C:/dev/KT")
INDEX_DIR = KT_ROOT / "index"

class KTIndexTool:
    """Query KT index system"""
    
    def __init__(self):
        self.branch_index = INDEX_DIR / "branch-index.json"
        self.project_index = INDEX_DIR / "project-index.json"
        self.tag_index = INDEX_DIR / "global-tag-index.json"
        self.node_layer_index = INDEX_DIR / "node-layer-index.json"
    
    def query_branches(self, branch_type=None, status=None):
        """Query branches by type or status"""
        with open(self.branch_index, 'r') as f:
            data = json.load(f)
        
        branches = data.get('branches', [])
        
        # Filter by type
        if branch_type:
            branches = [b for b in branches if b.get('type') == branch_type]
        
        # Filter by status
        if status:
            branches = [b for b in branches if b.get('status') == status]
        
        return branches
    
    def get_branch_info(self, branch_id):
        """Get detailed info about a specific branch"""
        with open(self.branch_index, 'r') as f:
            data = json.load(f)
        
        for branch in data.get('branches', []):
            if branch.get('id') == branch_id:
                return branch
        
        return None
    
    def list_all_branches(self):
        """List all branches with basic info"""
        with open(self.branch_index, 'r') as f:
            data = json.load(f)
        
        branches = data.get('branches', [])
        
        result = []
        for b in branches:
            result.append({
                'id': b.get('id'),
                'name': b.get('name'),
                'type': b.get('type'),
                'status': b.get('status'),
                'nodes': b.get('nodes', 0)
            })
        
        return result
    
    def query_tags(self, tag_name=None):
        """Query global tag index"""
        if not self.tag_index.exists():
            return {"error": "Tag index not found"}
        
        with open(self.tag_index, 'r') as f:
            data = json.load(f)
        
        if tag_name:
            return data.get('tags', {}).get(tag_name, [])
        
        return data.get('tags', {})
    
    def get_stats(self):
        """Get overall KT statistics"""
        with open(self.branch_index, 'r') as f:
            branch_data = json.load(f)
        
        branches = branch_data.get('branches', [])
        
        stats = {
            'total_branches': len(branches),
            'by_type': branch_data.get('by_type', {}),
            'by_status': {},
            'total_nodes': sum(b.get('nodes', 0) for b in branches),
            'github_enabled': len(branch_data.get('github_projects_ready', []))
        }
        
        # Count by status
        for branch in branches:
            status = branch.get('status', 'unknown')
            stats['by_status'][status] = stats['by_status'].get(status, 0) + 1
        
        return stats


def main():
    parser = argparse.ArgumentParser(description='Query KT Index System')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # List branches
    list_parser = subparsers.add_parser('list', help='List branches')
    list_parser.add_argument('--type', help='Filter by type')
    list_parser.add_argument('--status', help='Filter by status')
    
    # Get branch info
    info_parser = subparsers.add_parser('info', help='Get branch info')
    info_parser.add_argument('branch_id', help='Branch ID')
    
    # Query tags
    tags_parser = subparsers.add_parser('tags', help='Query tags')
    tags_parser.add_argument('--tag', help='Specific tag name')
    
    # Get stats
    subparsers.add_parser('stats', help='Get KT statistics')
    
    args = parser.parse_args()
    
    tool = KTIndexTool()
    
    if args.command == 'list':
        result = tool.query_branches(branch_type=args.type, status=args.status)
    elif args.command == 'info':
        result = tool.get_branch_info(args.branch_id)
    elif args.command == 'tags':
        result = tool.query_tags(tag_name=args.tag)
    elif args.command == 'stats':
        result = tool.get_stats()
    else:
        parser.print_help()
        return
    
    # Output as JSON
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
