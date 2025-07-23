"""
API quirks handling for VoIP.ms client.

This module contains method-specific transformations and fixes
for known API inconsistencies.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

try:
    # Python 3.9+ with files() API
    from importlib.resources import files
except ImportError:
    try:
        # Backport for older Python versions
        from importlib_resources import files
    except ImportError:
        # Fallback for even older versions
        files = None
        try:
            from importlib import resources
        except ImportError:
            import importlib_resources as resources

logger = logging.getLogger(__name__)


class APIQuirksHandler:
    """Handles API-specific quirks and parameter transformations."""
    
    def __init__(self, debug: bool = False, quirks_path: str = 'api_quirks.json'):
        self.debug = debug
        self.quirks_config = self._load_quirks_config(quirks_path)
        self._quirks = self.quirks_config.get('quirks', {})
    
    def _load_quirks_config(self, quirks_path: str) -> Dict[str, Any]:
        """Load quirks configuration from JSON file."""
        # Try as direct path first
        if Path(quirks_path).exists():
            with open(quirks_path) as f:
                return json.load(f)
        
        # Try as package resource
        try:
            import voipms
            
            if files is not None:
                # Modern API (Python 3.9+ or with importlib_resources)
                resource_path = files(voipms) / quirks_path
                return json.loads(resource_path.read_text())
            else:
                # Legacy API (Python 3.7-3.8)
                with resources.path(voipms, quirks_path) as resource_path:
                    with open(resource_path) as f:
                        return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load quirks configuration from {quirks_path}: {e}")
            # Return empty config if file not found
            return {"quirks": {}, "error_code_additions": {}}
    
    def apply_quirks(self, op_name: str, params_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Apply known API quirks and fixes."""
        if op_name not in self._quirks:
            return params_dict

        method_quirks = self._quirks[op_name]
        result = params_dict.copy()

        # Apply yes/no string conversions
        for param in method_quirks.get("yes_no_strings", []):
            if param in result and isinstance(result[param], bool):
                old_value = result[param]
                result[param] = "yes" if result[param] else "no"
                if self.debug:
                    logger.debug(f"API quirk: {op_name}.{param}: {old_value} -> {result[param]}")

        # Apply list to semicolon-separated string conversions
        for param in method_quirks.get("list_to_semicolon", []):
            if param in result and isinstance(result[param], list):
                old_value = result[param]
                result[param] = ";".join(str(item) for item in result[param])
                if self.debug:
                    logger.debug(f"API quirk: {op_name}.{param}: {old_value} -> {result[param]}")

        # Apply special value handling (None → "none", etc.)
        for param, mapping in method_quirks.get("special_values", {}).items():
            if param in result:
                # Handle None values (represented as "__none__" in JSON)
                if result[param] is None and "__none__" in mapping:
                    old_value = result[param]
                    result[param] = mapping["__none__"]
                    if self.debug:
                        logger.debug(f"API quirk: {op_name}.{param}: {old_value} -> {result[param]}")
                # Handle numeric values (JSON keys are strings)
                elif str(result[param]) in mapping:
                    old_value = result[param]
                    result[param] = mapping[str(result[param])]
                    if self.debug:
                        logger.debug(f"API quirk: {op_name}.{param}: {old_value} -> {result[param]}")

        # Apply date validations for methods that need them
        if "date_validations" in method_quirks:
            self._validate_dates(op_name, result, method_quirks["date_validations"])

        # Apply parameter aliases
        for old_name, new_name in method_quirks.get("aliases", {}).items():
            if old_name in result:
                value = result.pop(old_name)
                result[new_name] = value
                if self.debug:
                    logger.debug(f"API quirk: {op_name} parameter {old_name} -> {new_name}")

        # Apply required defaults
        for param, default_value in method_quirks.get("defaults", {}).items():
            if param not in result:
                result[param] = default_value
                if self.debug:
                    logger.debug(f"API quirk: {op_name} added required default {param}={default_value}")

        return result
    
    def _validate_dates(self, op_name: str, params: Dict[str, Any], date_config: Dict[str, Any]) -> None:
        """Validate date parameters."""
        if "date_from" in params and "date_to" in params:
            try:
                date_from = datetime.strptime(params["date_from"], "%Y-%m-%d")
                date_to = datetime.strptime(params["date_to"], "%Y-%m-%d")

                # Check date order
                if date_from > date_to:
                    raise ValueError(f"{op_name}: date_from must be before or equal to date_to")

                # Check future dates
                if date_to > datetime.now():
                    raise ValueError(f"{op_name}: date_to cannot be in the future")

                # Check date range
                if "max_days" in date_config:
                    days_diff = (date_to - date_from).days
                    if days_diff > date_config["max_days"]:
                        raise ValueError(
                            f"{op_name}: Date range cannot exceed {date_config['max_days']} days "
                            f"(got {days_diff} days)"
                        )

            except ValueError as e:
                if "strptime" in str(e):
                    pass  # Invalid date format, let API handle it
                else:
                    raise
    
    def get_quirks_for_method(self, op_name: str) -> Dict[str, Any]:
        """Get quirks configuration for a specific method."""
        return self._quirks.get(op_name, {})