#!/usr/bin/env python3
"""
KT Starter Kit - Complete Workflow Automation
Demonstrates the full cycle: Create → Structure → Summarize → Index → Query
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

KT_ROOT = Path(__file__).parent
TOOLS_DIR = KT_ROOT / "branches" / "system-documentation" / "tools"

class KTWorkflow:
    """Complete KT workflow automation"""
    
    def __init__(self, kt_root: Path = KT_ROOT):
        self.kt_root = kt_root
        self.branches_dir = kt_root / "branches"
        self.iss_dir = kt_root / "index-scrolling-system"
        self.tools_dir = TOOLS_DIR
        
    def create_example_branch(self, branch_name: str, example_type: str = "simple"):
        """
        Create an example branch with nodes
        
        Args:
            branch_name: Name of branch to create
            example_type: "simple" (5 nodes), "medium" (12 nodes), or "complex" (25 nodes)
        """
        print(f"\n[STEP 1] Creating example branch: {branch_name}")
        
        branch_dir = self.branches_dir / branch_name
        branch_dir.mkdir(parents=True, exist_ok=True)
        knowledge_dir = branch_dir / "knowledge"
        knowledge_dir.mkdir(exist_ok=True)
        
        # Create nodes based on example type
        nodes = self._get_example_nodes(branch_name, example_type)
        
        # Write to tree.jsonl
        tree_file = knowledge_dir / "tree.jsonl"
        with open(tree_file, 'w', encoding='utf-8') as f:
            for node in nodes:
                f.write(json.dumps(node) + '\n')
        
        print(f"[OK] Created {branch_name} with {len(nodes)} nodes")
        print(f"[OK] Location: {branch_dir}")
        
        return branch_dir
    
    def _get_example_nodes(self, branch_name: str, example_type: str) -> list:
        """Generate example nodes"""
        
        base_nodes = [
            {
                "id": 0,
                "type": "init",
                "branch": branch_name,
                "message": f"{branch_name.replace('-', ' ').title()} - Example Project",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "tags": ["example", example_type]
            }
        ]
        
        if example_type == "simple":
            # 5 nodes total - simple todo app
            base_nodes.extend([
                {
                    "id": 1,
                    "type": "decision",
                    "message": "Use localStorage for data persistence",
                    "reasoning": "Simple, no backend needed, good for learning",
                    "decision": "localStorage with JSON serialization",
                    "tags": ["architecture", "storage"],
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                },
                {
                    "id": 2,
                    "type": "commit",
                    "message": "Add task creation functionality",
                    "content": "Users can add new tasks with title and description",
                    "tags": ["feature", "crud"],
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                },
                {
                    "id": 3,
                    "type": "commit",
                    "message": "Add task completion toggle",
                    "content": "Click checkbox to mark tasks complete/incomplete",
                    "tags": ["feature", "ui"],
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                },
                {
                    "id": 4,
                    "type": "summary",
                    "message": "Basic CRUD operations complete",
                    "content": "Todo app has create, read, update (toggle), and persist to localStorage. Ready for basic use.",
                    "tags": ["milestone"],
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            ])
        
        elif example_type == "medium":
            # 12 nodes - API with authentication
            base_nodes.extend([
                {
                    "id": 1,
                    "type": "decision",
                    "message": "Use JWT for authentication",
                    "reasoning": "Stateless, scalable, industry standard",
                    "decision": "JWT with refresh token pattern",
                    "tags": ["architecture", "auth", "security"],
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                },
                {
                    "id": 2,
                    "type": "decision",
                    "message": "PostgreSQL for data storage",
                    "reasoning": "ACID compliance, relational data, mature ecosystem",
                    "decision": "PostgreSQL 14+ with connection pooling",
                    "tags": ["architecture", "database"],
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                },
                # Add more nodes...
                {
                    "id": 11,
                    "type": "summary",
                    "message": "API v1 complete with authentication",
                    "content": "REST API with JWT auth, user management, and core endpoints deployed",
                    "tags": ["milestone", "v1"],
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            ])
        
        return base_nodes
    
    def generate_summaries(self, branch_name: str):
        """
        Generate fractal summaries for branch
        
        Args:
            branch_name: Branch to summarize
        """
        print(f"\n[STEP 2] Generating fractal summaries for {branch_name}")
        
        summarizer = self.tools_dir / "kt-hierarchical-summarizer.py"
        
        if not summarizer.exists():
            print(f"[ERROR] Summarizer not found at {summarizer}")
            return
        
        # Run summarizer
        result = subprocess.run(
            [sys.executable, str(summarizer), "--branch", branch_name],
            capture_output=True,
            text=True,
            cwd=self.tools_dir
        )
        
        if result.returncode == 0:
            print("[OK] Summaries generated successfully")
            
            # Show summary location
            summary_dir = self.iss_dir / "meta-tree" / "summaries" / branch_name
            if summary_dir.exists():
                layers = list(summary_dir.glob("*.md"))
                print(f"[OK] Generated {len(layers)} layer summaries:")
                for layer in layers:
                    print(f"     - {layer.name}")
        else:
            print(f"[ERROR] Summarizer failed: {result.stderr}")
    
    def update_iss_index(self):
        """Update ISS indexes"""
        print(f"\n[STEP 3] Updating ISS indexes")
        
        indexer = self.tools_dir / "iss-hierarchical-indexer.py"
        
        if not indexer.exists():
            print(f"[ERROR] Indexer not found at {indexer}")
            return
        
        # Run indexer
        result = subprocess.run(
            [sys.executable, str(indexer)],
            capture_output=True,
            text=True,
            cwd=self.tools_dir
        )
        
        if result.returncode == 0:
            print("[OK] ISS indexes updated")
            
            # Show index files
            index_dir = self.iss_dir / "meta-tree" / "index"
            if index_dir.exists():
                indexes = list(index_dir.glob("*.json"))
                print(f"[OK] Generated {len(indexes)} index files")
        else:
            print(f"[ERROR] Indexer failed: {result.stderr}")
    
    def query_context(self, query: str):
        """
        Query for relevant context
        
        Args:
            query: Search query
        """
        print(f"\n[STEP 4] Querying for context: '{query}'")
        
        # Use kt-integration tools
        search_tool = self.kt_root / "tools" / "kt-integration" / "tools" / "iss-query.py"
        
        if not search_tool.exists():
            print(f"[ERROR] Search tool not found")
            return
        
        # Run search
        result = subprocess.run(
            [sys.executable, str(search_tool), "search", query],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            try:
                results = json.loads(result.stdout)
                print(f"[OK] Found {len(results)} relevant trees:")
                for r in results:
                    print(f"     - {r['tree_id']} ({r['layer']})")
            except:
                print(result.stdout)
        else:
            print(f"[ERROR] Search failed: {result.stderr}")
    
    def demonstrate_token_efficiency(self, branch_name: str):
        """Show token efficiency comparison"""
        print(f"\n[STEP 5] Token Efficiency Demonstration")
        
        summary_dir = self.iss_dir / "meta-tree" / "summaries" / branch_name
        
        if not summary_dir.exists():
            print("[ERROR] No summaries found")
            return
        
        # Count tokens in each layer
        strategic = summary_dir / "strategic.md"
        tactical = summary_dir / "tactical.md"
        implementation = summary_dir / "implementation.md"
        
        def count_tokens(file_path):
            """Rough token count (words * 1.3)"""
            if not file_path.exists():
                return 0
            text = file_path.read_text(encoding='utf-8')
            words = len(text.split())
            return int(words * 1.3)
        
        strategic_tokens = count_tokens(strategic)
        tactical_tokens = count_tokens(tactical)
        implementation_tokens = count_tokens(implementation)
        total_tokens = strategic_tokens + tactical_tokens + implementation_tokens
        
        # Estimate full tree tokens (assume 25,000 for medium project)
        full_tree_estimate = 25000
        
        print(f"\n{'Layer':<20} {'Tokens':<10} {'% of Full Tree':<15}")
        print("=" * 45)
        
        if strategic_tokens > 0:
            savings = ((full_tree_estimate - strategic_tokens) / full_tree_estimate) * 100
            print(f"{'Strategic':<20} {strategic_tokens:<10} {savings:.1f}% savings")
        
        if tactical_tokens > 0:
            combined = strategic_tokens + tactical_tokens
            savings = ((full_tree_estimate - combined) / full_tree_estimate) * 100
            print(f"{'+ Tactical':<20} {tactical_tokens:<10} {savings:.1f}% savings")
        
        if implementation_tokens > 0:
            savings = ((full_tree_estimate - total_tokens) / full_tree_estimate) * 100
            print(f"{'+ Implementation':<20} {implementation_tokens:<10} {savings:.1f}% savings")
        
        print("=" * 45)
        print(f"{'Full Tree (est.)':<20} {full_tree_estimate:<10} {'0% savings':<15}")
        
        print(f"\n[INSIGHT] Loading strategic only saves {((full_tree_estimate - strategic_tokens) / full_tree_estimate * 100):.0f}% tokens!")

def main():
    """Run complete workflow demonstration"""
    
    print("=" * 60)
    print("KT Starter Kit - Complete Workflow Demonstration")
    print("=" * 60)
    
    workflow = KTWorkflow()
    
    # Create example branch
    branch_name = "example-todo-app"
    workflow.create_example_branch(branch_name, "simple")
    
    # Generate summaries
    workflow.generate_summaries(branch_name)
    
    # Update ISS
    workflow.update_iss_index()
    
    # Query for context
    workflow.query_context("todo")
    
    # Show token efficiency
    workflow.demonstrate_token_efficiency(branch_name)
    
    print("\n" + "=" * 60)
    print("Complete! Your example branch is ready.")
    print("=" * 60)
    print(f"\nNext steps:")
    print(f"1. View summaries: cd index-scrolling-system/meta-tree/summaries/{branch_name}")
    print(f"2. Query: python tools/kt-integration/tools/iss-query.py layer {branch_name} strategic")
    print(f"3. Create your own: Modify this script with your project data")

if __name__ == "__main__":
    main()
