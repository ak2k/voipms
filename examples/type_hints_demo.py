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
Demo: Type Hints and IDE Support

This script demonstrates how the generated type stubs improve the developer experience
with IDE autocomplete, parameter hints, and type checking.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from voipms import VoIPMSClient

def main():
    """Demonstrate type hints benefits."""
    print("VoIP.ms Type Hints Demo")
    print("=======================")
    print("\nType stubs enable rich IDE support for our dynamically-generated methods.")
    
    # Initialize client
    client = VoIPMSClient(
        username="demo",
        password="demo",
        debug=True  # IDE shows this parameter exists!
    )
    
    print("\n1. AUTOCOMPLETE")
    print("----------------")
    print("In your IDE, typing 'client.' will show all 217 available methods:")
    print("  client.get<TAB>  →  getBalance, getCDR, getSMS, ...")
    print("  client.set<TAB>  →  setVoicemail, setQueue, setSMS, ...")
    
    print("\n2. PARAMETER HINTS")
    print("------------------")
    print("When you type a method, IDE shows required and optional parameters:")
    print("\n  client.getCDR(")
    print("    # IDE shows:")
    print("    # date_from: str (required)")
    print("    # date_to: str (required)")
    print("    # timezone: Optional[int] = None")
    print("    # answered: Optional[bool] = None")
    print("    # ...etc")
    
    print("\n3. TYPE CHECKING")
    print("-----------------")
    print("Static type checkers catch errors before runtime:")
    
    # This would be correct
    # result = client.getCDR(date_from="2025-07-01", date_to="2025-07-18")
    
    # These would show type errors in IDE/mypy:
    # result = client.getCDR(date_from=20250701)  # Error: int not str
    # result = client.getCDR(date_from="2025-07-01")  # Error: missing date_to
    # result = client.getCDR(from_date="2025-07-01")  # Error: unknown parameter
    
    print("\n4. DOCUMENTATION ON HOVER")
    print("-------------------------")
    print("Hovering over methods in IDE shows documentation:")
    print("  getCDR: 'Retrieve cdr information'")
    print("  Including parameter descriptions and notes about quirks")
    
    print("\n5. LITERAL TYPES")
    print("-----------------")
    print("Some parameters have restricted values:")
    print("  calltype: Literal['inbound', 'outbound']")
    print("  billing_type: Literal['1', '2']  # 1=PerMinute, 2=Flat")
    
    print("\n6. RESERVED KEYWORD HANDLING")
    print("-----------------------------")
    print("Parameters that are Python keywords get underscore suffix:")
    print("  getFaxMessages(from_='2025-07-01', to_='2025-07-18')")
    print("  getMessageByID(id_=12345)")
    
    print("\n7. ASYNC SUPPORT")
    print("-----------------")
    print("Type hints work for async client too:")
    print("  async with VoIPMSClientAsync() as client:")
    print("    result = await client.getBalance()  # IDE knows this is async!")
    
    print("\n" + "="*60)
    print("BENEFITS SUMMARY")
    print("="*60)
    print("\n✅ Full IDE autocomplete for all 217 methods")
    print("✅ Parameter names and types shown during coding")
    print("✅ Type errors caught before runtime")
    print("✅ Documentation available in IDE")
    print("✅ Works with mypy, pyright, pylance")
    print("✅ No runtime overhead - stubs are development-time only")
    
    print("\n🎯 The library feels 'native' despite being dynamically generated!")

if __name__ == "__main__":
    main()