#!/usr/bin/env python3
"""
ISS Hierarchical Summary Indexer
Updates ISS with the new hierarchical markdown summaries
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import yaml

KT_PATH = Path("C:/dev/KT")
sys.path.insert(0, str(KT_PATH))


class ISSHierarchicalIndexer:
    """Index hierarchical summaries for ISS access"""
    
    def __init__(self):
        self.kt_path = KT_PATH
        self.summaries_path = self.kt_path / "index-scrolling-system" / "meta-tree" / "summaries"
        self.index_path = self.kt_path / "index-scrolling-system" / "meta-tree" / "index"
        self.index_path.mkdir(parents=True, exist_ok=True)
        
    def scan_summaries(self) -> List[Dict[str, Any]]:
        """Scan all generated hierarchical summaries"""
        summaries = []
        
        for branch_dir in self.summaries_path.iterdir():
            if not branch_dir.is_dir():
                continue
            
            index_file = branch_dir / "index.json"
            if not index_file.exists():
                continue
            
            try:
                with open(index_file, 'r') as f:
                    index_data = json.load(f)
                
                # Load layer metadata from each layer file
                layers = {}
                for layer in index_data.get('layers', []):
                    layer_file = branch_dir / f"{layer}.md"
                    if layer_file.exists():
                        metadata = self._parse_frontmatter(layer_file)
                        layers[layer] = metadata
                
                summary_info = {
                    'branch': index_data['branch'],
                    'layers': index_data['layers'],
                    'files': {
                        layer: str(branch_dir / f"{layer}.md")
                        for layer in index_data['layers']
                    },
                    'combined': str(branch_dir / "summary.md"),
                    'metadata': layers,
                    'generated_at': index_data.get('generated_at'),
                    'total_nodes': sum(m.get('node_count', 0) for m in layers.values()),
                    'total_tokens': sum(m.get('token_estimate', 0) for m in layers.values())
                }
                
                summaries.append(summary_info)
                
            except Exception as e:
                print(f"[ERROR] Processing {branch_dir}: {e}")
        
        return summaries
    
    def _parse_frontmatter(self, file_path: Path) -> Dict[str, Any]:
        """Parse YAML frontmatter from markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.startswith('---'):
                return {}
            
            # Find end of frontmatter
            end = content.find('---', 3)
            if end == -1:
                return {}
            
            frontmatter = content[3:end].strip()
            return yaml.safe_load(frontmatter)
            
        except Exception as e:
            print(f"[WARN] Could not parse frontmatter from {file_path}: {e}")
            return {}
    
    def create_master_index(self, summaries: List[Dict[str, Any]]):
        """Create master index of all hierarchical summaries"""
        
        index = {
            'version': '1.0',
            'type': 'hierarchical-summaries-index',
            'generated_at': datetime.utcnow().isoformat() + 'Z',
            'total_branches': len(summaries),
            'branches': {}
        }
        
        # Index by branch
        for summary in summaries:
            branch = summary['branch']
            index['branches'][branch] = {
                'layers': summary['layers'],
                'files': {
                    layer: str(Path(file).relative_to(self.summaries_path))
                    for layer, file in summary['files'].items()
                },
                'combined': str(Path(summary['combined']).relative_to(self.summaries_path)),
                'total_nodes': summary['total_nodes'],
                'total_tokens': summary['total_tokens'],
                'generated_at': summary['generated_at']
            }
        
        # Save master index
        master_index_file = self.index_path / "hierarchical-summaries.json"
        with open(master_index_file, 'w') as f:
            json.dump(index, f, indent=2)
        
        print(f"[OK] Created master index: {master_index_file}")
        return index
    
    def create_layer_index(self, summaries: List[Dict[str, Any]]):
        """Create index organized by layer type"""
        
        layer_index = {
            'strategic': [],
            'tactical': [],
            'implementation': []
        }
        
        for summary in summaries:
            branch = summary['branch']
            
            for layer in summary['layers']:
                if layer in layer_index:
                    layer_metadata = summary['metadata'].get(layer, {})
                    layer_index[layer].append({
                        'branch': branch,
                        'file': str(Path(summary['files'][layer]).relative_to(self.summaries_path)),
                        'node_count': layer_metadata.get('node_count', 0),
                        'token_estimate': layer_metadata.get('token_estimate', 0)
                    })
        
        # Save layer index
        layer_index_file = self.index_path / "by-layer.json"
        with open(layer_index_file, 'w') as f:
            json.dump(layer_index, f, indent=2)
        
        print(f"[OK] Created layer index: {layer_index_file}")
        return layer_index
    
    def create_quick_access_map(self, summaries: List[Dict[str, Any]]):
        """Create quick access map for ISS API"""
        
        quick_map = {}
        
        for summary in summaries:
            branch = summary['branch']
            quick_map[branch] = {
                # Fast strategic load (smallest token count)
                'strategic': str(Path(summary['files'].get('strategic', '')).relative_to(self.summaries_path)) if 'strategic' in summary['layers'] else None,
                
                # Full progressive load
                'progressive': [
                    str(Path(summary['files'][layer]).relative_to(self.summaries_path))
                    for layer in ['strategic', 'tactical', 'implementation']
                    if layer in summary['layers']
                ],
                
                # Combined summary (all layers)
                'combined': str(Path(summary['combined']).relative_to(self.summaries_path)),
                
                # Metadata for smart loading
                'metadata': {
                    'total_nodes': summary['total_nodes'],
                    'total_tokens': summary['total_tokens'],
                    'available_layers': summary['layers'],
                    'strategic_tokens': summary['metadata'].get('strategic', {}).get('token_estimate', 0)
                }
            }
        
        # Save quick access map
        quick_map_file = self.index_path / "quick-access.json"
        with open(quick_map_file, 'w') as f:
            json.dump(quick_map, f, indent=2)
        
        print(f"[OK] Created quick access map: {quick_map_file}")
        return quick_map
    
    def generate_stats(self, summaries: List[Dict[str, Any]]):
        """Generate statistics about hierarchical summaries"""
        
        stats = {
            'total_branches': len(summaries),
            'total_nodes': sum(s['total_nodes'] for s in summaries),
            'total_tokens': sum(s['total_tokens'] for s in summaries),
            'by_layer': {
                'strategic': len([s for s in summaries if 'strategic' in s['layers']]),
                'tactical': len([s for s in summaries if 'tactical' in s['layers']]),
                'implementation': len([s for s in summaries if 'implementation' in s['layers']])
            },
            'average_tokens_per_branch': round(sum(s['total_tokens'] for s in summaries) / len(summaries)) if summaries else 0,
            'branches': [s['branch'] for s in summaries]
        }
        
        # Save stats
        stats_file = self.index_path / "stats.json"
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
        
        print(f"[OK] Created stats: {stats_file}")
        return stats
    
    def update_iss(self):
        """Complete ISS update with hierarchical summaries"""
        
        print("[INFO] Scanning hierarchical summaries...")
        summaries = self.scan_summaries()
        print(f"[OK] Found {len(summaries)} branch summaries")
        
        if not summaries:
            print("[WARN] No summaries found to index")
            return
        
        print("[INFO] Creating indexes...")
        
        # Create all indexes
        master_index = self.create_master_index(summaries)
        layer_index = self.create_layer_index(summaries)
        quick_map = self.create_quick_access_map(summaries)
        stats = self.generate_stats(summaries)
        
        print("\n[SUCCESS] ISS indexes updated!")
        print(f"[INFO] Total branches: {stats['total_branches']}")
        print(f"[INFO] Total nodes: {stats['total_nodes']}")
        print(f"[INFO] Total tokens: {stats['total_tokens']}")
        print(f"[INFO] Average tokens/branch: {stats['average_tokens_per_branch']}")
        print(f"[INFO] Strategic layers: {stats['by_layer']['strategic']}")
        print(f"[INFO] Tactical layers: {stats['by_layer']['tactical']}")
        print(f"[INFO] Implementation layers: {stats['by_layer']['implementation']}")


def main():
    """Update ISS with hierarchical summaries"""
    
    print("=" * 60)
    print("ISS Hierarchical Summary Indexer")
    print("=" * 60)
    print()
    
    indexer = ISSHierarchicalIndexer()
    indexer.update_iss()
    
    print()
    print("=" * 60)
    print("ISS Updated!")
    print("=" * 60)


if __name__ == "__main__":
    main()
