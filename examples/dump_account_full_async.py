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
Async Full VoIP.ms Account State Dump

This script calls ALL available read-only API methods (70+ methods) in parallel
for maximum speed. What would take 30-40 seconds sequentially runs in ~5 seconds.

Output: account_state_full_async.json (can be several MB)

Usage:
    uv run dump_account_full_async.py
    uv run dump_account_full_async.py --output my_backup.json
"""

import sys
import os
import json
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from voipms import VoIPMSClientAsync, VoIPMSError

async def call_method_safely(client: VoIPMSClientAsync, method_name: str) -> Tuple[str, Dict[str, Any]]:
    """Call a method and return (method_name, result_dict)"""
    try:
        result = await getattr(client, method_name)()
        return method_name, {
            'status': 'success',
            'response': result
        }
    except VoIPMSError as e:
        return method_name, {
            'status': 'api_error',
            'error': str(e),
            'code': e.code
        }
    except Exception as e:
        return method_name, {
            'status': 'error',
            'error': str(e),
            'type': 'unexpected'
        }

async def dump_account_state_async(output_file: str = 'account_state_full_async.json'):
    """Dump complete account state using async for maximum speed"""
    
    print("Async VoIP.ms Full Account State Dumper")
    print("=" * 50)
    
    start_time = datetime.now()
    
    async with VoIPMSClientAsync() as client:
        # Get all safe methods
        all_methods = client.get_available_methods()
        safe_methods = []
        
        for method_name in all_methods:
            if method_name.startswith('get'):
                method_info = client.get_method_info(method_name)
                required_params = [
                    name for name, info in method_info.get('parameters', {}).items() 
                    if info.get('required', False)
                ]
                if not required_params:
                    safe_methods.append(method_name)
        
        print(f"Found {len(safe_methods)} safe methods to call")
        print("Executing all methods in parallel...")
        
        # Create tasks for all methods
        tasks = [call_method_safely(client, method) for method in safe_methods]
        
        # Execute all in parallel with progress indicator
        print(f"\n[{'.' * len(tasks)}]")
        print("[", end="", flush=True)
        
        # Run all tasks
        results = await asyncio.gather(*tasks)
        print("]")
        
        # Process results
        account_state = {
            'dump_timestamp': datetime.now().isoformat(),
            'total_methods': len(all_methods),
            'methods_called': len(safe_methods),
            'data': {},
            'errors': []
        }
        
        successful = 0
        for method_name, result in results:
            if result['status'] == 'success':
                account_state['data'][method_name] = result['response']
                successful += 1
            else:
                account_state['errors'].append({
                    'method': method_name,
                    'error': result.get('error'),
                    'code': result.get('code'),
                    'type': result.get('type', 'api_error')
                })
        
        # Add execution time
        execution_time = (datetime.now() - start_time).total_seconds()
        account_state['execution_time_seconds'] = round(execution_time, 2)
        
        # Save to file
        print(f"\nSaving to {output_file}...")
        with open(output_file, 'w') as f:
            json.dump(account_state, f, indent=2, sort_keys=True)
        
        # Summary
        print(f"\n✅ Complete!")
        print(f"   - Total API methods: {len(all_methods)}")
        print(f"   - Methods called: {len(safe_methods)}")
        print(f"   - Successful: {successful}")
        print(f"   - Errors: {len(account_state['errors'])}")
        print(f"   - Execution time: {execution_time:.1f} seconds")
        print(f"\n⚡ Speed boost: ~{len(safe_methods) * 0.5 / execution_time:.1f}x faster than sequential")
        print(f"📄 Full state saved to: {output_file}")
        
        # Show some interesting stats
        if 'getBalance' in account_state['data']:
            balance = account_state['data']['getBalance'].get('balance', {}).get('current_balance')
            if balance:
                print(f"\n💰 Current balance: ${balance}")

async def main():
    """Main async entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Async full VoIP.ms account dump')
    parser.add_argument('--output', '-o', default='account_state_full_async.json',
                      help='Output file (default: account_state_full_async.json)')
    
    args = parser.parse_args()
    await dump_account_state_async(args.output)

if __name__ == '__main__':
    asyncio.run(main())