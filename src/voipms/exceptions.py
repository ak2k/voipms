"""
VoIP.ms API exceptions.
"""

from typing import Any, Dict, Optional


class VoIPMSError(Exception):
    """VoIP.ms API error"""

    def __init__(self, code: str, message: str, response: Optional[Dict[str, Any]] = None):
        self.code = code
        self.message = message
        self.response = response
        super().__init__(f"{code}: {message}")
