"""
Tests based on VoIP.ms PHP API examples
Auto-generated from PHP example files
"""

from unittest.mock import MagicMock, patch

import pytest

from voipms import VoIPMSClient


class TestAPIExamples:
    """Test cases derived from official PHP examples"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test client with mock credentials"""
        with patch.dict(
            "os.environ", {"VOIPMS_USERNAME": "test@example.com", "VOIPMS_API_PASSWORD": "testpass"}
        ):
            self.client = VoIPMSClient()

    @patch("httpx.Client.get")
    def test_getlanguages_0(self, mock_get):
        """Test getLanguages - Evaluate Response"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "success",
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # Make API call
        result = self.client.getLanguages()

        # Verify response
        assert result["status"] == "success"

    @patch("httpx.Client.get")
    def test_getregistrationstatus_1(self, mock_get):
        """Test getRegistrationStatus - Registration Status"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "success",
            "registered": "test_value",
            "registrations": "test_value",
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # Make API call
        result = self.client.getRegistrationStatus(account="100001_VoIP")

        # Verify response
        assert result["status"] == "success"
        assert "registered" in result
        assert "registrations" in result

    @patch("httpx.Client.get")
    def test_getclients_2(self, mock_get):
        """Test getClients - Client Login"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "success",
            "clients": "test_value",
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # Make API call
        result = self.client.getClients(email="Jane.doe@mydomain.com")

        # Verify response
        assert result["status"] == "success"
        assert "clients" in result

    @patch("httpx.Client.get")
    def test_getsubaccounts_3(self, mock_get):
        """Test getSubAccounts - Client Accounts"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "success",
            "accounts": "test_value",
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # Make API call
        result = self.client.getSubAccounts(account="500000")

        # Verify response
        assert result["status"] == "success"
        assert "accounts" in result

    @patch("httpx.Client.get")
    def test_getvoicemails_4(self, mock_get):
        """Test getVoicemails - Voicemails"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "success",
            "accounts": "test_value",
            "voicemails": "test_value",
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # Make API call
        result = self.client.getVoicemails(mailbox="900000")

        # Verify response
        assert result["status"] == "success"
        assert "accounts" in result
        assert "voicemails" in result

    @patch("httpx.Client.get")
    def test_getclients_5(self, mock_get):
        """Test getClients - Clients"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "success",
            "clients": "test_value",
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # Make API call
        result = self.client.getClients()

        # Verify response
        assert result["status"] == "success"
        assert "clients" in result

    @patch("httpx.Client.get")
    def test_getpackages_6(self, mock_get):
        """Test getPackages - Packages"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "success",
            "packages": "test_value",
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # Make API call
        result = self.client.getPackages()

        # Verify response
        assert result["status"] == "success"
        assert "packages" in result

    @patch("httpx.Client.get")
    def test_getcdr_7(self, mock_get):
        """Test getCDR - Cdr"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "success",
            "cdr": "test_value",
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # Make API call
        result = self.client.getCDR(date_from="2024-01-01", date_to="2024-01-31")

        # Verify response
        assert result["status"] == "success"
        assert "cdr" in result

    @patch("httpx.Client.get")
    def test_getresellercdr_8(self, mock_get):
        """Test getResellerCDR - Cdr Reseller"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "success",
            "cdr": "test_value",
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # Make API call
        result = self.client.getResellerCDR(date_from="2024-01-01", date_to="2024-01-31")

        # Verify response
        assert result["status"] == "success"
        assert "cdr" in result
