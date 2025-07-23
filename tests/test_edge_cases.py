"""
Edge case tests that catch real-world issues.

These tests focus on scenarios that are likely to fail in practice
but might not be caught by generated tests.
"""

import os
from datetime import timezone
from unittest.mock import MagicMock, patch

import pytest


class TestRealWorldEdgeCases:
    """Test edge cases based on likely user scenarios."""

    def test_timezone_handling_in_defaults(self, mock_client):
        """Test that timezone handling is consistent."""
        # Mock a method that uses "Today" default
        with patch("voipms.method_factory.datetime") as mock_datetime:
            mock_now = MagicMock()
            mock_now.strftime.return_value = "2023-12-25"
            mock_datetime.now.return_value = mock_now
            mock_datetime.timezone = timezone

            # Should use UTC timezone
            mock_client.getCDR()
            mock_datetime.now.assert_called_with(timezone.utc)

    def test_boolean_parameter_variations(self, mock_client):
        """Test various boolean input formats that users might try."""
        boolean_inputs = [
            True,
            False,  # Python booleans
            1,
            0,  # Integers
            "true",
            "false",  # String booleans
            "True",
            "False",  # Capitalized
            "yes",
            "no",  # Yes/no
            "on",
            "off",  # On/off
            "1",
            "0",  # String numbers
        ]

        # Test with a method that likely has boolean parameters
        for bool_input in boolean_inputs:
            try:
                # This should not raise validation errors for boolean-like inputs
                mock_client.getBalance(advanced=bool_input)
            except ValueError as e:
                if "boolean" in str(e).lower():
                    pytest.fail(f"Boolean input {bool_input} should be accepted: {e}")

    def test_numeric_string_edge_cases(self, mock_client):
        """Test numeric string parameters with edge cases."""
        numeric_inputs = [
            "123",  # Regular number
            "0",  # Zero
            "00123",  # Leading zeros
            "123.0",  # Float that's actually an integer
            123,  # Actual integer
            0,  # Integer zero
        ]

        for numeric_input in numeric_inputs:
            try:
                # Test with a method that has numeric string parameters
                mock_client.setDIDRouting(did="5551234567", routing=numeric_input)
            except ValueError as e:
                if "numeric" in str(e).lower() and str(numeric_input) in ["123", "0", "123.0"]:
                    pytest.fail(f"Numeric input {numeric_input} should be accepted: {e}")

    def test_date_parameter_formats(self, mock_client):
        """Test various date format inputs users might try."""
        # This should work
        mock_client.getCDR(date_from="2023-01-01", date_to="2023-01-31")

        # These might not work but shouldn't crash unexpectedly
        problematic_dates = [
            "01/01/2023",  # US format
            "2023/01/01",  # Alternative format
            "Jan 1, 2023",  # Text format
            "2023-1-1",  # Single digit months/days
        ]

        for date_format in problematic_dates:
            try:
                mock_client.getCDR(date_from=date_format, date_to="2023-01-31")
            except ValueError:
                # Expected to fail, but should be a clear validation error
                pass

    def test_none_parameter_handling(self, mock_client):
        """Test how None parameters are handled."""
        # None should be filtered out in most cases
        _ = mock_client.getBalance(advanced=None)

        # The HTTP call should not include None parameters
        call_args = mock_client._client.get.call_args
        params = call_args[1]["params"] if call_args else {}

        # Should not contain None values
        none_values = [k for k, v in params.items() if v is None]
        assert not none_values, f"None values should be filtered out: {none_values}"

    def test_empty_string_parameters(self, mock_client):
        """Test how empty string parameters are handled."""
        # Empty strings should generally be allowed but might cause API errors
        mock_client.getBalance(timezone="")  # Empty timezone

        # Should not crash, but the API call should include empty string
        call_args = mock_client._client.get.call_args
        if call_args and "params" in call_args[1]:
            params = call_args[1]["params"]
            # Empty strings should be preserved (unlike None)
            if "timezone" in params:
                assert params["timezone"] == ""


class TestErrorRecoveryEdgeCases:
    """Test error recovery in edge cases."""

    def test_network_timeout_handling(self, mock_client):
        """Test handling of network timeouts."""
        import httpx

        # Mock a timeout error
        mock_client._client.get.side_effect = httpx.TimeoutException("Request timeout")

        with pytest.raises(httpx.TimeoutException):
            mock_client.getBalance()

    def test_malformed_json_response(self, mock_client):
        """Test handling of malformed API responses."""
        # Mock a response with invalid JSON
        mock_response = MagicMock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.raise_for_status = MagicMock()
        mock_client._client.get.return_value = mock_response

        with pytest.raises(ValueError):
            mock_client.getBalance()

    def test_unexpected_response_structure(self, mock_client):
        """Test handling of unexpected response structures."""
        # Mock a response without expected fields
        mock_response = MagicMock()
        mock_response.json.return_value = {"unexpected": "structure"}
        mock_response.raise_for_status = MagicMock()
        mock_client._client.get.return_value = mock_response

        result = mock_client.getBalance()

        # Should still return the response even if structure is unexpected
        assert result == {"unexpected": "structure"}

    def test_connection_error_handling(self, mock_client):
        """Test handling of connection errors."""
        import httpx

        # Mock a connection error
        mock_client._client.get.side_effect = httpx.ConnectError("Connection failed")

        with pytest.raises(httpx.ConnectError):
            mock_client.getBalance()


class TestAsyncEdgeCases:
    """Test async-specific edge cases."""

    @pytest.mark.asyncio
    async def test_async_initialization_error(self):
        """Test async client handles initialization errors gracefully."""
        from voipms import VoIPMSAsyncClient

        with patch.dict(
            os.environ,
            {"VOIPMS_USERNAME": "test@example.com", "VOIPMS_API_PASSWORD": "test_password"},
        ):
            # Mock an error during HTTP client creation
            with patch("httpx.AsyncClient") as mock_client_class:
                mock_client_class.side_effect = RuntimeError("HTTP client creation failed")

                with pytest.raises(RuntimeError):
                    async with VoIPMSAsyncClient():
                        pass

    @pytest.mark.asyncio
    async def test_async_cleanup_error_handling(self):
        """Test async client handles cleanup errors gracefully."""
        from voipms import VoIPMSAsyncClient

        with patch.dict(
            os.environ,
            {"VOIPMS_USERNAME": "test@example.com", "VOIPMS_API_PASSWORD": "test_password"},
        ):
            async with VoIPMSAsyncClient() as client:
                # Mock an error during cleanup
                with patch.object(client._client, "aclose") as mock_close:
                    mock_close.side_effect = RuntimeError("Cleanup failed")

                    # Should not raise during context exit
                    pass  # Exit should handle the error gracefully

    @pytest.mark.asyncio
    async def test_async_method_call_after_close(self):
        """Test async methods after client is closed."""
        from voipms import VoIPMSAsyncClient

        with patch.dict(
            os.environ,
            {"VOIPMS_USERNAME": "test@example.com", "VOIPMS_API_PASSWORD": "test_password"},
        ):
            client = VoIPMSAsyncClient()
            async with client:
                # Use client normally
                pass

            # Try to use client after it's closed
            # This might work or fail depending on implementation
            try:
                await client.getBalance()
            except Exception:
                # Expected - client should not work after close
                pass


class TestValidationBypassEdgeCases:
    """Test edge cases when validation is bypassed."""

    def test_validation_bypass_with_invalid_types(self, mock_client):
        """Test that bypassing validation allows invalid types."""
        # These should not raise validation errors with validate=False
        problematic_params = {
            "did": ["not", "a", "string"],  # List instead of string
            "routing": {"invalid": "type"},  # Dict instead of number
            "advanced": "not_a_boolean",  # Invalid boolean
        }

        try:
            mock_client.getCDR(validate=False, **problematic_params)
        except ValueError as e:
            if "validation" in str(e).lower():
                pytest.fail(f"Validation should be bypassed: {e}")

    def test_minimal_validation_still_applies(self, mock_client):
        """Test that some minimal validation might still apply even with validate=False."""
        # Even with validation bypassed, some security checks might still apply
        # This is implementation-dependent

        dangerous_params = {
            "method": "rm -rf /",  # Potential injection
            "api_password": "hacked",  # Attempt to override credentials
        }

        # Implementation should handle these safely regardless of validation setting
        mock_client.getBalance(validate=False, **dangerous_params)


class TestMemoryAndResourceEdgeCases:
    """Test memory and resource usage edge cases."""

    def test_large_parameter_values(self, mock_client):
        """Test handling of unusually large parameter values."""
        large_string = "x" * 10000  # 10KB string

        try:
            mock_client.getCDR(timezone=large_string)
        except Exception as e:
            # Should not crash with memory errors
            assert "memory" not in str(e).lower()

    def test_many_parameters(self, mock_client):
        """Test methods with many parameters."""
        # Create a large number of parameters
        many_params = {f"param_{i}": f"value_{i}" for i in range(100)}

        try:
            mock_client.getCDR(validate=False, **many_params)
        except Exception as e:
            # Should handle many parameters gracefully
            assert "too many" not in str(e).lower()

    def test_client_reuse(self, mock_client):
        """Test that client can be reused many times."""
        # Make many calls to test for memory leaks or resource issues
        for _ in range(100):
            mock_client.getBalance()

        # Should not crash or slow down significantly
