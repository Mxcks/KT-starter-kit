#!/usr/bin/env python3
"""
ISS Query Tool - OpenClaw Integration
Query Index Scrolling System for AI-friendly tree discovery
"""

import json
import sys
import argparse
from pathlib import Path

# KT paths
KT_ROOT = Path("C:/dev/KT")
ISS_DIR = KT_ROOT / "index-scrolling-system"
META_TREE_DIR = ISS_DIR / "meta-tree"

class ISSTool:
    """Query ISS system"""
    
    def __init__(self):
        self.summaries_dir = META_TREE_DIR / "summaries"
        self.index_dir = META_TREE_DIR / "index"
    
    def list_summaries(self):
        """List all available tree summaries"""
        summaries = []
        
        if self.summaries_dir.exists():
            for summary_dir in self.summaries_dir.iterdir():
                if summary_dir.is_dir():
                    summaries.append({
                        'tree_id': summary_dir.name,
                        'path': str(summary_dir)
                    })
        
        return summaries
    
    def get_summary(self, tree_id):
        """Get summary for a specific tree"""
        summary_path = self.summaries_dir / tree_id
        
        if not summary_path.exists():
            return {"error": f"Tree {tree_id} not found"}
        
        # Look for summary files
        strategic = summary_path / "strategic.md"
        tactical = summary_path / "tactical.md"
        implementation = summary_path / "implementation.md"
        index_file = summary_path / "index.json"
        
        result = {
            'tree_id': tree_id,
            'layers': {}
        }
        
        if strategic.exists():
            result['layers']['strategic'] = strategic.read_text(encoding='utf-8')
        
        if tactical.exists():
            result['layers']['tactical'] = tactical.read_text(encoding='utf-8')
        
        if implementation.exists():
            result['layers']['implementation'] = implementation.read_text(encoding='utf-8')
        
        if index_file.exists():
            with open(index_file, 'r') as f:
                result['index'] = json.load(f)
        
        return result
    
    def get_layer(self, tree_id, layer):
        """Get specific layer from tree"""
        layer_file = self.summaries_dir / tree_id / f"{layer}.md"
        
        if not layer_file.exists():
            return {"error": f"Layer {layer} not found for {tree_id}"}
        
        return {
            'tree_id': tree_id,
            'layer': layer,
            'content': layer_file.read_text(encoding='utf-8')
        }
    
    def get_indexes(self):
        """Get ISS index files"""
        indexes = {}
        
        if self.index_dir.exists():
            for index_file in self.index_dir.glob("*.json"):
                with open(index_file, 'r') as f:
                    indexes[index_file.stem] = json.load(f)
        
        return indexes
    
    def search_summaries(self, query):
        """Search summaries by keyword"""
        results = []
        
        if not self.summaries_dir.exists():
            return results
        
        query_lower = query.lower()
        
        for summary_dir in self.summaries_dir.iterdir():
            if not summary_dir.is_dir():
                continue
            
            # Check strategic layer for keywords
            strategic = summary_dir / "strategic.md"
            if strategic.exists():
                content = strategic.read_text(encoding='utf-8').lower()
                if query_lower in content:
                    results.append({
                        'tree_id': summary_dir.name,
                        'layer': 'strategic',
                        'path': str(strategic)
                    })
        
        return results
    
    def get_stats(self):
        """Get ISS statistics"""
        stats = {
            'total_trees': 0,
            'trees_with_layers': {},
            'total_summaries': 0
        }
        
        if self.summaries_dir.exists():
            for summary_dir in self.summaries_dir.iterdir():
                if summary_dir.is_dir():
                    stats['total_trees'] += 1
                    
                    # Count layers
                    layers = []
                    if (summary_dir / "strategic.md").exists():
                        layers.append('strategic')
                    if (summary_dir / "tactical.md").exists():
                        layers.append('tactical')
                    if (summary_dir / "implementation.md").exists():
                        layers.append('implementation')
                    
                    stats['trees_with_layers'][summary_dir.name] = layers
                    stats['total_summaries'] += len(layers)
        
        return stats


def main():
    parser = argparse.ArgumentParser(description='Query ISS System')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # List summaries
    subparsers.add_parser('list', help='List all tree summaries')
    
    # Get summary
    summary_parser = subparsers.add_parser('summary', help='Get tree summary')
    summary_parser.add_argument('tree_id', help='Tree ID')
    
    # Get layer
    layer_parser = subparsers.add_parser('layer', help='Get specific layer')
    layer_parser.add_argument('tree_id', help='Tree ID')
    layer_parser.add_argument('layer', choices=['strategic', 'tactical', 'implementation'])
    
    # Get indexes
    subparsers.add_parser('indexes', help='Get all ISS indexes')
    
    # Search
    search_parser = subparsers.add_parser('search', help='Search summaries')
    search_parser.add_argument('query', help='Search query')
    
    # Get stats
    subparsers.add_parser('stats', help='Get ISS statistics')
    
    args = parser.parse_args()
    
    tool = ISSTool()
    
    if args.command == 'list':
        result = tool.list_summaries()
    elif args.command == 'summary':
        result = tool.get_summary(args.tree_id)
    elif args.command == 'layer':
        result = tool.get_layer(args.tree_id, args.layer)
    elif args.command == 'indexes':
        result = tool.get_indexes()
    elif args.command == 'search':
        result = tool.search_summaries(args.query)
    elif args.command == 'stats':
        result = tool.get_stats()
    else:
        parser.print_help()
        return
    
    # Output as JSON (or plain text for markdown content)
    if isinstance(result, dict) and 'content' in result:
        # Plain markdown output
        print(result['content'])
    else:
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
