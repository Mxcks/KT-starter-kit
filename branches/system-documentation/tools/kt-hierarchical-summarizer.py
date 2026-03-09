#!/usr/bin/env python3
"""
KT Hierarchical Summary Generator
Creates standardized markdown summaries with 3-layer hierarchy for ISS
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict

KT_PATH = Path("C:/dev/KT")
sys.path.insert(0, str(KT_PATH))


class HierarchicalSummaryGenerator:
    """Generate standardized hierarchical markdown summaries for ISS"""
    
    def __init__(self):
        self.kt_path = KT_PATH
        self.nodes_path = self.kt_path / "nodes"
        self.output_path = self.kt_path / "index-scrolling-system" / "meta-tree" / "summaries"
        self.output_path.mkdir(parents=True, exist_ok=True)
        
    def load_enriched_nodes(self) -> List[Dict[str, Any]]:
        """Load all enriched nodes with summaries"""
        nodes = []
        
        for jsonl_file in self.nodes_path.glob("*-enriched.jsonl"):
            try:
                with open(jsonl_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            node = json.loads(line)
                            # Only include nodes that have summaries
                            content = node.get('content', {})
                            if isinstance(content, dict) and content.get('summary'):
                                nodes.append(node)
            except Exception as e:
                print(f"[ERROR] Loading {jsonl_file}: {e}")
        
        return nodes
    
    def group_by_branch(self, nodes: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group nodes by branch"""
        branches = defaultdict(list)
        
        for node in nodes:
            branch = node.get('branch', 'unknown')
            branches[branch].append(node)
        
        return dict(branches)
    
    def classify_node_layer(self, node: Dict[str, Any]) -> str:
        """Classify node into strategic/tactical/implementation layer"""
        
        node_type = node.get('type', '')
        tags = node.get('tags', {})
        
        # Get tag categories
        if isinstance(tags, dict):
            categories = tags.get('categories', [])
        elif isinstance(tags, list):
            categories = tags
        else:
            categories = []
        
        # Strategic: High-level decisions, architecture
        strategic_indicators = ['architecture', 'decision', 'strategy', 'goal', 'priority']
        if node_type in ['decision'] or any(ind in str(categories).lower() for ind in strategic_indicators):
            return 'strategic'
        
        # Implementation: Specific code, commits, details
        implementation_indicators = ['commit', 'bug', 'fix', 'implementation', 'code']
        if node_type in ['commit'] or any(ind in str(categories).lower() for ind in implementation_indicators):
            return 'implementation'
        
        # Tactical: Everything in between
        return 'tactical'
    
    def estimate_tokens(self, text: str) -> int:
        """Rough token estimate (4 chars ≈ 1 token)"""
        return len(text) // 4
    
    def generate_branch_summary(
        self, 
        branch: str, 
        nodes: List[Dict[str, Any]]
    ) -> Dict[str, str]:
        """Generate 3-layer summary for a branch"""
        
        # Classify nodes by layer
        layers = {
            'strategic': [],
            'tactical': [],
            'implementation': []
        }
        
        for node in nodes:
            layer = self.classify_node_layer(node)
            layers[layer].append(node)
        
        # Generate markdown for each layer
        summaries = {}
        
        for layer_name, layer_nodes in layers.items():
            if not layer_nodes:
                continue
                
            md = self._generate_layer_markdown(branch, layer_name, layer_nodes)
            summaries[layer_name] = md
        
        return summaries
    
    def _generate_layer_markdown(
        self,
        branch: str,
        layer: str,
        nodes: List[Dict[str, Any]]
    ) -> str:
        """Generate markdown for a single layer"""
        
        # Count by node type
        type_counts = defaultdict(int)
        for node in nodes:
            type_counts[node.get('type', 'unknown')] += 1
        
        # Extract all summaries
        summaries = []
        for node in nodes:
            content = node.get('content', {})
            if isinstance(content, dict):
                summary = content.get('summary', '')
            elif isinstance(content, str):
                summary = content
            else:
                summary = ''
            
            if summary:
                summaries.append({
                    'id': node.get('id', ''),
                    'type': node.get('type', ''),
                    'summary': summary
                })
        
        # Estimate tokens
        total_text = ' '.join([s['summary'] for s in summaries])
        tokens = self.estimate_tokens(total_text)
        
        # Generate YAML frontmatter
        frontmatter = f"""---
branch: {branch}
layer: {layer}
node_count: {len(nodes)}
token_estimate: {tokens}
generated_at: {datetime.utcnow().isoformat()}Z
generator: OpenClaw-Macks-Hierarchical-Summary-v1
node_types:
{self._yaml_list(type_counts)}
---

"""
        
        # Generate body
        body = f"""# {branch.title()} - {layer.title()} Layer

**Summary:** {len(nodes)} nodes covering {', '.join(type_counts.keys())}

---

## Overview

This layer contains {layer}-level information for the {branch} branch.

"""
        
        # Add node summaries by type
        for node_type, count in sorted(type_counts.items()):
            body += f"## {node_type.title()} ({count})\n\n"
            
            type_nodes = [s for s in summaries if s['type'] == node_type]
            for s in type_nodes:
                body += f"### Node {s['id']}\n\n"
                body += f"{s['summary']}\n\n"
                body += "---\n\n"
        
        return frontmatter + body
    
    def _yaml_list(self, items: Dict[str, int]) -> str:
        """Format dict as YAML list"""
        return '\n'.join([f"  {k}: {v}" for k, v in items.items()])
    
    def generate_combined_summary(
        self,
        branch: str,
        layer_summaries: Dict[str, str]
    ) -> str:
        """Generate combined summary with all layers"""
        
        # Get total stats
        total_nodes = 0
        total_tokens = 0
        
        for layer_md in layer_summaries.values():
            # Parse frontmatter to get counts
            if '---' in layer_md:
                fm_end = layer_md.find('---', 3)
                frontmatter = layer_md[3:fm_end]
                
                for line in frontmatter.split('\n'):
                    if 'node_count:' in line:
                        total_nodes += int(line.split(':')[1].strip())
                    if 'token_estimate:' in line:
                        total_tokens += int(line.split(':')[1].strip())
        
        # Generate combined frontmatter
        frontmatter = f"""---
branch: {branch}
type: combined-hierarchical-summary
layers: {list(layer_summaries.keys())}
total_nodes: {total_nodes}
total_tokens: {total_tokens}
generated_at: {datetime.utcnow().isoformat()}Z
generator: OpenClaw-Macks-Hierarchical-Summary-v1
structure:
  strategic: High-level decisions and architecture
  tactical: Implementation approaches and patterns
  implementation: Specific code, commits, and details
---

"""
        
        # Generate body
        body = f"""# {branch.title()} - Complete Hierarchical Summary

**Total Nodes:** {total_nodes} | **Estimated Tokens:** {total_tokens}

---

## Quick Navigation

- [Strategic Layer](#strategic-layer) - High-level overview
- [Tactical Layer](#tactical-layer) - Implementation approaches
- [Implementation Layer](#implementation-layer) - Detailed work

---

## How to Use This Summary

**For quick context:** Read Strategic layer only  
**For implementation planning:** Strategic + Tactical  
**For full details:** All three layers

---

"""
        
        # Add each layer
        for layer_name in ['strategic', 'tactical', 'implementation']:
            if layer_name in layer_summaries:
                body += f"## {layer_name.title()} Layer\n\n"
                body += f"<details>\n<summary>Click to expand {layer_name} layer</summary>\n\n"
                
                # Get body from layer (skip frontmatter)
                layer_md = layer_summaries[layer_name]
                if '---' in layer_md:
                    fm_end = layer_md.find('---', 3)
                    layer_body = layer_md[fm_end + 3:].strip()
                else:
                    layer_body = layer_md
                
                body += layer_body + "\n\n"
                body += "</details>\n\n"
                body += "---\n\n"
        
        return frontmatter + body
    
    def save_summaries(
        self,
        branch: str,
        layer_summaries: Dict[str, str],
        combined_summary: str
    ):
        """Save all summary files"""
        
        # Create branch directory
        branch_dir = self.output_path / branch
        branch_dir.mkdir(parents=True, exist_ok=True)
        
        # Save individual layers
        for layer_name, content in layer_summaries.items():
            file_path = branch_dir / f"{layer_name}.md"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] Created {file_path}")
        
        # Save combined
        combined_path = branch_dir / "summary.md"
        with open(combined_path, 'w', encoding='utf-8') as f:
            f.write(combined_summary)
        print(f"[OK] Created {combined_path}")
        
        # Create JSON index for ISS
        index = {
            "branch": branch,
            "layers": list(layer_summaries.keys()),
            "files": {
                layer: f"{branch}/{layer}.md"
                for layer in layer_summaries.keys()
            },
            "combined": f"{branch}/summary.md",
            "generated_at": datetime.utcnow().isoformat() + "Z"
        }
        
        index_path = branch_dir / "index.json"
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)
        print(f"[OK] Created {index_path}")
    
    def generate_all(self):
        """Generate hierarchical summaries for all branches"""
        
        print("[INFO] Loading enriched nodes...")
        nodes = self.load_enriched_nodes()
        print(f"[OK] Loaded {len(nodes)} enriched nodes")
        
        print("[INFO] Grouping by branch...")
        branches = self.group_by_branch(nodes)
        print(f"[OK] Found {len(branches)} branches")
        
        print("[INFO] Generating hierarchical summaries...")
        
        for branch, branch_nodes in branches.items():
            print(f"\n[INFO] Processing branch: {branch} ({len(branch_nodes)} nodes)")
            
            # Generate layer summaries
            layer_summaries = self.generate_branch_summary(branch, branch_nodes)
            
            if not layer_summaries:
                print(f"[WARN] No summaries generated for {branch}")
                continue
            
            # Generate combined
            combined = self.generate_combined_summary(branch, layer_summaries)
            
            # Save
            self.save_summaries(branch, layer_summaries, combined)
            
            print(f"[OK] Completed {branch}: {list(layer_summaries.keys())}")
        
        print(f"\n[SUCCESS] Generated hierarchical summaries for {len(branches)} branches")
        print(f"[INFO] Output: {self.output_path}")


def main():
    """Run hierarchical summary generation"""
    
    print("=" * 60)
    print("KT Hierarchical Summary Generator")
    print("=" * 60)
    print()
    
    generator = HierarchicalSummaryGenerator()
    generator.generate_all()
    
    print()
    print("=" * 60)
    print("Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
