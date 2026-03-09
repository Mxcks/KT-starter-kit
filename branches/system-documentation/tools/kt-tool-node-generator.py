#!/usr/bin/env python3
"""
KT Tool Node Generator
Scans Python/batch scripts and creates tool nodes using local Ollama LLM
"""

import json
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import os

KT_PATH = Path("C:/dev/KT")
sys.path.insert(0, str(KT_PATH))

OLLAMA_PATH = Path(os.environ.get('LOCALAPPDATA')) / "Programs" / "Ollama" / "ollama.exe"


class ToolNodeGenerator:
    """Generate tool nodes from scripts using local LLM"""
    
    def __init__(self, model: str = "qwen2.5-coder:3b"):
        self.kt_path = KT_PATH
        self.model = model
        self.tools_output = self.kt_path / "nodes" / "tools.jsonl"
        self.ollama = OLLAMA_PATH
        
    def scan_tools(self, limit: Optional[int] = None) -> List[Path]:
        """Scan for Python and batch scripts"""
        
        tools = []
        
        # Scan Python files
        for py_file in self.kt_path.rglob("*.py"):
            # Skip venv, node_modules, __pycache__
            if any(skip in str(py_file) for skip in ['venv', 'node_modules', '__pycache__', '.git']):
                continue
            tools.append(py_file)
        
        # Scan batch files
        for bat_file in self.kt_path.rglob("*.bat"):
            if '.git' not in str(bat_file):
                tools.append(bat_file)
        
        # Sort by modification time (newest first)
        tools.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        
        if limit:
            tools = tools[:limit]
        
        return tools
    
    def extract_code_preview(self, file_path: Path, max_lines: int = 50) -> str:
        """Extract first N lines of code"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()[:max_lines]
                return ''.join(lines)
        except:
            return ""
    
    def analyze_tool_with_llm(self, file_path: Path) -> Dict[str, Any]:
        """Use local LLM to analyze tool"""
        
        code_preview = self.extract_code_preview(file_path)
        
        prompt = f"""Analyze this script and extract key information in JSON format.

File: {file_path.name}
Code preview:
```
{code_preview}
```

Provide a JSON response with:
{{
  "purpose": "Brief description of what this tool does (1 sentence)",
  "usage": "How to run it (command line syntax if available)",
  "dependencies": ["list", "of", "dependencies"],
  "when_to_use": "When should someone use this tool?",
  "keywords": ["relevant", "search", "keywords"]
}}

Only respond with valid JSON, no additional text."""

        try:
            result = subprocess.run(
                [str(self.ollama), 'run', self.model],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Try to parse JSON from response
            response = result.stdout.strip()
            
            # Extract JSON if wrapped in markdown
            if '```json' in response:
                json_start = response.find('```json') + 7
                json_end = response.find('```', json_start)
                response = response[json_start:json_end].strip()
            elif '```' in response:
                json_start = response.find('```') + 3
                json_end = response.find('```', json_start)
                response = response[json_start:json_end].strip()
            
            analysis = json.loads(response)
            return analysis
            
        except subprocess.TimeoutExpired:
            print(f"[WARN] LLM timeout for {file_path.name}")
            return self._fallback_analysis(file_path, code_preview)
        except json.JSONDecodeError as e:
            print(f"[WARN] JSON parse error for {file_path.name}: {e}")
            return self._fallback_analysis(file_path, code_preview)
        except Exception as e:
            print(f"[ERROR] LLM analysis failed for {file_path.name}: {e}")
            return self._fallback_analysis(file_path, code_preview)
    
    def _fallback_analysis(self, file_path: Path, code: str) -> Dict[str, Any]:
        """Fallback rule-based analysis if LLM fails"""
        
        lines = code.split('\n')
        
        # Extract docstring
        purpose = "Unknown purpose"
        for line in lines[:10]:
            if '"""' in line or "'''" in line:
                purpose = line.strip().strip('"""').strip("'''").strip()
                break
            if line.strip().startswith('#') and len(line.strip()) > 5:
                purpose = line.strip().lstrip('#').strip()
                break
        
        # Try to find usage
        usage = f"python {file_path.name}"
        for line in lines[:20]:
            if 'usage:' in line.lower() or 'example:' in line.lower():
                usage = line.split(':', 1)[1].strip() if ':' in line else usage
                break
        
        return {
            "purpose": purpose[:200],
            "usage": usage[:200],
            "dependencies": [],
            "when_to_use": "See documentation",
            "keywords": [file_path.stem.replace('_', '-')]
        }
    
    def create_tool_node(self, file_path: Path, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create a tool node"""
        
        rel_path = file_path.relative_to(self.kt_path)
        
        node = {
            "id": f"tool-{file_path.stem}",
            "type": "tool",
            "branch": "tools",
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "content": {
                "name": file_path.name,
                "path": str(rel_path),
                "full_path": str(file_path),
                "file_type": file_path.suffix,
                "purpose": analysis['purpose'],
                "usage": analysis['usage'],
                "dependencies": analysis.get('dependencies', []),
                "when_to_use": analysis.get('when_to_use', ''),
                "keywords": analysis.get('keywords', []),
                "size_bytes": file_path.stat().st_size,
                "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat() + 'Z'
            },
            "tags": {
                "categories": ["tool", file_path.suffix[1:] if file_path.suffix else "script"],
                "keywords": analysis.get('keywords', [])
            },
            "metadata": {
                "generated_at": datetime.utcnow().isoformat() + 'Z',
                "generator": "ToolNodeGenerator-v1-Ollama",
                "model": self.model
            }
        }
        
        return node
    
    def generate_tool_nodes(self, limit: Optional[int] = 10, batch_size: int = 5):
        """Generate tool nodes for scripts"""
        
        print("[INFO] Scanning for tools...")
        tools = self.scan_tools(limit)
        print(f"[OK] Found {len(tools)} tools to process")
        
        if not tools:
            print("[WARN] No tools found")
            return
        
        # Create output file
        nodes = []
        processed = 0
        
        for i, tool_path in enumerate(tools, 1):
            print(f"\n[{i}/{len(tools)}] Analyzing: {tool_path.name}")
            
            try:
                analysis = self.analyze_tool_with_llm(tool_path)
                node = self.create_tool_node(tool_path, analysis)
                nodes.append(node)
                
                print(f"  Purpose: {analysis['purpose'][:80]}...")
                print(f"  [OK] Node created")
                
                processed += 1
                
                # Save batch
                if processed % batch_size == 0:
                    self._save_nodes(nodes)
                    print(f"\n[BATCH] Saved {len(nodes)} nodes")
                    
            except Exception as e:
                print(f"  [ERROR] Failed: {e}")
        
        # Save remaining
        if nodes:
            self._save_nodes(nodes)
            print(f"\n[SUCCESS] Processed {processed}/{len(tools)} tools")
            print(f"[INFO] Output: {self.tools_output}")
    
    def _save_nodes(self, nodes: List[Dict[str, Any]]):
        """Append nodes to JSONL file"""
        
        self.tools_output.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.tools_output, 'a', encoding='utf-8') as f:
            for node in nodes:
                f.write(json.dumps(node) + '\n')
        
        nodes.clear()


def main():
    """Run tool node generation"""
    
    print("=" * 60)
    print("KT Tool Node Generator (Local LLM)")
    print("=" * 60)
    print()
    
    # Check Ollama
    if not OLLAMA_PATH.exists():
        print(f"[ERROR] Ollama not found at {OLLAMA_PATH}")
        print("[INFO] Install Ollama from https://ollama.ai")
        return
    
    print(f"[OK] Using Ollama: {OLLAMA_PATH}")
    print(f"[OK] Model: qwen2.5-coder:3b")
    print()
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=10, help='Number of tools to process')
    parser.add_argument('--batch-size', type=int, default=5, help='Save after N tools')
    args = parser.parse_args()
    
    generator = ToolNodeGenerator()
    generator.generate_tool_nodes(limit=args.limit, batch_size=args.batch_size)
    
    print()
    print("=" * 60)
    print("Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
