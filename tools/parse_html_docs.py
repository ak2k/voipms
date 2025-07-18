#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "beautifulsoup4>=4.12.0",
# ]
# ///
"""
Final Enhanced HTML Documentation Parser for VoIP.ms API
Properly extracts all metadata including error codes, notes, and constraints
"""

from bs4 import BeautifulSoup, NavigableString
import re
import json
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

class FinalVoIPMSDocumentationParser:
    """Final parser to extract all available metadata from VoIP.ms HTML documentation"""
    
    def __init__(self, html_path: str):
        self.html_path = html_path
        self.methods = {}
        self.error_codes = {}
        self.global_notes = []
        self.rate_limits = {}
        
    def parse(self) -> Dict[str, Any]:
        """Parse HTML documentation comprehensively"""
        print("Loading HTML documentation...")
        with open(self.html_path, 'r', encoding='utf-8', errors='ignore') as f:
            self.soup = BeautifulSoup(f.read(), 'html.parser')
        
        print("Extracting comprehensive documentation...")
        
        # Extract in order
        self._extract_global_notes()
        self._extract_error_codes()
        self._extract_rate_limits()
        self._extract_methods()
        
        return {
            'methods': self.methods,
            'error_codes': self.error_codes,
            'global_notes': self.global_notes,
            'rate_limits': self.rate_limits
        }
    
    def _extract_global_notes(self):
        """Extract global notes and important information"""
        # Look for introduction and important notes
        intro_sections = self.soup.find_all('div', class_='normaltext paddingxx')
        
        for section in intro_sections:
            text = section.get_text().strip()
            
            # Look for important global information
            if any(keyword in text for keyword in ['INTRODUCTION', 'UPDATE API PASSWORD', 'ENABLE IP ADDRESSES', 'not enabled by default', 'A2P']):
                # Extract key points
                lines = text.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and len(line) > 20:  # Skip short lines
                        if any(indicator in line for indicator in [
                            'API is not enabled by default',
                            'By default no IP Address',
                            'must be enabled',
                            'limit is 100 SMS per day',
                            'A2P',
                            'verification process',
                            'requirements and fees vary'
                        ]):
                            self.global_notes.append(line)
    
    def _extract_error_codes(self):
        """Extract error codes from the dedicated error codes table"""
        # Find the error codes section
        error_header = None
        for td in self.soup.find_all('td', class_='toptitlex normaltextbold'):
            if td.get_text().strip() == 'Error Codes':
                error_header = td
                break
        
        if not error_header:
            print("Warning: Could not find Error Codes section")
            return
        
        # Find the table containing error codes
        error_table = error_header.find_parent('table')
        if not error_table:
            return
        
        # Extract error codes from the table
        for row in error_table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) == 2:
                # Check if this is an error code row
                code_cell = cells[0]
                desc_cell = cells[1]
                
                if 'leftmenubottomtdlinefull' in code_cell.get('class', []):
                    code = code_cell.get_text().strip()
                    description = desc_cell.get_text().strip()
                    
                    # Skip if it's not a valid error code
                    if code and not code.startswith('<') and '_' in code:
                        self.error_codes[code] = description
    
    def _extract_rate_limits(self):
        """Extract rate limiting information"""
        # Look for rate limit mentions
        all_text = self.soup.get_text()
        
        # Common rate limit patterns
        rate_patterns = [
            r'(\d+)\s*(?:requests?|calls?)\s*per\s*(minute|hour|day)',
            r'limit(?:ed)?\s*to\s*(\d+)\s*per\s*(minute|hour|day)',
            r'maximum\s*of\s*(\d+)\s*(?:requests?|calls?)\s*per\s*(minute|hour|day)'
        ]
        
        for pattern in rate_patterns:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            for match in matches:
                count = match[0]
                period = match[1]
                self.rate_limits[f"api_{period}"] = int(count)
        
        # Look for specific API rate limit error
        if 'api_limit_exceeded' in self.error_codes:
            desc = self.error_codes['api_limit_exceeded']
            if 'per minute' in desc:
                self.rate_limits['api_requests_per_minute'] = 'See api_limit_exceeded error'
    
    def _extract_methods(self):
        """Extract all API methods with enhanced metadata"""
        # Find all method sections
        method_headers = self.soup.find_all('td', class_='toptitlex normaltextbold')
        
        for header in method_headers:
            method_name = header.get_text().strip()
            
            # Skip section headers and error codes
            if (method_name and 
                not any(skip in method_name for skip in ['VoIP', 'Error Codes', 'FUNCTION']) and
                not method_name.isupper() and
                len(method_name) > 3):
                
                self._parse_method_final(header, method_name)
    
    def _parse_method_final(self, header_cell, method_name: str):
        """Parse a single method with all available metadata"""
        current_row = header_cell.parent
        
        method_info = {
            'name': method_name,
            'parameters': {},
            'output_example': None,
            'description': self._generate_description(method_name),
            'notes': [],
            'warnings': [],
            'errors': [],
            'rate_limit': None,
            'authentication': None,
            'related_methods': [],
            'requirements': []
        }
        
        # Track what we've found
        found_sections = set()
        
        # Look for method details in subsequent rows
        while current_row:
            current_row = current_row.find_next_sibling('tr')
            if not current_row:
                break
                
            # Check if this row contains a new method header
            if current_row.find('td', class_='toptitlex'):
                break
                
            cells = current_row.find_all('td')
            if len(cells) >= 2:
                label_cell = cells[0]
                content_cell = cells[1]
                
                label_text = label_cell.get_text().strip()
                
                if label_text == 'Parameters' and 'parameters' not in found_sections:
                    found_sections.add('parameters')
                    params_content = self._get_cell_content(content_cell)
                    method_info['parameters'] = self._parse_parameters_final(params_content, method_name)
                    
                elif label_text == 'Output' and 'output' not in found_sections:
                    found_sections.add('output')
                    code_block = content_cell.find('code')
                    if code_block:
                        method_info['output_example'] = code_block.get_text().strip()
                        
                elif label_text in ['Note', 'Notes', 'Important', 'Warning']:
                    note_text = content_cell.get_text().strip()
                    if note_text:
                        if label_text == 'Warning':
                            method_info['warnings'].append(note_text)
                        else:
                            method_info['notes'].append(note_text)
                            
                        # Extract requirements from notes
                        if 'require' in note_text.lower():
                            method_info['requirements'].append(note_text)
                            
                elif label_text == 'Errors':
                    errors_text = content_cell.get_text().strip()
                    method_info['errors'] = self._parse_method_errors(errors_text)
                    
                elif label_text in ['Authentication', 'Permission']:
                    auth_text = content_cell.get_text().strip()
                    method_info['authentication'] = auth_text
        
        # Look for related methods in description or notes
        all_text = ' '.join([method_info['description']] + method_info['notes'])
        related = re.findall(r'\b(get|set|del|add|create)[A-Z]\w+\b', all_text)
        method_info['related_methods'] = list(set(related) - {method_name})
        
        self.methods[method_name] = method_info
    
    def _get_cell_content(self, cell):
        """Extract content from a cell, preserving structure"""
        # First try to get code block
        code_block = cell.find('code')
        if code_block:
            return code_block.get_text().strip()
        
        # Otherwise get all text, preserving line breaks
        content = []
        for element in cell.descendants:
            if isinstance(element, NavigableString):
                text = str(element).strip()
                if text:
                    content.append(text)
            elif element.name == 'br':
                content.append('\n')
        
        return '\n'.join(content)
    
    def _parse_parameters_final(self, params_text: str, method_name: str) -> Dict[str, Dict[str, Any]]:
        """Final parameter parsing with all metadata extraction"""
        parameters = {}
        
        # Split by lines and process each parameter
        lines = params_text.split('\n')
        current_param = None
        current_info = {}
        continuation_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this is a parameter definition line (has =>)
            if '=>' in line and not line.startswith(' '):
                # Save previous parameter if exists
                if current_param:
                    # Process any continuation lines
                    if continuation_lines:
                        full_desc = current_info['description'] + ' ' + ' '.join(continuation_lines)
                        current_info['description'] = full_desc
                        # Re-extract metadata from full description
                        self._update_parameter_metadata(current_info, full_desc)
                    
                    parameters[current_param] = current_info
                    continuation_lines = []
                
                # Parse new parameter
                parts = line.split('=>', 1)
                param_name = parts[0].strip()
                description = parts[1].strip() if len(parts) > 1 else ''
                
                # Check if required
                required = '[Required]' in description
                if required:
                    description = description.replace('[Required]', '').strip()
                
                current_param = param_name
                type_info = self._infer_type_final(param_name, description)
                
                current_info = {
                    'description': description,
                    'required': required,
                    'type': type_info.get('type', 'string'),
                    'examples': self._extract_examples(description),
                    'constraints': self._extract_constraints_final(description),
                    'default': self._extract_default(description),
                    'format': self._extract_format(description),
                    'units': self._extract_units(description),
                    'validation': self._extract_validation(description)
                }
                
                # Add enum if present
                if 'enum' in type_info:
                    current_info['enum'] = type_info['enum']
                    
            elif current_param and line:
                # This is a continuation of the previous parameter's description
                continuation_lines.append(line)
                
        # Save last parameter
        if current_param:
            if continuation_lines:
                full_desc = current_info['description'] + ' ' + ' '.join(continuation_lines)
                current_info['description'] = full_desc
                self._update_parameter_metadata(current_info, full_desc)
            
            parameters[current_param] = current_info
            
        return parameters
    
    def _update_parameter_metadata(self, param_info: Dict, description: str):
        """Update parameter metadata based on full description"""
        # Re-extract with full description
        if not param_info['default']:
            param_info['default'] = self._extract_default(description)
        if not param_info['format']:
            param_info['format'] = self._extract_format(description)
        if not param_info['units']:
            param_info['units'] = self._extract_units(description)
        
        # Update constraints
        new_constraints = self._extract_constraints_final(description)
        param_info['constraints'].update(new_constraints)
        
        # Update examples
        new_examples = self._extract_examples(description)
        param_info['examples'] = list(set(param_info['examples'] + new_examples))
        
        # Update validation
        if not param_info.get('validation'):
            param_info['validation'] = self._extract_validation(description)
    
    def _infer_type_final(self, param_name: str, description: str) -> Dict[str, Any]:
        """Final type inference with comprehensive enum extraction"""
        description_lower = description.lower()
        result = {}
        
        # Special boolean patterns that use string "1"/"0"
        if any(pattern in description for pattern in ['Boolean: 1/0', '(Boolean: 1/0)', 'Values: 1=', 'Values:1=']):
            result = {'type': 'string', 'enum': ['0', '1']}
            
        # Pattern for "true"/"false" string booleans
        elif any(pattern in description for pattern in ['Set to true if', 'true if', 'false if']):
            result = {'type': 'string', 'enum': ['true', 'false']}
            
        # yes/no booleans
        elif 'yes/no' in description_lower or 'yes or no' in description_lower:
            result = {'type': 'string', 'enum': ['yes', 'no']}
            
        # Extract explicit enums with patterns like "0 = value1, 1 = value2"
        elif enum_match := re.search(r'(\d+)\s*=\s*[\w\s]+(?:\s*[,;]\s*\d+\s*=\s*[\w\s]+)+', description):
            # Extract all enum values
            enum_values = re.findall(r'(\d+)\s*=\s*[^,;]+', description)
            result = {'type': 'string', 'enum': [re.match(r'(\d+)', val).group(1) for val in enum_values]}
            
        # Extract allowed values patterns like "Allowed values: 1, 2, 3"
        elif allowed_match := re.search(r'[Aa]llowed values?:\s*([^.]+)', description):
            values_text = allowed_match.group(1)
            # Extract numeric or string values
            if ',' in values_text:
                values = [v.strip() for v in values_text.split(',')]
                # Clean up values
                clean_values = []
                for v in values:
                    # Remove any trailing description
                    v = re.split(r'\s*[-=]\s*', v)[0].strip()
                    if v and v[0].isdigit():
                        clean_values.append(v)
                if clean_values:
                    result = {'type': 'string', 'enum': clean_values}
            
        # Extract comma-separated value lists (e.g., "100, 120, 140, 160")
        elif value_list_match := re.search(r'(?:values?:?\s*)?(\d+(?:\s*,\s*\d+){2,})', description_lower):
            values = [v.strip() for v in value_list_match.group(1).split(',')]
            result = {'type': 'string', 'enum': values}
            
        # Check for specific value options in parentheses
        elif options_match := re.search(r'\((?:options?:?\s*)?([\w\s,/]+)\)', description):
            options_text = options_match.group(1)
            if ',' in options_text or '/' in options_text:
                delim = ',' if ',' in options_text else '/'
                options = [o.strip() for o in options_text.split(delim)]
                if all(o and (o[0].isdigit() or o in ['true', 'false', 'yes', 'no']) for o in options):
                    result = {'type': 'string', 'enum': options}
        
        # If no enum found, determine basic type
        if not result:
            # Integer indicators
            if any(indicator in description_lower for indicator in ['id', 'code', 'number of', 'count', 'port']):
                result = {'type': 'integer'}
            # Float/Decimal indicators
            elif any(indicator in description_lower for indicator in ['amount', 'dollars', 'decimal', 'price', 'rate', 'charge']):
                result = {'type': 'number'}
            # Date indicators
            elif any(indicator in description_lower for indicator in ['date', 'yyyy-mm-dd']):
                result = {'type': 'string', 'format': 'date'}
            # List indicators
            elif any(indicator in description_lower for indicator in ['separated by', 'list of', 'comma-separated']):
                result = {'type': 'string', 'format': 'list'}
            else:
                # Default to string
                result = {'type': 'string'}
            
        return result
    
    def _extract_default(self, description: str) -> Optional[str]:
        """Extract default value from description"""
        patterns = [
            r'[Dd]efault(?:\s+value)?:\s*([^,\n.;]+)',
            r'[Dd]efaults?\s+to\s+([^,\n.;]+)',
            r'\(default:\s*([^)]+)\)',
            r'By default,?\s+([^,\n.;]+)',
            r'Default:\s*"([^"]+)"',
            r"Default:\s*'([^']+)'"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, description)
            if match:
                default = match.group(1).strip()
                # Clean up common suffixes
                default = re.sub(r'\s*\(.*\)$', '', default)
                return default
        return None
    
    def _extract_format(self, description: str) -> Optional[str]:
        """Extract format specification from description"""
        # Date formats
        if 'YYYY-MM-DD' in description or 'yyyy-mm-dd' in description.lower():
            return 'date'
        
        # Time formats
        if 'HH:MM:SS' in description or 'hh:mm:ss' in description.lower():
            return 'time'
        
        # IP address formats
        if any(pattern in description for pattern in ['192.168.1.0/24', 'IP Address', 'CIDR']):
            return 'ip_address'
        
        # Email format
        if 'email' in description.lower() or '@' in description:
            return 'email'
        
        # Phone number formats
        if 'E.164' in description or 'phone' in description.lower():
            return 'phone'
        
        # Base64
        if 'base64' in description.lower() or 'base 64' in description.lower():
            return 'base64'
        
        # File formats
        format_match = re.search(r'\b(CSV|XML|SQL|JSON|XLS|Excel|PDF|MP3|WAV)\b', description, re.IGNORECASE)
        if format_match:
            return format_match.group(1).lower()
        
        return None
    
    def _extract_units(self, description: str) -> Optional[str]:
        """Extract units of measurement from description"""
        units_patterns = [
            (r'\b\d+\s*seconds?\b|\bseconds?\b', 'seconds'),
            (r'\b\d+\s*minutes?\b|\bminutes?\b', 'minutes'),
            (r'\b\d+\s*hours?\b|\bhours?\b', 'hours'),
            (r'\b\d+\s*days?\b|\bdays?\b', 'days'),
            (r'\b\d+\s*milliseconds?\b|\bmilliseconds?\b', 'milliseconds'),
            (r'\b\d+\s*ms\b|\bms\b', 'milliseconds'),
            (r'\$|dollars?|USD', 'dollars'),
            (r'%|percent', 'percent'),
            (r'\bGB\b|gigabytes?', 'gigabytes'),
            (r'\bMB\b|megabytes?', 'megabytes'),
            (r'\bKB\b|kilobytes?', 'kilobytes')
        ]
        
        for pattern, unit in units_patterns:
            if re.search(pattern, description, re.IGNORECASE):
                return unit
        
        return None
    
    def _extract_constraints_final(self, description: str) -> Dict[str, Any]:
        """Extract all types of constraints from description"""
        constraints = {}
        
        # Range constraints with 'between X and Y'
        range_match = re.search(r'between\s+(\d+)\s+and\s+(\d+)', description, re.IGNORECASE)
        if range_match:
            constraints['minimum'] = int(range_match.group(1))
            constraints['maximum'] = int(range_match.group(2))
        
        # Maximum value patterns
        max_patterns = [
            r'[Mm]ax(?:imum)?:?\s*(\d+)',
            r'up\s+to\s+(\d+)',
            r'no\s+more\s+than\s+(\d+)',
            r'≤\s*(\d+)',
            r'<=\s*(\d+)'
        ]
        for pattern in max_patterns:
            max_match = re.search(pattern, description)
            if max_match and 'maximum' not in constraints:
                constraints['maximum'] = int(max_match.group(1))
        
        # Minimum value patterns
        min_patterns = [
            r'[Mm]in(?:imum)?:?\s*(\d+)',
            r'at\s+least\s+(\d+)',
            r'no\s+less\s+than\s+(\d+)',
            r'≥\s*(\d+)',
            r'>=\s*(\d+)'
        ]
        for pattern in min_patterns:
            min_match = re.search(pattern, description)
            if min_match and 'minimum' not in constraints:
                constraints['minimum'] = int(min_match.group(1))
        
        # Length constraints
        length_patterns = [
            (r'(\d+)\s*characters?\s*(?:or less|max)', 'maxLength'),
            (r'[Mm]ax(?:imum)?\s+length:?\s*(\d+)', 'maxLength'),
            (r'[Mm]in(?:imum)?\s+length:?\s*(\d+)', 'minLength'),
            (r'exactly\s+(\d+)\s*characters?', 'exactLength')
        ]
        for pattern, constraint_type in length_patterns:
            match = re.search(pattern, description)
            if match:
                constraints[constraint_type] = int(match.group(1))
        
        # Pattern constraints
        if 'format' in description.lower() or 'pattern' in description.lower():
            if 'E.164' in description:
                constraints['pattern'] = r'^\+?[1-9]\d{1,14}$'
            elif 'email' in description.lower():
                constraints['pattern'] = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            elif re.search(r'^\d{4}-\d{2}-\d{2}$', description):
                constraints['pattern'] = r'^\d{4}-\d{2}-\d{2}$'
        
        # Date range constraints
        date_range_match = re.search(r'(\d+)\s*days?\s*or\s*less', description)
        if date_range_match:
            constraints['date_range_days'] = int(date_range_match.group(1))
        
        # Values from another method
        values_patterns = [
            r'Values?\s+from\s+(\w+)',
            r'see\s+(\w+)\s+for\s+(?:valid\s+)?values',
            r'use\s+(\w+)\s+to\s+get\s+(?:valid\s+)?values'
        ]
        for pattern in values_patterns:
            values_match = re.search(pattern, description, re.IGNORECASE)
            if values_match:
                constraints['values_from'] = values_match.group(1)
                break
        
        # Rate limit constraints
        limit_match = re.search(r'(\d+)\s*per\s*(day|hour|minute)', description)
        if limit_match:
            constraints['rate_limit'] = {
                'count': int(limit_match.group(1)),
                'period': limit_match.group(2)
            }
        
        # Multiple values allowed
        if any(indicator in description.lower() for indicator in ['comma-separated', 'separated by', 'multiple']):
            constraints['multiple'] = True
            
            # Delimiter
            if 'comma' in description.lower():
                constraints['delimiter'] = ','
            elif 'semicolon' in description.lower():
                constraints['delimiter'] = ';'
            elif 'pipe' in description.lower():
                constraints['delimiter'] = '|'
        
        return constraints
    
    def _extract_validation(self, description: str) -> Optional[Dict[str, Any]]:
        """Extract validation rules from description"""
        validation = {}
        
        # Required format validations
        if 'must be' in description.lower():
            validation['strict'] = True
            
        # Conditional requirements
        if 'required if' in description.lower() or 'required when' in description.lower():
            validation['conditional'] = True
            
        # Mutually exclusive
        if 'cannot be used with' in description.lower() or 'mutually exclusive' in description.lower():
            validation['exclusive'] = True
        
        return validation if validation else None
    
    def _parse_method_errors(self, errors_text: str) -> List[str]:
        """Parse method-specific errors"""
        errors = []
        
        # Try different delimiters
        if ',' in errors_text:
            errors = [e.strip() for e in errors_text.split(',')]
        elif ';' in errors_text:
            errors = [e.strip() for e in errors_text.split(';')]
        elif '\n' in errors_text:
            errors = [e.strip() for e in errors_text.split('\n')]
        else:
            # Single error
            errors = [errors_text.strip()]
        
        # Clean up errors
        clean_errors = []
        for error in errors:
            error = error.strip()
            if error and not error.startswith('<'):
                # Remove any trailing punctuation
                error = error.rstrip('.,;')
                clean_errors.append(error)
        
        return clean_errors
    
    def _extract_examples(self, description: str) -> List[str]:
        """Extract example values from description"""
        examples = []
        
        # Look for explicit example patterns
        example_patterns = [
            r'\(Example:\s*([^)]+)\)',
            r'Example:\s*([^,\n.;]+)',
            r'\(e\.g\.,?\s*([^)]+)\)',
            r'such as\s+([^,\n.;]+)',
            r'like\s+([^,\n.;]+)'
        ]
        
        for pattern in example_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            for match in matches:
                # Split if multiple examples
                if ',' in match:
                    examples.extend([e.strip() for e in match.split(',')])
                else:
                    examples.append(match.strip())
        
        # Also extract quoted values as potential examples
        quoted_values = re.findall(r"'([^']+)'", description) + re.findall(r'"([^"]+)"', description)
        for value in quoted_values:
            # Filter out non-example quotes
            if len(value) < 50 and not any(skip in value.lower() for skip in ['the', 'this', 'that', 'which']):
                examples.append(value)
        
        # Clean and deduplicate
        clean_examples = []
        for ex in examples:
            ex = ex.strip().rstrip('.')
            if ex and ex not in clean_examples:
                clean_examples.append(ex)
        
        return clean_examples[:5]  # Limit to 5 examples
    
    def _generate_description(self, method_name: str) -> str:
        """Generate method description from name"""
        patterns = {
            r'^get(.+)$': 'Retrieve {} information',
            r'^set(.+)$': 'Update {} settings',
            r'^del(.+)$': 'Delete {}',
            r'^delete(.+)$': 'Delete {}',
            r'^add(.+)$': 'Add new {}',
            r'^create(.+)$': 'Create new {}',
            r'^search(.+)$': 'Search for {}',
            r'^send(.+)$': 'Send {}',
            r'^cancel(.+)$': 'Cancel {}',
            r'^order(.+)$': 'Order {}',
            r'^backOrder(.+)$': 'Backorder {}',
            r'^signup(.+)$': 'Sign up {}',
            r'^assign(.+)$': 'Assign {}',
            r'^connect(.+)$': 'Connect {}'
        }
        
        for pattern, template in patterns.items():
            match = re.match(pattern, method_name)
            if match:
                resource = match.group(1)
                # Convert camelCase to readable
                words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', resource)
                resource = ' '.join(words).lower()
                return template.format(resource)
        
        # Default: convert camelCase to sentence
        words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', method_name)
        return ' '.join(words).capitalize()
    
    def generate_final_schema(self) -> Dict[str, Any]:
        """Generate final comprehensive schema"""
        return {
            'version': '2.0',
            'source': 'Final Enhanced HTML Documentation Parser',
            'methods': self.methods,
            'error_codes': self.error_codes,
            'global_notes': self.global_notes,
            'rate_limits': self.rate_limits,
            'statistics': {
                'total_methods': len(self.methods),
                'total_error_codes': len(self.error_codes),
                'methods_with_notes': sum(1 for m in self.methods.values() if m.get('notes')),
                'methods_with_warnings': sum(1 for m in self.methods.values() if m.get('warnings')),
                'methods_with_constraints': sum(1 for m in self.methods.values() 
                                              if any(p.get('constraints') for p in m['parameters'].values())),
                'methods_with_defaults': sum(1 for m in self.methods.values() 
                                           if any(p.get('default') for p in m['parameters'].values())),
                'methods_with_enums': sum(1 for m in self.methods.values() 
                                        if any(p.get('enum') for p in m['parameters'].values()))
            }
        }
    
    def generate_final_report(self) -> str:
        """Generate final comprehensive extraction report"""
        report = "# Final VoIP.ms API Documentation Extraction Report\n\n"
        
        # Statistics
        stats = self.generate_final_schema()['statistics']
        report += "## Summary Statistics\n"
        for key, value in stats.items():
            report += f"- {key.replace('_', ' ').title()}: {value}\n"
        
        report += f"\n## Global Information\n"
        report += f"- Global notes extracted: {len(self.global_notes)}\n"
        report += f"- Error codes extracted: {len(self.error_codes)}\n"
        report += f"- Rate limits found: {self.rate_limits}\n"
        
        # Sample global notes
        if self.global_notes:
            report += f"\n### Sample Global Notes:\n"
            for note in self.global_notes[:3]:
                report += f"- {note[:100]}...\n" if len(note) > 100 else f"- {note}\n"
        
        # Methods with most metadata
        report += "\n## Methods with Rich Metadata\n\n"
        
        # Score methods by metadata richness
        method_scores = []
        for method_name, method_info in self.methods.items():
            score = 0
            param_count = len(method_info['parameters'])
            
            for param in method_info['parameters'].values():
                if param.get('default'): score += 2
                if param.get('constraints'): score += 3
                if param.get('enum'): score += 3
                if param.get('format'): score += 1
                if param.get('units'): score += 1
                if param.get('examples'): score += 1
                
            if method_info.get('notes'): score += 5
            if method_info.get('warnings'): score += 5
            if method_info.get('requirements'): score += 3
            
            method_scores.append((method_name, score, param_count))
        
        # Sort by score
        method_scores.sort(key=lambda x: x[1], reverse=True)
        
        report += "### Top 5 Most Documented Methods:\n"
        for method, score, param_count in method_scores[:5]:
            report += f"\n#### {method} (metadata score: {score}, parameters: {param_count})\n"
            method_info = self.methods[method]
            
            # Show sample parameter with rich metadata
            for param_name, param_info in list(method_info['parameters'].items())[:2]:
                if any(param_info.get(k) for k in ['default', 'constraints', 'enum', 'format']):
                    report += f"- **{param_name}**:\n"
                    if param_info.get('description'):
                        report += f"  - Description: {param_info['description'][:80]}...\n"
                    if param_info.get('type'):
                        report += f"  - Type: {param_info['type']}\n"
                    if param_info.get('default'):
                        report += f"  - Default: {param_info['default']}\n"
                    if param_info.get('enum'):
                        report += f"  - Enum values: {param_info['enum']}\n"
                    if param_info.get('constraints'):
                        report += f"  - Constraints: {param_info['constraints']}\n"
                    if param_info.get('format'):
                        report += f"  - Format: {param_info['format']}\n"
                    if param_info.get('units'):
                        report += f"  - Units: {param_info['units']}\n"
            
            if method_info.get('notes'):
                report += f"- Notes: {len(method_info['notes'])} note(s)\n"
            if method_info.get('warnings'):
                report += f"- Warnings: {len(method_info['warnings'])} warning(s)\n"
        
        # Error codes sample
        report += "\n## Sample Error Codes\n"
        for code, desc in list(self.error_codes.items())[:10]:
            report += f"- **{code}**: {desc[:80]}...\n" if len(desc) > 80 else f"- **{code}**: {desc}\n"
        
        return report


if __name__ == "__main__":
    parser = FinalVoIPMSDocumentationParser("resources/voipms_api_documentation.html")
    
    print("Parsing HTML documentation with final enhanced extraction...")
    result = parser.parse()
    
    print(f"\nExtracted documentation for {len(result['methods'])} methods")
    print(f"Extracted {len(result['error_codes'])} error codes")
    print(f"Extracted {len(result['global_notes'])} global notes")
    print(f"Extracted rate limits: {result['rate_limits']}")
    
    # Generate final schema
    schema = parser.generate_final_schema()
    with open("voipms_documentation_final.json", "w") as f:
        json.dump(schema, f, indent=2)
    print("\nGenerated final documentation schema")
    
    # Generate final report
    report = parser.generate_final_report()
    with open("final_extraction_report.md", "w") as f:
        f.write(report)
    print("Generated final extraction report")
    
    # Show sample of extracted data
    print("\nSample extraction:")
    for method_name, method_info in list(result['methods'].items())[:1]:
        if method_info['parameters']:
            print(f"\nMethod: {method_name}")
            print(f"Description: {method_info['description']}")
            if method_info.get('notes'):
                print(f"Notes: {method_info['notes']}")
            
            for param_name, param_info in list(method_info['parameters'].items())[:2]:
                print(f"\nParameter '{param_name}':")
                for key, value in param_info.items():
                    if value and key != 'description':
                        print(f"  {key}: {value}")