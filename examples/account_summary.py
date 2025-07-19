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
Account Summary - Quick overview of your VoIP.ms account

More comprehensive than basic_usage.py - shows:
- Balance
- Sub-accounts with details
- Registration status (online/offline count)
- Voicemail boxes
- Your current IP
- Available servers

Also includes option to dump complete account state to JSON.
"""

import json

from voipms import VoIPMSClient, VoIPMSError


def get_account_summary():
    """Get essential account information"""

    client = VoIPMSClient()
    summary = {}

    print("VoIP.ms Account Summary")
    print("=" * 40)

    # 1. Balance
    try:
        result = client.getBalance()
        balance = result['balance']['current_balance']
        summary['balance'] = f"${balance}"
        print(f"Balance: ${balance}")
    except VoIPMSError as e:
        print(f"Balance: Error - {e}")

    # 2. Sub-accounts
    try:
        result = client.getSubAccounts()
        accounts = result.get('accounts', [])
        summary['sub_accounts'] = len(accounts)
        print(f"Sub-accounts: {len(accounts)}")

        # Show account details
        for acc in accounts[:3]:  # First 3 only
            print(f"  - {acc['account']} ({acc['description']})")
        if len(accounts) > 3:
            print(f"  ... and {len(accounts) - 3} more")
    except VoIPMSError as e:
        print(f"Sub-accounts: Error - {e}")

    # 3. Registration Status
    try:
        result = client.getRegistrationStatus()
        registrations = result.get('registrations', [])
        registered = [r for r in registrations if r.get('registered') == 'yes']
        summary['registrations'] = f"{len(registered)}/{len(registrations)} online"
        print(f"Registrations: {len(registered)}/{len(registrations)} online")
    except VoIPMSError as e:
        print(f"Registrations: Error - {e}")

    # 4. Voicemail boxes
    try:
        result = client.getVoicemailSetups()
        voicemails = result.get('voicemails', [])
        summary['voicemail_boxes'] = len(voicemails)
        print(f"Voicemail boxes: {len(voicemails)}")
    except VoIPMSError as e:
        print(f"Voicemail: Error - {e}")

    # 5. Your IP
    try:
        result = client.getIP()
        if 'ip' in result:
            summary['your_ip'] = result['ip']
            print(f"Your IP: {result['ip']}")
    except VoIPMSError as e:
        print(f"IP: Error - {e}")

    # 6. Server Info
    try:
        result = client.getServersInfo()
        servers = result.get('servers', [])
        summary['available_servers'] = len(servers)
        print(f"Available servers: {len(servers)}")
    except VoIPMSError as e:
        print(f"Servers: Error - {e}")

    return summary

def dump_full_state(filename='account_state.json'):
    """
    Dump complete account state to a JSON file.
    This calls ALL safe read-only methods.
    """
    client = VoIPMSClient()

    print(f"\nDumping full account state to {filename}...")
    print("This will call many API methods and may take a minute...\n")

    # Get all methods that start with 'get' and don't require parameters
    all_methods = client.get_available_methods()
    safe_methods = []

    for method_name in all_methods:
        if method_name.startswith('get'):
            method_info = client.get_method_info(method_name)
            params = method_info.get('parameters', {})
            required = [p for p, info in params.items() if info.get('required', False)]

            if not required:  # No required parameters
                safe_methods.append(method_name)

    print(f"Found {len(safe_methods)} safe methods to call")

    # Call each method and collect results
    state = {
        'timestamp': str(datetime.now()),
        'data': {},
        'errors': []
    }

    for i, method_name in enumerate(safe_methods, 1):
        print(f"[{i}/{len(safe_methods)}] {method_name}...", end='', flush=True)

        try:
            result = getattr(client, method_name)()
            state['data'][method_name] = result
            print(" ✓")
        except Exception as e:
            state['errors'].append({
                'method': method_name,
                'error': str(e)
            })
            print(f" ✗ {str(e)}")

    # Save to file
    with open(filename, 'w') as f:
        json.dump(state, f, indent=2)

    print(f"\n✅ Saved to {filename}")
    print(f"   - Successful calls: {len(state['data'])}")
    print(f"   - Errors: {len(state['errors'])}")

    return state

if __name__ == '__main__':
    from datetime import datetime

    # Quick summary
    summary = get_account_summary()

    # Optionally dump full state
    print("\n" + "=" * 40)
    try:
        response = input("Dump full account state? (y/N): ")
        if response.lower() == 'y':
            dump_full_state()
    except EOFError:
        print("\nRun interactively to dump full state, or use:")
        print("  python3 -c \"from account_summary import dump_full_state; dump_full_state()\"")
