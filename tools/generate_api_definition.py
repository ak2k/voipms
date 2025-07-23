#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests>=2.31.0",
#     "beautifulsoup4>=4.12.0",
#     "lxml>=4.9.0",
# ]
# ///
"""
Final API Definition Generator for VoIP.ms
Uses the enhanced HTML parser to generate comprehensive API definitions
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from bs4 import BeautifulSoup

sys.path.append(str(Path(__file__).parent))

# Import our HTML parser
try:
    from parse_html_docs import FinalVoIPMSDocumentationParser
except ImportError:
    # Try importing from parsers module
    from parsers.html import FinalVoIPMSDocumentationParser


class FinalVoIPMSJSONGenerator:
    """Final generator that creates comprehensive API definitions"""

    def __init__(self):
        self.wsdl_url = "https://voip.ms/api/v1/server.wsdl"
        self.base_api_def = {
            "version": "2.0",
            "generated_at": datetime.now().isoformat(),
            "base_url": "https://voip.ms/api/v1/rest.php",
            "authentication": {
                "type": "api_credentials",
                "parameters": ["api_username", "api_password"],
            },
            "global_parameters": {
                "api_username": {
                    "type": "string",
                    "required": True,
                    "description": "API username (email address)",
                },
                "api_password": {"type": "string", "required": True, "description": "API password"},
            },
            "operations": {},
            "error_codes": {},
            "global_notes": [],
            "rate_limits": {},
        }

        # Load type overrides
        self.type_overrides = {}
        override_file = Path(__file__).parent / "wsdl_type_overrides.json"
        if override_file.exists():
            with open(override_file) as f:
                override_data = json.load(f)
                self.type_overrides = override_data.get("type_overrides", {})
                print(f"Loaded {len(self.type_overrides)} type overrides")

    def generate_with_documentation(self, html_file: Optional[str] = None) -> Dict[str, Any]:
        """Generate API definition with comprehensive documentation"""

        # Step 1: Parse WSDL to get basic structure
        print("Fetching WSDL from VoIP.ms...")
        try:
            response = requests.get(self.wsdl_url, timeout=30)
            response.raise_for_status()
            wsdl_content = response.text
            print("Successfully fetched WSDL")
        except Exception as e:
            print(f"Error fetching WSDL: {e}")
            return self.base_api_def

        # Parse WSDL to get methods
        soup = BeautifulSoup(wsdl_content, "xml")
        operations = self._parse_wsdl_operations(soup)

        # Step 2: Use enhanced parser if HTML is available
        if html_file and Path(html_file).exists():
            print(f"\nUsing enhanced parser on: {html_file}")
            parser = FinalVoIPMSDocumentationParser(html_file)
            doc_data = parser.parse()

            # Merge error codes
            self.base_api_def["error_codes"] = doc_data["error_codes"]
            self.base_api_def["global_notes"] = doc_data["global_notes"]
            self.base_api_def["rate_limits"] = doc_data["rate_limits"]

            # Enrich operations with documentation
            enriched_count = 0
            for op_name, op_data in operations.items():
                if op_name in doc_data["methods"]:
                    method_doc = doc_data["methods"][op_name]
                    enriched_count += 1

                    # Update operation description
                    if method_doc.get("description"):
                        op_data["description"] = method_doc["description"]

                    # Add notes and warnings
                    if method_doc.get("notes"):
                        op_data["notes"] = method_doc["notes"]
                    if method_doc.get("warnings"):
                        op_data["warnings"] = method_doc["warnings"]
                    if method_doc.get("requirements"):
                        op_data["requirements"] = method_doc["requirements"]

                    # Enrich parameters
                    for param_name, param_info in method_doc.get("parameters", {}).items():
                        if param_name in op_data["parameters"]:
                            # Merge parameter information
                            wsdl_param = op_data["parameters"][param_name]

                            # Update type if we have better info
                            if param_info.get("type"):
                                wsdl_param["type"] = self._map_type(param_info["type"])

                            # Add all enhanced metadata
                            if param_info.get("enum"):
                                wsdl_param["enum"] = param_info["enum"]
                                wsdl_param["type"] = "string"  # Enums are always strings

                            if param_info.get("default"):
                                wsdl_param["default"] = param_info["default"]

                            if param_info.get("format"):
                                wsdl_param["format"] = param_info["format"]

                            if param_info.get("constraints"):
                                # Map constraints to JSON Schema keywords
                                constraints = param_info["constraints"]
                                if "minimum" in constraints:
                                    wsdl_param["minimum"] = constraints["minimum"]
                                if "maximum" in constraints:
                                    wsdl_param["maximum"] = constraints["maximum"]
                                if "minLength" in constraints:
                                    wsdl_param["minLength"] = constraints["minLength"]
                                if "maxLength" in constraints:
                                    wsdl_param["maxLength"] = constraints["maxLength"]
                                if "pattern" in constraints:
                                    wsdl_param["pattern"] = constraints["pattern"]
                                if "values_from" in constraints:
                                    wsdl_param["values_from"] = constraints["values_from"]
                                if "rate_limit" in constraints:
                                    wsdl_param["rate_limit"] = constraints["rate_limit"]
                                if "multiple" in constraints:
                                    wsdl_param["multiple"] = constraints["multiple"]
                                if "delimiter" in constraints:
                                    wsdl_param["delimiter"] = constraints["delimiter"]

                            if param_info.get("units"):
                                wsdl_param["units"] = param_info["units"]

                            if param_info.get("examples"):
                                wsdl_param["examples"] = param_info["examples"]

                            if param_info.get("validation"):
                                wsdl_param["validation"] = param_info["validation"]

                            # Use enhanced description if available
                            if param_info.get("description"):
                                wsdl_param["description"] = param_info["description"]

                            # Use required field from HTML docs (more accurate than WSDL)
                            if "required" in param_info:
                                wsdl_param["required"] = param_info["required"]

                    # Add output example
                    if method_doc.get("output_example"):
                        op_data["example_response"] = method_doc["output_example"]

                    # Add method-specific errors
                    if method_doc.get("errors"):
                        op_data["method_errors"] = method_doc["errors"]

            print(f"\nEnriched {enriched_count} operations with documentation")

        # Apply type overrides to fix WSDL errors (must be done after HTML enrichment)
        self._apply_type_overrides(operations)

        # Add statistics
        self.base_api_def["statistics"] = {
            "total_operations": len(operations),
            "enriched_operations": enriched_count,
            "coverage_percentage": round(enriched_count / len(operations) * 100, 2),
            "operations_with_enums": sum(
                1
                for op in operations.values()
                if any(p.get("enum") for p in op["parameters"].values())
            ),
            "operations_with_constraints": sum(
                1
                for op in operations.values()
                if any(self._has_constraints(p) for p in op["parameters"].values())
            ),
            "operations_with_defaults": sum(
                1
                for op in operations.values()
                if any(p.get("default") for p in op["parameters"].values())
            ),
            "total_error_codes": len(self.base_api_def["error_codes"]),
        }

        # Step 3: Add operations to base definition
        self.base_api_def["operations"] = operations

        # Step 4: Write to file
        output_file = Path("src/voipms/api_definition_source.json")
        output_file.parent.mkdir(exist_ok=True)

        with open(output_file, "w") as f:
            json.dump(self.base_api_def, f, indent=2)

        print(f"\nGenerated source API definition: {output_file}")

        return self.base_api_def

    def _parse_wsdl_operations(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Parse operations from WSDL with complex type support"""
        operations = {}

        # Find all operation elements
        for operation in soup.find_all("operation"):
            op_name = operation.get("name")
            if not op_name:
                continue

            # Get input message
            input_msg = operation.find("input")
            if not input_msg:
                continue

            msg_name = input_msg.get("message", "").split(":")[-1]

            # Find message definition
            message_def = soup.find("message", {"name": msg_name})
            if not message_def:
                continue

            # Extract parameters
            parameters = {}
            for part in message_def.find_all("part"):
                param_name = part.get("name")
                param_type = part.get("type", "string").split(":")[-1]

                # Check if this is a complex type reference (e.g., params: getCDRInput)
                if param_name == "params" and "Input" in param_type:
                    # Find the complex type definition
                    complex_type = soup.find("complexType", {"name": param_type})
                    if complex_type:
                        # Extract parameters from the complex type
                        sequence = complex_type.find("sequence")
                        if sequence:
                            for element in sequence.find_all("element"):
                                elem_name = element.get("name")
                                elem_type = element.get("type", "string").split(":")[-1]
                                min_occurs = element.get("minOccurs", "1")

                                # Skip auth parameters
                                if elem_name and elem_name not in ["api_username", "api_password"]:
                                    parameters[elem_name] = {
                                        "type": self._map_type(elem_type),
                                        "required": min_occurs != "0",
                                        "description": "",
                                    }
                else:
                    # Handle simple parameters (fallback for non-complex types)
                    if param_name and param_name not in ["api_username", "api_password"]:
                        parameters[param_name] = {
                            "type": self._map_type(param_type),
                            "required": False,
                            "description": "",
                        }

            operations[op_name] = {
                "method": op_name,
                "category": self._categorize_method(op_name),
                "description": self._generate_description(op_name),
                "parameters": parameters,
                "returns": {"type": "object", "description": f"Response from {op_name} operation"},
            }

        return operations

    def _apply_type_overrides(self, operations: Dict[str, Any]) -> None:
        """Apply type overrides to fix WSDL errors"""
        if not self.type_overrides:
            return

        override_count = 0
        not_found = []
        for override_key, correct_type in self.type_overrides.items():
            op_name, param_name = override_key.split(".")

            if op_name in operations:
                if param_name in operations[op_name]["parameters"]:
                    operations[op_name]["parameters"][param_name]["type"] = correct_type
                    override_count += 1
                else:
                    not_found.append(f"{op_name}.{param_name}")
            else:
                not_found.append(f"{op_name} (operation not found)")

        if override_count > 0:
            print(f"Applied {override_count} type overrides to fix WSDL errors")
        if not_found:
            print(f"Could not apply {len(not_found)} overrides: {', '.join(not_found[:5])}...")

    def _has_constraints(self, param: Dict) -> bool:
        """Check if parameter has any constraints"""
        constraint_keys = [
            "minimum",
            "maximum",
            "minLength",
            "maxLength",
            "pattern",
            "values_from",
            "rate_limit",
            "multiple",
        ]
        return any(key in param for key in constraint_keys)

    def _map_type(self, wsdl_type: str) -> str:
        """Map WSDL types to JSON Schema types"""
        type_mapping = {
            "string": "string",
            "str": "string",
            "int": "integer",
            "integer": "integer",
            "float": "number",
            "double": "number",
            "decimal": "number",
            "boolean": "boolean",
            "bool": "boolean",
            "dateTime": "string",
            "date": "string",
            "List[str]": "array",
        }
        return type_mapping.get(wsdl_type, "string")

    def _categorize_method(self, method_name: str) -> str:
        """Categorize method based on name patterns"""
        patterns = {
            "create": r"^(create|add|signup)",
            "read": r"^(get|search)",
            "update": r"^(set|update)",
            "delete": r"^(del|delete|cancel|remove)",
            "action": r"^(send|order|backOrder|connect|assign)",
        }

        for category, pattern in patterns.items():
            if re.match(pattern, method_name, re.IGNORECASE):
                return category

        return "other"

    def _generate_description(self, method_name: str) -> str:
        """Generate method description from name"""
        patterns = {
            r"^get(.+)$": "Retrieve {} information",
            r"^set(.+)$": "Update {} settings",
            r"^del(.+)$": "Delete {}",
            r"^delete(.+)$": "Delete {}",
            r"^add(.+)$": "Add new {}",
            r"^create(.+)$": "Create new {}",
            r"^search(.+)$": "Search for {}",
            r"^send(.+)$": "Send {}",
            r"^cancel(.+)$": "Cancel {}",
            r"^order(.+)$": "Order {}",
            r"^backOrder(.+)$": "Backorder {}",
            r"^signup(.+)$": "Sign up {}",
            r"^assign(.+)$": "Assign {}",
            r"^connect(.+)$": "Connect {}",
        }

        for pattern, template in patterns.items():
            match = re.match(pattern, method_name)
            if match:
                resource = match.group(1)
                # Convert camelCase to readable
                words = re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)", resource)
                resource = " ".join(words).lower()
                return template.format(resource)

        # Default: convert camelCase to sentence
        words = re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)", method_name)
        return " ".join(words).capitalize()

    def show_enrichment_summary(self, api_def: Dict[str, Any]):
        """Display summary of enrichments"""
        print("\n" + "=" * 60)
        print("COMPREHENSIVE API DEFINITION SUMMARY")
        print("=" * 60)

        if "statistics" in api_def:
            stats = api_def["statistics"]
            print("\nOperations:")
            print(f"  Total: {stats['total_operations']}")
            print(f"  Enriched: {stats['enriched_operations']} ({stats['coverage_percentage']}%)")
            print(f"  With Enums: {stats['operations_with_enums']}")
            print(f"  With Constraints: {stats['operations_with_constraints']}")
            print(f"  With Defaults: {stats['operations_with_defaults']}")

        print(f"\nError Codes: {len(api_def.get('error_codes', {}))}")
        print(f"Global Notes: {len(api_def.get('global_notes', []))}")
        print(f"Rate Limits: {api_def.get('rate_limits', {})}")

        # Show sample enriched operation
        print("\n" + "-" * 60)
        print("SAMPLE ENRICHED OPERATION")
        print("-" * 60)

        # Find the most enriched operation
        best_op = None
        best_score = 0

        for op_name, op_data in api_def["operations"].items():
            score = 0
            for param in op_data["parameters"].values():
                if param.get("enum"):
                    score += 3
                if param.get("default"):
                    score += 2
                if self._has_constraints(param):
                    score += 3
                if param.get("format"):
                    score += 1
                if param.get("units"):
                    score += 1

            if score > best_score:
                best_score = score
                best_op = (op_name, op_data)

        if best_op:
            op_name, op_data = best_op
            print(f"\nOperation: {op_name}")
            print(f"Description: {op_data.get('description', 'N/A')}")

            if op_data.get("notes"):
                print(f"Notes: {op_data['notes']}")

            print("\nEnriched Parameters:")
            for param_name, param_info in op_data["parameters"].items():
                if any(
                    param_info.get(k)
                    for k in ["enum", "default", "format", "units", "minimum", "maximum"]
                ):
                    print(f"\n  {param_name}:")
                    print(f"    Type: {param_info.get('type')}")
                    print(f"    Required: {param_info.get('required', False)}")
                    if param_info.get("enum"):
                        print(f"    Enum: {param_info['enum']}")
                    if param_info.get("default"):
                        print(f"    Default: {param_info['default']}")
                    if param_info.get("format"):
                        print(f"    Format: {param_info['format']}")
                    if param_info.get("units"):
                        print(f"    Units: {param_info['units']}")
                    if param_info.get("minimum") or param_info.get("maximum"):
                        print(
                            f"    Range: {param_info.get('minimum', 'N/A')} - {param_info.get('maximum', 'N/A')}"
                        )
                    if param_info.get("values_from"):
                        print(f"    Values From: {param_info['values_from']}")


if __name__ == "__main__":
    generator = FinalVoIPMSJSONGenerator()

    # Check for existing HTML file
    html_file = None
    for possible_file in [
        "../resources/voipms_api_documentation.html",
        "voipms_api_documentation.html",
        "resources/voipms_api_documentation.html",
    ]:
        if Path(possible_file).exists():
            html_file = possible_file
            break

    if html_file:
        print(f"Using HTML documentation: {html_file}")
        api_def = generator.generate_with_documentation(html_file=html_file)
        generator.show_enrichment_summary(api_def)
    else:
        print("No HTML documentation found, generating from WSDL only...")
        api_def = generator.generate_with_documentation()
        print("\nGenerated basic API definition from WSDL")
