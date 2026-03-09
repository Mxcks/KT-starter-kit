#!/usr/bin/env python3
"""
KT Config Manager - Toggle intelligent features
"""

import json
import sys
import argparse
from pathlib import Path

CONFIG_FILE = Path(__file__).parent.parent / "config" / "settings.json"

def load_config():
    """Load current settings"""
    if not CONFIG_FILE.exists():
        return {
            "auto_preload": False,
            "auto_search_on_planning": True,
            "auto_load_strategic": True,
            "auto_load_tactical": False,
            "auto_load_implementation": False,
            "search_threshold": 0.7,
            "max_auto_trees": 3,
            "quiet_mode": False
        }
    
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config):
    """Save settings"""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Configure KT Integration')
    
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # Show current settings
    subparsers.add_parser('show', help='Show current settings')
    
    # Set a setting
    set_parser = subparsers.add_parser('set', help='Set a setting')
    set_parser.add_argument('key', help='Setting key')
    set_parser.add_argument('value', help='Setting value')
    
    # Toggle presets
    subparsers.add_parser('smart', help='Enable smart features (auto_search, auto_load_strategic)')
    subparsers.add_parser('manual', help='Disable all auto features (manual queries only)')
    subparsers.add_parser('quiet', help='Enable quiet mode')
    subparsers.add_parser('verbose', help='Disable quiet mode')
    
    args = parser.parse_args()
    
    config = load_config()
    
    if args.command == 'show' or args.command is None:
        print(json.dumps(config, indent=2))
    
    elif args.command == 'set':
        key = args.key
        value = args.value
        
        # Parse value
        if value.lower() == 'true':
            value = True
        elif value.lower() == 'false':
            value = False
        elif value.replace('.', '').isdigit():
            value = float(value) if '.' in value else int(value)
        
        config[key] = value
        save_config(config)
        print(f"✅ Set {key} = {value}")
    
    elif args.command == 'smart':
        config['auto_search_on_planning'] = True
        config['auto_load_strategic'] = True
        config['quiet_mode'] = False
        save_config(config)
        print("✅ Smart features enabled")
    
    elif args.command == 'manual':
        config['auto_preload'] = False
        config['auto_search_on_planning'] = False
        config['auto_load_strategic'] = False
        config['auto_load_tactical'] = False
        config['auto_load_implementation'] = False
        save_config(config)
        print("✅ Manual mode enabled (all auto features off)")
    
    elif args.command == 'quiet':
        config['quiet_mode'] = True
        save_config(config)
        print("✅ Quiet mode enabled")
    
    elif args.command == 'verbose':
        config['quiet_mode'] = False
        save_config(config)
        print("✅ Verbose mode enabled")

if __name__ == '__main__':
    main()
