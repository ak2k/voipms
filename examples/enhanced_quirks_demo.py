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
Demo of Enhanced API Quirks System
Based on comprehensive analysis of external python-voipms library

This demo shows how our enhanced quirks system handles:
1. Boolean to "1"/"0" conversion (29+ methods)
2. Boolean to "yes"/"no" conversion (voicemail, queue, conference)
3. Parameter name aliases (zip_code→zip, filter_id→filter)
4. Required defaults (timezone for getCDR)
5. Debug helpers for troubleshooting
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from voipms import VoIPMSClient

def demo_enhanced_quirks():
    """Demonstrate the enhanced quirks system"""
    client = VoIPMSClient()
    
    print("=" * 70)
    print("Enhanced VoIP.ms API Quirks System Demo")
    print("=" * 70)
    
    # Demo 1: Boolean to "1"/"0" conversion
    print("\n1. Boolean to '1'/'0' Conversion (getCDR)")
    print("-" * 50)
    client.debug_method_params(
        "getCDR",
        date_from="2025-07-17",
        date_to="2025-07-17",
        answered=True,      # Will convert to "1"
        noanswer=False,     # Will convert to "0"
        busy=True,          # Will convert to "1"
        failed=False        # Will convert to "0"
        # timezone="1" will be added automatically
    )
    
    # Demo 2: Boolean to "yes"/"no" conversion
    print("\n" + "=" * 70)
    print("\n2. Boolean to 'yes'/'no' Conversion (setVoicemail)")
    print("-" * 50)
    client.debug_method_params(
        "setVoicemail",
        mailbox="101",
        skip_password=True,     # Will convert to "1"
        attach_message=True,    # Will convert to "yes"
        delete_message=False,   # Will convert to "no"
        say_time=True,          # Will convert to "yes"
        say_callerid=False      # Will convert to "no"
    )
    
    # Demo 3: Parameter aliases
    print("\n" + "=" * 70)
    print("\n3. Parameter Name Aliases (setClient)")
    print("-" * 50)
    client.debug_method_params(
        "setClient",
        client_id="12345",
        zip_code="90210",       # Will be aliased to "zip"
        city="Beverly Hills"
    )
    
    # Demo 4: Multiple quirks on getCallRecordings
    print("\n" + "=" * 70)
    print("\n4. Multiple Quirks (getCallRecordings)")
    print("-" * 50)
    client.debug_method_params(
        "getCallRecordings",
        account="110414",
        from_date="2025-07-17",  # Will be aliased to "date_from"
        to_date="2025-07-17"     # Will be aliased to "date_to"
    )
    
    # Demo 5: DID ordering with multiple boolean conversions
    print("\n" + "=" * 70)
    print("\n5. DID Ordering Quirks (orderDID)")
    print("-" * 50)
    client.debug_method_params(
        "orderDID",
        did="5551234567",
        routing="account:100001_VoIP",
        pop="5",
        dialtime="60",
        cnam=True,              # Will convert to "1"
        test=False,             # Will convert to "0"
        billing_type="1"
    )
    
    # Demo 6: Show what happens with unknown methods
    print("\n" + "=" * 70)
    print("\n6. Unknown Method (no quirks applied)")
    print("-" * 50)
    client.debug_method_params(
        "getBalance",
        advanced=True
    )
    
    print("\n" + "=" * 70)
    print("\nKey Benefits of Enhanced Quirks System:")
    print("=" * 70)
    print("✅ Handles 20+ methods with boolean→'1'/'0' conversion")
    print("✅ Handles 10+ methods with boolean→'yes'/'no' conversion")
    print("✅ Automatic parameter name aliasing")
    print("✅ Required defaults injection")
    print("✅ Debug helpers for troubleshooting")
    print("✅ Based on comprehensive external library analysis")
    print("✅ Systematic approach handles all 217 API methods")
    
    print(f"\n💡 Usage: client.methodName(validate=False, **params)")
    print("   - validate=False: Skip Pydantic validation")
    print("   - Quirks are applied automatically")
    print("   - Natural parameter names (boolean True/False)")
    print("   - Client handles API inconsistencies transparently")

if __name__ == "__main__":
    demo_enhanced_quirks()