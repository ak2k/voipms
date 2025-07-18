#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx>=0.24.0",
#     "pydantic>=2.0.0",
#     "python-dotenv>=1.0.0",
# ]
# ///
"""
Full VoIP.ms Account State Dump

This script calls ALL available read-only API methods (70+ methods) to create 
a complete snapshot of your VoIP.ms account configuration and state.

Output: account_state_full.json (can be several MB)

Usage:
    uv run dump_account_full.py
    uv run dump_account_full.py --output my_backup.json
    uv run dump_account_full.py --list  # Show what would be called
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, Any, List

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from voipms import VoIPMSClient, VoIPMSError

def is_safe_readonly_method(method_name: str, method_info: Dict[str, Any]) -> bool:
    """
    Determine if a method is safe and read-only.
    
    We consider 'get' methods safe, but exclude a few that might have side effects.
    """
    # Methods that start with 'get' are generally read-only
    if not method_name.startswith('get'):
        return False
    
    # Exclude any 'get' methods that might trigger actions
    # (being extra cautious here)
    unsafe_patterns = [
        'getCallRecording',  # Might trigger download/billing
        'getFaxMessage',     # Might mark as read or trigger download
        'getRecording',      # Might trigger download/billing
    ]
    
    for pattern in unsafe_patterns:
        if pattern in method_name:
            return False
            
    return True

def get_required_params(method_info: Dict[str, Any]) -> List[str]:
    """Get list of required parameters for a method"""
    params = method_info.get('parameters', {})
    return [name for name, info in params.items() if info.get('required', False)]

def dump_account_state(output_file: str = 'account_state_full.json'):
    """Dump complete account state using all safe read-only methods"""
    
    print("VoIP.ms Account State Dumper")
    print("=" * 50)
    
    client = VoIPMSClient()
    all_methods = client.get_available_methods()
    
    # Filter to safe read-only methods
    safe_methods = []
    for method_name in all_methods:
        method_info = client.get_method_info(method_name)
        if is_safe_readonly_method(method_name, method_info):
            required_params = get_required_params(method_info)
            # Only include methods that don't require parameters
            # (we can't call methods that need specific IDs without knowing them)
            if not required_params:
                safe_methods.append(method_name)
    
    print(f"Found {len(safe_methods)} safe read-only methods to call")
    print(f"(out of {len(all_methods)} total methods)")
    print()
    
    # Collect all data
    account_state = {
        'dump_timestamp': datetime.now().isoformat(),
        'total_methods': len(all_methods),
        'methods_called': len(safe_methods),
        'data': {}
    }
    
    # Call each safe method
    for i, method_name in enumerate(sorted(safe_methods), 1):
        print(f"[{i}/{len(safe_methods)}] Calling {method_name}...", end='', flush=True)
        
        try:
            # Call the method
            result = getattr(client, method_name)()
            account_state['data'][method_name] = {
                'status': 'success',
                'response': result
            }
            print(" ✓")
            
        except VoIPMSError as e:
            # API error (like permissions)
            account_state['data'][method_name] = {
                'status': 'api_error',
                'error': str(e),
                'error_code': e.code
            }
            print(f" ✗ API Error: {e.code}")
            
        except Exception as e:
            # Other errors
            account_state['data'][method_name] = {
                'status': 'error',
                'error': str(e)
            }
            print(f" ✗ Error: {str(e)}")
    
    # Save to file
    print(f"\nSaving account state to {output_file}...")
    with open(output_file, 'w') as f:
        json.dump(account_state, f, indent=2, sort_keys=True)
    
    # Summary
    successful = sum(1 for m in account_state['data'].values() if m['status'] == 'success')
    print(f"\n✅ Complete! Successfully called {successful}/{len(safe_methods)} methods")
    print(f"📄 Account state saved to: {output_file}")
    
    # Show some interesting stats
    print("\nQuick Summary:")
    
    # Balance
    balance_data = account_state['data'].get('getBalance', {}).get('response', {})
    if balance_data.get('status') == 'success':
        print(f"  • Balance: ${balance_data['balance']['current_balance']}")
    
    # DIDs count
    dids_data = account_state['data'].get('getDIDsInfo', {}).get('response', {})
    if dids_data.get('status') == 'success' and 'dids' in dids_data:
        print(f"  • DIDs: {len(dids_data['dids'])}")
    
    # Voicemail count
    vm_data = account_state['data'].get('getVoicemails', {}).get('response', {})
    if vm_data.get('status') == 'success' and 'voicemails' in vm_data:
        print(f"  • Voicemails: {len(vm_data['voicemails'])}")
    
    return account_state

def list_safe_methods():
    """List all safe methods we would call"""
    client = VoIPMSClient()
    all_methods = client.get_available_methods()
    
    print("Safe read-only methods that would be called:")
    print("=" * 50)
    
    safe_count = 0
    for method_name in sorted(all_methods):
        method_info = client.get_method_info(method_name)
        if is_safe_readonly_method(method_name, method_info):
            required_params = get_required_params(method_info)
            if not required_params:
                print(f"  ✓ {method_name}")
                safe_count += 1
            else:
                print(f"  ⚠️  {method_name} (requires: {', '.join(required_params)})")
    
    print(f"\nTotal: {safe_count} methods can be called without parameters")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Dump VoIP.ms account state')
    parser.add_argument('--list', action='store_true', 
                      help='List safe methods instead of calling them')
    parser.add_argument('--output', '-o', default='account_state_full.json',
                      help='Output file (default: account_state_full.json)')
    
    args = parser.parse_args()
    
    if args.list:
        list_safe_methods()
    else:
        dump_account_state(args.output)