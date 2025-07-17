#!/usr/bin/env python3
"""
VoIP.ms Documentation Fetcher (Simple Version)
Uses requests to fetch authenticated API documentation
"""

import requests
import getpass
import sys
from pathlib import Path
from typing import Optional, Dict
import re


class SimpleVoIPMSDocumentationFetcher:
    """Fetches VoIP.ms API documentation using requests"""
    
    def __init__(self):
        self.session = requests.Session()
        # Set a user agent to appear like a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-GPC': '1',
        })
        
    def fetch_documentation(
        self, 
        username: str, 
        password: str, 
        output_file: str = "api_docs_fetched.html"
    ) -> Optional[str]:
        """
        Fetch API documentation by logging into VoIP.ms.
        
        Args:
            username: VoIP.ms username (email)
            password: VoIP.ms password
            output_file: Where to save the documentation HTML
            
        Returns:
            Path to saved file if successful, None otherwise
        """
        try:
            print("Step 1: Getting login page...")
            if not self._get_login_page():
                return None
                
            print("Step 2: Performing login...")
            if not self._perform_login(username, password):
                return None
                
            print("Step 3: Fetching API documentation...")
            html_content = self._fetch_api_docs()
            if not html_content:
                return None
                
            print("Step 4: Saving documentation...")
            return self._save_documentation(html_content, output_file)
            
        except Exception as e:
            print(f"Error: {e}")
            return None
            
    def _get_login_page(self) -> bool:
        """Get the login page to establish session and get any tokens"""
        try:
            login_url = "https://voip.ms/signin/index.php"
            response = self.session.get(login_url, timeout=30)
            response.raise_for_status()
            
            # Extract any CSRF tokens if present
            self._extract_tokens(response.text)
            
            return True
            
        except Exception as e:
            print(f"Failed to get login page: {e}")
            return False
            
    def _extract_tokens(self, html: str):
        """Extract any hidden tokens from the login form"""
        # Look for common CSRF token patterns
        token_patterns = [
            r'<input[^>]*name="csrf_token"[^>]*value="([^"]+)"',
            r'<input[^>]*name="_token"[^>]*value="([^"]+)"',
            r'<meta[^>]*name="csrf-token"[^>]*content="([^"]+)"',
            r'<input[^>]*name="token"[^>]*value="([^"]+)"',
        ]
        
        self.tokens = {}
        for pattern in token_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                token_name = re.search(r'name="([^"]+)"', match.group(0)).group(1)
                self.tokens[token_name] = match.group(1)
                print(f"  Found token: {token_name}")
                
    def _perform_login(self, username: str, password: str) -> bool:
        """Perform the login"""
        try:
            login_url = "https://voip.ms/signin/index.php"
            
            # Build login data
            login_data = {
                'username': username,
                'password': password,
                'redirect': '/m/apidocs.php',
                'submitted': '1',
                'Login': 'Login',
            }
            
            # Add any tokens we found
            login_data.update(self.tokens)
            
            # Update referer
            self.session.headers['Referer'] = login_url
            
            # Perform login
            response = self.session.post(
                login_url,
                data=login_data,
                allow_redirects=True,
                timeout=30
            )
            
            # Check if login was successful
            if response.status_code == 200:
                # Check for signs of successful login
                if any(indicator in response.text for indicator in [
                    'Logout', 'logout', 'Dashboard', 'dashboard', 
                    'apidocs', 'API Documentation'
                ]):
                    print("  Login successful!")
                    return True
                else:
                    print("  Login failed - invalid credentials?")
                    # Save response for debugging
                    Path("login_response.html").write_text(response.text)
                    print("  Login response saved to login_response.html for debugging")
                    return False
            else:
                print(f"  Login failed with status code: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"  Login error: {e}")
            return False
            
    def _fetch_api_docs(self) -> Optional[str]:
        """Fetch the API documentation page"""
        try:
            # Try multiple possible API documentation URLs
            api_urls = [
                "https://voip.ms/m/apidocs.php",
                "https://voip.ms/m/api.php",
                "https://voip.ms/members/api.php",
            ]
            
            for url in api_urls:
                print(f"  Trying {url}...")
                response = self.session.get(url, timeout=30)
                
                if response.status_code == 200:
                    # Check if we got the API documentation
                    if any(indicator in response.text for indicator in [
                        'getBalance', 'Parameters', 'Output', 
                        'API Documentation', 'toptitlex'
                    ]):
                        print("  ✓ Found API documentation!")
                        return response.text
                        
            print("  Could not find API documentation")
            return None
            
        except Exception as e:
            print(f"  Error fetching API docs: {e}")
            return None
            
    def _save_documentation(self, html_content: str, output_file: str) -> str:
        """Save the documentation HTML"""
        output_path = Path(output_file)
        output_path.write_text(html_content, encoding='utf-8')
        
        print(f"  Documentation saved to: {output_path.absolute()}")
        return str(output_path.absolute())


def main():
    """Interactive documentation fetcher"""
    print("=== VoIP.ms Documentation Fetcher (Simple) ===\n")
    
    # Get credentials
    username = input("VoIP.ms username (email): ").strip()
    if not username:
        print("Username is required")
        return
        
    password = getpass.getpass("VoIP.ms password: ").strip()
    if not password:
        print("Password is required")
        return
        
    # Output file
    output_file = input("\nOutput file [api_docs_fetched.html]: ").strip()
    if not output_file:
        output_file = "api_docs_fetched.html"
        
    # Fetch documentation
    print("\nFetching documentation...\n")
    fetcher = SimpleVoIPMSDocumentationFetcher()
    
    result = fetcher.fetch_documentation(username, password, output_file)
    
    if result:
        print("\n✓ Documentation fetched successfully!")
        print(f"  Saved to: {result}")
        print("\nYou can now run the client builder:")
        print("  python complete_client_builder.py")
    else:
        print("\n✗ Failed to fetch documentation")
        print("\nTroubleshooting:")
        print("1. Check your credentials")
        print("2. Make sure API access is enabled in your VoIP.ms account")
        print("3. Check if your IP is whitelisted for API access")
        print("\nAlternatively, you can:")
        print("1. Manually save the HTML from https://voip.ms/m/apidocs.php")
        print("2. Use the curl command you provided earlier")


if __name__ == "__main__":
    main()