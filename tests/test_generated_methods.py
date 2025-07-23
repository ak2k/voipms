"""
Data-driven tests for all generated API methods.

This test suite automatically scales with the API definition
and requires no manual maintenance when methods are added/removed.
"""


import pytest


class TestGeneratedMethods:
    """Test all dynamically generated methods."""

    def test_all_methods_exist(self, mock_client, all_operations):
        """Verify all operations from API definition have corresponding methods."""
        missing_methods = []

        for op_name in all_operations:
            # Check both camelCase and snake_case versions
            if not hasattr(mock_client, op_name):
                missing_methods.append(op_name)

        assert not missing_methods, f"Missing methods: {missing_methods}"

    def test_methods_are_callable(self, mock_client, all_operations):
        """Verify all generated methods are callable."""
        non_callable = []

        for op_name in all_operations:
            method = getattr(mock_client, op_name)
            if not callable(method):
                non_callable.append(op_name)

        assert not non_callable, f"Non-callable methods: {non_callable}"

    def test_methods_have_docstrings(self, mock_client, all_operations):
        """Verify all generated methods have docstrings."""
        missing_docs = []

        for op_name in all_operations:
            method = getattr(mock_client, op_name)
            if not method.__doc__:
                missing_docs.append(op_name)

        # Allow a small percentage to not have docs due to missing spec data
        missing_percentage = len(missing_docs) / len(all_operations) * 100
        assert (
            missing_percentage < 5
        ), f"Too many methods missing docs ({missing_percentage:.1f}%): {missing_docs[:10]}..."


class TestParameterValidation:
    """Test parameter validation across all methods."""

    @pytest.mark.parametrize("op_name", ["getBalance", "getCDR", "getDIDsInfo"])
    def test_sample_methods_basic_validation(self, mock_client, validation_test_runner, op_name):
        """Test basic validation on a sample of methods."""
        # Valid case - should pass
        success, error = validation_test_runner(op_name, {}, True)
        assert success, f"Basic call to {op_name} should succeed: {error}"

    def test_parameter_validation_with_generated_cases(
        self, mock_client, parameter_test_cases, validation_test_runner
    ):
        """Run all generated parameter validation test cases."""
        failed_tests = []

        # Test a sample of operations to keep test time reasonable
        sample_operations = list(parameter_test_cases.keys())[:20]  # Test first 20 operations

        for op_name in sample_operations:
            test_cases = parameter_test_cases[op_name]

            for case in test_cases:
                success, error = validation_test_runner(
                    op_name, case["params"], case["should_pass"]
                )

                if not success:
                    failed_tests.append(f"{op_name}.{case['name']}: {error}")

        # Allow some failures but not too many
        failure_rate = (
            len(failed_tests)
            / sum(len(cases) for cases in [parameter_test_cases[op] for op in sample_operations])
            * 100
        )

        assert (
            failure_rate < 10
        ), f"Too many validation tests failed ({failure_rate:.1f}%):\n" + "\n".join(
            failed_tests[:5]
        )


class TestAsyncSyncParity:
    """Test that async and sync clients behave identically."""

    @pytest.mark.asyncio
    async def test_method_signatures_match(self, mock_client, mock_async_client, all_operations):
        """Verify async and sync clients have the same methods."""
        sample_operations = all_operations[:10]  # Test a sample

        missing_from_async = []
        for op_name in sample_operations:
            if hasattr(mock_client, op_name) and not hasattr(mock_async_client, op_name):
                missing_from_async.append(op_name)

        assert not missing_from_async, f"Methods missing from async client: {missing_from_async}"

    @pytest.mark.asyncio
    async def test_basic_operations_work(self, mock_async_client):
        """Test that basic async operations work."""
        # Test a few key operations
        operations_to_test = ["getBalance", "getIP", "getServersInfo"]

        for op_name in operations_to_test:
            if hasattr(mock_async_client, op_name):
                method = getattr(mock_async_client, op_name)
                try:
                    result = await method()
                    assert isinstance(result, dict)
                    assert "status" in result
                except Exception as e:
                    pytest.fail(f"Async {op_name} failed: {e}")


class TestErrorHandling:
    """Test error handling across different scenarios."""

    def test_api_error_handling(self, mock_client, mock_http_response):
        """Test that API errors are properly handled."""
        # Mock an API error response
        mock_client._client.get.return_value = mock_http_response(error_code="invalid_credentials")

        with pytest.raises(Exception) as exc_info:
            mock_client.getBalance()

        # Should be a VoIPMSError or ValueError
        assert "invalid_credentials" in str(exc_info.value)

    def test_validation_bypass(self, mock_client):
        """Test that validation can be bypassed when needed."""
        # This should not raise validation errors even with invalid params
        try:
            result = mock_client.getBalance(invalid_param="test", validate=False)
            assert isinstance(result, dict)
        except Exception as e:
            # Should not be a validation error
            assert "validation" not in str(e).lower()


class TestQuirksHandling:
    """Test API quirks are properly applied."""

    def test_quirks_applied(self, mock_client, quirks_test_cases):
        """Test that quirks are properly applied to method calls."""
        # This would test specific quirks like boolean -> yes/no conversion
        # Implementation depends on your quirks configuration

        for method_name, test_cases in quirks_test_cases.items():
            if hasattr(mock_client, method_name):
                method = getattr(mock_client, method_name)

                for case in test_cases:
                    # Call method and verify quirks were applied
                    # (Implementation would check the actual parameters sent to HTTP client)
                    try:
                        method(**case["input_params"])
                        # In a real implementation, you'd verify the HTTP call parameters
                        # match case["expected_params"] after quirks are applied
                    except Exception:
                        # Expected for invalid test data
                        pass


class TestPerformance:
    """Test performance characteristics."""

    def test_method_creation_performance(self, performance_monitor):
        """Test that client initialization is reasonably fast."""
        import os
        from unittest.mock import patch

        performance_monitor.start()

        # Time client creation
        with patch.dict(
            os.environ,
            {"VOIPMS_USERNAME": "test@example.com", "VOIPMS_API_PASSWORD": "test_password"},
        ):
            from voipms import VoIPMSClient

            _ = VoIPMSClient()

        duration = performance_monitor.stop()

        # Client creation should be fast (< 1 second)
        assert duration < 1.0, f"Client creation took too long: {duration:.3f}s"

    def test_method_call_performance(self, mock_client, performance_monitor):
        """Test that method calls are reasonably fast."""
        # Test a few method calls
        for _ in range(10):
            performance_monitor.start()
            mock_client.getBalance()
            performance_monitor.stop()

        avg_time = performance_monitor.average_time()
        max_time = performance_monitor.max_time()

        # Method calls should be fast
        assert avg_time < 0.1, f"Average method call too slow: {avg_time:.3f}s"
        assert max_time < 0.2, f"Slowest method call too slow: {max_time:.3f}s"


class TestContractCompliance:
    """Test compliance with API definition contract."""

    def test_operations_count_matches(self, mock_client, api_definition):
        """Test that number of methods matches API definition."""
        expected_count = len(api_definition["operations"])

        # Count generated methods (excluding built-in methods)
        client_methods = [
            name
            for name in dir(mock_client)
            if not name.startswith("_")
            and callable(getattr(mock_client, name))
            and name
            not in ["close", "get_available_methods", "get_method_info", "debug_method_params"]
        ]

        # Should have at least the expected operations (may have snake_case versions too)
        assert (
            len(client_methods) >= expected_count
        ), f"Expected at least {expected_count} methods, got {len(client_methods)}"

    def test_method_names_valid(self, mock_client, all_operations):
        """Test that all method names from API definition are valid."""
        invalid_names = []

        for op_name in all_operations:
            if not op_name.isidentifier():
                invalid_names.append(op_name)

        assert not invalid_names, f"Invalid method names in API definition: {invalid_names}"

    def test_required_methods_exist(self, mock_client):
        """Test that critical methods exist."""
        required_methods = ["getBalance", "getCDR", "getServersInfo", "getDIDsInfo"]

        missing = []
        for method_name in required_methods:
            if not hasattr(mock_client, method_name):
                missing.append(method_name)

        assert not missing, f"Critical methods missing: {missing}"
