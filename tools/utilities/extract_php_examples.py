#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Extract test data from PHP examples to create Python test fixtures
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional


class PHPExampleExtractor:
    """Extract API examples from PHP files"""
    
    def __init__(self, php_dir: str = "../API/Examples REST for PHP"):
        self.php_dir = Path(php_dir)
        self.test_cases = []
        
    def extract_all(self) -> List[Dict[str, Any]]:
        """Extract test cases from all PHP files"""
        for php_file in sorted(self.php_dir.glob("*.php")):
            print(f"Processing {php_file.name}...")
            test_case = self.extract_from_file(php_file)
            if test_case:
                self.test_cases.append(test_case)
                
        return self.test_cases
        
    def extract_from_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Extract test case from a single PHP file"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Extract method name
        method_match = re.search(r'\$method\s*=\s*"([^"]+)"', content)
        if not method_match:
            return None
            
        method = method_match.group(1)
        
        # Extract parameters
        params = {}
        
        # Look for parameters in the URL
        url_match = re.search(r'CURLOPT_URL.*?rest\.php\?([^"]+)', content)
        if url_match:
            query_string = url_match.group(1)
            # Parse parameters from query string
            param_matches = re.findall(r'&(\w+)=\{?\$?(\w+)\}?', query_string)
            for param_name, var_name in param_matches:
                if param_name not in ['api_username', 'api_password', 'method']:
                    # Try to find the variable value
                    var_match = re.search(rf'\${var_name}\s*=\s*"([^"]+)"', content)
                    if var_match:
                        params[param_name] = var_match.group(1)
                        
        # Extract response handling
        response_checks = []
        
        # Look for status checks
        if 'status' in content:
            response_checks.append({
                'field': 'status',
                'expected': 'success',
                'type': 'equality'
            })
            
        # Look for array access patterns
        array_accesses = re.findall(r'\$response\[([^\]]+)\]', content)
        for field in array_accesses:
            field = field.strip('"\'')
            if field not in ['status']:
                response_checks.append({
                    'field': field,
                    'type': 'exists'
                })
                
        # Extract description from filename
        description = file_path.stem.replace('-', ' ').replace('_', ' ')
        if description.startswith(('00.', '01.', '02.', '03.', '04.', '05.', '06.', '07.', '08.', '09.')):
            description = description[3:]
            
        return {
            'file': file_path.name,
            'method': method,
            'description': description.title(),
            'parameters': params,
            'response_checks': response_checks,
            'has_error_handling': 'status' in content and 'success' in content
        }
        
    def generate_test_fixtures(self, output_path: str = "test_fixtures.json"):
        """Generate test fixtures file"""
        fixtures = {
            'test_cases': self.test_cases,
            'metadata': {
                'source': 'VoIP.ms PHP REST examples',
                'total_cases': len(self.test_cases)
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(fixtures, f, indent=2)
            
        print(f"\nGenerated {output_path} with {len(self.test_cases)} test cases")
        
    def generate_python_tests(self, output_path: str = "../tests/test_api_examples.py"):
        """Generate Python test file based on PHP examples"""
        
        test_code = '''"""
Tests based on VoIP.ms PHP API examples
Auto-generated from PHP example files
"""

import pytest
from unittest.mock import patch, MagicMock
from voipms import VoIPMSClient


class TestAPIExamples:
    """Test cases derived from official PHP examples"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test client with mock credentials"""
        with patch.dict('os.environ', {
            'VOIPMS_USERNAME': 'test@example.com',
            'VOIPMS_PASSWORD': 'testpass'
        }):
            self.client = VoIPMSClient()
'''
        
        # Generate test methods
        for i, test_case in enumerate(self.test_cases):
            method_name = test_case['method']
            test_name = f"test_{method_name.lower()}_{i}"
            
            test_code += f'''
            
    @patch('httpx.Client.post')
    def {test_name}(self, mock_post):
        """Test {method_name} - {test_case['description']}"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {{
            'status': 'success',
'''
            
            # Add expected response fields
            for check in test_case['response_checks']:
                if check['field'] != 'status':
                    test_code += f"            '{check['field']}': 'test_value',\n"
                    
            test_code += '''        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response
        
        # Make API call
'''
            
            # Generate method call
            if test_case['parameters']:
                param_str = ', '.join(f"{k}='{v}'" for k, v in test_case['parameters'].items())
                test_code += f"        result = self.client.{method_name}({param_str})\n"
            else:
                test_code += f"        result = self.client.{method_name}()\n"
                
            test_code += '''        
        # Verify response
        assert result['status'] == 'success'
'''
            
            # Add field existence checks
            for check in test_case['response_checks']:
                if check['field'] != 'status':
                    test_code += f"        assert '{check['field']}' in result\n"
                    
        with open(output_path, 'w') as f:
            f.write(test_code)
            
        print(f"Generated {output_path}")


def main():
    """Extract test data from PHP examples"""
    extractor = PHPExampleExtractor()
    
    print("Extracting test cases from PHP examples...")
    test_cases = extractor.extract_all()
    
    print(f"\nFound {len(test_cases)} test cases:")
    for case in test_cases:
        print(f"  - {case['method']}: {case['description']}")
        if case['parameters']:
            print(f"    Parameters: {case['parameters']}")
            
    # Generate outputs
    extractor.generate_test_fixtures("test_fixtures.json")
    extractor.generate_python_tests()
    

if __name__ == "__main__":
    main()