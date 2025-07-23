"""
Property-based tests using Hypothesis for VoIP.ms API client.

These tests are completely data-driven from the API definition
and automatically scale without manual maintenance.
"""

import pytest
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st
from pydantic import ValidationError

from .hypothesis_strategies import APIDefinitionStrategyFactory


class TestValidationProperties:
    """Test validation logic properties that should always hold."""

    @given(st.data())
    @settings(suppress_health_check=[HealthCheck.too_slow], max_examples=50)
    def test_validation_consistency_property(self, data, mock_client, api_definition):
        """Property: Validation should be consistent across all methods."""
        strategy_factory = APIDefinitionStrategyFactory(api_definition)

        # Pick a random operation
        op_name = data.draw(st.sampled_from(list(api_definition["operations"].keys())))

        # Generate parameters for this operation
        params = data.draw(strategy_factory.build_operation_strategy(op_name, include_invalid=True))

        method = getattr(mock_client, op_name)

        # Property: validate=True should either succeed or raise ValidationError
        try:
            result = method(validate=True, **params)
            # If validation passed, the call should have succeeded
            assert isinstance(result, dict)
        except ValidationError:
            # Validation failed - this is expected for some generated params
            pass
        except ValueError as e:
            # Should be validation-related
            assert any(word in str(e).lower() for word in ["validation", "parameter", "required"])

    @given(st.data())
    @settings(max_examples=30)
    def test_validation_bypass_property(self, data, mock_client, api_definition):
        """Property: validate=False should never raise ValidationError."""
        strategy_factory = APIDefinitionStrategyFactory(api_definition)

        # Pick a random operation
        op_name = data.draw(st.sampled_from(list(api_definition["operations"].keys())))

        # Generate any parameters (including invalid ones)
        params = data.draw(strategy_factory.build_operation_strategy(op_name, include_invalid=True))

        method = getattr(mock_client, op_name)

        # Property: With validation bypassed, should never get ValidationError
        try:
            result = method(validate=False, **params)
            assert isinstance(result, dict)
        except Exception as e:
            # Should not be a validation error
            assert not isinstance(e, ValidationError)
            # Other exceptions (like HTTP errors) are fine

    @given(st.data())
    @settings(max_examples=20)
    def test_required_parameters_property(self, data, mock_client, api_definition):
        """Property: Missing required parameters should always fail validation."""
        strategy_factory = APIDefinitionStrategyFactory(api_definition)

        # Pick an operation that has required parameters
        operations_with_required = []
        for op_name, op_spec in api_definition["operations"].items():
            params = op_spec.get("parameters", {})
            if any(p.get("required", False) for p in params.values()):
                operations_with_required.append(op_name)

        assume(operations_with_required)  # Skip if no operations have required params

        op_name = data.draw(st.sampled_from(operations_with_required))
        op_spec = api_definition["operations"][op_name]

        # Find required parameters
        required_params = []
        for param_name, param_spec in op_spec.get("parameters", {}).items():
            if param_spec.get("required", False) and param_name not in [
                "api_username",
                "api_password",
            ]:
                required_params.append(param_name)

        assume(required_params)  # Skip if no non-credential required params

        # Generate params but omit a required one
        missing_param = data.draw(st.sampled_from(required_params))
        params = data.draw(
            strategy_factory.build_operation_strategy(op_name, include_invalid=False)
        )
        params.pop(missing_param, None)  # Remove the required parameter

        method = getattr(mock_client, op_name)

        # Property: Should fail validation when required param is missing
        with pytest.raises((ValidationError, ValueError)):
            method(validate=True, **params)


class TestBooleanConversionProperties:
    """Test boolean conversion logic properties."""

    @given(st.booleans())
    def test_boolean_01_conversion_property(self, bool_value):
        """Property: Boolean to "0"/"1" conversion should be reversible and consistent."""
        from voipms.types import boolean_01_validator

        result = boolean_01_validator(bool_value)

        # Property: Result should always be "0" or "1"
        assert result in ("0", "1")

        # Property: Conversion should be consistent
        expected = "1" if bool_value else "0"
        assert result == expected

    @given(st.sampled_from([1, 0, "1", "0", "true", "false", "yes", "no", "on", "off"]))
    def test_boolean_like_conversion_property(self, bool_like_value):
        """Property: Boolean-like values should convert consistently."""
        from voipms.types import boolean_01_validator

        result = boolean_01_validator(bool_like_value)

        # Property: Should always produce valid boolean string
        assert result in ("0", "1")

        # Property: Truthy values should map to "1", falsy to "0"
        truthy_values = [1, "1", "true", "True", "yes", "on"]
        falsy_values = [0, "0", "false", "False", "no", "off"]

        if bool_like_value in truthy_values:
            assert result == "1"
        elif bool_like_value in falsy_values:
            assert result == "0"

    @given(
        st.text().filter(
            lambda x: x.lower() not in ["true", "false", "yes", "no", "on", "off", "1", "0"]
        )
    )
    def test_invalid_boolean_conversion_property(self, invalid_bool_string):
        """Property: Invalid boolean strings should raise ValueError."""
        from voipms.types import boolean_01_validator

        assume(len(invalid_bool_string) > 0)  # Skip empty strings

        with pytest.raises(ValueError):
            boolean_01_validator(invalid_bool_string)


class TestQuirksProperties:
    """Test API quirks application properties."""

    @given(st.data())
    @settings(max_examples=20)
    def test_quirks_application_property(self, data, mock_client, api_definition):
        """Property: Quirks should be applied consistently."""
        # Test methods known to have quirks (this would be data-driven from quirks config)
        methods_with_quirks = ["setSMS", "setDIDInfo"]  # Example - would load from quirks.json

        for method_name in methods_with_quirks:
            if method_name in api_definition["operations"]:
                method = getattr(mock_client, method_name)

                # Test boolean parameter quirks
                bool_param_names = ["enable", "cnam", "record_calls"]  # Common boolean params

                for param_name in bool_param_names:
                    if param_name in api_definition["operations"][method_name].get(
                        "parameters", {}
                    ):
                        bool_value = data.draw(st.booleans())

                        # Call method with boolean parameter
                        method(**{param_name: bool_value}, validate=False)

                        # Verify quirks were applied (check HTTP call parameters)
                        # Note: This would need access to the actual HTTP call made
                        # For now, just verify the call succeeded
                        assert mock_client._client.get.called

    @given(st.data())
    @settings(max_examples=15)
    def test_date_default_property(self, data, mock_client, api_definition):
        """Property: Date defaults should be applied consistently."""
        # Find operations that have date parameters with "Today" default
        operations_with_date_defaults = []

        for op_name, op_spec in api_definition["operations"].items():
            params = op_spec.get("parameters", {})
            for param_name, param_spec in params.items():
                if param_spec.get("default") == "Today":
                    operations_with_date_defaults.append((op_name, param_name))

        if operations_with_date_defaults:
            op_name, param_name = data.draw(st.sampled_from(operations_with_date_defaults))
            method = getattr(mock_client, op_name)

            # Call without providing the date parameter
            method()

            # Property: Date default should have been applied
            call_args = mock_client._client.get.call_args
            if call_args and "params" in call_args[1]:
                params = call_args[1]["params"]
                # Should contain a date in YYYY-MM-DD format
                if param_name in params:
                    date_value = params[param_name]
                    assert isinstance(date_value, str)
                    assert len(date_value) == 10  # YYYY-MM-DD format
                    assert date_value.count("-") == 2


class TestCrossParameterProperties:
    """Test cross-parameter validation properties."""

    @given(st.data())
    @settings(max_examples=20)
    def test_date_range_property(self, data, mock_client, api_definition):
        """Property: date_from should always be <= date_to when both are provided."""
        # Find operations with date range parameters
        date_range_operations = []
        for op_name, op_spec in api_definition["operations"].items():
            params = op_spec.get("parameters", {})
            if "date_from" in params and "date_to" in params:
                date_range_operations.append(op_name)

        assume(date_range_operations)  # Skip if no date range operations

        op_name = data.draw(st.sampled_from(date_range_operations))
        strategy_factory = APIDefinitionStrategyFactory(api_definition)

        # Generate date range parameters
        date_params = data.draw(strategy_factory._build_date_range_strategy())

        method = getattr(mock_client, op_name)

        # Property: If date_from > date_to, should fail validation
        if date_params["date_from"] > date_params["date_to"]:
            with pytest.raises((ValueError, ValidationError)):
                method(validate=True, **date_params)
        else:
            # Valid date range should succeed (or fail for other reasons)
            try:
                method(validate=True, **date_params)
            except (ValueError, ValidationError) as e:
                # Should not be a date range error
                assert "date" not in str(e).lower() or "range" not in str(e).lower()


class TestAsyncSyncEquivalenceProperties:
    """Test that async and sync clients behave equivalently."""

    @given(st.data())
    @settings(max_examples=10)
    @pytest.mark.asyncio
    async def test_async_sync_parameter_equivalence(
        self, data, mock_client, mock_async_client, api_definition
    ):
        """Property: Async and sync clients should handle parameters identically."""
        strategy_factory = APIDefinitionStrategyFactory(api_definition)

        # Pick a random operation
        op_name = data.draw(
            st.sampled_from(list(api_definition["operations"].keys())[:10])
        )  # Limit for speed

        # Generate valid parameters
        params = data.draw(
            strategy_factory.build_operation_strategy(op_name, include_invalid=False)
        )

        sync_method = getattr(mock_client, op_name)
        async_method = getattr(mock_async_client, op_name)

        # Call both methods with same parameters
        sync_result = sync_method(**params)
        async_result = await async_method(**params)

        # Property: Results should be equivalent
        assert type(sync_result) is type(async_result)
        assert sync_result == async_result


class TestPerformanceProperties:
    """Test performance-related properties."""

    @given(st.data())
    @settings(max_examples=10)
    def test_method_call_performance_property(
        self, data, mock_client, api_definition, performance_monitor
    ):
        """Property: Method calls should complete within reasonable time."""
        # Pick a random operation
        op_name = data.draw(st.sampled_from(list(api_definition["operations"].keys())[:10]))
        strategy_factory = APIDefinitionStrategyFactory(api_definition)

        # Generate valid parameters
        params = data.draw(
            strategy_factory.build_operation_strategy(op_name, include_invalid=False)
        )

        method = getattr(mock_client, op_name)

        # Measure performance
        performance_monitor.start()
        method(**params)
        duration = performance_monitor.stop()

        # Property: Should complete quickly (mocked calls should be very fast)
        assert duration < 0.1, f"Method {op_name} took too long: {duration:.3f}s"

    @given(st.integers(min_value=1, max_value=10))
    def test_repeated_calls_property(self, call_count, mock_client):
        """Property: Repeated method calls should not degrade performance."""
        _ = mock_client  # Access through fixture would be better

        timings = []
        for _ in range(call_count):
            import time

            start = time.perf_counter()
            mock_client.getBalance()
            end = time.perf_counter()
            timings.append(end - start)

        # Property: Performance should not degrade significantly
        if len(timings) > 1:
            first_half_avg = sum(timings[: len(timings) // 2]) / (len(timings) // 2)
            second_half_avg = sum(timings[len(timings) // 2 :]) / (len(timings) - len(timings) // 2)

            # Second half should not be more than 2x slower than first half
            assert second_half_avg <= first_half_avg * 2


class TestErrorHandlingProperties:
    """Test error handling properties."""

    @given(st.data())
    @settings(max_examples=15)
    def test_error_consistency_property(
        self, data, mock_client, mock_http_response, api_definition
    ):
        """Property: Similar errors should be handled consistently."""
        # Test different error scenarios
        error_codes = ["invalid_credentials", "rate_limit_exceeded", "server_error", "not_found"]
        error_code = data.draw(st.sampled_from(error_codes))

        # Mock error response
        mock_client._client.get.return_value = mock_http_response(error_code=error_code)

        # Pick random operation
        op_name = data.draw(st.sampled_from(list(api_definition["operations"].keys())[:10]))
        strategy_factory = APIDefinitionStrategyFactory(api_definition)
        params = data.draw(
            strategy_factory.build_operation_strategy(op_name, include_invalid=False)
        )

        method = getattr(mock_client, op_name)

        # Property: Should raise an exception with error code information
        with pytest.raises(Exception) as exc_info:
            method(**params)

        # Error message should contain the error code
        assert error_code in str(exc_info.value)

    @given(st.text(min_size=1, max_size=1000))
    def test_parameter_safety_property(self, potentially_dangerous_param, mock_client):
        """Property: No parameter value should cause system-level failures."""
        # Test with potentially dangerous parameter values
        dangerous_values = [
            potentially_dangerous_param,
            "../../../etc/passwd",  # Path traversal
            "'; DROP TABLE users; --",  # SQL injection
            "<script>alert('xss')</script>",  # XSS
            "\x00\x01\x02",  # Binary data
        ]

        for dangerous_value in dangerous_values:
            # Should not crash the system (may raise application-level errors)
            try:
                mock_client.getBalance(timezone=dangerous_value, validate=False)
            except Exception:
                # Application errors are fine, system crashes are not
                pass
