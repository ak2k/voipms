#!/usr/bin/env python3
"""
HTML Documentation Parser for VoIP.ms API
Extracts rich documentation from the HTML API docs
"""

from bs4 import BeautifulSoup
import re
import json
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

class VoIPMSDocumentationParser:
    """Parse VoIP.ms HTML documentation to extract method details"""
    
    def __init__(self, html_path: str):
        self.html_path = html_path
        self.methods = {}
        
    def parse(self) -> Dict[str, Any]:
        """Parse HTML documentation"""
        print("Loading HTML documentation...")
        with open(self.html_path, 'r', encoding='utf-8', errors='ignore') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        print("Extracting method documentation...")
        
        # Find all method sections
        # Methods are in cells with class "toptitlex normaltextbold"
        method_headers = soup.find_all('td', class_='toptitlex normaltextbold')
        
        for header in method_headers:
            method_name = header.get_text().strip()
            if method_name and not method_name.startswith('VoIP'):  # Skip section headers
                self._parse_method(header, method_name)
        
        return self.methods
    
    def _parse_method(self, header_cell, method_name: str):
        """Parse a single method's documentation"""
        # Find the parent table row, then navigate to parameter and output rows
        current_row = header_cell.parent
        
        method_info = {
            'name': method_name,
            'parameters': {},
            'output_example': None,
            'description': self._generate_description(method_name)
        }
        
        # Look for the next rows containing Parameters and Output
        while current_row:
            current_row = current_row.find_next_sibling('tr')
            if not current_row:
                break
                
            cells = current_row.find_all('td')
            if len(cells) >= 2:
                label_cell = cells[0]
                content_cell = cells[1]
                
                label_text = label_cell.get_text().strip()
                
                if label_text == 'Parameters':
                    # Parse parameters
                    params_text = content_cell.get_text(separator='\n').strip()
                    method_info['parameters'] = self._parse_parameters(params_text)
                    
                elif label_text == 'Output':
                    # Parse output example
                    code_block = content_cell.find('code')
                    if code_block:
                        method_info['output_example'] = code_block.get_text().strip()
                    
                # Check if we've hit the next method
                if cells[0].get('class') and 'toptitlex' in cells[0].get('class', []):
                    break
        
        self.methods[method_name] = method_info
    
    def _parse_parameters(self, params_text: str) -> Dict[str, Dict[str, Any]]:
        """Parse parameter documentation"""
        parameters = {}
        
        # Split by lines and process each parameter
        lines = params_text.split('\n')
        current_param = None
        current_info = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this is a parameter definition line (has =>)
            if '=>' in line:
                # Save previous parameter if exists
                if current_param:
                    parameters[current_param] = current_info
                
                # Parse new parameter
                parts = line.split('=>', 1)
                param_name = parts[0].strip()
                description = parts[1].strip() if len(parts) > 1 else ''
                
                # Check if required
                required = '[Required]' in description
                if required:
                    description = description.replace('[Required]', '').strip()
                
                current_param = param_name
                current_info = {
                    'description': description,
                    'required': required,
                    'type': self._infer_type(param_name, description),
                    'examples': self._extract_examples(description),
                    'constraints': self._extract_constraints(description)
                }
            elif current_param and line:
                # This is a continuation of the previous parameter's description
                current_info['description'] += ' ' + line
                
        # Save last parameter
        if current_param:
            parameters[current_param] = current_info
            
        return parameters
    
    def _infer_type(self, param_name: str, description: str) -> str:
        """Infer parameter type from name and description"""
        description_lower = description.lower()
        
        # Boolean indicators
        if any(indicator in description_lower for indicator in ['boolean:', '(1/0)', 'true/false', 'enable', 'disable']):
            return 'bool'
        
        # Integer indicators
        if any(indicator in description_lower for indicator in ['between', 'seconds', 'minutes', 'id', 'code', 'number of']):
            return 'int'
        
        # Float/Decimal indicators
        if any(indicator in description_lower for indicator in ['amount', 'dollars', 'decimal', 'price']):
            return 'float'
        
        # Date indicators
        if any(indicator in description_lower for indicator in ['date', 'yyyy-mm-dd']):
            return 'str'  # Could be datetime
        
        # List indicators
        if any(indicator in description_lower for indicator in ['separated by', 'list of', 'comma-separated']):
            return 'List[str]'
        
        # Default to string
        return 'str'
    
    def _extract_examples(self, description: str) -> List[str]:
        """Extract example values from description"""
        examples = []
        
        # Look for patterns like (Example: ...) or Example: ...
        example_patterns = [
            r'\(Example:\s*([^)]+)\)',
            r'Example:\s*([^,\n]+)',
            r'\(e\.g\.,?\s*([^)]+)\)',
            r"'([^']+)'",  # Single quoted values
            r'"([^"]+)"'   # Double quoted values
        ]
        
        for pattern in example_patterns:
            matches = re.findall(pattern, description)
            examples.extend(matches)
        
        return list(set(examples))  # Remove duplicates
    
    def _extract_constraints(self, description: str) -> Dict[str, Any]:
        """Extract constraints from description"""
        constraints = {}
        
        # Range constraints
        range_match = re.search(r'between\s+(\d+)\s+and\s+(\d+)', description)
        if range_match:
            constraints['min'] = int(range_match.group(1))
            constraints['max'] = int(range_match.group(2))
        
        # Values from another method
        values_match = re.search(r'Values from\s+(\w+)', description)
        if values_match:
            constraints['values_from'] = values_match.group(1)
        
        # Specific values
        if 'could have the following values:' in description:
            constraints['enum'] = True
        
        return constraints
    
    def _generate_description(self, method_name: str) -> str:
        """Generate method description from name"""
        # Similar to the enhanced builder
        patterns = {
            r'^get(.+)$': 'Retrieve {} information',
            r'^set(.+)$': 'Update {} settings',
            r'^del(.+)$': 'Delete {}',
            r'^add(.+)$': 'Add new {}',
            r'^create(.+)$': 'Create new {}',
            r'^search(.+)$': 'Search for {}',
        }
        
        for pattern, template in patterns.items():
            match = re.match(pattern, method_name)
            if match:
                resource = match.group(1)
                # Convert camelCase to readable
                words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', resource)
                resource = ' '.join(words).lower()
                return template.format(resource)
        
        # Default
        words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', method_name)
        return ' '.join(words).capitalize()
    
    def generate_enhanced_schema(self) -> Dict[str, Any]:
        """Generate enhanced schema with documentation"""
        schema = {
            'version': '1.0',
            'source': 'HTML Documentation',
            'methods': {}
        }
        
        for method_name, method_info in self.methods.items():
            schema['methods'][method_name] = {
                'description': method_info['description'],
                'parameters': method_info['parameters'],
                'response_example': method_info.get('output_example')
            }
        
        return schema
    
    def generate_documentation_summary(self) -> str:
        """Generate a summary of extracted documentation"""
        summary = f"# VoIP.ms API Documentation Summary\n\n"
        summary += f"Total methods documented: {len(self.methods)}\n\n"
        
        # Methods with most parameters
        methods_by_params = sorted(
            [(name, len(info['parameters'])) for name, info in self.methods.items()],
            key=lambda x: x[1],
            reverse=True
        )
        
        summary += "## Methods with most parameters:\n"
        for method, param_count in methods_by_params[:10]:
            summary += f"- {method}: {param_count} parameters\n"
        
        # Required vs optional parameter stats
        total_params = 0
        required_params = 0
        
        for method_info in self.methods.values():
            for param_info in method_info['parameters'].values():
                total_params += 1
                if param_info.get('required'):
                    required_params += 1
        
        summary += f"\n## Parameter Statistics:\n"
        summary += f"- Total parameters: {total_params}\n"
        summary += f"- Required parameters: {required_params} ({required_params/total_params*100:.1f}%)\n"
        summary += f"- Optional parameters: {total_params - required_params} ({(total_params-required_params)/total_params*100:.1f}%)\n"
        
        return summary


if __name__ == "__main__":
    parser = VoIPMSDocumentationParser("VoIP.ms - API Documentation.html")
    
    print("Parsing HTML documentation...")
    methods = parser.parse()
    
    print(f"\nExtracted documentation for {len(methods)} methods")
    
    # Generate enhanced schema
    schema = parser.generate_enhanced_schema()
    with open("voipms_documentation_schema.json", "w") as f:
        json.dump(schema, f, indent=2)
    print("Generated documentation schema")
    
    # Generate summary
    summary = parser.generate_documentation_summary()
    with open("documentation_summary.md", "w") as f:
        f.write(summary)
    print("Generated documentation summary")
    
    # Show sample of extracted data
    print("\nSample extracted documentation:")
    sample_method = next(iter(methods.items()))
    print(f"\nMethod: {sample_method[0]}")
    print(f"Description: {sample_method[1]['description']}")
    print(f"Parameters: {len(sample_method[1]['parameters'])}")
    
    if sample_method[1]['parameters']:
        param_name, param_info = next(iter(sample_method[1]['parameters'].items()))
        print(f"\nSample parameter '{param_name}':")
        print(f"  Required: {param_info.get('required', False)}")
        print(f"  Type: {param_info.get('type', 'str')}")
        print(f"  Description: {param_info.get('description', '')[:100]}...")
        if param_info.get('examples'):
            print(f"  Examples: {param_info['examples'][:3]}")