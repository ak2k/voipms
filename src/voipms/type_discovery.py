"""
Type discovery system for VoIP.ms API client.

This module logs parameter types and values from successful API calls
to help discover patterns and improve type definitions.
"""

import json
import logging
import os
import secrets
import threading
import time
from collections import Counter, defaultdict
from contextvars import ContextVar
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass
class ParameterDiscovery:
    """Stores discovery information for a single parameter."""

    expected_type: Optional[str]  # None means unknown parameter
    actual_types: Counter = field(default_factory=Counter)  # JSON type -> count
    sample_values: Counter = field(default_factory=Counter)  # value -> count
    
    @property
    def is_unknown(self) -> bool:
        """Check if this is an unknown parameter."""
        return self.expected_type is None
    
    @property
    def has_mismatches(self) -> bool:
        """Check if there are type mismatches."""
        if self.is_unknown:
            return False
        return any(t != self.expected_type for t in self.actual_types)
    
    @property
    def total_observations(self) -> int:
        """Get total number of observations."""
        return sum(self.actual_types.values())


@dataclass
class PendingDiscovery:
    """Holds parameter data until we know if the API call succeeded."""

    method: str
    parameters: Dict[str, Tuple[Any, Optional[str]]] = field(default_factory=dict)


class TypeDiscoveryLogger:
    """
    Logs type discoveries from API usage.

    Thread-safe and async-safe implementation that only logs successful calls.
    """

    # Minimal exclusion list - only truly sensitive/unhelpful parameters
    EXCLUDED_PARAMS = {
        # Authentication credentials
        "api_password",
        "password",
        "confirm_password",
        "queue_password",
        # Actual message content
        "message",
        "sms",
        "email_attach_file",
        "transcription",
        "unavailable_message_recording",
        # Descriptions and notes (free-form text)
        "description",
        "note",
        "notes",
        "cancelcomment",
        # Actual file/binary content
        "file",
        "recording_file",
        "base64",
    }

    def __init__(self, enabled: bool = True):
        """Initialize the type discovery logger."""
        self.enabled = enabled
        self.session_start = time.time()

        # Thread safety
        self._lock = threading.Lock()
        
        # Single source of truth: (method, param) -> ParameterDiscovery
        self.discoveries: Dict[Tuple[str, str], ParameterDiscovery] = {}

        # Async-safe pending discovery storage using ContextVar
        self._pending_context: ContextVar[Optional[PendingDiscovery]] = ContextVar(
            "pending_discovery", default=None
        )

    def start_call(self, method: str) -> None:
        """Start tracking a new API call (async-safe)."""
        if not self.enabled:
            return

        # Each async context gets its own pending discovery
        self._pending_context.set(PendingDiscovery(method=method))

    def log_parameter(self, param: str, value: Any, expected_type: Optional[str]) -> None:
        """Stage a parameter for logging (pending success)."""
        if not self.enabled:
            return

        pending = self._pending_context.get()
        if pending and self._should_track_value(param, value):
            pending.parameters[param] = (value, expected_type)

    def commit_discoveries(self, success: bool) -> None:
        """Commit or discard pending discoveries based on API call result."""
        if not self.enabled:
            return

        pending = self._pending_context.get()
        if not pending:
            return

        if success:
            # Only log discoveries from successful calls
            with self._lock:
                for param, (value, expected_type) in pending.parameters.items():
                    key = (pending.method, param)
                    actual_type = self._get_json_type(value)

                    # Get or create discovery
                    if key not in self.discoveries:
                        self.discoveries[key] = ParameterDiscovery(expected_type)

                    discovery = self.discoveries[key]
                    
                    # Track actual type
                    discovery.actual_types[actual_type] += 1

                    # Track sample value
                    discovery.sample_values[str(value)] += 1

        # Clear pending regardless of success
        self._pending_context.set(None)


    def _should_track_value(self, param_name: str, value: Any) -> bool:
        """Determine if we should track this specific value."""
        # Check exclusion list
        if param_name in self.EXCLUDED_PARAMS:
            return False

        # Check basic type - allow more types including None, list, dict
        if value is not None and not isinstance(value, (str, int, float, bool, list, dict)):
            return False

        # Size check
        str_val = str(value)
        return len(str_val) <= 100
    
    def _get_json_type(self, value: Any) -> str:
        """Get JSON-compatible type name for a value."""
        if value is None:
            return "null"
        elif isinstance(value, bool):
            return "boolean"
        elif isinstance(value, int):
            return "integer"
        elif isinstance(value, float):
            return "number"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, list):
            return "array"
        elif isinstance(value, dict):
            return "object"
        else:
            return "unknown"

    def save_session(self, output_dir: Optional[Path] = None) -> None:
        """Save discoveries to disk on exit."""
        if not self.enabled:
            return

        try:
            # Use default directory if not specified
            if output_dir is None:
                output_dir = Path.home() / ".voipms" / "discoveries"

            output_dir.mkdir(parents=True, exist_ok=True)

            # Create unique filename
            from datetime import datetime
            timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            random_suffix = secrets.token_hex(4)
            filename = f"discovery_{timestamp_str}_{random_suffix}.json"

            # Get discoveries in standard format
            discoveries = self.get_discoveries()
            
            # Convert discoveries to JSON-serializable format
            output = {
                "version": "1.0",
                "session_id": secrets.token_hex(8),
                "timestamp": timestamp_str,
                "session_start": self.session_start,
                "session_end": time.time(),
                "type_mismatches": discoveries["type_mismatches"],
                "unknown_parameters": discoveries["unknown_parameters"],
            }

            # Write to disk
            output_path = output_dir / filename
            with open(output_path, "w") as f:
                json.dump(output, f, indent=2)

            logger.debug(f"Saved type discoveries to {output_path}")

        except Exception as e:
            logger.warning(f"Failed to save type discoveries: {e}")

    def get_discoveries(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get current discoveries in a format suitable for analysis.
        
        Returns:
            Dictionary with 'type_mismatches' and 'unknown_parameters' lists
        """
        type_mismatches = []
        unknown_parameters = []
        
        with self._lock:
            for (method, param), discovery in self.discoveries.items():
                if discovery.is_unknown:
                    # Unknown parameter - report all observed types
                    for actual_type, count in discovery.actual_types.items():
                        # Get sample values for this type
                        samples = list(discovery.sample_values.keys())[:5]
                        
                        unknown_parameters.append({
                            "method": method,
                            "parameter": param,
                            "actual_type": actual_type,
                            "count": count,
                            "sample_values": samples
                        })
                elif discovery.has_mismatches:
                    # Type mismatches - report types that don't match expected
                    for actual_type, count in discovery.actual_types.items():
                        if actual_type != discovery.expected_type:
                            # Get sample values for this type
                            samples = list(discovery.sample_values.keys())[:5]
                            
                            type_mismatches.append({
                                "method": method,
                                "parameter": param,
                                "expected_type": discovery.expected_type,
                                "actual_type": actual_type,
                                "count": count,
                                "sample_values": samples
                            })
        
        return {
            "type_mismatches": type_mismatches,
            "unknown_parameters": unknown_parameters
        }