#!/usr/bin/env python3
"""
KT Intelligent System Discovery & Auto-Loader
Understands what systems exist and loads relevant ones automatically based on context
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml

KT_PATH = Path("C:/dev/KT")
sys.path.insert(0, str(KT_PATH))


class SystemDiscovery:
    """Discover and map all available systems in KT"""
    
    def __init__(self):
        self.kt_path = KT_PATH
        self.index_path = self.kt_path / "index-scrolling-system" / "meta-tree" / "index"
        self.summaries_path = self.kt_path / "index-scrolling-system" / "meta-tree" / "summaries"
        
        # Load indexes
        self.master_index = self._load_json(self.index_path / "hierarchical-summaries.json")
        self.quick_access = self._load_json(self.index_path / "quick-access.json")
        self.layer_index = self._load_json(self.index_path / "by-layer.json")
        
        # System map
        self.systems_map = {}
        
    def _load_json(self, file_path: Path) -> Dict:
        """Load JSON file safely"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def discover_systems(self) -> Dict[str, Any]:
        """Discover all available systems from hierarchical summaries"""
        
        print("[INFO] Discovering systems...")
        
        systems = {}
        
        if not self.master_index or 'branches' not in self.master_index:
            print("[WARN] No master index found")
            return systems
        
        for branch, metadata in self.master_index['branches'].items():
            # Load strategic layer to understand system purpose
            strategic_file = self.summaries_path / metadata['files'].get('strategic', '')
            
            if strategic_file.exists():
                system_info = self._extract_system_info(branch, strategic_file, metadata)
                systems[branch] = system_info
                print(f"[OK] Discovered: {branch} - {system_info['purpose']}")
        
        self.systems_map = systems
        return systems
    
    def _extract_system_info(
        self, 
        branch: str, 
        strategic_file: Path, 
        metadata: Dict
    ) -> Dict[str, Any]:
        """Extract system information from strategic layer"""
        
        # Parse frontmatter
        frontmatter = {}
        content = ""
        
        try:
            with open(strategic_file, 'r', encoding='utf-8') as f:
                text = f.read()
            
            if text.startswith('---'):
                end = text.find('---', 3)
                if end != -1:
                    frontmatter = yaml.safe_load(text[3:end])
                    content = text[end+3:].strip()
        except:
            pass
        
        # Extract purpose (first paragraph after headers)
        purpose = self._extract_purpose(content)
        
        # Extract capabilities (from headers)
        capabilities = self._extract_capabilities(content)
        
        # Infer system type
        system_type = self._infer_system_type(branch, content)
        
        return {
            'branch': branch,
            'purpose': purpose,
            'type': system_type,
            'capabilities': capabilities,
            'layers': metadata.get('layers', []),
            'total_tokens': metadata.get('total_tokens', 0),
            'node_count': metadata.get('total_nodes', 0),
            'strategic_file': str(strategic_file.relative_to(self.summaries_path)),
            'keywords': self._extract_keywords(content)
        }
    
    def _extract_purpose(self, content: str) -> str:
        """Extract purpose from content"""
        lines = content.split('\n')
        
        # Look for "Summary:" or first paragraph
        for i, line in enumerate(lines):
            if line.strip().startswith('**Summary:**'):
                return line.replace('**Summary:**', '').strip()
            
            # First non-empty, non-header paragraph
            if line.strip() and not line.startswith('#') and not line.startswith('**'):
                return line.strip()[:200]
        
        return f"System: {content[:100]}" if content else "Unknown purpose"
    
    def _extract_capabilities(self, content: str) -> List[str]:
        """Extract capabilities from content headers"""
        capabilities = []
        
        lines = content.split('\n')
        for line in lines:
            # Look for ### headers (specific capabilities)
            if line.startswith('### '):
                cap = line.replace('### ', '').strip()
                if cap and not cap.lower().startswith('node'):
                    capabilities.append(cap)
        
        return capabilities[:10]  # Limit to 10
    
    def _infer_system_type(self, branch: str, content: str) -> str:
        """Infer system type from branch name and content"""
        
        branch_lower = branch.lower()
        content_lower = content.lower()
        
        if 'ui' in branch_lower or 'builder' in branch_lower:
            return 'ui-system'
        elif 'research' in branch_lower or 'lab' in branch_lower:
            return 'research-system'
        elif 'workspace' in branch_lower:
            return 'workspace-system'
        elif 'knowledge' in branch_lower or 'tree' in branch_lower:
            return 'knowledge-system'
        elif 'orchestrat' in branch_lower or 'workflow' in branch_lower:
            return 'automation-system'
        elif 'decision' in content_lower:
            return 'decision-system'
        else:
            return 'general-system'
    
    def _extract_keywords(self, content: str) -> List[str]:
        """Extract keywords from content"""
        # Simple keyword extraction
        common_keywords = [
            'architecture', 'api', 'automation', 'build', 'component',
            'data', 'decision', 'deployment', 'design', 'development',
            'framework', 'integration', 'interface', 'pattern', 'system',
            'testing', 'ui', 'workflow'
        ]
        
        content_lower = content.lower()
        found = [kw for kw in common_keywords if kw in content_lower]
        
        return found[:10]
    
    def save_system_map(self, output_path: Optional[Path] = None):
        """Save system map to JSON"""
        
        if not output_path:
            output_path = self.index_path / "system-map.json"
        
        system_map_data = {
            'generated_at': self.master_index.get('generated_at'),
            'total_systems': len(self.systems_map),
            'systems': self.systems_map
        }
        
        with open(output_path, 'w') as f:
            json.dump(system_map_data, f, indent=2)
        
        print(f"[OK] Saved system map: {output_path}")
        return output_path


class IntelligentLoader:
    """Automatically load relevant systems based on query/context"""
    
    def __init__(self, system_map: Dict[str, Any]):
        self.system_map = system_map
        self.summaries_path = Path("C:/dev/KT/index-scrolling-system/meta-tree/summaries")
    
    def find_relevant_systems(
        self, 
        query: str, 
        max_systems: int = 5
    ) -> List[Dict[str, Any]]:
        """Find systems relevant to query"""
        
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        # Score each system
        scored = []
        
        for system_id, system_info in self.system_map.items():
            score = 0
            
            # Match branch name
            if any(word in system_id.lower() for word in query_words):
                score += 10
            
            # Match purpose
            purpose_words = set(system_info['purpose'].lower().split())
            score += len(query_words & purpose_words) * 5
            
            # Match keywords
            keyword_matches = sum(1 for kw in system_info['keywords'] if kw in query_lower)
            score += keyword_matches * 3
            
            # Match type
            if system_info['type'].replace('-', ' ') in query_lower:
                score += 7
            
            # Match capabilities
            for cap in system_info['capabilities']:
                if any(word in cap.lower() for word in query_words):
                    score += 2
            
            if score > 0:
                scored.append((score, system_id, system_info))
        
        # Sort by score, take top N
        scored.sort(reverse=True, key=lambda x: x[0])
        
        return [
            {
                'system': system_id,
                'relevance_score': score,
                'info': info
            }
            for score, system_id, info in scored[:max_systems]
        ]
    
    def load_systems(
        self,
        query: str,
        layer: str = 'strategic',
        max_systems: int = 3
    ) -> Dict[str, str]:
        """Load relevant systems and return their content"""
        
        relevant = self.find_relevant_systems(query, max_systems)
        
        loaded = {}
        
        for item in relevant:
            system_id = item['system']
            info = item['info']
            
            # Get file path for requested layer
            if layer in info['layers']:
                file_path = self.summaries_path / info['strategic_file'].replace('strategic.md', f'{layer}.md')
            else:
                # Fallback to strategic if layer not available
                file_path = self.summaries_path / info['strategic_file']
            
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        loaded[system_id] = {
                            'content': f.read(),
                            'layer': layer,
                            'relevance': item['relevance_score'],
                            'purpose': info['purpose']
                        }
                except:
                    pass
        
        return loaded
    
    def get_context_for_task(
        self,
        task: str,
        include_implementation: bool = False
    ) -> str:
        """Get full context for a task by auto-loading relevant systems"""
        
        # Determine which layer to load
        layer = 'implementation' if include_implementation else 'strategic'
        
        # Load relevant systems
        systems = self.load_systems(task, layer=layer, max_systems=3)
        
        if not systems:
            return f"No relevant systems found for task: {task}"
        
        # Build context
        context_parts = [f"# Context for: {task}\n"]
        
        for system_id, data in systems.items():
            context_parts.append(f"\n## System: {system_id}")
            context_parts.append(f"**Purpose:** {data['purpose']}")
            context_parts.append(f"**Relevance Score:** {data['relevance']}")
            context_parts.append(f"**Layer:** {data['layer']}\n")
            context_parts.append("---\n")
            context_parts.append(data['content'])
            context_parts.append("\n---\n")
        
        return '\n'.join(context_parts)


def main():
    """Run system discovery and create intelligent loader"""
    
    print("=" * 60)
    print("KT Intelligent System Discovery")
    print("=" * 60)
    print()
    
    # Discover systems
    discovery = SystemDiscovery()
    systems = discovery.discover_systems()
    
    print(f"\n[SUCCESS] Discovered {len(systems)} systems")
    
    # Save system map
    discovery.save_system_map()
    
    # Create intelligent loader
    loader = IntelligentLoader(systems)
    
    print("\n[INFO] Testing intelligent loader...")
    
    # Test queries
    test_queries = [
        "How do I build UI components?",
        "What systems handle automation?",
        "Knowledge management and organization"
    ]
    
    for query in test_queries:
        print(f"\n[TEST] Query: '{query}'")
        relevant = loader.find_relevant_systems(query, max_systems=3)
        
        for item in relevant:
            print(f"  - {item['system']} (score: {item['relevance_score']})")
    
    print("\n=" * 60)
    print("System Discovery Complete!")
    print("=" * 60)
    print("\nUsage:")
    print("  from kt_intelligent_loader import SystemDiscovery, IntelligentLoader")
    print("  loader = IntelligentLoader(systems_map)")
    print("  context = loader.get_context_for_task('your task here')")


if __name__ == "__main__":
    main()
