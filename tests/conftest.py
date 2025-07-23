"""
Test configuration and fixtures
"""

import pytest
from unittest.mock import patch


@pytest.fixture(autouse=True)
def mock_dotenv():
    """Mock dotenv to prevent loading .env file during tests"""
    with patch('voipms.base_client.load_dotenv'):
        yield