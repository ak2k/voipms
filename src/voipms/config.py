"""
Configuration classes for VoIP.ms client using dataclasses.

This provides clean, type-safe configuration instead of complex __init__ methods.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class VoIPMSConfig:
    """
    Configuration for VoIP.ms client using dataclass best practices.

    This replaces the complex parameter passing in __init__ methods
    with a clean, type-safe configuration object.
    """

    # Authentication - use None as default, resolve in __post_init__
    username: Optional[str] = None
    password: Optional[str] = None

    # Connection settings
    base_url: str = "https://voip.ms/api/v1/rest.php"
    timeout: float = 30.0
    verify_ssl: bool = True

    # Retry settings
    enable_retries: bool = True
    max_retries: int = 3

    # Debugging
    debug: bool = False

    # API definition
    api_definition_path: str = "api_definition.json"

    def __post_init__(self):
        """Validate configuration after initialization"""
        # Resolve credentials from environment if not provided
        if self.username is None:
            self.username = os.getenv("VOIPMS_USERNAME")
        if self.password is None:
            self.password = os.getenv("VOIPMS_API_PASSWORD")

        if not self.username or not self.password:
            raise ValueError(
                "VoIP.ms credentials required. Set VOIPMS_USERNAME and "
                "VOIPMS_API_PASSWORD environment variables or provide them in config."
            )

    @classmethod
    def from_env(cls, **kwargs) -> "VoIPMSConfig":
        """Create configuration from environment variables with optional overrides.
        
        Args:
            **kwargs: Optional parameters to override defaults
            
        Returns:
            VoIPMSConfig instance with credentials from environment and any overrides
        """
        return cls(**kwargs)

    @classmethod
    def for_testing(cls, username: str = "test", password: str = "test") -> "VoIPMSConfig":
        """Create configuration for testing"""
        return cls(
            username=username, password=password, debug=True, enable_retries=False  # Faster tests
        )
