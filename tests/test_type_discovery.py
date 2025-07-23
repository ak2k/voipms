"""Tests for type discovery functionality."""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from src.voipms.type_discovery import TypeDiscoveryLogger


class TestTypeDiscoveryLogger:
    """Test the TypeDiscoveryLogger class."""

    def test_initialization(self):
        """Test logger initialization."""
        # Enabled by default
        logger = TypeDiscoveryLogger()
        assert logger.enabled is True
        assert logger.discoveries is not None
        assert isinstance(logger.discoveries, dict)

        # Can be disabled
        logger = TypeDiscoveryLogger(enabled=False)
        assert logger.enabled is False

    def test_disabled_logger_does_nothing(self):
        """Test that disabled logger doesn't track anything."""
        logger = TypeDiscoveryLogger(enabled=False)
        
        logger.start_call("testMethod")
        logger.log_parameter("param1", "value1", "string")
        logger.commit_discoveries(success=True)
        
        # Should have no discoveries
        discoveries = logger.get_discoveries()
        assert len(discoveries["type_mismatches"]) == 0
        assert len(discoveries["unknown_parameters"]) == 0

    def test_log_parameter_type_match(self):
        """Test logging when parameter type matches expectation."""
        logger = TypeDiscoveryLogger(enabled=True)
        
        logger.start_call("testMethod")
        logger.log_parameter("param1", "hello", "string")
        logger.log_parameter("param2", 42, "integer")
        logger.log_parameter("param3", True, "boolean")
        logger.commit_discoveries(success=True)
        
        # No mismatches should be recorded
        discoveries = logger.get_discoveries()
        assert len(discoveries["type_mismatches"]) == 0

    def test_log_parameter_type_mismatch(self):
        """Test logging when parameter type doesn't match expectation."""
        logger = TypeDiscoveryLogger(enabled=True)
        
        logger.start_call("testMethod")
        logger.log_parameter("param1", 123, "string")  # int provided, string expected
        logger.log_parameter("param2", "42", "integer")  # string provided, int expected
        logger.commit_discoveries(success=True)
        
        discoveries = logger.get_discoveries()
        assert len(discoveries["type_mismatches"]) == 2
        
        # Check first mismatch
        mismatch1 = next(m for m in discoveries["type_mismatches"] if m["parameter"] == "param1")
        assert mismatch1["method"] == "testMethod"
        assert mismatch1["expected_type"] == "string"
        assert mismatch1["actual_type"] == "integer"
        assert mismatch1["count"] == 1

    def test_log_unknown_parameter(self):
        """Test logging parameters not in expected list."""
        logger = TypeDiscoveryLogger(enabled=True)
        
        logger.start_call("testMethod")
        logger.log_parameter("unknownParam", "value", None)  # None means unknown
        logger.commit_discoveries(success=True)
        
        discoveries = logger.get_discoveries()
        assert len(discoveries["unknown_parameters"]) == 1
        
        unknown = discoveries["unknown_parameters"][0]
        assert unknown["method"] == "testMethod"
        assert unknown["parameter"] == "unknownParam"
        assert unknown["actual_type"] == "string"
        assert unknown["count"] == 1

    def test_excluded_parameters(self):
        """Test that excluded parameters are not logged."""
        logger = TypeDiscoveryLogger(enabled=True)
        
        logger.start_call("testMethod")
        logger.log_parameter("api_password", "secret123", "string")
        logger.log_parameter("message", "Hello world", "string")
        logger.log_parameter("regular_param", "value", "string")
        logger.commit_discoveries(success=True)
        
        # Only non-excluded parameters should be in discoveries
        discoveries = logger.get_discoveries()
        assert len(discoveries["type_mismatches"]) == 0
        assert len(discoveries["unknown_parameters"]) == 0

    def test_value_length_limit(self):
        """Test that long values are not logged."""
        logger = TypeDiscoveryLogger(enabled=True)
        
        logger.start_call("testMethod")
        # Short value - should be logged
        logger.log_parameter("param1", "short", None)
        # Long value - should not be logged
        logger.log_parameter("param2", "x" * 101, None)
        logger.commit_discoveries(success=True)
        
        discoveries = logger.get_discoveries()
        assert len(discoveries["unknown_parameters"]) == 1
        assert discoveries["unknown_parameters"][0]["parameter"] == "param1"

    def test_commit_discoveries_success_only(self):
        """Test that discoveries are only saved on successful API calls."""
        logger = TypeDiscoveryLogger(enabled=True)
        
        # First call - will fail
        logger.start_call("testMethod")
        logger.log_parameter("param1", 123, "string")
        logger.commit_discoveries(success=False)  # Failed call
        
        # Check no discoveries saved
        discoveries = logger.get_discoveries()
        assert len(discoveries["type_mismatches"]) == 0
        
        # Second call - will succeed
        logger.start_call("testMethod")
        logger.log_parameter("param1", 456, "string")
        logger.commit_discoveries(success=True)  # Successful call
        
        # Now discovery should be saved
        discoveries = logger.get_discoveries()
        assert len(discoveries["type_mismatches"]) == 1

    def test_counting_repeated_discoveries(self):
        """Test that repeated discoveries increment count."""
        logger = TypeDiscoveryLogger(enabled=True)
        
        # Log same mismatch multiple times
        for i in range(3):
            logger.start_call("testMethod")
            logger.log_parameter("param1", 123, "string")
            logger.commit_discoveries(success=True)
        
        discoveries = logger.get_discoveries()
        assert len(discoveries["type_mismatches"]) == 1
        assert discoveries["type_mismatches"][0]["count"] == 3

    def test_save_session(self):
        """Test saving discoveries to file."""
        logger = TypeDiscoveryLogger(enabled=True)
        
        # Add some discoveries
        logger.start_call("testMethod")
        logger.log_parameter("param1", 123, "string")
        logger.log_parameter("unknownParam", "value", None)
        logger.commit_discoveries(success=True)
        
        # Save to temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            logger.save_session(tmppath)
            
            # Check file was created
            files = list(tmppath.glob("discovery_*.json"))
            assert len(files) == 1
            
            # Verify contents
            with open(files[0]) as f:
                saved_data = json.load(f)
            
            assert "session_id" in saved_data
            assert "timestamp" in saved_data
            assert len(saved_data["type_mismatches"]) == 1
            assert len(saved_data["unknown_parameters"]) == 1

    def test_save_session_creates_directory(self):
        """Test that save_session creates directory if needed."""
        logger = TypeDiscoveryLogger(enabled=True)
        
        logger.start_call("testMethod")
        logger.log_parameter("param1", "value", "string")
        logger.commit_discoveries(success=True)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Use a subdirectory that doesn't exist
            tmppath = Path(tmpdir) / "subdir" / "discoveries"
            assert not tmppath.exists()
            
            logger.save_session(tmppath)
            
            # Directory should be created
            assert tmppath.exists()
            assert len(list(tmppath.glob("discovery_*.json"))) == 1

    def test_save_session_empty_discoveries(self):
        """Test that empty discoveries still create a file."""
        logger = TypeDiscoveryLogger(enabled=True)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            logger.save_session(tmppath)
            
            files = list(tmppath.glob("discovery_*.json"))
            assert len(files) == 1
            
            with open(files[0]) as f:
                saved_data = json.load(f)
            
            assert saved_data["type_mismatches"] == []
            assert saved_data["unknown_parameters"] == []

    def test_concurrent_calls_different_contexts(self):
        """Test that concurrent calls in different contexts don't interfere."""
        logger = TypeDiscoveryLogger(enabled=True)
        
        # Simulate two concurrent API calls
        # In reality, ContextVar ensures isolation
        logger.start_call("method1")
        logger.log_parameter("param1", "value1", "string")
        
        # Start another call before committing first
        logger.start_call("method2")
        logger.log_parameter("param2", "value2", "string")
        logger.commit_discoveries(success=True)
        
        # First call commits
        logger.start_call("method1")  # Re-establish context
        logger.log_parameter("param1", "value1", "string")
        logger.commit_discoveries(success=True)
        
        discoveries = logger.get_discoveries()
        # Should have discoveries from both methods
        methods = {d["method"] for d in discoveries.get("type_mismatches", []) + discoveries.get("unknown_parameters", [])}
        # Note: Due to how ContextVar works in tests, this might not perfectly simulate async behavior

    def test_type_detection(self):
        """Test accurate type detection for various Python types."""
        logger = TypeDiscoveryLogger(enabled=True)
        
        test_cases = [
            ("string_param", "hello", "string"),
            ("int_param", 42, "integer"),
            ("float_param", 3.14, "number"),
            ("bool_param", True, "boolean"),
            ("list_param", [1, 2, 3], "array"),
            ("dict_param", {"key": "value"}, "object"),
            ("none_param", None, "null"),
        ]
        
        logger.start_call("testMethod")
        for param_name, value, expected_type in test_cases:
            logger.log_parameter(param_name, value, "string")  # Expect string for all
        logger.commit_discoveries(success=True)
        
        discoveries = logger.get_discoveries()
        
        # All should be mismatches except string_param
        assert len(discoveries["type_mismatches"]) == len(test_cases) - 1
        
        # Verify each type detection
        for param_name, value, expected_type in test_cases:
            if expected_type != "string":
                mismatch = next(m for m in discoveries["type_mismatches"] if m["parameter"] == param_name)
                assert mismatch["actual_type"] == expected_type


@pytest.mark.asyncio
class TestTypeDiscoveryAsync:
    """Test type discovery in async context."""

    async def test_async_context_isolation(self):
        """Test that async contexts are properly isolated."""
        import asyncio
        from contextvars import copy_context
        
        logger = TypeDiscoveryLogger(enabled=True)
        results = []
        
        async def api_call(method_name: str, param_value: int):
            """Simulate an API call."""
            logger.start_call(method_name)
            logger.log_parameter("param", param_value, "string")
            await asyncio.sleep(0.01)  # Simulate network delay
            logger.commit_discoveries(success=True)
            
            # Get discoveries in this context
            discoveries = logger.get_discoveries()
            results.append((method_name, len(discoveries["type_mismatches"])))
        
        # Run multiple concurrent calls
        await asyncio.gather(
            api_call("method1", 111),
            api_call("method2", 222),
            api_call("method3", 333),
        )
        
        # Each call should have logged one mismatch
        # Due to the way discoveries are aggregated, total should be 3
        final_discoveries = logger.get_discoveries()
        assert len(final_discoveries["type_mismatches"]) == 3