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
Simple VoIP.ms Account Backup

This script creates a backup of your VoIP.ms account configuration
focusing on settings that don't require specific parameters.

Perfect for regular backups of account configuration.

Output: voipms_backup_simple_YYYY-MM-DD.json

Usage:
    uv run backup_account_simple.py
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Any, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from voipms import VoIPMSAsyncClient, VoIPMSError

# Categories of methods to backup
BACKUP_CATEGORIES = {
    "Account": [
        "getBalance",
        "getIP",
        "getRegistrationStatus",
        "getClientThreshold",
        "getBalanceManagement",
    ],
    "Configuration": [
        "getServersInfo",
        "getProtocols",
        "getAllowedCodecs",
        "getAuthTypes",
        "getLanguages",
        "getCountries",
        "getProvinces",
        "getStates",
        "getLocales",
    ],
    "Phone Features": [
        "getCallAccounts",
        "getSubAccounts",
        "getForwardings",
        "getCallHuntings",
        "getRingGroups",
        "getQueues",
        "getIVRs",
        "getTimeConditions",
        "getDISAs",
        "getCallbacks",
        "getSIPURIs",
        "getVoicemailSetups",
    ],
    "Settings": [
        "getPhonebook",
        "getPhonebookGroups",
        "getStaticMembers",
        "getRingStrategies",
        "getCallTypes",
        "getJoinWhenEmptyTypes",
        "getInternationalTypes",
        "getRoutes",
    ],
    "Fax": [
        "getFaxNumbersInfo",
        "getFaxFolders",
        "getEmailToFax",
        "getFaxProvinces",
        "getFaxStates",
    ],
    "Rates & Billing": [
        "getCharges",
        "getDeposits",
        "getCallBilling",
        "getClientPackages",
        "getPackages",
        "getRates",
        "getTerminationRates",
        "getCarriers",
    ],
    "Conference": ["getConference", "getConferenceMembers"],
}


async def call_method_safe(client: VoIPMSAsyncClient, method_name: str) -> Tuple[str, Any]:
    """Safely call a method and return result"""
    try:
        result = await getattr(client, method_name)()
        return method_name, {"status": "success", "data": result}
    except VoIPMSError as e:
        return method_name, {"status": "error", "error": str(e), "code": e.code}
    except Exception as e:
        return method_name, {"status": "error", "error": str(e)}


async def backup_account_simple():
    """Create a simple backup of account configuration"""
    print("VoIP.ms Simple Account Backup")
    print("=" * 40)

    start_time = datetime.now()
    backup_data = {
        "backup_timestamp": datetime.now().isoformat(),
        "backup_type": "simple",
        "categories": {},
    }

    async with VoIPMSAsyncClient() as client:
        total_methods = sum(len(methods) for methods in BACKUP_CATEGORIES.values())
        print(f"Backing up {total_methods} configuration items...\n")

        successful = 0
        failed = 0

        # Process each category
        for category, methods in BACKUP_CATEGORIES.items():
            print(f"{category}:")
            backup_data["categories"][category] = {}

            # Call all methods in parallel for this category
            tasks = [call_method_safe(client, method) for method in methods]
            results = await asyncio.gather(*tasks)

            # Process results
            for method_name, result in results:
                backup_data["categories"][category][method_name] = result

                if result["status"] == "success":
                    print(f"  ✓ {method_name}")
                    successful += 1
                else:
                    print(f"  ✗ {method_name} ({result.get('code', 'error')})")
                    failed += 1

            print()

        # Add summary
        execution_time = (datetime.now() - start_time).total_seconds()
        backup_data["summary"] = {
            "total_methods": total_methods,
            "successful": successful,
            "failed": failed,
            "execution_time_seconds": round(execution_time, 2),
        }

        # Extract key information for quick summary
        if "Account" in backup_data["categories"]:
            balance_data = backup_data["categories"]["Account"].get("getBalance", {})
            if balance_data.get("status") == "success":
                balance = balance_data["data"].get("balance", {}).get("current_balance")
                backup_data["summary"]["current_balance"] = balance

        # Save backup
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"voipms_backup_simple_{date_str}.json"

        print(f"Saving backup to {filename}...")
        with open(filename, "w") as f:
            json.dump(backup_data, f, indent=2, sort_keys=True)

        # Summary
        print("\n" + "=" * 40)
        print("Backup Complete!")
        print("=" * 40)
        print(f"✓ Successful: {successful}/{total_methods}")
        print(f"✓ Failed: {failed}")
        print(f"✓ Time: {execution_time:.1f} seconds")
        print(f"✓ File: {filename} ({os.path.getsize(filename) / 1024:.1f} KB)")

        if "current_balance" in backup_data["summary"]:
            print(f"\n💰 Current balance: ${backup_data['summary']['current_balance']}")

        return backup_data


if __name__ == "__main__":
    asyncio.run(backup_account_simple())
