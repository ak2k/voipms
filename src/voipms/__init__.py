"""
VoIP.ms Python Client

A data-driven Python client for the VoIP.ms API.
"""

from .async_client import VoIPMSClientAsync
from .base_client import VoIPMSError
from .client import VoIPMSClient

__version__ = "1.0.0"
__all__ = ["VoIPMSClient", "VoIPMSClientAsync", "VoIPMSError"]
