"""
Basic tests for VoIP.ms client functionality
"""

from unittest.mock import MagicMock, patch

import pytest

from voipms import VoIPMSAsyncClient, VoIPMSClient, VoIPMSError


class TestBasicClient:
    """Test basic client functionality"""

    def test_client_requires_credentials(self):
        """Test that client requires credentials"""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="VoIP.ms credentials required"):
                with VoIPMSClient() as client:
                    pass

    def test_client_loads_with_credentials(self):
        """Test successful client initialization"""
        # Note: .env file may contain actual credentials, so we just verify client loads
        with patch.dict(
            "os.environ",
            {"VOIPMS_USERNAME": "test@example.com", "VOIPMS_API_PASSWORD": "testpass"},
            clear=True,
        ):
            with VoIPMSClient() as client:
                assert client.username == "test@example.com"
                assert client.password == "testpass"
                assert hasattr(client, "getBalance")

    @patch("httpx.Client.get")
    def test_successful_api_call(self, mock_get):
        """Test a successful API call"""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "success",
            "balance": {"current_balance": "100.50", "spent_today": "5.25"},
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        with patch.dict(
            "os.environ",
            {"VOIPMS_USERNAME": "test@example.com", "VOIPMS_API_PASSWORD": "testpass"},
            clear=True,
        ):
            with VoIPMSClient() as client:
                result = client.getBalance()

                # Verify result
                assert result["status"] == "success"
                assert result["balance"]["current_balance"] == "100.50"

                # Verify the request was made with correct parameters
                mock_get.assert_called_once()
                call_args = mock_get.call_args
                params = call_args[1]["params"]
                assert params["api_username"] == "test@example.com"
                assert params["api_password"] == "testpass"
                assert params["method"] == "getBalance"

    @patch("httpx.Client.get")
    def test_api_error_handling(self, mock_get):
        """Test API error handling"""
        # Mock error response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "invalid_credentials",
            "message": "Invalid username or password",
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        with patch.dict(
            "os.environ",
            {"VOIPMS_USERNAME": "test@example.com", "VOIPMS_API_PASSWORD": "testpass"},
            clear=True,
        ):
            with VoIPMSClient() as client:
                with pytest.raises(VoIPMSError) as exc_info:
                    client.getBalance()

                assert exc_info.value.code == "invalid_credentials"
                assert "Username or Password is incorrect" in str(exc_info.value)

    def test_method_with_required_parameters(self):
        """Test validation of required parameters"""
        with patch.dict(
            "os.environ",
            {"VOIPMS_USERNAME": "test@example.com", "VOIPMS_API_PASSWORD": "testpass"},
            clear=True,
        ):
            with VoIPMSClient() as client:
                # Try calling a method that requires parameters without providing them
                with pytest.raises(ValueError, match="Parameter validation failed"):
                    client.addCharge()  # This method requires parameters

    @patch("httpx.Client.get")
    def test_boolean_parameter_conversion(self, mock_get):
        """Test that boolean parameters are converted correctly"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success", "cdr": []}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        with patch.dict(
            "os.environ",
            {"VOIPMS_USERNAME": "test@example.com", "VOIPMS_API_PASSWORD": "testpass"},
            clear=True,
        ):
            with VoIPMSClient() as client:
                # Call getCDR with boolean parameter 'answered'
                # This should convert True to "1"
                client.getCDR(
                    date_from="2024-01-01",
                    date_to="2024-01-31",
                    timezone="1",  # Required parameter
                    answered=True,  # Should be converted to "1"
                )

                # Check the parameters sent
                call_args = mock_get.call_args
                params = call_args[1]["params"]
                assert params["answered"] == "1"  # Boolean to "1"/"0"


@pytest.mark.asyncio
class TestAsyncClient:
    """Test async client functionality"""

    async def test_async_client_initialization(self):
        """Test async client can be initialized"""
        with patch.dict(
            "os.environ",
            {"VOIPMS_USERNAME": "test@example.com", "VOIPMS_API_PASSWORD": "testpass"},
            clear=True,
        ):
            async with VoIPMSAsyncClient() as client:
                assert hasattr(client, "getBalance")
                assert client.config.username == "test@example.com"

    @patch("httpx.AsyncClient.get")
    async def test_async_api_call(self, mock_get):
        """Test async API call"""
        # Mock response
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
            "os.environ",
            {"VOIPMS_USERNAME": "test@example.com", "VOIPMS_API_PASSWORD": "testpass"},
            clear=True,
        ):
            async with VoIPMSAsyncClient() as client:
                result = await client.getBalance()
                assert result["status"] == "success"
                assert result["balance"]["current_balance"] == "100.50"
