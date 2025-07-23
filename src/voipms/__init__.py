"""
VoIP.ms Python Client

A data-driven Python client for the VoIP.ms API.
"""

from .async_client import VoIPMSAsyncClient
from .client import VoIPMSClient
from .config import VoIPMSConfig
from .exceptions import VoIPMSError

__version__ = "2.0.0"
__all__ = ["VoIPMSClient", "VoIPMSAsyncClient", "VoIPMSError", "VoIPMSConfig"]
