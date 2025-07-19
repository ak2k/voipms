#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
VoIP.ms WSDL Parser
Extracts API structure and operations from WSDL file
"""

import json
import logging
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from bs4 import BeautifulSoup
    HAS_BEAUTIFULSOUP = True
except ImportError:
    HAS_BEAUTIFULSOUP = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoIPMSAPIJSONGenerator:
    """Generates comprehensive JSON API definition from WSDL and HTML sources"""

    def __init__(self, wsdl_path: str = "../resources/server.wsdl", html_path: Optional[str] = None):
        self.wsdl_path = wsdl_path
        self.html_path = html_path
        self.namespaces = {
            'wsdl': 'http://schemas.xmlsoap.org/wsdl/',
            'xsd': 'http://www.w3.org/2001/XMLSchema',
            'xsd1': 'https://voip.ms/api/schema'
        }
        self.api_definition = {
            "version": "1.0",
            "generated_at": datetime.now().isoformat(),
            "base_url": "https://voip.ms/api/v1/rest.php",
            "authentication": {
                "type": "api_credentials",
                "parameters": ["api_username", "api_password"]
            },
            "global_parameters": {
                "api_username": {
                    "type": "string",
                    "required": True,
                    "description": "API username (email address)"
                },
                "api_password": {
                    "type": "string",
                    "required": True,
                    "description": "API password"
                }
            },
            "operations": {},
            "types": {},
            "error_codes": {}
        }

    def generate(self, output_path: str = "../src/voipms/api_definition.json") -> Dict[str, Any]:
        """Generate comprehensive API definition JSON"""
        logger.info("Starting API definition generation...")

        # Extract from WSDL
        self._parse_wsdl()

        # Extract from HTML if available
        if self.html_path and Path(self.html_path).exists():
            self._parse_html_documentation()

        # Add type definitions
        self._add_type_definitions()

        # Add error codes
        self._add_error_codes()

        # Write JSON
        with open(output_path, 'w') as f:
            json.dump(self.api_definition, f, indent=2)

        logger.info(f"Generated API definition with {len(self.api_definition['operations'])} operations")
        return self.api_definition

    def _parse_wsdl(self):
        """Parse WSDL to extract operations and structure"""
        logger.info(f"Parsing WSDL from {self.wsdl_path}")
        tree = ET.parse(self.wsdl_path)
        root = tree.getroot()

        types = root.find('.//xsd:schema', self.namespaces)
        if types:
            for complex_type in types.findall('.//xsd:complexType', self.namespaces):
                name = complex_type.get('name')
                if name and name.endswith('Input'):
                    op_name = name.replace('Input', '')
                    self._parse_operation(complex_type, op_name)

    def _parse_operation(self, complex_type, op_name: str):
        """Parse a single operation from WSDL"""
        parameters = {}
        sequence = complex_type.find('.//xsd:sequence', self.namespaces)

        if sequence:
            for element in sequence.findall('.//xsd:element', self.namespaces):
                param_name = element.get('name')
                if param_name not in ['api_username', 'api_password']:
                    xsd_type = element.get('type', 'xsd:string')
                    parameters[param_name] = {
                        "type": self._map_xsd_to_json_type(xsd_type),
                        "required": self._is_parameter_required(op_name, param_name),
                        "description": self._generate_param_description(op_name, param_name)
                    }

        self.api_definition['operations'][op_name] = {
            "method": op_name,
            "category": self._categorize_operation(op_name),
            "description": self._generate_operation_description(op_name),
            "parameters": parameters,
            "returns": {
                "type": "object",
                "description": f"Response from {op_name} operation"
            },
            "errors": self._get_possible_errors(op_name)
        }

    def _parse_html_documentation(self):
        """Parse HTML documentation to enhance API definition"""
        logger.info(f"Parsing HTML documentation from {self.html_path}")

        with open(self.html_path, encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Find method documentation sections
        method_sections = soup.find_all('div', class_='method-section')

        for section in method_sections:
            method_name = section.find('h3', class_='method-name')
            if method_name:
                op_name = method_name.text.strip()
                if op_name in self.api_definition['operations']:
                    self._enhance_operation_from_html(section, op_name)

    def _enhance_operation_from_html(self, section, op_name: str):
        """Enhance operation definition with HTML documentation"""
        operation = self.api_definition['operations'][op_name]

        # Extract detailed description
        desc_elem = section.find('div', class_='description')
        if desc_elem:
            operation['description'] = desc_elem.text.strip()

        # Extract parameter details
        param_table = section.find('table', class_='parameters')
        if param_table:
            for row in param_table.find_all('tr')[1:]:  # Skip header
                cells = row.find_all('td')
                if len(cells) >= 3:
                    param_name = cells[0].text.strip()
                    cells[1].text.strip()
                    param_desc = cells[2].text.strip()

                    if param_name in operation['parameters']:
                        operation['parameters'][param_name]['description'] = param_desc

        # Extract example
        example_elem = section.find('pre', class_='example')
        if example_elem:
            operation['example'] = example_elem.text.strip()

    def _add_type_definitions(self):
        """Add common type definitions"""
        self.api_definition['types'] = {
            "BillingType": {
                "type": "enum",
                "values": {
                    "1": "Per minute billing",
                    "2": "Flat rate billing"
                }
            },
            "ProtocolType": {
                "type": "enum",
                "values": {
                    "1": "SIP protocol",
                    "3": "IAX protocol"
                }
            },
            "AuthType": {
                "type": "enum",
                "values": {
                    "1": "Password authentication",
                    "2": "IP authentication"
                }
            },
            "RouteType": {
                "type": "enum",
                "values": [
                    "account", "ivr", "sip", "sys", "callback", "none"
                ]
            },
            "DeviceType": {
                "type": "enum",
                "values": [
                    "ata", "softphone", "smartphone", "pbx",
                    "router", "tablet", "other"
                ]
            },
            "LanguageCode": {
                "type": "enum",
                "values": [
                    "en", "es", "fr", "it", "pt", "ru", "de",
                    "pl", "nl", "ja", "zh", "tr", "he", "ar"
                ]
            },
            "DTMFMode": {
                "type": "enum",
                "values": ["inband", "rfc2833", "info", "auto"]
            },
            "NATOption": {
                "type": "enum",
                "values": ["yes", "no", "force_rport", "comedia", "auto"]
            },
            "CodecType": {
                "type": "enum",
                "values": [
                    "ulaw", "alaw", "gsm", "g723", "g729",
                    "g726", "g722", "ilbc", "speex", "opus"
                ]
            },
            "PhoneNumber": {
                "type": "string",
                "pattern": "^\\d{10,11}$",
                "description": "10 or 11 digit phone number"
            },
            "DateString": {
                "type": "string",
                "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
                "description": "Date in YYYY-MM-DD format"
            },
            "MoneyAmount": {
                "type": "number",
                "minimum": 0,
                "description": "Money amount in dollars"
            }
        }

    def _add_error_codes(self):
        """Add comprehensive error code definitions"""
        self.api_definition['error_codes'] = {
            "invalid_credentials": {
                "message": "Invalid username or password",
                "category": "authentication",
                "http_status": 401
            },
            "ip_not_enabled": {
                "message": "This IP is not enabled for API access",
                "category": "authentication",
                "http_status": 403
            },
            "missing_required_parameter": {
                "message": "A required parameter was not provided",
                "category": "validation",
                "http_status": 400
            },
            "invalid_parameter": {
                "message": "One or more parameters have invalid values",
                "category": "validation",
                "http_status": 400
            },
            "insufficient_funds": {
                "message": "Insufficient funds in account",
                "category": "billing",
                "http_status": 402
            },
            "rate_limit_exceeded": {
                "message": "API rate limit exceeded",
                "category": "rate_limit",
                "http_status": 429
            },
            "did_not_found": {
                "message": "The specified DID was not found",
                "category": "not_found",
                "http_status": 404
            },
            "server_error": {
                "message": "Internal server error occurred",
                "category": "server",
                "http_status": 500
            }
        }

    def _is_parameter_required(self, op_name: str, param_name: str) -> bool:
        """
        Determine if a parameter is required based on operation and parameter name.
        Since WSDL doesn't specify minOccurs, we use heuristics based on API knowledge.
        """
        # Known required parameters
        required_params = {
            'getCDR': ['date_from', 'date_to'],
            'getResellerCDR': ['date_from', 'date_to'],
            'sendSMS': ['did', 'destination', 'message'],
            'sendMMS': ['did', 'destination', 'message'],
            'createSubAccount': ['username', 'protocol', 'auth_type', 'password'],
            'createVoicemail': ['digits', 'email', 'password', 'skip_password', 'attach_message', 'delete_message', 'say_time', 'timezone', 'say_callerid', 'play_instructions', 'language'],
            'addCharge': ['client', 'charge', 'description', 'test'],
            'addPayment': ['client', 'payment', 'description', 'test'],
            'deleteCDR': ['account', 'cdr'],
            'deleteVoicemail': ['mailbox'],
            'setSubAccount': ['account'],
            'sendCallRecordingEmail': ['account', 'recording', 'email'],
            'sendFaxMessage': ['fax_number', 'destination', 'file']
        }

        # Check if this operation/parameter combo is known to be required
        if op_name in required_params:
            return param_name in required_params[op_name]

        # Most VoIP.ms API parameters are optional
        return False

    def _map_xsd_to_json_type(self, xsd_type: str) -> str:
        """Map XSD types to JSON schema types"""
        mapping = {
            'xsd:string': 'string',
            'xsd:integer': 'integer',
            'xsd:decimal': 'number',
            'xsd:boolean': 'boolean',
            'xsd:dateTime': 'string'
        }
        return mapping.get(xsd_type, 'string')

    def _categorize_operation(self, op_name: str) -> str:
        """Categorize operation based on name"""
        categories = {
            'get': 'query',
            'set': 'update',
            'add': 'create',
            'del': 'delete',
            'send': 'action',
            'cancel': 'action'
        }

        for prefix, category in categories.items():
            if op_name.lower().startswith(prefix):
                return category

        # Specific categorizations
        if 'balance' in op_name.lower():
            return 'billing'
        elif 'did' in op_name.lower():
            return 'did'
        elif 'sms' in op_name.lower():
            return 'sms'
        elif 'voicemail' in op_name.lower():
            return 'voicemail'
        elif 'cdr' in op_name.lower():
            return 'cdr'
        elif 'account' in op_name.lower() or 'client' in op_name.lower():
            return 'account'

        return 'general'

    def _generate_operation_description(self, op_name: str) -> str:
        """Generate human-readable operation description"""
        # Convert camelCase to words
        words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', op_name)
        return ' '.join(words).capitalize()

    def _generate_param_description(self, op_name: str, param_name: str) -> str:
        """Generate parameter description based on context"""
        # Common parameter descriptions
        common_params = {
            'did': 'DID (phone number) in format 1234567890',
            'client': 'Client/sub-account ID',
            'date_from': 'Start date in YYYY-MM-DD format',
            'date_to': 'End date in YYYY-MM-DD format',
            'timezone': 'Timezone offset (-12 to 12)',
            'limit': 'Maximum number of records to return',
            'destination': 'Destination phone number',
            'message': 'Message content',
            'description': 'Description or note',
            'enabled': 'Enable/disable status (0 or 1)',
            'priority': 'Priority level',
            'recording': 'Recording file or ID'
        }

        if param_name in common_params:
            return common_params[param_name]

        # Generate based on name patterns
        if param_name.endswith('_id'):
            return f"{param_name.replace('_id', '').title()} identifier"
        elif param_name.startswith('is_'):
            return f"Whether {param_name.replace('is_', '').replace('_', ' ')}"
        elif param_name.endswith('_type'):
            return f"Type of {param_name.replace('_type', '').replace('_', ' ')}"

        return f"{param_name.replace('_', ' ').title()}"

    def _get_possible_errors(self, op_name: str) -> List[str]:
        """Get possible error codes for an operation"""
        errors = ["invalid_credentials", "missing_required_parameter"]

        if 'get' in op_name.lower():
            errors.append("not_found")
        elif 'add' in op_name.lower() or 'create' in op_name.lower():
            errors.append("already_exists")
        elif 'balance' in op_name.lower() or 'charge' in op_name.lower():
            errors.append("insufficient_funds")
        elif 'sms' in op_name.lower():
            errors.extend(["sms_not_enabled", "invalid_sms_destination"])

        return errors


if __name__ == "__main__":
    generator = VoIPMSAPIJSONGenerator()
    api_def = generator.generate()
    print("\nGenerated API definition: voipms_api.json")
    print(f"Total operations: {len(api_def['operations'])}")
    print(f"Total types: {len(api_def['types'])}")
    print(f"Total error codes: {len(api_def['error_codes'])}")
