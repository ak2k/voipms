"""
VoIP.ms Python Client

Type stubs for the VoIP.ms API client package.
"""

from .async_client import (
    VoIPMSAsyncClient as VoIPMSAsyncClient,
    VoIPMSAsyncService as VoIPMSAsyncService,
)
from .client import VoIPMSClient as VoIPMSClient, VoIPMSService as VoIPMSService
from .config import VoIPMSConfig as VoIPMSConfig
from .exceptions import VoIPMSError as VoIPMSError

__version__: str
__all__: list[str]
