#!/usr/bin/env python3
"""
Enhanced VoIP.ms API JSON Generator
Combines WSDL structure with HTML documentation for rich API definition
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Import our existing parsers
from json_api_generator import VoIPMSAPIJSONGenerator
from html_documentation_parser import VoIPMSDocumentationParser
from fetch_documentation_simple import SimpleVoIPMSDocumentationFetcher


class EnhancedVoIPMSJSONGenerator:
    """Enhanced generator that combines WSDL and HTML documentation"""
    
    def __init__(self, wsdl_path: str = "server.wsdl"):
        self.wsdl_path = wsdl_path
        self.base_generator = VoIPMSAPIJSONGenerator(wsdl_path)
        
    def generate_with_documentation(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        html_file: Optional[str] = None,
        output_path: str = "voipms_api_enriched.json"
    ) -> Dict[str, Any]:
        """
        Generate enriched API definition with HTML documentation.
        
        Args:
            username: VoIP.ms username for fetching docs (optional if html_file provided)
            password: VoIP.ms password for fetching docs (optional if html_file provided)
            html_file: Path to existing HTML documentation (optional)
            output_path: Where to save the enriched JSON
            
        Returns:
            The enriched API definition
        """
        print("=" * 60)
        print("Enhanced VoIP.ms API JSON Generator")
        print("=" * 60)
        
        # Step 1: Generate base API definition from WSDL
        print("\n1. Generating base API definition from WSDL...")
        api_def = self.base_generator.generate("temp_base_api.json")
        print(f"   ✓ Found {len(api_def['operations'])} operations")
        
        # Step 2: Get HTML documentation
        if html_file and Path(html_file).exists():
            print(f"\n2. Using existing HTML documentation: {html_file}")
            doc_file = html_file
        elif username and password:
            print("\n2. Fetching HTML documentation from VoIP.ms...")
            fetcher = SimpleVoIPMSDocumentationFetcher()
            doc_file = fetcher.fetch_documentation(username, password, "api_docs_enriched.html")
            if not doc_file:
                print("   ⚠ Failed to fetch documentation, using WSDL only")
                Path("temp_base_api.json").unlink()
                with open(output_path, 'w') as f:
                    json.dump(api_def, f, indent=2)
                return api_def
        else:
            print("\n2. No HTML documentation available, using WSDL only")
            Path("temp_base_api.json").unlink()
            with open(output_path, 'w') as f:
                json.dump(api_def, f, indent=2)
            return api_def
            
        # Step 3: Parse HTML documentation
        print("\n3. Parsing HTML documentation...")
        parser = VoIPMSDocumentationParser(doc_file)
        html_methods = parser.parse()
        print(f"   ✓ Extracted documentation for {len(html_methods)} methods")
        
        # Step 4: Merge documentation into API definition
        print("\n4. Enriching API definition with documentation...")
        enriched_count = 0
        
        for method_name, html_info in html_methods.items():
            if method_name in api_def['operations']:
                operation = api_def['operations'][method_name]
                
                # Enhance description
                if html_info.get('description'):
                    operation['description'] = html_info['description']
                    
                # Enhance parameter descriptions
                for param_name, param_info in html_info.get('parameters', {}).items():
                    if param_name in operation['parameters']:
                        operation['parameters'][param_name].update({
                            'description': param_info.get('description', ''),
                            'example': param_info.get('example'),
                            'validation': param_info.get('validation')
                        })
                        
                # Add output example
                if html_info.get('output_example'):
                    operation['example_response'] = html_info['output_example']
                    
                enriched_count += 1
                
        print(f"   ✓ Enriched {enriched_count} operations with documentation")
        
        # Step 5: Add metadata
        api_def['metadata'] = {
            'generated_at': datetime.now().isoformat(),
            'generator_version': '2.0',
            'documentation_source': 'WSDL + HTML',
            'total_operations': len(api_def['operations']),
            'documented_operations': enriched_count
        }
        
        # Step 6: Save enriched API definition
        print(f"\n5. Saving enriched API definition to {output_path}")
        with open(output_path, 'w') as f:
            json.dump(api_def, f, indent=2)
            
        # Cleanup
        Path("temp_base_api.json").unlink(missing_ok=True)
        
        print("\n✅ Successfully generated enriched API definition!")
        print(f"   - Total operations: {len(api_def['operations'])}")
        print(f"   - Documented operations: {enriched_count}")
        print(f"   - Output file: {output_path}")
        
        return api_def
        
    def show_sample_enrichment(self, api_def: Dict[str, Any]):
        """Show a sample of the enriched documentation"""
        print("\n" + "=" * 60)
        print("Sample Enriched Operations:")
        print("=" * 60)
        
        # Find operations with the most documentation
        enriched_ops = [
            (name, op) for name, op in api_def['operations'].items()
            if any(
                param.get('example') or len(param.get('description', '')) > 50
                for param in op['parameters'].values()
            )
        ]
        
        for i, (name, op) in enumerate(enriched_ops[:3]):
            print(f"\n{i+1}. {name}:")
            print(f"   Description: {op['description']}")
            print("   Parameters:")
            for param_name, param_info in op['parameters'].items():
                print(f"     - {param_name} ({param_info['type']}):")
                if param_info.get('description'):
                    print(f"       {param_info['description']}")
                if param_info.get('example'):
                    print(f"       Example: {param_info['example']}")


def main():
    """Main entry point"""
    import getpass
    
    generator = EnhancedVoIPMSJSONGenerator()
    
    # Check for existing HTML file
    existing_html = None
    for possible_file in ["VoIP.ms - API Documentation.html", "api_docs_fetched.html", "api_docs_enriched.html"]:
        if Path(possible_file).exists():
            existing_html = possible_file
            break
            
    if existing_html:
        print(f"Found existing HTML documentation: {existing_html}")
        use_existing = input("Use this file? [Y/n]: ").strip().lower()
        if use_existing != 'n':
            api_def = generator.generate_with_documentation(html_file=existing_html)
            generator.show_sample_enrichment(api_def)
            return
            
    # Otherwise, ask for credentials
    print("\nTo fetch the latest documentation, please provide your VoIP.ms credentials:")
    username = input("Username (email): ").strip()
    if username:
        password = getpass.getpass("Password: ")
        api_def = generator.generate_with_documentation(username=username, password=password)
        generator.show_sample_enrichment(api_def)
    else:
        print("\nGenerating from WSDL only...")
        api_def = generator.generate_with_documentation()
        

if __name__ == "__main__":
    # For non-interactive use, directly generate with existing HTML
    generator = EnhancedVoIPMSJSONGenerator()
    
    # Check for existing HTML file
    existing_html = None
    for possible_file in ["VoIP.ms - API Documentation.html", "api_docs_fetched.html", "api_docs_enriched.html"]:
        if Path(possible_file).exists():
            existing_html = possible_file
            break
            
    if existing_html:
        print(f"Using existing HTML documentation: {existing_html}")
        api_def = generator.generate_with_documentation(html_file=existing_html)
        generator.show_sample_enrichment(api_def)
    else:
        print("No HTML documentation found, generating from WSDL only...")
        api_def = generator.generate_with_documentation()