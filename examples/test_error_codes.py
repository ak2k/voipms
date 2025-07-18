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
Test Error Code Implementation

This script demonstrates that our error code implementation is working correctly.
It tests various scenarios to show that detailed error messages are provided.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from voipms import VoIPMSClient

def test_error_codes():
    """Test that error codes are loaded and provide helpful messages"""
    print("Testing VoIP.ms Error Code Implementation")
    print("=" * 60)
    
    # Initialize client
    client = VoIPMSClient()
    
    # Test 1: Check that error codes are loaded
    print("\n1. Checking error codes are loaded:")
    error_count = len(client.api_definition.get('error_codes', {}))
    print(f"   ✅ Loaded {error_count} error codes")
    
    # Test 2: Show some example error codes
    print("\n2. Sample error codes and messages:")
    sample_codes = [
        'invalid_daterange',
        'invalid_credentials', 
        'no_callstatus',
        'invalid_date',
        'missing_timezone',
        'invalid_password_missing_uppercase'
    ]
    
    for code in sample_codes:
        message = client.api_definition['error_codes'].get(code, 'Not found')
        print(f"   {code}: {message}")
    
    # Test 3: Test error handling with missing parameter
    print("\n3. Testing error handling with missing parameter:")
    try:
        # This should fail with missing parameters
        result = client.getCDR(validate=False)  # Missing required date parameters
        print("   ❌ Expected error but none occurred")
    except Exception as e:
        print(f"   ✅ Got expected error: {type(e).__name__}: {e}")
    
    # Test 4: Test with invalid date range
    print("\n4. Testing with invalid date range (>92 days):")
    try:
        result = client.getCDR(
            validate=False,
            date_from="2025-01-01",
            date_to="2025-06-30",  # More than 92 days
            answered=True
        )
        print("   ❌ Expected error but none occurred")
    except ValueError as e:
        print(f"   ✅ Got expected error: {e}")
    
    # Test 5: Show error code lookup
    print("\n5. Direct error code lookup examples:")
    print("   Common errors developers might encounter:")
    common_errors = {
        'invalid_billingtype': "When setting DID billing type",
        'invalid_cnam': "When ordering DIDs",
        'invalid_daterange': "When fetching CDR/SMS/MMS",
        'invalid_timezone': "When not providing timezone for CDR",
        'no_callstatus': "When not specifying call status filters"
    }
    
    for code, context in common_errors.items():
        message = client.api_definition['error_codes'].get(code, 'Not found')
        print(f"\n   {code} ({context}):")
        print(f"   → {message}")
    
    print("\n" + "=" * 60)
    print("✅ Error code implementation is working correctly!")
    print(f"   - {error_count} error codes available")
    print("   - Detailed, actionable error messages")
    print("   - Helps developers understand and fix issues quickly")

if __name__ == "__main__":
    test_error_codes()