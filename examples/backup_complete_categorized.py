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
Async Categorized VoIP.ms Account Dump

This script dumps your VoIP.ms account state organized by functional categories
using async/await for much faster execution (parallel API calls).

Instead of 70+ sequential calls taking ~30 seconds, this runs in ~3-5 seconds.

Output: account_state_categorized_async.json

Usage:
    uv run dump_account_categorized_async.py
    uv run dump_account_categorized_async.py --output my_backup.json
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from voipms import VoIPMSAsyncClient, VoIPMSError

# Same categories as sync version
METHOD_CATEGORIES = {
    "Account Info": [
        "getBalance",
        "getIP",
        "getRegistrationStatus",
        "getClientThreshold",
    ],
    "Configuration": [
        "getServersInfo",
        "getLanguages",
        "getCountries",
        "getProvinces",
        "getStates",
        "getProtocols",
        "getAllowedCodecs",
        "getAuthTypes",
    ],
    "Phone Numbers": [
        "getDIDsInternationalGeographic",
        "getDIDsInternationalNational",
        "getDIDsInternationalTollFree",
        "getDIDCountries",
    ],
    "Calling Features": [
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
    ],
    "Voicemail": [
        "getVoicemailSetups",
        "getVoicemailFolders",
        "getVoicemailAttachmentFormats",
    ],
    "Fax": [
        "getFaxNumbersInfo",
        "getFaxFolders",
        "getEmailToFax",
    ],
    "Billing": [
        "getCharges",
        "getDeposits",
        "getCallBilling",
        "getClientPackages",
        "getPackages",
        "getRates",
        "getTerminationRates",
    ],
    "Conference": [
        "getConference",
        "getConferenceMembers",
    ],
    "Reseller": [
        "getClients",
        "getResellerBalance",
        "getResellerSMS",
        "getResellerMMS",
    ],
}


async def call_method_safely(
    client: VoIPMSAsyncClient, method_name: str
) -> Tuple[str, Dict[str, Any]]:
    """Call a method and return (method_name, result_dict)"""
    try:
        result = await getattr(client, method_name)()
        return method_name, {"status": "success", "response": result}
    except VoIPMSError as e:
        return method_name, {"status": "api_error", "error": str(e), "code": e.code}
    except Exception as e:
        return method_name, {"status": "error", "error": str(e), "type": "unexpected"}


async def dump_account_categorized_async(output_file: str = "account_state_categorized_async.json"):
    """Dump account state organized by category using async for speed"""

    print("Async VoIP.ms Account Dumper")
    print("=" * 50)

    start_time = datetime.now()

    async with VoIPMSAsyncClient() as client:
        # Get all safe methods
        all_methods = client.get_available_methods()  # Not async
        safe_methods = []

        for method_name in all_methods:
            if method_name.startswith("get"):
                method_info = client.get_method_info(method_name)  # Not async
                required_params = [
                    name
                    for name, info in method_info.get("parameters", {}).items()
                    if info.get("required", False)
                ]
                if not required_params:
                    safe_methods.append(method_name)

        print(f"Found {len(safe_methods)} safe methods to call")
        print("Using async/await for parallel execution...\n")

        # Organize output
        account_state = {
            "dump_timestamp": datetime.now().isoformat(),
            "summary": {},
            "categories": {},
            "errors": [],
        }

        # Create all tasks at once for maximum parallelism
        all_tasks = []
        method_to_category = {}

        # Prepare tasks by category
        for category, methods in METHOD_CATEGORIES.items():
            for method_name in methods:
                if method_name in safe_methods:
                    all_tasks.append(call_method_safely(client, method_name))
                    method_to_category[method_name] = category

        # Add uncategorized methods
        other_methods = [
            m
            for m in safe_methods
            if all(m not in methods for methods in METHOD_CATEGORIES.values())
        ]
        for method_name in other_methods:
            all_tasks.append(call_method_safely(client, method_name))
            method_to_category[method_name] = "Other"

        # Execute all tasks in parallel
        print(f"Executing {len(all_tasks)} API calls in parallel...")
        results = await asyncio.gather(*all_tasks)

        # Process results
        successful_calls = 0
        for method_name, result in results:
            category = method_to_category[method_name]

            if category not in account_state["categories"]:
                account_state["categories"][category] = {}

            account_state["categories"][category][method_name] = result

            if result["status"] == "success":
                successful_calls += 1

                # Extract summary info
                if method_name == "getBalance" and "response" in result:
                    balance_data = result["response"]
                    if "balance" in balance_data:
                        account_state["summary"]["balance"] = balance_data["balance"][
                            "current_balance"
                        ]
                elif method_name == "getSubAccounts" and "response" in result:
                    accounts_data = result["response"]
                    if "accounts" in accounts_data:
                        account_state["summary"]["sub_accounts"] = len(accounts_data["accounts"])
                elif method_name == "getVoicemailSetups" and "response" in result:
                    vm_data = result["response"]
                    if "voicemails" in vm_data:
                        account_state["summary"]["voicemail_boxes"] = len(vm_data["voicemails"])
            else:
                account_state["errors"].append(
                    {
                        "method": method_name,
                        "error": result.get("error"),
                        "code": result.get("code"),
                        "type": result.get("type", "api_error"),
                    }
                )

        # Update summary
        account_state["summary"]["methods_called"] = len(all_tasks)
        account_state["summary"]["successful_calls"] = successful_calls
        account_state["summary"]["errors"] = len(account_state["errors"])

        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds()
        account_state["summary"]["execution_time_seconds"] = round(execution_time, 2)

        # Save to file
        print(f"\n\nSaving to {output_file}...")
        with open(output_file, "w") as f:
            json.dump(account_state, f, indent=2, sort_keys=True)

        # Print summary
        print("\n✅ Complete!")
        print("\nSummary:")
        for key, value in account_state["summary"].items():
            print(f"  • {key}: {value}")

        print(f"\n⚡ Async advantage: {len(all_tasks)} calls in {execution_time:.1f} seconds")
        print(f"   (Would take ~{len(all_tasks) * 0.5:.0f} seconds sequentially)")

        print(f"\n📄 Full account state saved to: {output_file}")

        return account_state


async def main():
    """Main async entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Async categorized VoIP.ms account state dump")
    parser.add_argument(
        "--output",
        "-o",
        default="account_state_categorized_async.json",
        help="Output file (default: account_state_categorized_async.json)",
    )

    args = parser.parse_args()
    await dump_account_categorized_async(args.output)


if __name__ == "__main__":
    asyncio.run(main())
