#!/usr/bin/env python3
"""
Data-Driven VoIP.ms Client
Dynamically creates methods from JSON API definition
"""

import json
import os
from typing import Dict, Any, Optional, Union, List
from pathlib import Path
import httpx
import logging
from functools import wraps
from datetime import datetime
import asyncio
import pkg_resources

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoIPMSError(Exception):
    """VoIP.ms API error"""
    def __init__(self, code: str, message: str, response: Optional[Dict[str, Any]] = None):
        self.code = code
        self.message = message
        self.response = response
        super().__init__(f"{code}: {message}")


class DataDrivenVoIPMSClient:
    """
    Data-driven VoIP.ms client that dynamically creates methods from JSON definition
    
    Example:
        >>> client = DataDrivenVoIPMSClient()
        >>> balance = client.getBalance()
        >>> print(f"Balance: ${balance['balance']['current_balance']}")
    """
    
    def __init__(
        self,
        api_definition_path: str = "voipms_api.json",
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
        self.password = password or os.getenv("VOIPMS_PASSWORD")
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
        
        # Dynamically create methods
        self._create_methods()
        
    def _load_api_definition(self, path: str):
        """Load API definition from JSON file"""
        # Try as direct path first
        if Path(path).exists():
            with open(path, 'r') as f:
                self.api_definition = json.load(f)
        else:
            # Try as package resource
            try:
                resource_path = pkg_resources.resource_filename('voipms', path)
                with open(resource_path, 'r') as f:
                    self.api_definition = json.load(f)
            except:
                # Try with default name as package resource
                try:
                    resource_path = pkg_resources.resource_filename('voipms', 'voipms_api_enriched.json')
                    with open(resource_path, 'r') as f:
                        self.api_definition = json.load(f)
                except:
                    raise FileNotFoundError(f"API definition not found: {path}")
            
        logger.info(f"Loaded API definition with {len(self.api_definition.get('operations', {}))} operations")
        
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
        def method(**kwargs):
            # Validate parameters
            self._validate_parameters(op_name, op_spec, kwargs)
            
            # Execute request
            return self._execute(op_name, **kwargs)
            
        # Add documentation
        method.__name__ = op_name
        method.__doc__ = self._generate_method_doc(op_name, op_spec)
        
        return method
        
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
        
    def _validate_parameters(self, op_name: str, op_spec: Dict[str, Any], provided_params: Dict[str, Any]):
        """Validate provided parameters against specification"""
        param_specs = op_spec.get('parameters', {})
        
        # Check required parameters
        for param_name, param_spec in param_specs.items():
            if param_spec.get('required', False) and param_name not in provided_params:
                raise ValueError(f"Missing required parameter '{param_name}' for {op_name}")
                
        # Validate parameter types
        for param_name, param_value in provided_params.items():
            if param_name in param_specs:
                param_spec = param_specs[param_name]
                expected_type = param_spec.get('type', 'string')
                
                if not self._validate_type(param_value, expected_type):
                    raise TypeError(
                        f"Parameter '{param_name}' should be {expected_type}, "
                        f"got {type(param_value).__name__}"
                    )
                    
                # Validate patterns
                pattern = param_spec.get('pattern')
                if pattern and isinstance(param_value, str):
                    import re
                    if not re.match(pattern, param_value):
                        raise ValueError(
                            f"Parameter '{param_name}' value '{param_value}' "
                            f"does not match pattern '{pattern}'"
                        )
                        
    def _validate_type(self, value: Any, expected_type: str) -> bool:
        """Validate value matches expected type"""
        type_mapping = {
            'string': str,
            'integer': int,
            'number': (int, float),
            'boolean': bool,
            'array': list,
            'object': dict
        }
        
        expected_python_type = type_mapping.get(expected_type, str)
        return isinstance(value, expected_python_type)
        
    def _execute(self, method: str, **params) -> Dict[str, Any]:
        """Execute API method"""
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
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
                response = self._client.post("", data=payload)
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
        
        message = error_info.get('message', f"API error: {error_code}")
        raise VoIPMSError(error_code, message, data)
        
    def _to_snake_case(self, name: str) -> str:
        """Convert camelCase to snake_case"""
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
        
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


class AsyncDataDrivenVoIPMSClient(DataDrivenVoIPMSClient):
    """
    Asynchronous data-driven VoIP.ms client
    
    Example:
        >>> async with AsyncDataDrivenVoIPMSClient() as client:
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
        api_definition_path = self._init_kwargs.get('api_definition_path', 'voipms_api.json')
        self._load_api_definition(api_definition_path)
        
        # Set attributes
        self.username = self._init_kwargs.get('username') or os.getenv("VOIPMS_USERNAME")
        self.password = self._init_kwargs.get('password') or os.getenv("VOIPMS_PASSWORD")
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
        async def method(**kwargs):
            # Ensure initialized
            await self._async_init()
            
            # Validate parameters
            self._validate_parameters(op_name, op_spec, kwargs)
            
            # Execute request
            return await self._async_execute(op_name, **kwargs)
            
        # Add documentation
        method.__name__ = op_name
        method.__doc__ = self._generate_method_doc(op_name, op_spec)
        
        return method
        
    async def _async_execute(self, method: str, **params) -> Dict[str, Any]:
        """Execute API method asynchronously"""
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
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
                response = await self._client.post("", data=payload)
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
        with DataDrivenVoIPMSClient() as client:
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
            async with AsyncDataDrivenVoIPMSClient() as client:
                methods = await client.get_available_methods()
                print(f"\nAsync client has {len(methods)} methods available")
        except Exception as e:
            print(f"Async example: {e}")
            
    # Run async example
    asyncio.run(async_example())