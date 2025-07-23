"""
Test different async patterns and architectural approaches for the VoIP.ms async client.

These tests verify that various Python async best practices and patterns work correctly
with our implementation.
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from voipms import VoIPMSAsyncClient, VoIPMSConfig


@pytest.mark.asyncio
class TestAsyncPatterns:
    """Test different async patterns for using the VoIP.ms async client"""

    async def test_environment_variable_pattern(self):
        """Test the simplest pattern: environment variables only"""
        with patch.dict(
            "os.environ", {"VOIPMS_USERNAME": "env_user", "VOIPMS_API_PASSWORD": "env_pass"}
        ):
            mock_response = self._create_mock_response({"status": "success"})

            with patch("httpx.AsyncClient.get", return_value=mock_response):
                async with VoIPMSAsyncClient() as client:
                    result = await client.getBalance()
                    assert result["status"] == "success"
                    assert client.config.username == "env_user"

    async def test_dataclass_configuration_pattern(self):
        """Test explicit configuration using dataclass"""
        config = VoIPMSConfig(
            username="test_user",
            password="test_pass",
            timeout=60.0,
            debug=True,
            enable_retries=False,
        )

        mock_response = self._create_mock_response({"status": "success"})

        with patch("httpx.AsyncClient.get", return_value=mock_response):
            async with VoIPMSAsyncClient(config) as client:
                result = await client.getBalance()
                assert result["status"] == "success"
                assert client.config.timeout == 60.0
                assert client.config.debug == True
                assert client.config.enable_retries == False

    async def test_factory_configuration_helpers(self):
        """Test using configuration factory methods"""
        # Test from_env factory
        with patch.dict(
            "os.environ", {"VOIPMS_USERNAME": "factory_user", "VOIPMS_API_PASSWORD": "factory_pass"}
        ):
            config = VoIPMSConfig.from_env()
            assert config.username == "factory_user"
            assert config.password == "factory_pass"

        # Test for_testing factory
        test_config = VoIPMSConfig.for_testing(username="test", password="test")
        assert test_config.username == "test"
        assert test_config.debug == True
        assert test_config.enable_retries == False

    async def test_context_manager_cleanup_pattern(self):
        """Test that context manager properly cleans up resources"""
        cleanup_called = False

        # Mock httpx.AsyncClient to track cleanup
        mock_client = AsyncMock()
        mock_client.is_closed = False

        async def mock_aexit(*args):
            nonlocal cleanup_called
            cleanup_called = True
            mock_client.is_closed = True

        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = mock_aexit

        config = VoIPMSConfig.for_testing()

        with patch("httpx.AsyncClient", return_value=mock_client):
            async with VoIPMSAsyncClient(config) as client:
                # Client should be healthy during usage
                assert client.is_healthy() == True

            # Cleanup should have been called after context exit
            assert cleanup_called == True

    async def test_concurrent_usage_pattern(self):
        """Test multiple concurrent clients don't interfere"""
        config1 = VoIPMSConfig.for_testing(username="user1", password="pass1")
        config2 = VoIPMSConfig.for_testing(username="user2", password="pass2")

        mock_response = self._create_mock_response({"status": "success"})

        async def use_client(config, expected_user):
            with patch("httpx.AsyncClient.get", return_value=mock_response):
                async with VoIPMSAsyncClient(config) as client:
                    assert client.config.username == expected_user
                    result = await client.getBalance()
                    return result["status"]

        # Run multiple clients concurrently
        results = await asyncio.gather(use_client(config1, "user1"), use_client(config2, "user2"))

        assert all(result == "success" for result in results)

    async def test_dependency_injection_pattern(self):
        """Test using the client as a dependency in other services"""

        class VoIPService:
            """Example service that depends on VoIP.ms client"""

            def __init__(self, voip_client):
                self.voip_client = voip_client

            async def get_account_balance(self):
                result = await self.voip_client.getBalance()
                return float(result.get("balance", {}).get("current_balance", "0"))

        config = VoIPMSConfig.for_testing()
        mock_response = self._create_mock_response(
            {"status": "success", "balance": {"current_balance": "123.45"}}
        )

        with patch("httpx.AsyncClient.get", return_value=mock_response):
            async with VoIPMSAsyncClient(config) as client:
                service = VoIPService(client)
                balance = await service.get_account_balance()
                assert balance == 123.45

    async def test_health_monitoring_pattern(self):
        """Test health monitoring usage patterns"""
        config = VoIPMSConfig.for_testing()

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.is_closed = False
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            async with VoIPMSAsyncClient(config) as client:
                # Test lightweight health check (no API call)
                assert client.is_healthy() == True

                # Test connectivity check (makes API call)
                mock_response = self._create_mock_response({"status": "success"})
                mock_client.get.return_value = mock_response

                connectivity = await client.test_connectivity()
                assert connectivity == True

                # Test health check with closed client
                mock_client.is_closed = True
                assert client.is_healthy() == False

    async def test_error_handling_pattern(self):
        """Test proper error handling patterns"""
        config = VoIPMSConfig.for_testing()

        # Test network error handling
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_get.side_effect = Exception("Network error")

            async with VoIPMSAsyncClient(config) as client:
                with pytest.raises(Exception, match="Network error"):
                    await client.getBalance()

    async def test_retry_configuration_pattern(self):
        """Test different retry configuration patterns"""
        # Test with retries enabled
        config_with_retries = VoIPMSConfig(
            username="test", password="test", enable_retries=True, max_retries=2
        )

        # Test with retries disabled
        config_no_retries = VoIPMSConfig(username="test", password="test", enable_retries=False)

        mock_response = self._create_mock_response({"status": "success"})

        with patch("httpx.AsyncClient.get", return_value=mock_response):
            # Both should work, just with different retry behavior
            async with VoIPMSAsyncClient(config_with_retries) as client1:
                result = await client1.getBalance()
                assert result["status"] == "success"
                assert client1.config.enable_retries == True

            async with VoIPMSAsyncClient(config_no_retries) as client2:
                result = await client2.getBalance()
                assert result["status"] == "success"
                assert client2.config.enable_retries == False

    async def test_testing_helper_pattern(self):
        """Test patterns specifically designed for testing"""
        # Use the testing configuration helper
        test_config = VoIPMSConfig.for_testing()

        # Should have testing-friendly defaults
        assert test_config.debug == True
        assert test_config.enable_retries == False  # Faster tests

        mock_response = self._create_mock_response({"status": "success"})

        with patch("httpx.AsyncClient.get", return_value=mock_response):
            async with VoIPMSAsyncClient(test_config) as client:
                # Should work the same as production config
                result = await client.getBalance()
                assert result["status"] == "success"

    def _create_mock_response(self, json_data):
        """Helper to create consistent mock responses"""
        mock_response = MagicMock()
        mock_response.json.return_value = json_data
        mock_response.raise_for_status = MagicMock()
        return mock_response
