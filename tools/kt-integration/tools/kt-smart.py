#!/usr/bin/env python3
"""
KT Smart Helper - Intelligent context discovery
"""

import json
import sys
import argparse
from pathlib import Path
import subprocess

# Import other tools
TOOLS_DIR = Path(__file__).parent
KT_INDEX = TOOLS_DIR / "kt-index.py"
ISS_QUERY = TOOLS_DIR / "iss-query.py"
CONFIG_FILE = TOOLS_DIR.parent / "config" / "settings.json"

def load_config():
    """Load settings"""
    if not CONFIG_FILE.exists():
        return {}
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def run_tool(tool, args):
    """Run another tool and get JSON output"""
    result = subprocess.run(
        ['python', str(tool)] + args,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        try:
            return json.loads(result.stdout)
        except:
            return {"output": result.stdout}
    else:
        return {"error": result.stderr}

class SmartHelper:
    """Intelligent KT context helper"""
    
    def __init__(self):
        self.config = load_config()
    
    def discover(self, query):
        """Smart context discovery"""
        print(f"[DISCOVER] Searching for: {query}")
        
        # Search ISS
        results = run_tool(ISS_QUERY, ['search', query])
        
        if not results or 'error' in results:
            print("[ERROR] No results found")
            return
        
        print(f"\n[FOUND] {len(results)} relevant trees:")
        
        for i, result in enumerate(results[:self.config.get('max_auto_trees', 3)], 1):
            tree_id = result['tree_id']
            layer = result['layer']
            
            print(f"\n{i}. {tree_id} ({layer})")
            
            # Load strategic layer
            layer_data = run_tool(ISS_QUERY, ['layer', tree_id, 'strategic'])
            
            if 'content' in layer_data:
                # Show first few lines
                lines = layer_data['content'].split('\n')[:10]
                for line in lines:
                    if line.strip():
                        print(f"   {line}")
    
    def compare(self, tree1, tree2):
        """Compare two trees"""
        print(f"[COMPARE] {tree1} vs {tree2}")
        
        # Load strategic layers
        layer1 = run_tool(ISS_QUERY, ['layer', tree1, 'strategic'])
        layer2 = run_tool(ISS_QUERY, ['layer', tree2, 'strategic'])
        
        if 'error' in layer1 or 'error' in layer2:
            print("[ERROR] Error loading trees")
            return
        
        print(f"\n[TREE 1] {tree1}:")
        print(layer1.get('content', 'No content')[:500])
        
        print(f"\n[TREE 2] {tree2}:")
        print(layer2.get('content', 'No content')[:500])
    
    def suggest(self, task):
        """Suggest related context for a task"""
        print(f"[SUGGEST] Context for: {task}")
        
        # Extract keywords
        keywords = task.lower().split()
        
        # Search ISS for each keyword
        all_results = []
        for keyword in keywords:
            results = run_tool(ISS_QUERY, ['search', keyword])
            if results and 'error' not in results:
                all_results.extend(results)
        
        # Deduplicate by tree_id
        seen = set()
        unique_results = []
        for result in all_results:
            tree_id = result['tree_id']
            if tree_id not in seen:
                seen.add(tree_id)
                unique_results.append(result)
        
        if not unique_results:
            print("[ERROR] No relevant context found")
            return
        
        print(f"\n[SUGGESTED]")
        for i, result in enumerate(unique_results[:5], 1):
            print(f"{i}. {result['tree_id']}")
    
    def preload(self):
        """Preload context for session"""
        print("[PRELOAD] Loading session context...")
        
        # Get KT stats
        stats = run_tool(KT_INDEX, ['stats'])
        print(f"\n[KT STATUS]")
        print(f"   Branches: {stats.get('total_branches', 0)}")
        print(f"   Nodes: {stats.get('total_nodes', 0)}")
        
        # Get ISS stats
        iss_stats = run_tool(ISS_QUERY, ['stats'])
        print(f"\n[ISS STATUS]")
        print(f"   Trees: {iss_stats.get('total_trees', 0)}")
        print(f"   Summaries: {iss_stats.get('total_summaries', 0)}")
        
        # Check focus tree
        focus_result = run_tool(ISS_QUERY, ['layer', 'focus', 'strategic'])
        
        # Handle both JSON ({content: ...}) and wrapped text ({output: ...})
        content = focus_result.get('content') or focus_result.get('output')
        
        if content:
            print(f"\n[FOCUS CONTEXT]")
            
            # Skip YAML frontmatter and get meaningful content
            lines = content.split('\n')
            in_yaml = False
            shown = 0
            for line in lines:
                if line.strip() == '---':
                    in_yaml = not in_yaml
                    continue
                if not in_yaml and line.strip() and shown < 10:
                    print(f"   {line}")
                    shown += 1

def main():
    parser = argparse.ArgumentParser(description='KT Smart Helper')
    
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # Discover context
    discover_parser = subparsers.add_parser('discover', help='Discover context for query')
    discover_parser.add_argument('--query', required=True, help='Search query')
    
    # Compare trees
    compare_parser = subparsers.add_parser('compare', help='Compare two trees')
    compare_parser.add_argument('tree1', help='First tree ID')
    compare_parser.add_argument('tree2', help='Second tree ID')
    
    # Suggest context
    suggest_parser = subparsers.add_parser('suggest', help='Suggest context for task')
    suggest_parser.add_argument('--task', required=True, help='Task description')
    
    # Preload session
    subparsers.add_parser('preload', help='Preload session context')
    
    args = parser.parse_args()
    
    helper = SmartHelper()
    
    if args.command == 'discover':
        helper.discover(args.query)
    elif args.command == 'compare':
        helper.compare(args.tree1, args.tree2)
    elif args.command == 'suggest':
        helper.suggest(args.task)
    elif args.command == 'preload':
        helper.preload()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
