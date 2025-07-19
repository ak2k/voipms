#!/usr/bin/env python3
"""
Generate Type Stubs for VoIP.ms Client

This script generates .pyi stub files from api_definition.json to enable
IDE autocomplete, type checking, and better developer experience.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class TypeStubGenerator:
    """Generate Python type stubs from API definition."""

    def __init__(self, api_definition_path: str):
        """Initialize with path to API definition."""
        with open(api_definition_path) as f:
            self.api_definition = json.load(f)
        self.operations = self.api_definition.get('operations', {})

    def json_type_to_python(self, json_type: str, param_info: Dict[str, Any] = None) -> str:
        """Convert JSON type to Python type hint, with constraint annotations."""
        if param_info is None:
            param_info = {}

        base_type_map = {
            'string': 'str',
            'integer': 'int',
            'number': 'float',
            'boolean': 'bool',
            'array': 'List[Any]',
            'object': 'Dict[str, Any]'
        }

        base_type = base_type_map.get(json_type, 'Any')

        # Check for enum values first
        if enum_values := param_info.get('enum'):
            if all(isinstance(v, str) for v in enum_values):
                values = ', '.join(f'"{v}"' for v in enum_values)
                return f'Literal[{values}]'

        # For string types with numeric constraints, add constraint annotation
        if json_type == 'string':
            constraints = []

            # Add range constraints
            if 'minimum' in param_info and 'maximum' in param_info:
                constraints.append(f"Range: {param_info['minimum']}-{param_info['maximum']}")
            elif 'minimum' in param_info:
                constraints.append(f"Min: {param_info['minimum']}")
            elif 'maximum' in param_info:
                constraints.append(f"Max: {param_info['maximum']}")

            # Add length constraints
            if 'minLength' in param_info:
                constraints.append(f"MinLength: {param_info['minLength']}")
            if 'maxLength' in param_info:
                constraints.append(f"MaxLength: {param_info['maxLength']}")

            # Add format constraints
            if format_info := param_info.get('format'):
                constraints.append(f"Format: {format_info}")

            # Add units
            if units := param_info.get('units'):
                constraints.append(f"Units: {units}")

            # Create annotated type if we have constraints
            if constraints:
                constraint_str = '; '.join(constraints)
                return f'Annotated[str, "{constraint_str}"]'

        # For numeric types with constraints
        elif json_type in ['integer', 'number']:
            constraints = []
            if 'minimum' in param_info:
                constraints.append(f"Min: {param_info['minimum']}")
            if 'maximum' in param_info:
                constraints.append(f"Max: {param_info['maximum']}")

            if constraints:
                constraint_str = '; '.join(constraints)
                return f'Annotated[{base_type}, "{constraint_str}"]'

        return base_type

    def get_literal_values(self, param_name: str, param_info: Dict[str, Any]) -> Optional[str]:
        """Extract literal type values from description if applicable."""
        # Check if parameter has enum values from API definition
        if 'enum' in param_info:
            enum_values = param_info['enum']
            # Create Literal type for enum values
            if all(isinstance(v, str) for v in enum_values):
                values = ', '.join(f'"{v}"' for v in enum_values)
                return f'Literal[{values}]'

        # Common patterns for literal types (for backward compatibility)
        literal_params = {
            'calltype': ['inbound', 'outbound'],
            'billing_type': ['1', '2'],  # 1=PerMinute, 2=Flat
            'protocol': ['sip', 'iax2'],
            'language': ['en', 'es', 'fr'],
            'device_type': ['1', '2', '3', '4', '5'],  # Various device types
        }

        if param_name in literal_params:
            values = ', '.join(f'"{v}"' for v in literal_params[param_name])
            return f'Literal[{values}]'

        return None

    def generate_method_signature(self, method_name: str, method_info: Dict[str, Any]) -> str:
        """Generate a single method signature."""
        params = method_info.get('parameters', {})

        # Start with method definition
        lines = [f"    def {method_name}("]
        lines.append("        self,")
        lines.append("        validate: bool = True,")

        # Add parameters
        if params:
            lines.append("        *,")  # Force keyword-only arguments

            # Separate required and optional parameters
            required_params = []
            optional_params = []

            for param_name, param_info in params.items():
                param_type = param_info.get('type', 'string')

                # Use enhanced type generation that includes constraints and enums
                python_type = self.json_type_to_python(param_type, param_info)

                if param_info.get('required', False):
                    required_params.append((param_name, python_type, param_info))
                else:
                    optional_params.append((param_name, python_type, param_info))

            # Add required parameters first
            for param_name, python_type, param_info in required_params:
                # Handle reserved keywords
                safe_param_name = f"{param_name}_" if param_name in ['from', 'id', 'type', 'pass'] else param_name
                lines.append(f"        {safe_param_name}: {python_type},")

            # Add optional parameters
            for param_name, python_type, param_info in optional_params:
                # Handle reserved keywords
                safe_param_name = f"{param_name}_" if param_name in ['from', 'id', 'type', 'pass'] else param_name
                lines.append(f"        {safe_param_name}: Optional[{python_type}] = None,")

        lines.append("    ) -> Dict[str, Any]:")

        # Generate docstring
        description = method_info.get('description', f'Execute {method_name} operation')
        docstring_lines = ['        """' + description]

        if params:
            docstring_lines.append("")
            docstring_lines.append("        Args:")
            docstring_lines.append("            validate: Whether to validate parameters with Pydantic")

            for param_name, param_info in params.items():
                param_desc = param_info.get('description', 'No description')
                required = " (required)" if param_info.get('required', False) else ""
                # Handle reserved keywords in docstring
                safe_param_name = f"{param_name}_" if param_name in ['from', 'id', 'type', 'pass'] else param_name
                docstring_lines.append(f"            {safe_param_name}: {param_desc}{required}")

        # Add return information
        docstring_lines.append("")
        docstring_lines.append("        Returns:")
        returns_desc = method_info.get('returns', {}).get('description', 'API response')
        docstring_lines.append(f"            {returns_desc}")

        # Add notes about quirks if applicable
        quirks_notes = self.get_quirks_notes(method_name)
        if quirks_notes:
            docstring_lines.append("")
            docstring_lines.append("        Note:")
            for note in quirks_notes:
                docstring_lines.append(f"            {note}")

        docstring_lines.append('        """')
        docstring_lines.append("        ...")

        # Combine signature and docstring
        return '\n'.join(lines) + '\n' + '\n'.join(docstring_lines)

    def get_quirks_notes(self, method_name: str) -> List[str]:
        """Get notes about API quirks for a method."""
        notes = []

        # Known quirks from our implementation
        if method_name == 'getCDR':
            notes.extend([
                "Date range limited to 92 days",
                "Boolean parameters are converted to '1'/'0' strings",
                "Timezone defaults to '1' if not provided"
            ])
        elif method_name in ['getSMS', 'getMMS']:
            notes.append("Date parameters use 'from' and 'to' instead of 'date_from' and 'date_to'")
        elif method_name in ['orderDID', 'backOrderDIDUSA', 'backOrderDIDCAN']:
            notes.append("CNAM parameter is converted to '1'/'0' string")
        elif method_name == 'setVoicemail':
            notes.extend([
                "Boolean parameters like attach_message use 'yes'/'no' strings",
                "skip_password uses '1'/'0' string"
            ])
        elif method_name == 'setQueue':
            notes.extend([
                "None values for certain parameters convert to 'none' or 'unlimited'",
                "Boolean parameters use 'yes'/'no' strings"
            ])

        return notes

    def generate_stub_file(self) -> str:
        """Generate the complete stub file content."""
        lines = [
            '"""',
            'Type stubs for VoIP.ms Client',
            '',
            f'Generated from api_definition.json on {datetime.now().strftime("%Y-%m-%d")}',
            'DO NOT EDIT MANUALLY - This file is auto-generated',
            '"""',
            '',
            'from typing import Dict, Any, Optional, List, Union, Literal, Annotated',
            'from pathlib import Path',
            '',
            '',
            'class VoIPMSError(Exception):',
            '    """VoIP.ms API error"""',
            '    code: str',
            '    message: str',
            '    response: Optional[Dict[str, Any]]',
            '    def __init__(self, code: str, message: str, response: Optional[Dict[str, Any]] = None) -> None: ...',
            '',
            '',
            'class VoIPMSClient:',
            '    """Data-driven VoIP.ms client that dynamically creates methods from JSON definition."""',
            '    ',
            '    api_definition: Dict[str, Any]',
            '    username: Optional[str]',
            '    password: Optional[str]',
            '    base_url: str',
            '    timeout: float',
            '    max_retries: int',
            '    verify_ssl: bool',
            '    debug: bool',
            '    ',
            '    def __init__(',
            '        self,',
            '        api_definition_path: str = "api_definition.json",',
            '        username: Optional[str] = None,',
            '        password: Optional[str] = None,',
            '        base_url: Optional[str] = None,',
            '        timeout: float = 30.0,',
            '        max_retries: int = 3,',
            '        verify_ssl: bool = True,',
            '        debug: bool = False',
            '    ) -> None: ...',
            '    ',
            '    def close(self) -> None: ...',
            '    def __enter__(self) -> "VoIPMSClient": ...',
            '    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...',
            '    ',
            '    def get_available_methods(self) -> List[str]: ...',
            '    def get_method_info(self, method_name: str) -> Optional[Dict[str, Any]]: ...',
            '    def debug_method_params(self, op_name: str, **kwargs: Any) -> None: ...',
            '',
            '    # API Methods',
        ]

        # Generate all method signatures
        for method_name in sorted(self.operations.keys()):
            method_info = self.operations[method_name]
            signature = self.generate_method_signature(method_name, method_info)
            lines.append('')
            lines.append(signature)

        # Add async client
        lines.extend([
            '',
            '',
            'class VoIPMSClientAsync(VoIPMSClient):',
            '    """Asynchronous data-driven VoIP.ms client."""',
            '    ',
            '    async def __aenter__(self) -> "VoIPMSClientAsync": ...',
            '    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...',
            '    async def close(self) -> None: ...',
            '',
            '    # Async API Methods',
        ])

        # Generate async method signatures
        for method_name in sorted(self.operations.keys()):
            method_info = self.operations[method_name]
            # Generate async version
            signature = self.generate_method_signature(method_name, method_info)
            # Convert to async
            signature = signature.replace('    def ', '    async def ')
            lines.append('')
            lines.append(signature)

        lines.append('')
        return '\n'.join(lines)

    def generate_init_stub(self) -> str:
        """Generate __init__.pyi stub."""
        return '''"""VoIP.ms API Client Library"""

from .client import VoIPMSClient, VoIPMSClientAsync, VoIPMSError

__all__ = ["VoIPMSClient", "VoIPMSClientAsync", "VoIPMSError"]
__version__ = "1.0.0"
'''


def main():
    """Generate type stubs."""
    # Paths
    project_root = Path(__file__).parent.parent
    api_def_path = project_root / "src" / "voipms" / "api_definition.json"
    output_dir = project_root / "src" / "voipms"

    # Create generator
    generator = TypeStubGenerator(str(api_def_path))

    # Generate client.pyi
    client_stub = generator.generate_stub_file()
    client_stub_path = output_dir / "client.pyi"
    with open(client_stub_path, 'w') as f:
        f.write(client_stub)
    print(f"Generated {client_stub_path}")

    # Generate __init__.pyi
    init_stub = generator.generate_init_stub()
    init_stub_path = output_dir / "__init__.pyi"
    with open(init_stub_path, 'w') as f:
        f.write(init_stub)
    print(f"Generated {init_stub_path}")

    # Create py.typed marker
    py_typed_path = output_dir / "py.typed"
    py_typed_path.touch()
    print(f"Created {py_typed_path}")

    # Summary
    print(f"\nGenerated type stubs for {len(generator.operations)} methods")
    print("Type checking is now enabled for the VoIP.ms client!")


if __name__ == "__main__":
    main()
