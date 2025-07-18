#!/usr/bin/env python3
"""
Test script to fetch VoIP.ms API documentation
"""

import sys
import os
from pathlib import Path
from fetch_documentation_simple import SimpleVoIPMSDocumentationFetcher


def main():
    """Test fetching documentation"""
    print("VoIP.ms API Documentation Fetcher Test")
    print("=" * 50)
    
    # Get credentials from environment or prompt
    username = os.getenv('VOIPMS_USERNAME')
    password = os.getenv('VOIPMS_PASSWORD')
    
    if not username or not password:
        print("\nNo credentials found in environment variables.")
        print("Please set:")
        print("  export VOIPMS_USERNAME='your-email@example.com'")
        print("  export VOIPMS_PASSWORD='your-password'")
        return
        
    print(f"\nUsing credentials for: {username}")
    
    # Create fetcher
    fetcher = SimpleVoIPMSDocumentationFetcher()
    
    # Output file
    output_file = "api_docs_fresh.html"
    
    print(f"\nFetching documentation...")
    print(f"Output file: {output_file}")
    
    try:
        result = fetcher.fetch_documentation(username, password, output_file)
        
        if result:
            # Check file size
            file_size = Path(result).stat().st_size
            print(f"\n✅ Success! Documentation saved to: {result}")
            print(f"   File size: {file_size:,} bytes")
            
            # Check if it contains API documentation
            with open(result, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if 'getBalance' in content and 'api_username' in content:
                print("   ✓ Contains API documentation")
                
                # Count methods
                import re
                methods = re.findall(r'<td class="toptitlex normaltextbold">(\w+)</td>', content)
                unique_methods = set(methods)
                print(f"   ✓ Found {len(unique_methods)} API methods")
                
                # Check for parameter documentation
                if '[Required]' in content:
                    print("   ✓ Contains parameter requirement information")
                    
            else:
                print("   ⚠ File doesn't appear to contain API documentation")
                
        else:
            print("\n❌ Failed to fetch documentation")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        

if __name__ == "__main__":
    main()