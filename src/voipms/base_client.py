"""
Base client with shared functionality for sync and async VoIP.ms clients.
"""

import json
import logging
import os
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import httpx

from .api_quirks import APIQuirksHandler

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

logger = logging.getLogger(__name__)


class VoIPMSError(Exception):
    """VoIP.ms API error"""
    def __init__(self, code: str, message: str, response: Optional[Dict[str, Any]] = None):
        self.code = code
        self.message = message
        self.response = response
        super().__init__(f"{code}: {message}")


class BaseVoIPMSClient(ABC):
    """
    Base class for VoIP.ms clients with shared functionality.
    """

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        verify_ssl: bool = True,
        debug: bool = False,
        api_definition_path: str = 'api_definition.json'
    ):
        """
        Initialize base VoIP.ms client
        
        Args:
            username: VoIP.ms API username (or use VOIPMS_USERNAME env var)
            password: VoIP.ms API password (or use VOIPMS_API_PASSWORD env var)
            base_url: API base URL (defaults to value from API definition)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            verify_ssl: Whether to verify SSL certificates
            debug: Enable debug logging
            api_definition_path: Path to API definition JSON file
        """
        # Set debug early for use in _load_api_definition
        self.debug = debug
        
        # Load API definition
        self._load_api_definition(api_definition_path)

        # Configuration
        self.username = username or os.getenv("VOIPMS_USERNAME")
        self.password = password or os.getenv("VOIPMS_API_PASSWORD")
        self.base_url = base_url or self.api_definition.get("base_url", "https://voip.ms/api/v1/rest.php")
        self.timeout = timeout
        self.max_retries = max_retries
        self.verify_ssl = verify_ssl

        # Validate credentials
        if not self.username or not self.password:
            raise ValueError(
                "VoIP.ms credentials required. Set VOIPMS_USERNAME and "
                "VOIPMS_API_PASSWORD environment variables or provide them as arguments."
            )

        # Will be set by subclasses
        self._client = None
        self._method_factory = None

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

        # Load quirks handler (temporarily) to get additional error codes
        quirks_handler = APIQuirksHandler(debug=self.debug)
        if error_additions := quirks_handler.quirks_config.get('error_code_additions', {}):
            # Merge additional error codes into API definition
            for error_id, error_info in error_additions.items():
                self.api_definition.setdefault('error_codes', {})[error_id] = error_info['message']

        logger.info(f"Loaded API definition with {len(self.api_definition.get('operations', {}))} operations and {len(self.api_definition.get('error_codes', {}))} error codes")

    def _create_http_client(self, client_class: type, user_agent: str) -> Union[httpx.Client, httpx.AsyncClient]:
        """Create HTTP client with common configuration"""
        return client_class(
            base_url=self.base_url,
            timeout=self.timeout,
            verify=self.verify_ssl,
            headers={"User-Agent": user_agent}
        )

    def _build_payload(self, method: str, **params) -> Dict[str, Any]:
        """Build API request payload"""
        return {
            "api_username": self.username,
            "api_password": self.password,
            "method": method,
            **params
        }

    def _handle_response(self, data: Dict[str, Any], method: str) -> Dict[str, Any]:
        """Handle API response"""
        status = data.get("status")

        if status == "success":
            if self.debug:
                logger.debug(f"Method {method} succeeded")
            return data

        # Handle error
        error_code = status
        error_messages = []

        # Get base error message
        if error_code in self.api_definition.get('error_codes', {}):
            # Error codes are stored as strings in the API definition
            base_message = self.api_definition['error_codes'][error_code]
            error_messages.append(base_message)
        else:
            error_messages.append(f"Unknown error code: {error_code}")

        error_message = " | ".join(error_messages)
        raise VoIPMSError(error_code, error_message, data)

    def _to_snake_case(self, name: str) -> str:
        """Convert camelCase to snake_case"""
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def _create_methods_from_definition(self):
        """Create methods from API definition"""
        operations = self.api_definition.get('operations', {})

        for op_name, op_spec in operations.items():
            # Create method name (camelCase to snake_case)
            method_name = self._to_snake_case(op_name)

            # Create the method using factory
            method = self._method_factory.create_method(op_name, op_spec)

            # Add to instance
            setattr(self, method_name, method)

            # Also add with original camelCase name for compatibility
            setattr(self, op_name, method)

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
        quirks_handler = self._method_factory.quirks_handler
        after_quirks = quirks_handler.apply_quirks(op_name, kwargs)
        if after_quirks != kwargs:
            print("\n   API quirks would transform:")
            for key, value in after_quirks.items():
                if key not in kwargs or kwargs[key] != value:
                    original = kwargs.get(key, '<added>')
                    print(f"   {key}: {original} -> {value}")

    def get_available_methods(self) -> List[str]:
        """Get list of available API methods"""
        return list(self.api_definition.get('operations', {}).keys())

    def get_method_info(self, method_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific method"""
        return self.api_definition.get('operations', {}).get(method_name)

    @abstractmethod
    def close(self):
        """Close HTTP client - must be implemented by subclasses"""
        pass