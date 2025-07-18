#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "click>=8.0.0",
# ]
# ///
"""
Demo: CLI Smart Defaults

This script demonstrates how the CLI provides intelligent defaults for common use cases,
making it easier to use the VoIP.ms API without remembering all parameter details.
"""

import subprocess
import sys
from datetime import datetime, timedelta

def run_command(cmd: str, description: str):
    """Run a CLI command and show the output."""
    print(f"\n{'='*60}")
    print(f"Demo: {description}")
    print(f"{'='*60}")
    print(f"Command: {cmd}")
    print("-" * 60)
    
    # Note: In a real scenario, this would actually run the command
    # For demo purposes, we're just showing what would happen
    print("Output: (simulated for demo)")
    
def main():
    """Demonstrate CLI smart defaults."""
    print("VoIP.ms CLI Smart Defaults Demo")
    print("================================")
    print("\nThe CLI layer adds intelligent defaults to make common tasks easier.")
    print("The client library remains predictable, while the CLI adds convenience.")
    
    # Demo 1: Date-based queries
    print("\n\n1. DATE-BASED QUERIES")
    print("---------------------")
    print("Without smart defaults, you need to specify dates:")
    print("  voipms getCDR --date_from=2025-07-11 --date_to=2025-07-18 --timezone=1")
    
    print("\nWith smart defaults:")
    print("  voipms getCDR")
    print("  → Automatically adds:")
    print(f"    - date_from: {(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')} (7 days ago)")
    print(f"    - date_to: {datetime.now().strftime('%Y-%m-%d')} (today)")
    print("    - timezone: 1 (EST)")
    
    # Demo 2: DID ordering
    print("\n\n2. DID ORDERING")
    print("---------------")
    print("Without smart defaults:")
    print("  voipms orderDID --did=5551234567 --routing=account:100001 --pop=1 --dialtime=60 --billing_type=1")
    
    print("\nWith smart defaults:")
    print("  voipms orderDID --did=5551234567 --routing=account:100001")
    print("  → Automatically adds:")
    print("    - pop: 1 (primary server)")
    print("    - dialtime: 60 (standard ring time)")
    print("    - billing_type: 1 (per-minute billing)")
    
    # Demo 3: Voicemail setup
    print("\n\n3. VOICEMAIL CONFIGURATION")
    print("--------------------------")
    print("Without smart defaults:")
    print("  voipms setVoicemail --mailbox=101 --password=1234 --attach_message=true --delete_message=false")
    
    print("\nWith smart defaults:")
    print("  voipms setVoicemail --mailbox=101 --password=1234")
    print("  → Automatically adds:")
    print("    - attach_message: true (email voicemails)")
    print("    - delete_message: false (keep messages)")
    
    # Demo 4: Help shows smart defaults
    print("\n\n4. HELP INTEGRATION")
    print("-------------------")
    print("The help command shows available smart defaults:")
    print("\n  voipms help getCDR")
    print("\nWould show:")
    print("  ...")
    print("  Smart Defaults:")
    print("    Date range defaults to last 7 days, timezone defaults to 1")
    print("  ...")
    
    # Demo 5: Override defaults
    print("\n\n5. OVERRIDING DEFAULTS")
    print("----------------------")
    print("Smart defaults can always be overridden:")
    print("\n  voipms getCDR --date_from=2025-01-01 --timezone=5")
    print("  → Uses your values instead of defaults")
    
    # Summary
    print("\n\n" + "="*60)
    print("BENEFITS OF CLI SMART DEFAULTS")
    print("="*60)
    print("\n✅ Faster command entry - less typing")
    print("✅ Production-ready defaults - not test values")
    print("✅ Reduced errors - common parameters handled")
    print("✅ Still explicit - shows what defaults were added")
    print("✅ Fully optional - can override any default")
    print("\n✅ Library stays predictable - defaults only in CLI")
    print("✅ Programmatic users unaffected - can build own defaults")
    
    print("\n\nNOTE: Smart defaults are shown in yellow when applied:")
    print('  Note: Added default timezone=1 (EST)')
    print('  Note: Added default date range (last 7 days)')

if __name__ == "__main__":
    main()