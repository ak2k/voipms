#!/usr/bin/env python3
"""
Generate Type Stubs for VoIP.ms Client

This script generates .pyi stub files from api_definition.json to enable
IDE autocomplete, type checking, and better developer experience.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class TypeStubGenerator:
    """Generate Python type stubs from API definition."""

    def __init__(self, api_definition_path: str):
        """Initialize with path to API definition."""
        with open(api_definition_path) as f:
            self.api_definition = json.load(f)
        self.operations = self.api_definition.get("operations", {})

    def json_type_to_python(self, json_type: str, param_info: dict[str, Any] = None) -> str:
        """Convert JSON type to Python type hint, with constraint annotations."""
        if param_info is None:
            param_info = {}

        base_type_map = {
            "string": "str",
            "integer": "int",
            "number": "float",
            "boolean": "bool",
            "array": "list[Any]",
            "object": "dict[str, Any]",
        }

        base_type = base_type_map.get(json_type, "Any")

        # Check for enum values first
        if enum_values := param_info.get("enum"):
            if all(isinstance(v, str) for v in enum_values):
                values = ", ".join(f'"{v}"' for v in enum_values)
                return f"Literal[{values}]"

        # For string types with numeric constraints, add constraint annotation
        if json_type == "string":
            constraints = []

            # Add range constraints
            if "minimum" in param_info and "maximum" in param_info:
                constraints.append(f"Range: {param_info['minimum']}-{param_info['maximum']}")
            elif "minimum" in param_info:
                constraints.append(f"Min: {param_info['minimum']}")
            elif "maximum" in param_info:
                constraints.append(f"Max: {param_info['maximum']}")

            # Add length constraints
            if "minLength" in param_info:
                constraints.append(f"MinLength: {param_info['minLength']}")
            if "maxLength" in param_info:
                constraints.append(f"MaxLength: {param_info['maxLength']}")

            # Add format constraints
            if format_info := param_info.get("format"):
                constraints.append(f"Format: {format_info}")

            # Add units
            if units := param_info.get("units"):
                constraints.append(f"Units: {units}")

            # Create annotated type if we have constraints
            if constraints:
                constraint_str = "; ".join(constraints)
                return f'Annotated[str, "{constraint_str}"]'

        # For numeric types with constraints
        elif json_type in ["integer", "number"]:
            constraints = []
            if "minimum" in param_info:
                constraints.append(f"Min: {param_info['minimum']}")
            if "maximum" in param_info:
                constraints.append(f"Max: {param_info['maximum']}")

            if constraints:
                constraint_str = "; ".join(constraints)
                return f'Annotated[{base_type}, "{constraint_str}"]'

        return base_type

    def get_literal_values(self, param_name: str, param_info: dict[str, Any]) -> str | None:
        """Extract literal type values from description if applicable."""
        # Check if parameter has enum values from API definition
        if "enum" in param_info:
            enum_values = param_info["enum"]
            # Create Literal type for enum values
            if all(isinstance(v, str) for v in enum_values):
                values = ", ".join(f'"{v}"' for v in enum_values)
                return f"Literal[{values}]"

        # Common patterns for literal types (for backward compatibility)
        literal_params = {
            "calltype": ["inbound", "outbound"],
            "billing_type": ["1", "2"],  # 1=PerMinute, 2=Flat
            "protocol": ["sip", "iax2"],
            "language": ["en", "es", "fr"],
            "device_type": ["1", "2", "3", "4", "5"],  # Various device types
        }

        if param_name in literal_params:
            values = ", ".join(f'"{v}"' for v in literal_params[param_name])
            return f"Literal[{values}]"

        return None

    def generate_method_signature(self, method_name: str, method_info: dict[str, Any]) -> str:
        """Generate a single method signature."""
        params = method_info.get("parameters", {})

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
                param_type = param_info.get("type", "string")

                # Use enhanced type generation that includes constraints and enums
                python_type = self.json_type_to_python(param_type, param_info)

                if param_info.get("required", False):
                    required_params.append((param_name, python_type, param_info))
                else:
                    optional_params.append((param_name, python_type, param_info))

            # Add required parameters first
            for param_name, python_type, _ in required_params:
                # Handle reserved keywords
                safe_param_name = (
                    f"{param_name}_" if param_name in ["from", "id", "type", "pass"] else param_name
                )
                lines.append(f"        {safe_param_name}: {python_type},")

            # Add optional parameters
            for param_name, python_type, _ in optional_params:
                # Handle reserved keywords
                safe_param_name = (
                    f"{param_name}_" if param_name in ["from", "id", "type", "pass"] else param_name
                )
                lines.append(f"        {safe_param_name}: {python_type} | None = None,")

        lines.append("    ) -> dict[str, Any]:")

        # Generate docstring
        description = method_info.get("description", f"Execute {method_name} operation")
        docstring_lines = ['        """' + description]

        if params:
            docstring_lines.append("")
            docstring_lines.append("        Args:")
            docstring_lines.append(
                "            validate: Whether to validate parameters with Pydantic"
            )

            for param_name, param_info in params.items():
                param_desc = param_info.get("description", "No description")
                required = " (required)" if param_info.get("required", False) else ""

                # Add note about boolean acceptance for boolean-like enums
                enum_values = param_info.get("enum", [])
                if set(enum_values) in [{"0", "1"}, {"1", "0"}]:
                    param_desc += " (accepts: true/false, yes/no, on/off, 0/1, boolean)"
                elif set(enum_values) in [{"true", "false"}, {"false", "true"}]:
                    param_desc += " (accepts: true/false, yes/no, on/off, 1/0, boolean)"
                elif set(enum_values) in [{"yes", "no"}, {"no", "yes"}]:
                    param_desc += " (accepts: yes/no, true/false, on/off, 1/0, boolean)"

                # Handle reserved keywords in docstring
                safe_param_name = (
                    f"{param_name}_" if param_name in ["from", "id", "type", "pass"] else param_name
                )
                docstring_lines.append(f"            {safe_param_name}: {param_desc}{required}")

        # Add return information
        docstring_lines.append("")
        docstring_lines.append("        Returns:")
        returns_desc = method_info.get("returns", {}).get("description", "API response")
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
        return "\n".join(lines) + "\n" + "\n".join(docstring_lines)

    def get_quirks_notes(self, method_name: str) -> list[str]:
        """Get notes about API quirks for a method."""
        notes = []

        # Known quirks from our implementation
        if method_name == "getCDR":
            notes.extend(
                [
                    "Date range limited to 92 days",
                    "Boolean parameters are converted to '1'/'0' strings",
                    "Timezone defaults to '1' if not provided",
                ]
            )
        elif method_name in ["getSMS", "getMMS"]:
            notes.append("Date parameters use 'from' and 'to' instead of 'date_from' and 'date_to'")
        elif method_name in ["orderDID", "backOrderDIDUSA", "backOrderDIDCAN"]:
            notes.append("CNAM parameter is converted to '1'/'0' string")
        elif method_name == "setVoicemail":
            notes.extend(
                [
                    "Boolean parameters like attach_message use 'yes'/'no' strings",
                    "skip_password uses '1'/'0' string",
                ]
            )
        elif method_name == "setQueue":
            notes.extend(
                [
                    "None values for certain parameters convert to 'none' or 'unlimited'",
                    "Boolean parameters use 'yes'/'no' strings",
                ]
            )

        return notes

    def generate_client_stub(self) -> str:
        """Generate client.pyi stub file content."""
        lines = [
            '"""',
            "Type stubs for VoIP.ms Client",
            "",
            f'Generated on {datetime.now().strftime("%Y-%m-%d")}',
            "DO NOT EDIT MANUALLY - This file is auto-generated",
            '"""',
            "",
            "from contextlib import contextmanager",
            "from typing import Any, Generator, Union, Literal, Annotated",
            "from .config import VoIPMSConfig",
            "",
            "",
            "class VoIPMSService:",
            '    """Synchronous VoIP.ms service that creates methods from JSON API definition."""',
            "    ",
            "    api_definition: dict[str, Any]",
            "    config: VoIPMSConfig",
            "    username: str",
            "    password: str",
            "    base_url: str",
            "    timeout: float",
            "    max_retries: int",
            "    verify_ssl: bool",
            "    debug: bool",
            "    enable_retries: bool",
            "    ",
            "    def __init__(",
            "        self,",
            "        http_client: Any,",  # Using Any to avoid httpx import
            "        config: VoIPMSConfig,",
            "        api_definition: dict[str, Any]",
            "    ) -> None: ...",
            "    ",
            "    def is_healthy(self) -> bool: ...",
            "    def test_connectivity(self) -> bool: ...",
            "    def get_available_methods(self) -> list[str]: ...",
            "    def get_method_info(self, method_name: str) -> dict[str, Any] | None: ...",
            "    def debug_method_params(self, op_name: str, **kwargs: Any) -> None: ...",
            "",
            "    # API Methods",
        ]

        # Generate all method signatures
        for method_name in sorted(self.operations.keys()):
            method_info = self.operations[method_name]
            signature = self.generate_method_signature(method_name, method_info)
            lines.append("")
            lines.append(signature)

        # Add the factory function
        lines.extend(
            [
                "",
                "",
                "@contextmanager",
                "def VoIPMSClient(",
                "    config: VoIPMSConfig | None = None,",
                "    **kwargs: Any",
                ") -> Generator[VoIPMSService, None, None]: ...",
                "",
            ]
        )

        return "\n".join(lines)

    def generate_async_client_stub(self) -> str:
        """Generate async_client.pyi stub file content."""
        lines = [
            '"""',
            "Type stubs for VoIP.ms Async Client",
            "",
            f'Generated on {datetime.now().strftime("%Y-%m-%d")}',
            "DO NOT EDIT MANUALLY - This file is auto-generated",
            '"""',
            "",
            "from contextlib import asynccontextmanager",
            "from typing import Any, AsyncGenerator, Union, Literal, Annotated",
            "from .config import VoIPMSConfig",
            "",
            "",
            "class VoIPMSAsyncService:",
            '    """Pure async service for VoIP.ms API calls."""',
            "    ",
            "    api_definition: dict[str, Any]",
            "    config: VoIPMSConfig",
            "    username: str",
            "    password: str",
            "    base_url: str",
            "    timeout: float",
            "    max_retries: int",
            "    verify_ssl: bool",
            "    debug: bool",
            "    enable_retries: bool",
            "    ",
            "    def is_healthy(self) -> bool: ...",
            "    async def test_connectivity(self) -> bool: ...",
            "    def get_available_methods(self) -> list[str]: ...",
            "    def get_method_info(self, method_name: str) -> dict[str, Any] | None: ...",
            "    def debug_method_params(self, op_name: str, **kwargs: Any) -> None: ...",
            "    ",
            "    # API Methods (async versions)",
        ]

        # Generate all async method signatures
        for method_name in sorted(self.operations.keys()):
            method_info = self.operations[method_name]
            # Generate async version
            signature = self.generate_method_signature(method_name, method_info)
            # Convert to async
            signature = signature.replace("    def ", "    async def ")
            lines.append("")
            lines.append(signature)

        # Add the factory function
        lines.extend(
            [
                "",
                "",
                "@asynccontextmanager",
                "async def VoIPMSAsyncClient(",
                "    config: VoIPMSConfig | None = None,",
                "    **kwargs: Any",
                ") -> AsyncGenerator[VoIPMSAsyncService, None]: ...",
                "",
            ]
        )

        return "\n".join(lines)

    def generate_init_stub(self) -> str:
        """Generate __init__.pyi stub."""
        return '''"""
VoIP.ms Python Client

Type stubs for the VoIP.ms API client package.
"""

from .async_client import VoIPMSAsyncClient as VoIPMSAsyncClient, VoIPMSAsyncService as VoIPMSAsyncService
from .client import VoIPMSClient as VoIPMSClient, VoIPMSService as VoIPMSService
from .config import VoIPMSConfig as VoIPMSConfig
from .exceptions import VoIPMSError as VoIPMSError

__version__: str
__all__: list[str]
'''


def generate_stubs(api_def_path: str, output_dir: str):
    """Generate type stubs from API definition."""
    # Create generator
    generator = TypeStubGenerator(api_def_path)

    # Convert to Path objects
    output_dir = Path(output_dir)

    # Generate client.pyi
    client_stub = generator.generate_client_stub()
    client_stub_path = output_dir / "client.pyi"
    with open(client_stub_path, "w") as f:
        f.write(client_stub)
    print(f"Generated {client_stub_path}")

    # Generate async_client.pyi
    async_client_stub = generator.generate_async_client_stub()
    async_client_stub_path = output_dir / "async_client.pyi"
    with open(async_client_stub_path, "w") as f:
        f.write(async_client_stub)
    print(f"Generated {async_client_stub_path}")

    # Generate __init__.pyi
    init_stub = generator.generate_init_stub()
    init_stub_path = output_dir / "__init__.pyi"
    with open(init_stub_path, "w") as f:
        f.write(init_stub)
    print(f"Generated {init_stub_path}")

    # Create py.typed marker
    py_typed_path = output_dir / "py.typed"
    py_typed_path.touch()
    print(f"Created {py_typed_path}")

    # Summary
    print(f"\nGenerated type stubs for {len(generator.operations)} methods")
    print("Type checking is now enabled for the VoIP.ms client!")


def main():
    """Generate type stubs."""
    # Paths
    project_root = Path(__file__).parent.parent
    api_def_path = project_root / "src" / "voipms" / "api_definition.json"
    output_dir = project_root / "src" / "voipms"

    generate_stubs(str(api_def_path), str(output_dir))


if __name__ == "__main__":
    main()
