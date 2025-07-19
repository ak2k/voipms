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
Complete VoIP.ms Account Backup (Non-Reseller)

This script creates a comprehensive backup of your VoIP.ms account including:
- All configuration without parameters
- All DIDs with their individual settings
- Call Detail Records (last 90 days)
- SMS/MMS history (last 90 days)
- Voicemail messages metadata
- And much more...

Output: voipms_backup_YYYY-MM-DD.json

Usage:
    uv run backup_account_complete.py
    uv run backup_account_complete.py --days 30  # Limit CDR/SMS history
    uv run backup_account_complete.py --output my_backup.json
"""

import asyncio
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from voipms import VoIPMSClientAsync, VoIPMSError


class CompleteAccountBackup:
    """Handles complete account backup with intelligent parameter handling"""

    def __init__(self, client: VoIPMSClientAsync, days_history: int = 90):
        self.client = client
        self.days_history = days_history
        self.backup_data = {
            'backup_timestamp': datetime.now().isoformat(),
            'backup_version': '1.0',
            'account_info': {},
            'configuration': {},
            'phone_numbers': {},
            'call_features': {},
            'messaging': {},
            'call_history': {},
            'voicemail': {},
            'fax': {},
            'billing': {},
            'errors': []
        }
        self.stats = {
            'total_calls': 0,
            'successful_calls': 0,
            'start_time': datetime.now()
        }

    async def backup_all(self) -> Dict[str, Any]:
        """Run complete backup"""
        print("VoIP.ms Complete Account Backup")
        print("=" * 50)
        print(f"Backing up {self.days_history} days of history\n")

        # Phase 1: Basic account info and configuration
        await self.backup_basic_info()

        # Phase 2: Get all DIDs and backup their individual settings
        await self.backup_phone_numbers()

        # Phase 3: Backup call features
        await self.backup_call_features()

        # Phase 4: Backup call history and messaging
        await self.backup_history()

        # Phase 5: Backup voicemail
        await self.backup_voicemail()

        # Phase 6: Backup billing info
        await self.backup_billing()

        # Add final stats
        self.backup_data['backup_stats'] = {
            'total_api_calls': self.stats['total_calls'],
            'successful_calls': self.stats['successful_calls'],
            'errors': len(self.backup_data['errors']),
            'backup_duration_seconds': (datetime.now() - self.stats['start_time']).total_seconds()
        }

        return self.backup_data

    async def call_method(self, method_name: str, **params) -> Optional[Dict[str, Any]]:
        """Call a method and track stats"""
        self.stats['total_calls'] += 1
        try:
            result = await getattr(self.client, method_name)(**params)
            self.stats['successful_calls'] += 1
            return result
        except VoIPMSError as e:
            self.backup_data['errors'].append({
                'method': method_name,
                'params': params,
                'error': str(e),
                'code': e.code
            })
            return None
        except Exception as e:
            self.backup_data['errors'].append({
                'method': method_name,
                'params': params,
                'error': str(e),
                'type': 'unexpected'
            })
            return None

    async def backup_basic_info(self):
        """Backup basic account information"""
        print("Phase 1: Basic Account Information")
        print("-" * 35)

        # Account info methods
        methods = [
            'getBalance', 'getIP', 'getRegistrationStatus',
            'getClientThreshold', 'getLanguages', 'getTimezones'
        ]

        tasks = [self.call_method(method) for method in methods]
        results = await asyncio.gather(*tasks)

        for method, result in zip(methods, results):
            if result:
                self.backup_data['account_info'][method] = result
                print(f"  ✓ {method}")
            else:
                print(f"  ✗ {method}")

        # Configuration
        config_methods = [
            'getServersInfo', 'getProtocols', 'getAllowedCodecs',
            'getAuthTypes', 'getDeviceTypes', 'getDTMFModes',
            'getMusicOnHold', 'getNAT', 'getPlayInstructions',
            'getLockInternational'
        ]

        tasks = [self.call_method(method) for method in config_methods]
        results = await asyncio.gather(*tasks)

        for method, result in zip(config_methods, results):
            if result:
                self.backup_data['configuration'][method] = result

        print(f"  Completed {len([r for r in results if r])} configuration items\n")

    async def backup_phone_numbers(self):
        """Backup all phone numbers and their settings"""
        print("Phase 2: Phone Numbers (DIDs)")
        print("-" * 35)

        # Get all DIDs first
        all_dids = []

        # Try to get DIDs without parameters first
        dids_result = await self.call_method('getDIDsInfo')
        if dids_result and 'dids' in dids_result:
            all_dids.extend(dids_result['dids'])
            print(f"  ✓ Found {len(dids_result['dids'])} DIDs")
        else:
            print("  ℹ getDIDsInfo requires parameters, skipping individual DID backup")

        # Get fax numbers
        fax_result = await self.call_method('getFaxNumbersInfo')
        if fax_result and 'fax_numbers' in fax_result:
            for fax in fax_result['fax_numbers']:
                all_dids.append({
                    'did': fax.get('did', fax.get('number')),
                    'type': 'fax',
                    **fax
                })
            print(f"  ✓ Found {len(fax_result['fax_numbers'])} fax numbers")

        # Now get detailed info for each DID
        if all_dids:
            print(f"\n  Getting details for {len(all_dids)} DIDs...")

            # Methods that take a DID parameter
            did_detail_methods = [
                'getCallerIDFiltering',
                'getSMS',
                'getMMS',
                'getPortability'
            ]

            for did_info in all_dids:
                did = did_info.get('did')
                if not did:
                    continue

                self.backup_data['phone_numbers'][did] = {
                    'info': did_info,
                    'settings': {}
                }

                # Get detailed settings for this DID
                for method in did_detail_methods:
                    if method in ['getSMS', 'getMMS']:
                        # For SMS/MMS, get recent history
                        to_date = datetime.now()
                        from_date = to_date - timedelta(days=self.days_history)
                        result = await self.call_method(
                            method,
                            did=did,
                            from_date=from_date.strftime('%Y-%m-%d'),
                            to_date=to_date.strftime('%Y-%m-%d')
                        )
                    else:
                        result = await self.call_method(method, did=did)

                    if result:
                        self.backup_data['phone_numbers'][did]['settings'][method] = result

            print(f"  ✓ Backed up {len(self.backup_data['phone_numbers'])} phone numbers\n")
        else:
            print("  ℹ No DIDs found to backup\n")

    async def backup_call_features(self):
        """Backup call features configuration"""
        print("Phase 3: Call Features")
        print("-" * 35)

        features = [
            'getCallAccounts', 'getSubAccounts', 'getForwardings',
            'getCallHuntings', 'getRingGroups', 'getQueues', 'getIVRs',
            'getTimeConditions', 'getDISAs', 'getCallbacks',
            'getSIPURIs', 'getCallParking', 'getPhonebook',
            'getPhonebookGroups', 'getStaticMembers',
            'getRingStrategies', 'getCallTypes'
        ]

        tasks = [self.call_method(method) for method in features]
        results = await asyncio.gather(*tasks)

        count = 0
        for method, result in zip(features, results):
            if result:
                self.backup_data['call_features'][method] = result
                count += 1

        print(f"  ✓ Backed up {count} call feature configurations\n")

    async def backup_history(self):
        """Backup call history and messaging"""
        print("Phase 4: Call History & Messaging")
        print("-" * 35)

        to_date = datetime.now()
        from_date = to_date - timedelta(days=self.days_history)
        date_params = {
            'date_from': from_date.strftime('%Y-%m-%d'),
            'date_to': to_date.strftime('%Y-%m-%d')
        }

        # CDR (Call Detail Records)
        print(f"  Getting CDR from {date_params['date_from']} to {date_params['date_to']}...")
        cdr_result = await self.call_method('getCDR', **date_params)
        if cdr_result:
            self.backup_data['call_history']['cdr'] = cdr_result
            cdr_count = len(cdr_result.get('cdr', []))
            print(f"  ✓ Found {cdr_count} call records")

        # Transaction History
        trans_result = await self.call_method('getTransactionHistory', **date_params)
        if trans_result:
            self.backup_data['billing']['transaction_history'] = trans_result
            trans_count = len(trans_result.get('transactions', []))
            print(f"  ✓ Found {trans_count} transactions")

        # Conference recordings
        conf_result = await self.call_method('getConferenceRecordings', **date_params)
        if conf_result:
            self.backup_data['call_history']['conference_recordings'] = conf_result
            conf_count = len(conf_result.get('recordings', []))
            print(f"  ✓ Found {conf_count} conference recordings")

        print()

    async def backup_voicemail(self):
        """Backup voicemail configuration and messages"""
        print("Phase 5: Voicemail")
        print("-" * 35)

        # Get voicemail setups
        vm_setups = await self.call_method('getVoicemailSetups')
        if vm_setups and 'voicemails' in vm_setups:
            self.backup_data['voicemail']['setups'] = vm_setups

            # Get messages for each mailbox
            for vm in vm_setups['voicemails']:
                mailbox = vm.get('mailbox')
                if mailbox:
                    # Get voicemail messages
                    messages = await self.call_method('getVoicemailMessages', mailbox=mailbox)
                    if messages:
                        if 'mailboxes' not in self.backup_data['voicemail']:
                            self.backup_data['voicemail']['mailboxes'] = {}
                        self.backup_data['voicemail']['mailboxes'][mailbox] = messages

            print(f"  ✓ Backed up {len(vm_setups['voicemails'])} voicemail boxes")

        # Get voicemail folders and attachment formats
        folders = await self.call_method('getVoicemailFolders')
        if folders:
            self.backup_data['voicemail']['folders'] = folders

        formats = await self.call_method('getVoicemailAttachmentFormats')
        if formats:
            self.backup_data['voicemail']['attachment_formats'] = formats

        print()

    async def backup_billing(self):
        """Backup billing information"""
        print("Phase 6: Billing Information")
        print("-" * 35)

        billing_methods = [
            'getCharges', 'getDeposits', 'getCallBilling',
            'getClientPackages', 'getPackages', 'getRates',
            'getTerminationRates', 'getBalanceManagement'
        ]

        tasks = [self.call_method(method) for method in billing_methods]
        results = await asyncio.gather(*tasks)

        count = 0
        for method, result in zip(billing_methods, results):
            if result:
                self.backup_data['billing'][method] = result
                count += 1

        print(f"  ✓ Backed up {count} billing configurations\n")


async def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Complete VoIP.ms account backup')
    parser.add_argument('--days', type=int, default=90,
                      help='Days of history to backup (default: 90)')
    parser.add_argument('--output', '-o',
                      help='Output file (default: voipms_backup_YYYY-MM-DD.json)')

    args = parser.parse_args()

    # Generate default filename with date
    if not args.output:
        date_str = datetime.now().strftime('%Y-%m-%d')
        args.output = f'voipms_backup_{date_str}.json'

    # Run backup
    async with VoIPMSClientAsync() as client:
        backup = CompleteAccountBackup(client, args.days)
        backup_data = await backup.backup_all()

        # Save to file
        print(f"Saving backup to {args.output}...")
        with open(args.output, 'w') as f:
            json.dump(backup_data, f, indent=2, sort_keys=True)

        # Summary
        stats = backup_data['backup_stats']
        print("\n" + "=" * 50)
        print("Backup Complete!")
        print("=" * 50)
        print(f"✓ Total API calls: {stats['total_api_calls']}")
        print(f"✓ Successful calls: {stats['successful_calls']}")
        print(f"✓ Errors: {stats['errors']}")
        print(f"✓ Duration: {stats['backup_duration_seconds']:.1f} seconds")
        print(f"✓ Output file: {args.output}")
        print(f"✓ File size: {os.path.getsize(args.output) / 1024:.1f} KB")

        # Show key metrics
        if 'account_info' in backup_data and 'getBalance' in backup_data['account_info']:
            balance = backup_data['account_info']['getBalance'].get('balance', {}).get('current_balance')
            if balance:
                print(f"\n💰 Current balance: ${balance}")

        phone_count = len(backup_data.get('phone_numbers', {}))
        if phone_count:
            print(f"📞 Phone numbers backed up: {phone_count}")

        if 'call_history' in backup_data and 'cdr' in backup_data['call_history']:
            cdr_count = len(backup_data['call_history']['cdr'].get('cdr', []))
            if cdr_count:
                print(f"📊 Call records backed up: {cdr_count}")

if __name__ == '__main__':
    asyncio.run(main())
