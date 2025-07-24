#!/usr/bin/env python3
"""
Data-Driven VoIP.ms Client
Dynamically creates methods from JSON API definition
"""

import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Generator, Optional

import httpx

from .base_client import BaseVoIPMSClient, load_api_definition
from .config import VoIPMSConfig
from .method_factory import MethodFactory

logger = logging.getLogger(__name__)


class VoIPMSService(BaseVoIPMSClient):
    """
    Synchronous VoIP.ms service that creates methods from JSON API definition.

    This is a pure service class similar to VoIPMSAsyncService.
    """

    def __init__(
        self, http_client: httpx.Client, config: VoIPMSConfig, api_definition: Dict[str, Any]
    ):
        """Initialize VoIP.ms service with provided HTTP client and config."""
        # Don't call super().__init__() since we're doing custom initialization
        # Set up the attributes that BaseVoIPMSClient methods expect
        self._client = http_client  # Use provided HTTP client
        self.config = config
        self.api_definition = api_definition
        self.debug = config.debug
        self.enable_retries = config.enable_retries

        # Set up attributes for base class compatibility
        self.username = config.username
        self.password = config.password
        self.base_url = config.base_url
        self.timeout = config.timeout
        self.max_retries = config.max_retries
        self.verify_ssl = config.verify_ssl

        # Create retry decorator if enabled
        if config.enable_retries:
            from .retry_config import create_api_retry_decorator

            self._retry_decorator = create_api_retry_decorator(
                max_attempts=config.max_retries, base_delay=1.0, max_delay=60.0
            )
        else:
            self._retry_decorator = None

        # Initialize type discovery
        from .type_discovery import TypeDiscoveryLogger
        self._type_discovery = TypeDiscoveryLogger(enabled=config.enable_type_discovery)

        # Create method factory for dynamic methods
        self._method_factory = MethodFactory(self, debug=config.debug, is_async=False)
        self._create_methods_from_definition()

    def _execute(self, method: str, **params) -> Dict[str, Any]:
        """Execute API method"""
        # Build payload
        payload = self._build_payload(method, **params)

        if self.debug:
            logger.debug(f"Executing {method} with {len(params)} parameters")

        # Make HTTP request (retries are handled by Tenacity decorator if enabled)
        response = self._client.get("", params=payload)
        response.raise_for_status()

        data = response.json()
        return self._handle_response(data, method)


@contextmanager
def VoIPMSClient(
    config: Optional[VoIPMSConfig] = None, **kwargs
) -> Generator[VoIPMSService, None, None]:
    """
    Factory function for creating VoIP.ms sync client using context management.

    This provides automatic resource management similar to the async client.

    Args:
        config: VoIPMSConfig object (if None, loads from environment)
        **kwargs: Direct parameters (username, password, etc.) - creates VoIPMSConfig internally

    Examples:
        # Simple direct parameters
        with VoIPMSClient(username="user", password="pass") as client:
            balance = client.getBalance()

        # Explicit config object (for advanced configuration)
        config = VoIPMSConfig(username="user", password="pass", debug=True)
        with VoIPMSClient(config) as client:
            balance = client.getBalance()

        # From environment variables
        with VoIPMSClient() as client:
            balance = client.getBalance()
    """
    if config is None:
        if kwargs:
            # Direct parameters provided, create config from them
            config = VoIPMSConfig(**kwargs)
        else:
            # No parameters, load from environment
            config = VoIPMSConfig.from_env()
    elif kwargs:
        # Both config object and kwargs provided - that's an error
        raise ValueError("Cannot provide both config object and direct parameters")

    # Load API definition
    api_definition = load_api_definition(config.api_definition_path)

    # Error codes are now baked into api_definition.json by apply_quirks.py
    logger.info(
        f"Loaded API definition with {len(api_definition.get('operations', {}))} operations and "
        f"{len(api_definition.get('error_codes', {}))} error codes"
    )

    # Create HTTP client with automatic lifecycle management
    client_kwargs = {
        "base_url": config.base_url,
        "timeout": config.timeout,
        "verify": config.verify_ssl,
        "headers": {"User-Agent": "VoIPMS-DataDriven-Sync/2.0"},
    }
    
    # Add custom limits if specified
    if config.http_limits is not None:
        client_kwargs["limits"] = config.http_limits
    
    with httpx.Client(**client_kwargs) as http_client:

        # Create service instance
        service = VoIPMSService(http_client, config, api_definition)

        try:
            yield service
        finally:
            # Save type discoveries
            try:
                if hasattr(service, "_type_discovery"):
                    discovery_dir = None
                    if config.type_discovery_dir:
                        discovery_dir = Path(config.type_discovery_dir)
                    service._type_discovery.save_session(discovery_dir)
            except Exception as e:
                logger.debug(f"Failed to save type discoveries: {e}")

            # Cleanup is automatic via httpx's context manager
            logger.debug("VoIP.ms sync client cleaned up automatically")
