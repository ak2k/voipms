#!/usr/bin/env python3
"""
Data-Driven VoIP.ms Client
Dynamically creates methods from JSON API definition
"""

import asyncio
import json
import logging
import os
from functools import wraps
from pathlib import Path
from typing import Annotated, Any, Dict, List, Optional, Type

import httpx
from pydantic import BaseModel, BeforeValidator, Field, ValidationError, create_model

from .error_codes import ERROR_CODES
from .types import boolean_01_validator, boolean_true_false_validator, boolean_yes_no_validator, numeric_string_validator

try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources

# Try to load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not installed, that's okay
    pass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Validator functions for string parameters with numeric constraints
def create_numeric_string_validator(minimum: Optional[float] = None, maximum: Optional[float] = None):
    """Create a validator for string parameters that should be numeric within constraints"""
    def validate_numeric_string(value: Any) -> str:
        if value is None:
            return value

        # Convert to string if not already
        str_value = str(value)

        # Try to parse as number for validation
        try:
            numeric_value = float(str_value)
        except ValueError:
            raise ValueError(f"Value must be numeric, got: {str_value}") from None

        # Check constraints
        if minimum is not None and numeric_value < minimum:
            raise ValueError(f"Value must be >= {minimum}, got: {numeric_value}")
        if maximum is not None and numeric_value > maximum:
            raise ValueError(f"Value must be <= {maximum}, got: {numeric_value}")

        # Return as string (as API expects)
        return str_value

    return validate_numeric_string


def create_integer_string_validator(minimum: Optional[int] = None, maximum: Optional[int] = None):
    """Create a validator for string parameters that should be integers within constraints"""
    def validate_integer_string(value: Any) -> str:
        if value is None:
            return value

        # Convert to string if not already
        str_value = str(value)

        # Try to parse as integer for validation
        try:
            int_value = int(float(str_value))  # Allow "60.0" -> 60
        except ValueError:
            raise ValueError(f"Value must be an integer, got: {str_value}") from None

        # Check constraints
        if minimum is not None and int_value < minimum:
            raise ValueError(f"Value must be >= {minimum}, got: {int_value}")
        if maximum is not None and int_value > maximum:
            raise ValueError(f"Value must be <= {maximum}, got: {int_value}")

        # Return as string representation of integer
        return str(int_value)

    return validate_integer_string


class VoIPMSError(Exception):
    """VoIP.ms API error"""
    def __init__(self, code: str, message: str, response: Optional[Dict[str, Any]] = None):
        self.code = code
        self.message = message
        self.response = response
        super().__init__(f"{code}: {message}")


class VoIPMSClient:
    """
    Data-driven VoIP.ms client that dynamically creates methods from JSON definition
    
    Example:
        >>> client = VoIPMSClient()
        >>> balance = client.getBalance()
        >>> print(f"Balance: ${balance['balance']['current_balance']}")
    """

    # Type mapping from API definition to Python/Pydantic types
    TYPE_MAP = {
        'string': str,
        'integer': int,
        'number': float,
        'boolean': bool,
        'array': List[Any],
        'object': Dict[str, Any]
    }

    def __init__(
        self,
        api_definition_path: str = "api_definition.json",
        username: Optional[str] = None,
        password: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        verify_ssl: bool = True,
        debug: bool = False
    ):
        """
        Initialize data-driven client.
        
        Args:
            api_definition_path: Path to JSON API definition
            username: API username (uses VOIPMS_USERNAME env var if not provided)
            password: API password (uses VOIPMS_PASSWORD env var if not provided)
            base_url: API base URL (uses definition default if not provided)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries
            verify_ssl: Whether to verify SSL certificates
            debug: Enable debug logging
        """
        # Load API definition
        self._load_api_definition(api_definition_path)

        # Configuration
        self.username = username or os.getenv("VOIPMS_USERNAME")
        self.password = password or os.getenv("VOIPMS_API_PASSWORD")
        self.base_url = base_url or self.api_definition.get("base_url", "https://voip.ms/api/v1/rest.php")
        self.timeout = timeout
        self.max_retries = max_retries
        self.verify_ssl = verify_ssl
        self.debug = debug

        # Validate credentials
        if not self.username or not self.password:
            raise ValueError(
                "VoIP.ms credentials required. Set VOIPMS_USERNAME and "
                "VOIPMS_PASSWORD environment variables or provide them as arguments."
            )

        # HTTP client
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            verify=self.verify_ssl,
            headers={"User-Agent": "VoIPMS-DataDriven/1.0"}
        )

        # Cache for Pydantic models
        self._model_cache: Dict[str, Type[BaseModel]] = {}

        # Dynamically create methods
        self._create_methods()

    def _load_api_definition(self, path: str):
        """Load API definition from JSON file"""
        # Try as direct path first
        if Path(path).exists():
            with open(path) as f:
                self.api_definition = json.load(f)
        else:
            # Try as package resource
            try:
                # Try to load from package resources
                import voipms
                if hasattr(resources, 'files'):
                    # Python 3.9+
                    package_files = resources.files(voipms)
                    resource_path = package_files / path
                    with resource_path.open('r') as f:
                        self.api_definition = json.load(f)
                else:
                    # Python 3.7-3.8
                    with resources.path(voipms, path) as resource_path:
                        with open(resource_path) as f:
                            self.api_definition = json.load(f)
            except Exception:
                # Try with default name
                try:
                    default_name = 'api_definition.json'
                    if hasattr(resources, 'files'):
                        package_files = resources.files(voipms)
                        resource_path = package_files / default_name
                        with resource_path.open('r') as f:
                            self.api_definition = json.load(f)
                    else:
                        with resources.path(voipms, default_name) as resource_path:
                            with open(resource_path) as f:
                                self.api_definition = json.load(f)
                except Exception:
                    raise FileNotFoundError(f"API definition not found: {path}") from None

        # Merge manually maintained error codes with auto-generated definition
        self.api_definition.setdefault('error_codes', {}).update(ERROR_CODES)

        logger.info(f"Loaded API definition with {len(self.api_definition.get('operations', {}))} operations and {len(self.api_definition.get('error_codes', {}))} error codes")

    def _create_methods(self):
        """Dynamically create methods from API definition"""
        operations = self.api_definition.get('operations', {})

        for op_name, op_spec in operations.items():
            # Create method name (camelCase to snake_case)
            method_name = self._to_snake_case(op_name)

            # Create the method
            method = self._create_method(op_name, op_spec)

            # Add to instance
            setattr(self, method_name, method)

            # Also add with original camelCase name for compatibility
            setattr(self, op_name, method)

    def _create_method(self, op_name: str, op_spec: Dict[str, Any]):
        """Create a method for an API operation"""
        @wraps(self._execute)
        def method(validate=True, **kwargs):
            if validate:
                # Get or create Pydantic model for this operation
                param_model = self._get_or_create_model(op_name, op_spec)

                try:
                    # Validate and coerce types using Pydantic
                    validated_params = param_model(**kwargs)
                    # Convert to dict, excluding None values
                    params_dict = validated_params.model_dump(exclude_none=True)
                except ValidationError as e:
                    # Format Pydantic errors into a more user-friendly message with constraint suggestions
                    errors = []
                    for error in e.errors():
                        field = error['loc'][0]
                        msg = error['msg']

                        # Add constraint suggestions based on parameter spec
                        param_spec = op_spec.get('parameters', {}).get(field, {})
                        constraint_hints = []

                        # Add enum suggestions
                        if enum_values := param_spec.get('enum'):
                            constraint_hints.append(f"valid options: {', '.join(enum_values)}")

                        # Add range suggestions
                        if 'minimum' in param_spec and 'maximum' in param_spec:
                            constraint_hints.append(f"range: {param_spec['minimum']}-{param_spec['maximum']}")
                        elif 'minimum' in param_spec:
                            constraint_hints.append(f"minimum: {param_spec['minimum']}")
                        elif 'maximum' in param_spec:
                            constraint_hints.append(f"maximum: {param_spec['maximum']}")

                        # Add length suggestions
                        if 'minLength' in param_spec:
                            constraint_hints.append(f"min length: {param_spec['minLength']}")
                        if 'maxLength' in param_spec:
                            constraint_hints.append(f"max length: {param_spec['maxLength']}")

                        # Add format suggestions
                        if format_info := param_spec.get('format'):
                            constraint_hints.append(f"format: {format_info}")

                        # Combine message with hints
                        error_msg = f"{field}: {msg}"
                        if constraint_hints:
                            error_msg += f" ({'; '.join(constraint_hints)})"

                        errors.append(error_msg)

                    raise ValueError(f"Parameter validation failed for {op_name}:\n  " + "\n  ".join(errors)) from None
            else:
                # Skip validation, use raw parameters
                params_dict = {k: v for k, v in kwargs.items() if v is not None}

            # Apply extracted HTML defaults before quirks
            params_dict = self._apply_html_defaults(op_name, params_dict)

            # Apply known API quirks/fixes
            params_dict = self._apply_api_quirks(op_name, params_dict)

            # Execute request with parameters (validated or raw)
            return self._execute(op_name, **params_dict)

        # Add documentation
        method.__name__ = op_name
        method.__doc__ = self._generate_method_doc(op_name, op_spec)

        return method

    def _apply_api_quirks(self, op_name: str, params_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Apply known API quirks and fixes"""
        # Known problematic methods and their fixes - based on comprehensive external library analysis
        quirks = {
            "getCDR": {
                # Add required defaults
                "defaults": {"timezone": "1"},
                # Date validation rules
                "date_validations": {"max_days": 92}
            },
            "getCallRecordings": {
                # Parameter name mapping (keep the correct ones)
                "aliases": {"from_date": "date_from", "to_date": "date_to"}
            },
            "getSMS": {
                "aliases": {"date_from": "from", "date_to": "to"}
            },
            "getMMS": {
                "aliases": {"date_from": "from", "date_to": "to"}
            },
            "setCallerIDFiltering": {
                "aliases": {"filter_id": "filter"}
            },
            # Account creation methods
            "createSubAccount": {
                "list_to_semicolon": ["allowed_codecs"]
            },
            # Voicemail methods
            "setVoicemail": {
                "yes_no_strings": ["attach_message", "delete_message", "say_time", "say_callerid"]
            },
            # Client management methods
            "setClient": {
                "aliases": {"zip_code": "zip"}
            },
            # Queue methods
            "setQueue": {
                "yes_no_strings": ["join_when_empty", "leave_when_empty", "ring_inuse"],
                "special_values": {
                    "join_announcement": {None: "none"},
                    "maximum_wait_time": {None: "unlimited", -1: "unlimited"},
                    "maximum_callers": {None: "unlimited", -1: "unlimited"}
                }
            },
            # Conference methods
            "setConferenceMember": {
                "yes_no_strings": ["admin", "start_muted", "announce_user_count"]
            },
            # Ring group methods
            "setRingGroup": {
                "list_to_semicolon": ["members"]
            },
            # Time condition methods
            "setTimeCondition": {
                "list_to_semicolon": ["routing_match", "routing_nomatch"]
            }
        }

        if op_name not in quirks:
            return params_dict

        method_quirks = quirks[op_name]
        result = params_dict.copy()
        params_dict.copy()

        # Apply yes/no string conversions
        for param in method_quirks.get("yes_no_strings", []):
            if param in result and isinstance(result[param], bool):
                old_value = result[param]
                result[param] = "yes" if result[param] else "no"
                if self.debug:
                    logger.debug(f"API quirk: {op_name}.{param}: {old_value} -> {result[param]}")

        # Apply list to semicolon-separated string conversions
        for param in method_quirks.get("list_to_semicolon", []):
            if param in result and isinstance(result[param], list):
                old_value = result[param]
                result[param] = ";".join(str(item) for item in result[param])
                if self.debug:
                    logger.debug(f"API quirk: {op_name}.{param}: {old_value} -> {result[param]}")

        # Apply special value handling (None → "none", etc.)
        for param, mapping in method_quirks.get("special_values", {}).items():
            if param in result and result[param] in mapping:
                old_value = result[param]
                result[param] = mapping[old_value]
                if self.debug:
                    logger.debug(f"API quirk: {op_name}.{param}: {old_value} -> {result[param]}")

        # Apply date validations for methods that need them
        if "date_validations" in method_quirks:
            date_fields = method_quirks["date_validations"]
            if "date_from" in result and "date_to" in result:
                try:
                    from datetime import datetime
                    date_from = datetime.strptime(result["date_from"], "%Y-%m-%d")
                    date_to = datetime.strptime(result["date_to"], "%Y-%m-%d")

                    # Check date order
                    if date_from > date_to:
                        raise ValueError(f"{op_name}: date_from must be before or equal to date_to")

                    # Check future dates
                    if date_to > datetime.now():
                        raise ValueError(f"{op_name}: date_to cannot be in the future")

                    # Check date range
                    if "max_days" in date_fields:
                        days_diff = (date_to - date_from).days
                        if days_diff > date_fields["max_days"]:
                            raise ValueError(f"{op_name}: Date range cannot exceed {date_fields['max_days']} days (got {days_diff} days)")

                except ValueError as e:
                    if "strptime" in str(e):
                        pass  # Invalid date format, let API handle it
                    else:
                        raise

        # Apply parameter aliases
        for old_name, new_name in method_quirks.get("aliases", {}).items():
            if old_name in result:
                value = result.pop(old_name)
                result[new_name] = value
                if self.debug:
                    logger.debug(f"API quirk: {op_name} parameter {old_name} -> {new_name}")

        # Apply required defaults
        for param, default_value in method_quirks.get("defaults", {}).items():
            if param not in result:
                result[param] = default_value
                if self.debug:
                    logger.debug(f"API quirk: {op_name} added required default {param}={default_value}")

        return result

    def _apply_html_defaults(self, op_name: str, params_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Apply default values extracted from HTML documentation"""
        if op_name not in self.api_definition.get('operations', {}):
            return params_dict

        op_spec = self.api_definition['operations'][op_name]
        param_specs = op_spec.get('parameters', {})
        result = params_dict.copy()

        for param_name, param_spec in param_specs.items():
            # Skip if parameter is already provided
            if param_name in result:
                continue

            # Check if parameter has a default value from HTML
            default_value = param_spec.get('default')
            if default_value is not None:
                # Handle special default values
                if default_value == "Today":
                    from datetime import datetime
                    result[param_name] = datetime.now().strftime('%Y-%m-%d')
                    if self.debug:
                        logger.debug(f"HTML default: {op_name}.{param_name} = {result[param_name]} (today's date)")
                elif default_value == "50" and param_name in ['limit', 'count', 'records']:
                    # Numeric defaults for common pagination parameters
                    result[param_name] = int(default_value)
                    if self.debug:
                        logger.debug(f"HTML default: {op_name}.{param_name} = {result[param_name]}")
                elif isinstance(default_value, str) and default_value.isdigit():
                    # Convert numeric string defaults to appropriate type
                    param_type = param_spec.get('type', 'string')
                    if param_type == 'integer':
                        result[param_name] = int(default_value)
                    elif param_type == 'number':
                        result[param_name] = float(default_value)
                    else:
                        result[param_name] = default_value
                    if self.debug:
                        logger.debug(f"HTML default: {op_name}.{param_name} = {result[param_name]}")
                else:
                    # Use default value as-is
                    result[param_name] = default_value
                    if self.debug:
                        logger.debug(f"HTML default: {op_name}.{param_name} = {result[param_name]}")

        return result

    def debug_method_params(self, op_name: str, **kwargs) -> None:
        """Debug helper: show what parameters a method expects vs what you're providing"""
        if op_name not in self.api_definition.get('operations', {}):
            print(f"❌ Method '{op_name}' not found in API definition")
            return

        op_spec = self.api_definition['operations'][op_name]
        expected_params = op_spec.get('parameters', {})

        print(f"\n🔍 Debug info for {op_name}:")
        print(f"   Expected parameters ({len(expected_params)}):")
        for param_name, param_spec in expected_params.items():
            required = "✓" if param_spec.get('required') else " "
            param_type = param_spec.get('type', 'unknown')
            print(f"   {required} {param_name}: {param_type}")

        print(f"\n   Your parameters ({len(kwargs)}):")
        for param_name, value in kwargs.items():
            if param_name in expected_params:
                print(f"   ✓ {param_name}: {type(value).__name__} = {value}")
            else:
                print(f"   ❌ {param_name}: {type(value).__name__} = {value} (unexpected)")

        print("\n   Missing required parameters:")
        missing = []
        for param_name, param_spec in expected_params.items():
            if param_spec.get('required') and param_name not in kwargs:
                missing.append(param_name)

        if missing:
            for param in missing:
                print(f"   ❌ {param}")
        else:
            print("   ✓ None")

        # Show API quirks that would be applied
        after_quirks = self._apply_api_quirks(op_name, kwargs)
        if after_quirks != kwargs:
            print("\n   API quirks would transform:")
            for key, value in after_quirks.items():
                if key not in kwargs or kwargs[key] != value:
                    original = kwargs.get(key, '<added>')
                    print(f"   {key}: {original} -> {value}")

        # Show specific quirk types that would apply
        # Extract the quirks dict (same as in _apply_api_quirks)
        quirks = {
            "getCDR": {"defaults": {"timezone": "1"}},
            "setQueue": {
                "yes_no_strings": ["join_when_empty", "leave_when_empty", "ring_inuse"],
                "special_values": {
                    "join_announcement": {None: "none"},
                    "maximum_wait_time": {None: "unlimited", -1: "unlimited"},
                    "maximum_callers": {None: "unlimited", -1: "unlimited"}
                }
            },
            "createSubAccount": {"list_to_semicolon": ["allowed_codecs"]},
            "setRingGroup": {"list_to_semicolon": ["members"]},
            # Add a few more for debugging
        }

        if op_name in quirks:
            method_quirks = quirks[op_name]
            print(f"\n   Available quirks for {op_name}:")
            if "yes_no_strings" in method_quirks:
                print(f"   - Boolean→'yes'/'no': {method_quirks['yes_no_strings']}")
            if "aliases" in method_quirks:
                print(f"   - Parameter aliases: {method_quirks['aliases']}")
            if "defaults" in method_quirks:
                print(f"   - Auto-added defaults: {method_quirks['defaults']}")
            if "special_values" in method_quirks:
                print(f"   - Special value mappings: {method_quirks['special_values']}")
            if "list_to_semicolon" in method_quirks:
                print(f"   - List→semicolon conversion: {method_quirks['list_to_semicolon']}")

    def _generate_method_doc(self, op_name: str, op_spec: Dict[str, Any]) -> str:
        """Generate method documentation from spec"""
        doc_parts = [op_spec.get('description', f'Execute {op_name} operation')]

        # Add parameters
        params = op_spec.get('parameters', {})
        if params:
            doc_parts.append("\nParameters:")
            for param_name, param_spec in params.items():
                required = "*" if param_spec.get('required', False) else ""
                param_type = param_spec.get('type', 'string')
                description = param_spec.get('description', '')
                doc_parts.append(f"    {param_name}{required} ({param_type}): {description}")

        # Add returns
        returns = op_spec.get('returns', {})
        if returns:
            doc_parts.append(f"\nReturns:\n    {returns.get('description', 'API response')}")

        # Add errors
        errors = op_spec.get('errors', [])
        if errors:
            doc_parts.append(f"\nPossible errors: {', '.join(errors)}")

        return '\n'.join(doc_parts)


    def _execute(self, method: str, **params) -> Dict[str, Any]:
        """Execute API method"""
        # Note: None values already excluded by Pydantic model_dump(exclude_none=True)

        # Build payload
        payload = {
            "api_username": self.username,
            "api_password": self.password,
            "method": method,
            **params
        }

        if self.debug:
            logger.debug(f"Executing {method} with {len(params)} parameters")

        # Retry logic
        last_error = None
        for attempt in range(self.max_retries):
            try:
                response = self._client.get("", params=payload)
                response.raise_for_status()

                data = response.json()
                return self._handle_response(data, method)

            except httpx.HTTPError as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    if self.debug:
                        logger.debug(f"Retry {attempt + 1} for {method}")
                    continue

        raise last_error

    def _handle_response(self, data: Dict[str, Any], method: str) -> Dict[str, Any]:
        """Handle API response"""
        status = data.get("status")

        if status == "success":
            if self.debug:
                logger.debug(f"Method {method} succeeded")
            return data

        # Handle error
        error_code = status
        error_codes = self.api_definition.get('error_codes', {})
        error_info = error_codes.get(error_code, {})

        # Handle both string and dict error formats
        if isinstance(error_info, str):
            message = error_info
        elif isinstance(error_info, dict):
            message = error_info.get('message', f"API error: {error_code}")
        else:
            message = f"API error: {error_code}"

        raise VoIPMSError(error_code, message, data)

    def _to_snake_case(self, name: str) -> str:
        """Convert camelCase to snake_case"""
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def _get_or_create_model(self, op_name: str, op_spec: Dict[str, Any]) -> Type[BaseModel]:
        """Get or create a Pydantic model for operation parameters"""
        if op_name in self._model_cache:
            return self._model_cache[op_name]

        # Build field definitions
        fields = {}
        param_specs = op_spec.get('parameters', {})

        for param_name, param_spec in param_specs.items():
            # Get the Python type
            param_type = param_spec.get('type', 'string')
            python_type = self.TYPE_MAP.get(param_type, str)

            # Create field with validation
            field_kwargs = {
                'description': param_spec.get('description', ''),
            }

            # Add pattern validation if specified
            if pattern := param_spec.get('pattern'):
                field_kwargs['pattern'] = pattern

            # Add Pydantic constraints
            # String length constraints
            if 'minLength' in param_spec:
                field_kwargs['min_length'] = param_spec['minLength']
            if 'maxLength' in param_spec:
                field_kwargs['max_length'] = param_spec['maxLength']

            # Numeric constraints (for integer/number types)
            if param_type in ['integer', 'number']:
                if 'minimum' in param_spec:
                    field_kwargs['ge'] = param_spec['minimum']
                if 'maximum' in param_spec:
                    field_kwargs['le'] = param_spec['maximum']

            # For string parameters with numeric constraints, use BeforeValidator
            elif param_type == 'string' and ('minimum' in param_spec or 'maximum' in param_spec):
                # Create appropriate validator based on parameter characteristics
                minimum = param_spec.get('minimum')
                maximum = param_spec.get('maximum')

                # Determine if this should be integer or float validation
                # Use integer validation if min/max are integers and examples suggest integers
                examples = param_spec.get('examples', [])
                use_integer = (
                    isinstance(minimum, int) and isinstance(maximum, int) and
                    all(str(ex).replace('.', '').isdigit() for ex in examples if ex)
                )

                if use_integer:
                    validator = create_integer_string_validator(minimum, maximum)
                else:
                    validator = create_numeric_string_validator(minimum, maximum)

                # Use Annotated type with BeforeValidator
                python_type = Annotated[str, BeforeValidator(validator)]

                # Add constraint info to description for user guidance
                constraints = []
                if minimum is not None:
                    constraints.append(f"min: {minimum}")
                if maximum is not None:
                    constraints.append(f"max: {maximum}")
                if constraints:
                    constraint_text = f" ({', '.join(constraints)})"
                    if field_kwargs['description']:
                        field_kwargs['description'] += constraint_text
                    else:
                        field_kwargs['description'] = constraint_text.strip(" ()")

            # Add enum validation if specified
            if enum_values := param_spec.get('enum'):
                # For string enums, we can use Literal type for better validation
                if param_type == 'string' and all(isinstance(v, str) for v in enum_values):
                    from typing import Literal
                    # Check for boolean-like enums and add validators
                    if set(enum_values) == {'0', '1'} or set(enum_values) == {'1', '0'}:
                        # Use Literal type with BeforeValidator for conversions
                        python_type = Annotated[Literal[tuple(enum_values)], BeforeValidator(boolean_01_validator)]
                        field_kwargs['description'] = field_kwargs.get('description', '') + ' (accepts: true/false, yes/no, on/off, 0/1, boolean)'
                    elif set(enum_values) == {'true', 'false'} or set(enum_values) == {'false', 'true'}:
                        python_type = Annotated[Literal[tuple(enum_values)], BeforeValidator(boolean_true_false_validator)]
                        field_kwargs['description'] = field_kwargs.get('description', '') + ' (accepts: true/false, yes/no, on/off, 1/0, boolean)'
                    elif set(enum_values) == {'yes', 'no'} or set(enum_values) == {'no', 'yes'}:
                        python_type = Annotated[Literal[tuple(enum_values)], BeforeValidator(boolean_yes_no_validator)]
                        field_kwargs['description'] = field_kwargs.get('description', '') + ' (accepts: yes/no, true/false, on/off, 1/0, boolean)'
                    elif all(v.isdigit() for v in enum_values):
                        # For numeric string enums like ["1", "2", "3"], accept integers
                        python_type = Annotated[Literal[tuple(enum_values)], BeforeValidator(numeric_string_validator)]
                        field_kwargs['description'] = field_kwargs.get('description', '') + ' (accepts: numeric values)'
                    else:
                        python_type = Literal[tuple(enum_values)]

            # Set default based on required status
            if param_spec.get('required', False):
                field_kwargs['default'] = ...  # Required field
            else:
                field_kwargs['default'] = None
                python_type = Optional[python_type]

            fields[param_name] = (python_type, Field(**field_kwargs))

        # Create the model dynamically with configuration
        model = create_model(
            f'{op_name}Params',
            __base__=BaseModel,
            __config__={
                'extra': 'forbid',  # Don't allow extra fields
                'validate_assignment': True,
                'use_enum_values': True,
                'str_strip_whitespace': True,  # Auto-strip whitespace from strings
            },
            **fields
        )

        self._model_cache[op_name] = model
        return model

    def close(self):
        """Close HTTP client"""
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_available_methods(self) -> List[str]:
        """Get list of available API methods"""
        return list(self.api_definition.get('operations', {}).keys())

    def get_method_info(self, method_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific method"""
        return self.api_definition.get('operations', {}).get(method_name)


class VoIPMSClientAsync(VoIPMSClient):
    """
    Asynchronous data-driven VoIP.ms client
    
    Example:
        >>> async with VoIPMSClientAsync() as client:
        ...     balance = await client.getBalance()
        ...     print(f"Balance: ${balance['balance']['current_balance']}")
    """

    def __init__(self, *args, **kwargs):
        # Don't create sync client in parent __init__
        self._init_args = args
        self._init_kwargs = kwargs
        self._initialized = False

    async def __aenter__(self):
        # Initialize in async context
        await self._async_init()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def _async_init(self):
        """Async initialization"""
        if self._initialized:
            return

        # Load API definition
        api_definition_path = self._init_kwargs.get('api_definition_path', 'api_definition.json')
        self._load_api_definition(api_definition_path)

        # Set attributes
        self.username = self._init_kwargs.get('username') or os.getenv("VOIPMS_USERNAME")
        self.password = self._init_kwargs.get('password') or os.getenv("VOIPMS_API_PASSWORD")
        self.base_url = self._init_kwargs.get('base_url') or self.api_definition.get("base_url")
        self.timeout = self._init_kwargs.get('timeout', 30.0)
        self.max_retries = self._init_kwargs.get('max_retries', 3)
        self.verify_ssl = self._init_kwargs.get('verify_ssl', True)
        self.debug = self._init_kwargs.get('debug', False)

        # Validate
        if not self.username or not self.password:
            raise ValueError("VoIP.ms credentials required")

        # Create async client
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            verify=self.verify_ssl,
            headers={"User-Agent": "VoIPMS-DataDriven-Async/1.0"}
        )

        # Initialize model cache
        self._model_cache: Dict[str, Type[BaseModel]] = {}

        # Create async methods
        self._create_async_methods()
        self._initialized = True

    def _create_async_methods(self):
        """Create async methods from API definition"""
        operations = self.api_definition.get('operations', {})

        for op_name, op_spec in operations.items():
            # Create method name
            method_name = self._to_snake_case(op_name)

            # Create async method
            method = self._create_async_method(op_name, op_spec)

            # Add to instance
            setattr(self, method_name, method)
            setattr(self, op_name, method)

    def _create_async_method(self, op_name: str, op_spec: Dict[str, Any]):
        """Create an async method for an API operation"""
        async def method(validate=True, **kwargs):
            # Ensure initialized
            await self._async_init()

            if validate:
                # Get or create Pydantic model for this operation
                param_model = self._get_or_create_model(op_name, op_spec)

                try:
                    # Validate and coerce types using Pydantic
                    validated_params = param_model(**kwargs)
                    # Convert to dict, excluding None values
                    params_dict = validated_params.model_dump(exclude_none=True)
                except ValidationError as e:
                    # Format Pydantic errors into a more user-friendly message with constraint suggestions
                    errors = []
                    for error in e.errors():
                        field = error['loc'][0]
                        msg = error['msg']

                        # Add constraint suggestions based on parameter spec
                        param_spec = op_spec.get('parameters', {}).get(field, {})
                        constraint_hints = []

                        # Add enum suggestions
                        if enum_values := param_spec.get('enum'):
                            constraint_hints.append(f"valid options: {', '.join(enum_values)}")

                        # Add range suggestions
                        if 'minimum' in param_spec and 'maximum' in param_spec:
                            constraint_hints.append(f"range: {param_spec['minimum']}-{param_spec['maximum']}")
                        elif 'minimum' in param_spec:
                            constraint_hints.append(f"minimum: {param_spec['minimum']}")
                        elif 'maximum' in param_spec:
                            constraint_hints.append(f"maximum: {param_spec['maximum']}")

                        # Add length suggestions
                        if 'minLength' in param_spec:
                            constraint_hints.append(f"min length: {param_spec['minLength']}")
                        if 'maxLength' in param_spec:
                            constraint_hints.append(f"max length: {param_spec['maxLength']}")

                        # Add format suggestions
                        if format_info := param_spec.get('format'):
                            constraint_hints.append(f"format: {format_info}")

                        # Combine message with hints
                        error_msg = f"{field}: {msg}"
                        if constraint_hints:
                            error_msg += f" ({'; '.join(constraint_hints)})"

                        errors.append(error_msg)

                    raise ValueError(f"Parameter validation failed for {op_name}:\n  " + "\n  ".join(errors)) from None
            else:
                # Skip validation, use raw parameters
                params_dict = {k: v for k, v in kwargs.items() if v is not None}

            # Apply extracted HTML defaults before quirks
            params_dict = self._apply_html_defaults(op_name, params_dict)

            # Apply known API quirks/fixes
            params_dict = self._apply_api_quirks(op_name, params_dict)

            # Execute request with parameters (validated or raw)
            return await self._async_execute(op_name, **params_dict)

        # Add documentation
        method.__name__ = op_name
        method.__doc__ = self._generate_method_doc(op_name, op_spec)

        return method

    async def _async_execute(self, method: str, **params) -> Dict[str, Any]:
        """Execute API method asynchronously"""
        # Note: None values already excluded by Pydantic model_dump(exclude_none=True)

        # Build payload
        payload = {
            "api_username": self.username,
            "api_password": self.password,
            "method": method,
            **params
        }

        if self.debug:
            logger.debug(f"Executing {method} with {len(params)} parameters")

        # Retry logic
        last_error = None
        for attempt in range(self.max_retries):
            try:
                response = await self._client.get("", params=payload)
                response.raise_for_status()

                data = response.json()
                return self._handle_response(data, method)

            except httpx.HTTPError as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    if self.debug:
                        logger.debug(f"Retry {attempt + 1} for {method}")
                    continue

        raise last_error

    async def close(self):
        """Close async HTTP client"""
        if hasattr(self, '_client'):
            await self._client.aclose()


if __name__ == "__main__":
    # Example usage
    print("Data-Driven VoIP.ms Client Example\n")

    # Synchronous example
    try:
        with VoIPMSClient() as client:
            print("Available methods:", len(client.get_available_methods()))
            print("\nSample methods:")
            for method in list(client.get_available_methods())[:5]:
                print(f"  - {method}")

    except Exception as e:
        print(f"Note: {e}")
        print("Set VOIPMS_USERNAME and VOIPMS_PASSWORD environment variables to test")

    # Async example
    async def async_example():
        try:
            async with VoIPMSClientAsync() as client:
                methods = await client.get_available_methods()
                print(f"\nAsync client has {len(methods)} methods available")
        except Exception as e:
            print(f"Async example: {e}")

    # Run async example
    asyncio.run(async_example())
