"""
Asynchronous VoIP.ms client implementation.
"""

import logging
from typing import Any, Dict

import httpx

from .base_client import BaseVoIPMSClient, VoIPMSError
from .method_factory import MethodFactory

logger = logging.getLogger(__name__)


class VoIPMSClientAsync(BaseVoIPMSClient):
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

        # Call parent init
        super().__init__(*self._init_args, **self._init_kwargs)

        # Create async client
        self._client = self._create_http_client(httpx.AsyncClient, "VoIPMS-DataDriven-Async/1.0")

        # Create method factory with async=True
        self._method_factory = MethodFactory(self, debug=self.debug, is_async=True)

        # Create async methods
        self._create_methods_from_definition()
        self._initialized = True

    async def _execute(self, method: str, **params) -> Dict[str, Any]:
        """Execute API method asynchronously"""
        # Ensure initialized
        if not self._initialized:
            await self._async_init()
            
        # Build payload
        payload = self._build_payload(method, **params)

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
        if hasattr(self, '_client') and self._client:
            await self._client.aclose()