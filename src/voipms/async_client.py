"""
Refactored async VoIP.ms client using Python best practices.

This implementation uses:
- @asynccontextmanager for clean resource management
- asyncio.Event() for proper async synchronization
- Dataclasses for configuration
- Dependency injection patterns
- Built-in httpx lifecycle management
"""

import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncGenerator, Dict, Optional

import httpx

from .base_client import BaseVoIPMSClient, load_api_definition
from .config import VoIPMSConfig
from .method_factory import MethodFactory
from .retry_config import create_api_retry_decorator

logger = logging.getLogger(__name__)


class VoIPMSAsyncService(BaseVoIPMSClient):
    """
    Pure async service for VoIP.ms API calls.

    This class has no lifecycle management complexity - it's a pure service
    that expects to be given a working HTTP client and configuration.
    Inherits shared functionality from BaseVoIPMSClient.
    """

    def __init__(
        self, http_client: httpx.AsyncClient, config: VoIPMSConfig, api_definition: Dict[str, Any]
    ):
        # Don't call super().__init__() since we're doing custom initialization
        # Set up the attributes that BaseVoIPMSClient methods expect
        self._client = http_client  # Standardized naming with sync client
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
            self._retry_decorator = create_api_retry_decorator(
                max_attempts=config.max_retries, base_delay=1.0, max_delay=60.0
            )
        else:
            self._retry_decorator = None

        # Initialize type discovery
        from .type_discovery import TypeDiscoveryLogger
        self._type_discovery = TypeDiscoveryLogger(enabled=config.enable_type_discovery)

        # Create method factory for dynamic methods
        self._method_factory = MethodFactory(self, debug=config.debug, is_async=True)
        self._create_methods_from_definition()

    async def _execute(self, method: str, **params) -> Dict[str, Any]:
        """Execute API method with optional retry logic"""
        # Apply retry decorator if enabled
        if self.config.enable_retries and self._retry_decorator:
            execute_func = self._retry_decorator(self._make_request)
            return await execute_func(method, **params)
        else:
            return await self._make_request(method, **params)

    async def _make_request(self, method: str, **params) -> Dict[str, Any]:
        """Make the actual HTTP request"""
        payload = {
            "api_username": self.config.username,
            "api_password": self.config.password,
            "method": method,
            **params,
        }

        if self.config.debug:
            logger.debug(f"Executing {method} with {len(params)} parameters")

        response = await self._client.get("", params=payload)
        response.raise_for_status()

        data = response.json()
        return self._handle_response(data, method)

    # is_healthy() method is now inherited from BaseVoIPMSClient

    async def test_connectivity(self) -> bool:
        """Test actual API connectivity with a lightweight call"""
        if not self.is_healthy():
            return False

        try:
            result = await self._execute("getBalance")
            return result.get("status") == "success"
        except Exception as e:
            logger.debug(f"Connectivity test failed: {e}")
            return False


@asynccontextmanager
async def VoIPMSAsyncClient(
    config: Optional[VoIPMSConfig] = None, **kwargs
) -> AsyncGenerator[VoIPMSAsyncService, None]:
    """
    Factory function for creating VoIP.ms async client using best practices.

    This is the cleanest, most Pythonic way to create and manage the client.
    All resource management is handled automatically by Python's async ecosystem.

    Args:
        config: VoIPMSConfig object (if None, loads from environment)
        **kwargs: Direct parameters (username, password, etc.) - creates VoIPMSConfig internally

    Examples:
        # Simple direct parameters
        async with VoIPMSAsyncClient(username="user", password="pass") as client:
            balance = await client.getBalance()

        # Explicit config object (for advanced configuration)
        config = VoIPMSConfig(username="user", password="pass", debug=True)
        async with VoIPMSAsyncClient(config) as client:
            balance = await client.getBalance()

        # From environment variables
        async with VoIPMSAsyncClient() as client:
            balance = await client.getBalance()
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
    async with httpx.AsyncClient(
        base_url=config.base_url,
        timeout=config.timeout,
        verify=config.verify_ssl,
        headers={"User-Agent": "VoIPMS-DataDriven-Async/2.0"},
    ) as http_client:

        # Create service instance
        service = VoIPMSAsyncService(http_client, config, api_definition)

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
            logger.debug("VoIP.ms client cleaned up automatically")
