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
Test date validation quirk
"""

import sys
import os
from datetime import datetime, timedelta
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from voipms import VoIPMSClient

def test_date_validation():
    """Test the date validation quirk"""
    client = VoIPMSClient()
    
    print("Testing Date Validation for getCDR")
    print("=" * 50)
    
    # Test 1: Valid date range (30 days)
    print("\n1. Valid date range (30 days):")
    try:
        result = client.getCDR(
            validate=False,
            date_from="2025-06-01",
            date_to="2025-06-30",
            answered=True
        )
        print("✅ Passed: 30-day range accepted")
    except ValueError as e:
        print(f"❌ Failed: {e}")
    
    # Test 2: Date range exceeds 92 days
    print("\n2. Date range exceeds 92 days:")
    try:
        result = client.getCDR(
            validate=False,
            date_from="2025-01-01",
            date_to="2025-06-30",
            answered=True
        )
        print("❌ Failed: Should have raised error for >92 days")
    except ValueError as e:
        print(f"✅ Passed: {e}")
    
    # Test 3: Future date
    print("\n3. Future date:")
    future = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    try:
        result = client.getCDR(
            validate=False,
            date_from="2025-01-01",
            date_to=future,
            answered=True
        )
        print("❌ Failed: Should have raised error for future date")
    except ValueError as e:
        print(f"✅ Passed: {e}")
    
    # Test 4: date_from after date_to
    print("\n4. date_from after date_to:")
    try:
        result = client.getCDR(
            validate=False,
            date_from="2025-06-30",
            date_to="2025-06-01",
            answered=True
        )
        print("❌ Failed: Should have raised error for reversed dates")
    except ValueError as e:
        print(f"✅ Passed: {e}")
    
    # Test 5: Method without date validation (should pass through)
    print("\n5. Method without date validation (getBalance):")
    try:
        # This should work fine - no date validation
        client.debug_method_params("getBalance", advanced=True)
        print("✅ Passed: Non-date method works normally")
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    test_date_validation()