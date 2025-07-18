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
Categorized VoIP.ms Account Dump

This script dumps your VoIP.ms account state organized by functional categories
(Account Info, Phone Numbers, Billing, etc.) for better readability.

This is more organized than the full dump and includes a summary section.

Output: account_state_categorized.json

Usage:
    uv run dump_account_categorized.py
    uv run dump_account_categorized.py --output my_backup.json
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, Any, List, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from voipms import VoIPMSClient, VoIPMSError

# Categorize methods for better organization
METHOD_CATEGORIES = {
    'Account Info': [
        'getBalance',
        'getIP',
        'getRegistrationStatus',
        'getClientThreshold',
    ],
    'Configuration': [
        'getServersInfo',
        'getLanguages',
        'getCountries',
        'getProvinces',
        'getStates',
        'getProtocols',
        'getAllowedCodecs',
        'getAuthTypes',
    ],
    'Phone Numbers': [
        'getDIDsInternationalGeographic',
        'getDIDsInternationalNational', 
        'getDIDsInternationalTollFree',
        'getDIDCountries',
        'getPortability',  # requires DID
    ],
    'Calling Features': [
        'getCallAccounts',
        'getSubAccounts',
        'getForwardings',
        'getCallHuntings',
        'getRingGroups',
        'getQueues',
        'getIVRs',
        'getTimeConditions',
        'getDISAs',
        'getCallbacks',
    ],
    'Voicemail': [
        'getVoicemailSetups',
        'getVoicemailFolders',
        'getVoicemailAttachmentFormats',
    ],
    'Fax': [
        'getFaxNumbersInfo',
        'getFaxFolders',
        'getEmailToFax',
    ],
    'Messaging': [
        'getSMS',  # requires DID
        'getMMS',  # requires DID
    ],
    'Billing': [
        'getCharges',
        'getDeposits',
        'getCallBilling',
        'getClientPackages',
        'getPackages',
        'getRates',
        'getTerminationRates',
    ],
    'Conference': [
        'getConference',
        'getConferenceMembers',
    ],
    'Reseller': [
        'getClients',
        'getResellerBalance',
        'getResellerSMS',
        'getResellerMMS',
    ],
}

def categorize_method(method_name: str) -> str:
    """Find which category a method belongs to"""
    for category, methods in METHOD_CATEGORIES.items():
        if method_name in methods:
            return category
    return 'Other'

def dump_account_categorized(output_file: str = 'account_state_categorized.json'):
    """Dump account state organized by category"""
    
    print("Smart VoIP.ms Account Dumper")
    print("=" * 50)
    
    client = VoIPMSClient()
    
    # Organize output by category
    account_state = {
        'dump_timestamp': datetime.now().isoformat(),
        'summary': {},
        'categories': {},
        'errors': []
    }
    
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
    
    print(f"Found {len(safe_methods)} safe methods to call\n")
    
    # Call methods by category
    methods_called = 0
    successful_calls = 0
    
    for category in METHOD_CATEGORIES:
        print(f"\n{category}:")
        print("-" * len(category))
        
        category_data = {}
        
        for method_name in METHOD_CATEGORIES[category]:
            if method_name not in safe_methods:
                continue
                
            methods_called += 1
            print(f"  {method_name}...", end='', flush=True)
            
            try:
                result = getattr(client, method_name)()
                category_data[method_name] = result
                successful_calls += 1
                
                # Extract summary info
                if method_name == 'getBalance' and 'balance' in result:
                    account_state['summary']['balance'] = result['balance']['current_balance']
                elif method_name == 'getSubAccounts' and 'accounts' in result:
                    account_state['summary']['sub_accounts'] = len(result['accounts'])
                elif method_name == 'getVoicemailSetups' and 'voicemails' in result:
                    account_state['summary']['voicemail_boxes'] = len(result['voicemails'])
                
                print(" ✓")
                
            except VoIPMSError as e:
                # Expected API errors (like no reseller access)
                account_state['errors'].append({
                    'method': method_name,
                    'error': str(e),
                    'code': e.code
                })
                print(f" - {e.code}")
            except Exception as e:
                # Unexpected errors
                account_state['errors'].append({
                    'method': method_name,
                    'error': str(e),
                    'type': 'unexpected'
                })
                print(f" ✗ {str(e)}")
        
        if category_data:
            account_state['categories'][category] = category_data
    
    # Handle uncategorized methods
    other_methods = [m for m in safe_methods if categorize_method(m) == 'Other']
    if other_methods:
        print(f"\nOther Methods ({len(other_methods)} methods):")
        print("-" * 20)
        other_data = {}
        
        for method_name in sorted(other_methods):
            methods_called += 1
            print(f"  {method_name}...", end='', flush=True)
            
            try:
                result = getattr(client, method_name)()
                other_data[method_name] = result
                successful_calls += 1
                print(" ✓")
            except VoIPMSError as e:
                account_state['errors'].append({
                    'method': method_name,
                    'error': str(e),
                    'code': e.code
                })
                print(f" - {e.code}")
            except Exception as e:
                account_state['errors'].append({
                    'method': method_name,
                    'error': str(e),
                    'type': 'unexpected'
                })
                print(f" ✗")
        
        if other_data:
            account_state['categories']['Other'] = other_data
    
    # Update summary
    account_state['summary']['methods_called'] = methods_called
    account_state['summary']['successful_calls'] = successful_calls
    account_state['summary']['errors'] = len(account_state['errors'])
    
    # Save to file
    print(f"\n\nSaving to {output_file}...")
    with open(output_file, 'w') as f:
        json.dump(account_state, f, indent=2, sort_keys=True)
    
    # Print summary
    print(f"\n✅ Complete!")
    print(f"\nSummary:")
    for key, value in account_state['summary'].items():
        print(f"  • {key}: {value}")
    
    print(f"\n📄 Full account state saved to: {output_file}")
    
    return account_state

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Categorized VoIP.ms account state dump')
    parser.add_argument('--output', '-o', default='account_state_categorized.json',
                      help='Output file (default: account_state_categorized.json)')
    
    args = parser.parse_args()
    dump_account_categorized(args.output)