#!/usr/bin/env python3
"""
Data-Driven VoIP.ms Client
Dynamically creates methods from JSON API definition
"""

import logging
from typing import Any, Dict

import httpx

from .base_client import BaseVoIPMSClient, VoIPMSError
from .method_factory import MethodFactory

logger = logging.getLogger(__name__)


class VoIPMSClient(BaseVoIPMSClient):
    """
    Data-driven VoIP.ms client that creates methods from JSON API definition
    
    Example:
        >>> client = VoIPMSClient()
        >>> balance = client.getBalance()
        >>> print(f"Balance: ${balance['balance']['current_balance']}")
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize VoIP.ms client
        
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
        super().__init__(*args, **kwargs)

        # HTTP client
        self._client = self._create_http_client(httpx.Client, "VoIPMS-DataDriven/1.0")

        # Create method factory
        self._method_factory = MethodFactory(self, debug=self.debug)

        # Dynamically create methods
        self._create_methods_from_definition()

    def _execute(self, method: str, **params) -> Dict[str, Any]:
        """Execute API method"""
        # Build payload
        payload = self._build_payload(method, **params)

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

    def close(self):
        """Close HTTP client"""
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()