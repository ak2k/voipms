"""
Pytest configuration and fixtures for VoIP.ms testing.

This module provides data-driven test fixtures that automatically
scale with the API definition without requiring manual maintenance.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List
from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError

from voipms import VoIPMSAsyncClient, VoIPMSClient


@pytest.fixture(autouse=True)
def mock_dotenv():
    """Mock dotenv to prevent loading .env file during tests"""
    with patch("voipms.base_client.load_dotenv"):
        yield


@pytest.fixture(scope="session")
def api_definition() -> Dict[str, Any]:
    """Load the API definition once per test session."""
    # Try multiple locations
    for path in [
        Path(__file__).parent.parent / "src" / "voipms" / "api_definition.json",
        Path(__file__).parent.parent / "api_definition.json",
        "api_definition.json",
    ]:
        if path.exists():
            with open(path) as f:
                return json.load(f)

    pytest.fail("Could not find api_definition.json")


@pytest.fixture(scope="session")
def all_operations(api_definition) -> List[str]:
    """Get list of all operation names from API definition."""
    return list(api_definition["operations"].keys())


@pytest.fixture(scope="session")
def operations_by_category(api_definition) -> Dict[str, List[str]]:
    """Group operations by category for targeted testing."""
    categories = {}
    for op_name, op_spec in api_definition["operations"].items():
        # Extract category from operation name or use first part
        if op_name.startswith("get"):
            category = "read"
        elif op_name.startswith(("set", "create", "add")):
            category = "write"
        elif op_name.startswith(("del", "cancel", "remove")):
            category = "delete"
        elif op_name.startswith(("order", "connect")):
            category = "provisioning"
        else:
            category = "other"

        categories.setdefault(category, []).append(op_name)

    return categories


@pytest.fixture
def mock_http_response():
    """Factory for creating mock HTTP responses."""

    def _create_response(status="success", data=None, error_code=None):
        mock_response = MagicMock()

        if error_code:
            response_data = {"status": error_code, "message": f"Mock error: {error_code}"}
        else:
            response_data = {"status": status, **(data or {})}

        mock_response.json.return_value = response_data
        mock_response.raise_for_status = MagicMock()
        return mock_response

    return _create_response


@pytest.fixture
def mock_client(mock_http_response):
    """Create a VoIP.ms client with mocked HTTP calls."""
    with patch.dict(
        os.environ, {"VOIPMS_USERNAME": "test@example.com", "VOIPMS_API_PASSWORD": "test_password"}
    ):
        client = VoIPMSClient()

        # Mock the HTTP client
        with patch.object(client, "_client") as mock_http_client:
            mock_http_client.get.return_value = mock_http_response()
            yield client


@pytest.fixture
async def mock_async_client(mock_http_response):
    """Create an async VoIP.ms client with mocked HTTP calls."""
    with patch.dict(
        os.environ, {"VOIPMS_USERNAME": "test@example.com", "VOIPMS_API_PASSWORD": "test_password"}
    ):
        async with VoIPMSAsyncClient() as client:
            # Mock the HTTP client
            with patch.object(client, "http_client") as mock_http_client:

                async def mock_get(*args, **kwargs):
                    return mock_http_response()

                mock_http_client.get.side_effect = mock_get
                yield client


@pytest.fixture(scope="session")
def parameter_test_cases(api_definition) -> Dict[str, List[Dict[str, Any]]]:
    """Generate test cases for parameter validation based on API definition."""
    test_cases = {}

    for op_name, op_spec in api_definition["operations"].items():
        parameters = op_spec.get("parameters", {})
        cases = []

        for param_name, param_spec in parameters.items():
            param_type = param_spec.get("type", "string")
            required = param_spec.get("required", False)
            enum_values = param_spec.get("enum")
            minimum = param_spec.get("minimum")
            maximum = param_spec.get("maximum")

            # Valid cases
            if param_type == "string":
                cases.append(
                    {
                        "name": f"valid_{param_name}_string",
                        "params": {param_name: "test_string"},
                        "should_pass": True,
                    }
                )

                if enum_values:
                    cases.append(
                        {
                            "name": f"valid_{param_name}_enum",
                            "params": {param_name: enum_values[0]},
                            "should_pass": True,
                        }
                    )

                    # Invalid enum case
                    cases.append(
                        {
                            "name": f"invalid_{param_name}_enum",
                            "params": {param_name: "invalid_enum_value"},
                            "should_pass": False,
                        }
                    )

            elif param_type == "integer":
                valid_int = minimum + 1 if minimum is not None else 42
                cases.append(
                    {
                        "name": f"valid_{param_name}_integer",
                        "params": {param_name: valid_int},
                        "should_pass": True,
                    }
                )

                # Test boundaries
                if minimum is not None:
                    cases.append(
                        {
                            "name": f"invalid_{param_name}_below_minimum",
                            "params": {param_name: minimum - 1},
                            "should_pass": False,
                        }
                    )

                if maximum is not None:
                    cases.append(
                        {
                            "name": f"invalid_{param_name}_above_maximum",
                            "params": {param_name: maximum + 1},
                            "should_pass": False,
                        }
                    )

            # Required parameter tests
            if required:
                cases.append(
                    {
                        "name": f"missing_required_{param_name}",
                        "params": {},  # Missing required parameter
                        "should_pass": False,
                    }
                )

        test_cases[op_name] = cases

    return test_cases


@pytest.fixture(scope="session")
def quirks_test_cases(api_definition) -> Dict[str, List[Dict[str, Any]]]:
    """Generate test cases for API quirks based on quirks configuration."""
    # This would read from api_quirks.json and generate test cases
    # For methods that have quirks defined
    test_cases = {}

    # Example: Methods that should convert boolean to yes/no
    boolean_to_yesno_methods = ["setSMS", "setDIDInfo"]  # Example methods

    for method in boolean_to_yesno_methods:
        if method in api_definition["operations"]:
            test_cases[method] = [
                {
                    "name": "boolean_true_to_yes",
                    "input_params": {"enable": True},
                    "expected_params": {"enable": "yes"},
                },
                {
                    "name": "boolean_false_to_no",
                    "input_params": {"enable": False},
                    "expected_params": {"enable": "no"},
                },
            ]

    return test_cases


@pytest.fixture
def validation_test_runner(mock_client):
    """Utility for running validation tests."""

    def run_validation_test(op_name: str, params: Dict[str, Any], should_pass: bool):
        """Run a validation test and return the result."""
        method = getattr(mock_client, op_name)

        if should_pass:
            try:
                method(**params)
                return True, None
            except Exception as e:
                return False, f"Expected success but got error: {e}"
        else:
            try:
                method(**params)
                return False, "Expected validation error but call succeeded"
            except (ValueError, ValidationError):
                return True, None
            except Exception as e:
                return False, f"Expected ValidationError but got: {type(e).__name__}: {e}"

    return run_validation_test


# Performance testing fixtures
@pytest.fixture
def performance_monitor():
    """Monitor for performance testing."""
    import time

    class PerformanceMonitor:
        def __init__(self):
            self.start_time = None
            self.timings = []

        def start(self):
            self.start_time = time.perf_counter()

        def stop(self):
            if self.start_time:
                duration = time.perf_counter() - self.start_time
                self.timings.append(duration)
                self.start_time = None
                return duration

        def average_time(self):
            return sum(self.timings) / len(self.timings) if self.timings else 0

        def max_time(self):
            return max(self.timings) if self.timings else 0

    return PerformanceMonitor()


# Hypothesis-specific fixtures
@pytest.fixture(scope="session")
def hypothesis_strategy_factory(api_definition):
    """Create Hypothesis strategy factory for API definition."""
    from .hypothesis_strategies import APIDefinitionStrategyFactory

    return APIDefinitionStrategyFactory(api_definition)


@pytest.fixture
def hypothesis_settings():
    """Configure Hypothesis settings for API testing."""
    from hypothesis import HealthCheck, settings

    return settings(
        max_examples=50,  # Reasonable default for CI
        deadline=5000,  # 5 seconds per test
        suppress_health_check=[HealthCheck.too_slow],  # Allow slow tests for thorough validation
    )


@pytest.fixture
def property_test_runner(mock_client, hypothesis_strategy_factory):
    """Utility for running property-based tests."""

    class PropertyTestRunner:
        def __init__(self, client, strategy_factory):
            self.client = client
            self.strategy_factory = strategy_factory

        def test_operation_property(self, op_name: str, property_function, **kwargs):
            """
            Test a property for a specific operation.

            Args:
                op_name: Operation name to test
                property_function: Function that takes (method, params) and tests a property
                **kwargs: Additional arguments for strategy generation
            """
            if op_name not in self.strategy_factory.api_definition.get("operations", {}):
                pytest.skip(f"Operation {op_name} not found in API definition")

            method = getattr(self.client, op_name)
            strategy = self.strategy_factory.build_operation_strategy(op_name, **kwargs)

            # This would be used with @given(strategy) in actual tests
            return strategy, method

        def validate_parameter_constraints(self, op_name: str, params: Dict[str, Any]) -> bool:
            """
            Validate that parameters meet the constraints defined in API definition.

            Args:
                op_name: Operation name
                params: Parameter dictionary to validate

            Returns:
                True if parameters are valid according to API definition
            """
            if op_name not in self.strategy_factory.api_definition.get("operations", {}):
                return False

            op_spec = self.strategy_factory.api_definition["operations"][op_name]
            param_specs = op_spec.get("parameters", {})

            for param_name, param_value in params.items():
                if param_name not in param_specs:
                    continue  # Allow extra parameters (will be filtered by quirks)

                param_spec = param_specs[param_name]

                # Check required parameters
                if param_spec.get("required", False) and param_value is None:
                    return False

                # Check type constraints
                param_type = param_spec.get("type", "string")
                if param_type == "string" and not isinstance(param_value, str):
                    # Allow type coercion for non-strings
                    continue
                elif param_type == "integer":
                    try:
                        int_val = int(param_value)
                        # Check range constraints
                        if "minimum" in param_spec and int_val < param_spec["minimum"]:
                            return False
                        if "maximum" in param_spec and int_val > param_spec["maximum"]:
                            return False
                    except (ValueError, TypeError):
                        return False

                # Check enum constraints
                if enum_values := param_spec.get("enum"):
                    if param_value not in enum_values:
                        return False

                # Check string length constraints
                if param_type == "string" and isinstance(param_value, str):
                    if "minLength" in param_spec and len(param_value) < param_spec["minLength"]:
                        return False
                    if "maxLength" in param_spec and len(param_value) > param_spec["maxLength"]:
                        return False

            return True

        def assert_validation_consistency(
            self, op_name: str, params: Dict[str, Any], should_pass: bool
        ):
            """
            Assert that validation behaves consistently with expectations.

            Args:
                op_name: Operation name
                params: Parameters to test
                should_pass: Whether validation should pass
            """
            method = getattr(self.client, op_name)

            if should_pass:
                try:
                    result = method(validate=True, **params)
                    assert isinstance(result, dict), f"Expected dict result for {op_name}"
                except Exception as e:
                    pytest.fail(f"Expected {op_name} to succeed with {params}, but got: {e}")
            else:
                with pytest.raises((ValueError, ValidationError)):
                    method(validate=True, **params)

    return PropertyTestRunner(mock_client, hypothesis_strategy_factory)


@pytest.fixture
def cross_parameter_validator(api_definition):
    """Validator for cross-parameter constraints."""

    class CrossParameterValidator:
        def __init__(self, api_def):
            self.api_definition = api_def

        def validate_date_range(self, params: Dict[str, Any]) -> bool:
            """Validate date range parameters."""
            if "date_from" in params and "date_to" in params:
                try:
                    from datetime import datetime

                    date_from = datetime.strptime(params["date_from"], "%Y-%m-%d")
                    date_to = datetime.strptime(params["date_to"], "%Y-%m-%d")
                    return date_from <= date_to
                except (ValueError, TypeError):
                    return False
            return True

        def validate_pagination(self, params: Dict[str, Any]) -> bool:
            """Validate pagination parameters."""
            # Limit should be positive
            if "limit" in params:
                try:
                    limit = int(params["limit"])
                    if limit <= 0:
                        return False
                except (ValueError, TypeError):
                    return False

            # Offset should be non-negative
            if "offset" in params:
                try:
                    offset = int(params["offset"])
                    if offset < 0:
                        return False
                except (ValueError, TypeError):
                    return False

            return True

        def validate_all_constraints(self, op_name: str, params: Dict[str, Any]) -> bool:
            """Validate all known cross-parameter constraints."""
            return (
                self.validate_date_range(params)
                and self.validate_pagination(params)
                # Add more cross-parameter validations as needed
            )

    return CrossParameterValidator(api_definition)


@pytest.fixture
def quirks_validator(api_definition):
    """Validator for API quirks application."""

    class QuirksValidator:
        def __init__(self, api_def):
            self.api_definition = api_def
            # Load quirks configuration
            try:
                import json
                from pathlib import Path

                quirks_path = Path(__file__).parent.parent / "src" / "voipms" / "api_quirks.json"
                if quirks_path.exists():
                    with open(quirks_path) as f:
                        self.quirks_config = json.load(f)
                else:
                    self.quirks_config = {"quirks": {}}
            except Exception:
                self.quirks_config = {"quirks": {}}

        def should_apply_boolean_quirk(self, op_name: str, param_name: str) -> bool:
            """Check if boolean quirk should be applied."""
            method_quirks = self.quirks_config.get("quirks", {}).get(op_name, {})
            return param_name in method_quirks.get("yes_no_strings", [])

        def expected_quirk_transformation(
            self, op_name: str, params: Dict[str, Any]
        ) -> Dict[str, Any]:
            """Return expected parameter transformation after quirks."""
            method_quirks = self.quirks_config.get("quirks", {}).get(op_name, {})
            transformed = params.copy()

            # Apply yes/no string conversions
            for param in method_quirks.get("yes_no_strings", []):
                if param in transformed and isinstance(transformed[param], bool):
                    transformed[param] = "yes" if transformed[param] else "no"

            # Apply other quirk transformations...
            # (This would include all the quirk types from your quirks handler)

            return transformed

    return QuirksValidator(api_definition)
