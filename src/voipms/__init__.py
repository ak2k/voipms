"""
VoIP.ms Python Client

A data-driven Python client for the VoIP.ms API.
"""

from .client import VoIPMSClient, VoIPMSClientAsync, VoIPMSError

__version__ = "1.0.0"
__all__ = ["VoIPMSClient", "VoIPMSClientAsync", "VoIPMSError"]