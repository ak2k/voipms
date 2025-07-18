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
Demo of Advanced API Quirks - The Missing Pieces

This demo shows the additional quirks we discovered but hadn't implemented:
1. Special value handling (None → "none", -1 → "unlimited")
2. List to semicolon-separated string conversion
3. Routing format validation (not implemented yet)
4. Range validations (not implemented yet)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from voipms import VoIPMSClient

def demo_advanced_quirks():
    """Demonstrate the advanced quirks we discovered"""
    client = VoIPMSClient()
    
    print("=" * 70)
    print("Advanced VoIP.ms API Quirks Demo")
    print("=" * 70)
    
    # Demo 1: Special value handling
    print("\n1. Special Value Handling (setQueue)")
    print("-" * 50)
    print("Setting None values that convert to special strings:")
    client.debug_method_params(
        "setQueue",
        queue="101",
        join_announcement=None,        # Will convert to "none"
        maximum_wait_time=None,         # Will convert to "unlimited"
        maximum_callers=-1,             # Will convert to "unlimited"
        join_when_empty=True,           # Will convert to "yes"
        leave_when_empty=False,         # Will convert to "no"
        ring_inuse=True                 # Will convert to "yes"
    )
    
    # Demo 2: List to semicolon conversion
    print("\n" + "=" * 70)
    print("\n2. List to Semicolon Conversion (createSubAccount)")
    print("-" * 50)
    print("Converting lists to semicolon-separated strings:")
    client.debug_method_params(
        "createSubAccount",
        username="testuser",
        password="testpass123",
        allowed_codecs=["ulaw", "g729", "gsm"],  # Will convert to "ulaw;g729;gsm"
        reseller_chargesetup=True                 # Will convert to "1"
    )
    
    # Demo 3: Ring group members
    print("\n" + "=" * 70)
    print("\n3. Ring Group Members (setRingGroup)")
    print("-" * 50)
    print("Complex routing member list:")
    client.debug_method_params(
        "setRingGroup",
        ring_group="1",
        members=["account:100001_VoIP", "fwd:16006", "vm:101"]  # Will convert to semicolon-separated
    )
    
    # Demo 4: Time condition routing
    print("\n" + "=" * 70)
    print("\n4. Time Condition Routing (setTimeCondition)")
    print("-" * 50)
    client.debug_method_params(
        "setTimeCondition",
        timecondition="1",
        routing_match=["account:100001", "vm:101"],      # Will convert to semicolon-separated
        routing_nomatch=["fwd:18005551234", "sys:echo"]  # Will convert to semicolon-separated
    )
    
    # Demo 5: What's still missing
    print("\n" + "=" * 70)
    print("\n5. Quirks Still Not Implemented")
    print("-" * 50)
    print("\n❌ Routing Format Validation:")
    print("   - Format: 'header:record_id'")
    print("   - Headers: account, fwd, vm, sip, grp, ivr, sys, recording, queue, cb, tc, disa, none")
    print("   - Examples: 'account:100001_VoIP', 'vm:101', 'sys:echo', 'none:'")
    
    print("\n❌ Range Validations:")
    print("   - agent_ring_timeout: 5-60 seconds")
    print("   - retry_timer: 5-60 seconds")
    print("   - wrapup_time: 1-60 seconds")
    print("   - maximum_wait_time: multiples of 30, max 1200")
    print("   - frequency_announcement: multiples of 15, max 1200")
    print("   - threshold: 1-250")
    
    print("\n❌ Conditional Required Parameters:")
    print("   - backOrderDIDUSA requires: quantity, state, ratecenter, etc.")
    print("   - backOrderDIDCAN requires: quantity, province, ratecenter, etc.")
    print("   - Different methods have different required field sets")
    
    print("\n❌ Phone Number Type Handling:")
    print("   - DIDs expected as integers: 5551234567")
    print("   - But preserving leading zeros might need strings")
    
    print("\n❌ Date Range Business Logic:")
    print("   - CDR limited to 92 days")
    print("   - No future dates allowed")
    print("   - Start date must be before end date")
    
    print("\n" + "=" * 70)
    print("\nImplementation Status:")
    print("=" * 70)
    print("✅ Boolean → '1'/'0' (20+ methods)")
    print("✅ Boolean → 'yes'/'no' (10+ methods)")
    print("✅ Parameter aliases (zip_code→zip, etc.)")
    print("✅ Required defaults (timezone='1')")
    print("✅ Special values (None→'none', -1→'unlimited')")
    print("✅ List → semicolon strings")
    print("❌ Routing format validation")
    print("❌ Range validations")
    print("❌ Conditional requirements")
    print("❌ Complex business logic")

if __name__ == "__main__":
    demo_advanced_quirks()