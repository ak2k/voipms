"""
Test configuration and fixtures
"""

from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def mock_dotenv():
    """Mock dotenv to prevent loading .env file during tests"""
    with patch("voipms.base_client.load_dotenv"):
        yield
