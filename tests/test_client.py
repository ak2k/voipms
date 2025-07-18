"""
Tests for VoIP.ms client
"""

import pytest
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
from voipms import VoIPMSClient, VoIPMSClientAsync, VoIPMSError


class TestVoIPMSClient:
    """Test synchronous client"""
    
    def test_client_initialization_without_credentials(self):
        """Test that client raises error without credentials"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="VoIP.ms credentials required"):
                VoIPMSClient()
                
    def test_client_initialization_with_credentials(self):
        """Test successful client initialization"""
        with patch.dict('os.environ', {
            'VOIPMS_USERNAME': 'test@example.com',
            'VOIPMS_PASSWORD': 'testpass'
        }):
            client = VoIPMSClient()
            assert client.username == 'test@example.com'
            assert client.password == 'testpass'
            
    def test_dynamic_method_creation(self):
        """Test that methods are created from API definition"""
        with patch.dict('os.environ', {
            'VOIPMS_USERNAME': 'test@example.com',
            'VOIPMS_PASSWORD': 'testpass'
        }):
            client = VoIPMSClient()
            
            # Check that methods exist
            assert hasattr(client, 'getBalance')
            assert hasattr(client, 'get_balance')  # snake_case version
            assert callable(client.getBalance)
            
    def test_parameter_validation(self):
        """Test parameter validation"""
        with patch.dict('os.environ', {
            'VOIPMS_USERNAME': 'test@example.com',
            'VOIPMS_PASSWORD': 'testpass'
        }):
            client = VoIPMSClient()
            
            # Test with missing required parameter
            with pytest.raises(ValueError, match="Missing required parameter"):
                # Assuming addCharge requires parameters
                client.addCharge()
                
    @patch('httpx.Client.post')
    def test_successful_api_call(self, mock_post):
        """Test successful API call"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'status': 'success',
            'balance': {
                'current_balance': '100.50',
                'spent_today': '5.25'
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response
        
        with patch.dict('os.environ', {
            'VOIPMS_USERNAME': 'test@example.com',
            'VOIPMS_PASSWORD': 'testpass'
        }):
            client = VoIPMSClient()
            result = client.getBalance(advanced=True)
            
            assert result['status'] == 'success'
            assert result['balance']['current_balance'] == '100.50'
            
    @patch('httpx.Client.post')
    def test_api_error_handling(self, mock_post):
        """Test API error handling"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'status': 'invalid_credentials',
            'message': 'Invalid username or password'
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response
        
        with patch.dict('os.environ', {
            'VOIPMS_USERNAME': 'test@example.com',
            'VOIPMS_PASSWORD': 'testpass'
        }):
            client = VoIPMSClient()
            
            with pytest.raises(VoIPMSError) as exc_info:
                client.getBalance()
                
            assert exc_info.value.code == 'invalid_credentials'
            

@pytest.mark.asyncio
class TestVoIPMSClientAsync:
    """Test asynchronous client"""
    
    async def test_async_client_initialization(self):
        """Test async client initialization"""
        with patch.dict('os.environ', {
            'VOIPMS_USERNAME': 'test@example.com',
            'VOIPMS_PASSWORD': 'testpass'
        }):
            async with VoIPMSClientAsync() as client:
                assert hasattr(client, 'getBalance')
                assert callable(client.getBalance)
                
    @patch('httpx.AsyncClient.post')
    async def test_async_api_call(self, mock_post):
        """Test async API call"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'status': 'success',
            'balance': {
                'current_balance': '100.50'
            }
        }
        mock_response.raise_for_status = MagicMock()
        
        # Make mock_post return an awaitable
        async def async_return(*args, **kwargs):
            return mock_response
            
        mock_post.side_effect = async_return
        
        with patch.dict('os.environ', {
            'VOIPMS_USERNAME': 'test@example.com',
            'VOIPMS_PASSWORD': 'testpass'
        }):
            async with VoIPMSClientAsync() as client:
                result = await client.getBalance(advanced=True)
                assert result['status'] == 'success'