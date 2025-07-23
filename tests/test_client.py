"""
Tests for VoIP.ms client
"""

from unittest.mock import MagicMock, patch

import pytest

from voipms import VoIPMSAsyncClient, VoIPMSClient, VoIPMSConfig, VoIPMSError


class TestVoIPMSClient:
    """Test synchronous client"""

    def test_client_initialization_without_credentials(self):
        """Test that client raises error without credentials"""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="VoIP.ms credentials required"):
                with VoIPMSClient():
                    pass

    def test_client_initialization_with_credentials(self):
        """Test successful client initialization"""
        with patch.dict(
            "os.environ", {"VOIPMS_USERNAME": "test@example.com", "VOIPMS_API_PASSWORD": "testpass"}
        ):
            with VoIPMSClient() as client:
                assert client.username == "test@example.com"
                assert client.password == "testpass"

    def test_dynamic_method_creation(self):
        """Test that methods are created from API definition"""
        config = VoIPMSConfig.for_testing(username="test@example.com", password="testpass")
        with VoIPMSClient(config) as client:
            # Check that methods exist
            assert hasattr(client, "getBalance")
            assert hasattr(client, "get_balance")  # snake_case version
            assert callable(client.getBalance)

    def test_parameter_validation(self):
        """Test parameter validation"""
        config = VoIPMSConfig.for_testing(username="test@example.com", password="testpass")
        with VoIPMSClient(config) as client:
            # Test with missing required parameter
            with pytest.raises(ValueError, match="Parameter validation failed"):
                # Assuming addCharge requires parameters
                client.addCharge()

    @patch("httpx.Client.get")
    def test_successful_api_call(self, mock_get):
        """Test successful API call"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "success",
            "balance": {"current_balance": "100.50", "spent_today": "5.25"},
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        config = VoIPMSConfig.for_testing(username="test@example.com", password="testpass")
        with VoIPMSClient(config) as client:
            result = client.getBalance(advanced=True)

            assert result["status"] == "success"
            assert result["balance"]["current_balance"] == "100.50"

    @patch("httpx.Client.get")
    def test_api_error_handling(self, mock_get):
        """Test API error handling"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "invalid_credentials",
            "message": "Invalid username or password",
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        config = VoIPMSConfig.for_testing(username="test@example.com", password="testpass")
        with VoIPMSClient(config) as client:
            with pytest.raises(VoIPMSError) as exc_info:
                client.getBalance()

            assert exc_info.value.code == "invalid_credentials"

    def test_method_naming(self):
        """Test method naming convention (camelCase and snake_case)"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "success",
            "balance": {"current_balance": "75.25"},
        }
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.Client.get", return_value=mock_response):
            config = VoIPMSConfig.for_testing(username="test@example.com", password="testpass")
            with VoIPMSClient(config) as client:
                # Test camelCase method works
                result = client.getBalance()
                assert result["status"] == "success"

                # Verify snake_case version also works
                result2 = client.get_balance()
                assert result2["status"] == "success"

                # Verify both are the same function object
                assert client.getBalance is client.get_balance

    def test_health_checks(self):
        """Test health check functionality"""
        config = VoIPMSConfig.for_testing(username="test@example.com", password="testpass")
        with VoIPMSClient(config) as client:
            # Test lightweight health check
            assert client.is_healthy()

            # Test connectivity check with successful response
            mock_response = MagicMock()
            mock_response.json.return_value = {"status": "success"}
            mock_response.raise_for_status = MagicMock()

            with patch("httpx.Client.get", return_value=mock_response):
                connectivity = client.test_connectivity()
                assert connectivity

    def test_custom_config_initialization(self):
        """Test sync client with custom configuration"""
        config = VoIPMSConfig(
            username="custom@example.com",
            password="custompass",
            timeout=45.0,
            debug=True,
            enable_retries=False,
        )

        with VoIPMSClient(config) as client:
            assert client.config.username == "custom@example.com"
            assert client.config.timeout == 45.0
            assert client.config.debug
            assert not client.config.enable_retries

    def test_environment_config_initialization(self):
        """Test sync client loading config from environment"""
        with patch.dict(
            "os.environ", {"VOIPMS_USERNAME": "env@example.com", "VOIPMS_API_PASSWORD": "envpass"}
        ):
            with VoIPMSClient() as client:
                assert client.username == "env@example.com"
                assert client.password == "envpass"

    def test_direct_parameters(self):
        """Test sync client with direct parameters"""
        with VoIPMSClient(username="direct@example.com", password="directpass") as client:
            assert client.username == "direct@example.com"
            assert client.password == "directpass"

    def test_direct_parameters_with_advanced_options(self):
        """Test sync client with direct parameters including advanced options"""
        with VoIPMSClient(
            username="advanced@example.com",
            password="advancedpass",
            debug=True,
            timeout=45.0,
            enable_retries=False,
        ) as client:
            assert client.username == "advanced@example.com"
            assert client.password == "advancedpass"
            assert client.config.debug
            assert client.config.timeout == 45.0
            assert not client.config.enable_retries

    def test_config_and_kwargs_error(self):
        """Test that providing both config and kwargs raises an error"""
        config = VoIPMSConfig.for_testing(username="test@example.com", password="testpass")
        with pytest.raises(
            ValueError, match="Cannot provide both config object and direct parameters"
        ):
            with VoIPMSClient(config, username="conflict@example.com"):
                pass

    def test_partial_parameters_with_env_fallback(self):
        """Test that username/password load from env when only other parameters are provided"""
        with patch.dict(
            "os.environ", {"VOIPMS_USERNAME": "env@example.com", "VOIPMS_API_PASSWORD": "envpass"}
        ):
            # Only provide non-credential parameters
            with VoIPMSClient(debug=True, timeout=45.0, enable_retries=False) as client:
                # Credentials should come from environment
                assert client.username == "env@example.com"
                assert client.password == "envpass"
                # Explicit parameters should be used
                assert client.config.debug
                assert client.config.timeout == 45.0
                assert not client.config.enable_retries


@pytest.mark.asyncio
class TestVoIPMSAsyncClient:
    """Test asynchronous client using clean implementation"""

    async def test_async_client_initialization(self):
        """Test async client initialization with environment variables"""
        with patch.dict(
            "os.environ", {"VOIPMS_USERNAME": "test@example.com", "VOIPMS_API_PASSWORD": "testpass"}
        ):
            async with VoIPMSAsyncClient() as client:
                assert hasattr(client, "getBalance")
                assert callable(client.getBalance)

    @patch("httpx.AsyncClient.get")
    async def test_async_api_call(self, mock_get):
        """Test async API call"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "success",
            "balance": {"current_balance": "100.50"},
        }
        mock_response.raise_for_status = MagicMock()

        # Make mock_get return an awaitable
        async def async_return(*args, **kwargs):
            return mock_response

        mock_get.side_effect = async_return

        with patch.dict(
            "os.environ", {"VOIPMS_USERNAME": "test@example.com", "VOIPMS_API_PASSWORD": "testpass"}
        ):
            async with VoIPMSAsyncClient() as client:
                result = await client.getBalance(advanced=True)
                assert result["status"] == "success"

    async def test_custom_config_initialization(self):
        """Test async client with custom configuration"""
        config = VoIPMSConfig(
            username="custom@example.com",
            password="custompass",
            timeout=45.0,
            debug=True,
            enable_retries=False,
        )

        async with VoIPMSAsyncClient(config) as client:
            assert client.config.username == "custom@example.com"
            assert client.config.timeout == 45.0
            assert client.config.debug
            assert not client.config.enable_retries

    async def test_method_naming(self):
        """Test method naming convention"""
        with patch.dict(
            "os.environ", {"VOIPMS_USERNAME": "test@example.com", "VOIPMS_API_PASSWORD": "testpass"}
        ):
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "status": "success",
                "balance": {"current_balance": "75.25"},
            }
            mock_response.raise_for_status = MagicMock()

            with patch("httpx.AsyncClient.get", return_value=mock_response):
                async with VoIPMSAsyncClient() as client:
                    # Test camelCase method works
                    result = await client.getBalance()
                    assert result["status"] == "success"

                    # Verify snake_case version also works
                    result2 = await client.get_balance()
                    assert result2["status"] == "success"

                    # Verify both are the same function object
                    assert client.getBalance is client.get_balance

    async def test_health_checks(self):
        """Test health check functionality"""
        with patch.dict(
            "os.environ", {"VOIPMS_USERNAME": "test@example.com", "VOIPMS_API_PASSWORD": "testpass"}
        ):
            async with VoIPMSAsyncClient() as client:
                # Test lightweight health check
                assert client.is_healthy()

                # Test connectivity check with successful response
                mock_response = MagicMock()
                mock_response.json.return_value = {"status": "success"}
                mock_response.raise_for_status = MagicMock()

                with patch("httpx.AsyncClient.get", return_value=mock_response):
                    connectivity = await client.test_connectivity()
                    assert connectivity

    async def test_config_from_env(self):
        """Test VoIPMSConfig.from_env() class method"""
        with patch.dict(
            "os.environ",
            {"VOIPMS_USERNAME": "env@example.com", "VOIPMS_API_PASSWORD": "envpass"},
            clear=True,
        ):
            config = VoIPMSConfig.from_env()
            assert config.username == "env@example.com"
            assert config.password == "envpass"

            async with VoIPMSAsyncClient(config) as client:
                assert client.config.username == "env@example.com"

    async def test_config_for_testing(self):
        """Test VoIPMSConfig.for_testing() class method"""
        config = VoIPMSConfig.for_testing(username="testuser", password="testpass")

        assert config.username == "testuser"
        assert config.password == "testpass"
        assert config.debug
        assert not config.enable_retries  # Faster tests

        async with VoIPMSAsyncClient(config) as client:
            assert not client.config.enable_retries

    async def test_direct_parameters(self):
        """Test async client with direct parameters"""
        async with VoIPMSAsyncClient(
            username="direct@example.com", password="directpass"
        ) as client:
            assert client.username == "direct@example.com"
            assert client.password == "directpass"

    async def test_direct_parameters_with_advanced_options(self):
        """Test async client with direct parameters including advanced options"""
        async with VoIPMSAsyncClient(
            username="advanced@example.com",
            password="advancedpass",
            debug=True,
            timeout=45.0,
            enable_retries=False,
        ) as client:
            assert client.username == "advanced@example.com"
            assert client.password == "advancedpass"
            assert client.config.debug
            assert client.config.timeout == 45.0
            assert not client.config.enable_retries

    async def test_config_and_kwargs_error(self):
        """Test that providing both config and kwargs raises an error"""
        config = VoIPMSConfig.for_testing(username="test@example.com", password="testpass")
        with pytest.raises(
            ValueError, match="Cannot provide both config object and direct parameters"
        ):
            async with VoIPMSAsyncClient(config, username="conflict@example.com"):
                pass

    async def test_partial_parameters_with_env_fallback(self):
        """Test that username/password load from env when only other parameters are provided"""
        with patch.dict(
            "os.environ", {"VOIPMS_USERNAME": "env@example.com", "VOIPMS_API_PASSWORD": "envpass"}
        ):
            # Only provide non-credential parameters
            async with VoIPMSAsyncClient(debug=True, timeout=45.0, enable_retries=False) as client:
                # Credentials should come from environment
                assert client.username == "env@example.com"
                assert client.password == "envpass"
                # Explicit parameters should be used
                assert client.config.debug
                assert client.config.timeout == 45.0
                assert not client.config.enable_retries
