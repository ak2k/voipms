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
Example of using the debugging helpers to understand API parameters
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from voipms import VoIPMSClient

def demo_debugging_helpers():
    """Show how debugging helpers work"""
    client = VoIPMSClient()
    
    print("=" * 60)
    print("VoIP.ms Client Debugging Helpers Demo")
    print("=" * 60)
    
    # Example 1: Check what getCDR expects vs what we're providing
    print("\n1. Debugging getCDR parameters:")
    client.debug_method_params(
        "getCDR",
        date_from="2025-07-17",
        date_to="2025-07-17", 
        answered=True,  # This will get converted to "1"
        wrong_param="oops"  # This will be flagged as unexpected
    )
    
    # Example 2: Check parameter aliases for getCallRecordings  
    print("\n" + "=" * 60)
    print("\n2. Debugging getCallRecordings with old parameter names:")
    client.debug_method_params(
        "getCallRecordings",
        account="110414",
        from_date="2025-07-17",  # Old name, will be aliased to date_from
        to_date="2025-07-17"     # Old name, will be aliased to date_to
    )
    
    # Example 3: Show a method with no quirks
    print("\n" + "=" * 60)
    print("\n3. Debugging getBalance (clean method):")
    client.debug_method_params("getBalance")
    
    print("\n" + "=" * 60)
    print("\nTip: Use client.debug_method_params() when you get parameter errors!")
    print("It shows expected vs provided parameters and API quirks that will be applied.")

if __name__ == "__main__":
    demo_debugging_helpers()