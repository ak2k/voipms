"""
Type validators for VoIP.ms API conversions.

These validators handle boolean-like inputs and numeric conversions
to match the API's expected string representations.
"""

import logging
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


def boolean_string_validator(true_val: str, false_val: str) -> Callable[[Any], str]:
    """
    Create a validator that converts boolean-like values to specified strings.

    Args:
        true_val: String to return for truthy values
        false_val: String to return for falsy values

    Returns:
        A validator function that converts inputs to the specified strings
    """

    def validator(v: Any) -> str:
        """Convert boolean-like values to specified strings."""
        if isinstance(v, bool):
            result = true_val if v else false_val
        elif isinstance(v, int) and v in (0, 1):
            result = true_val if v == 1 else false_val
        elif isinstance(v, str):
            lower_v = v.lower()
            # Accept various truthy values
            if lower_v in ("true", "yes", "on", "1", true_val.lower()):
                result = true_val
            # Accept various falsy values
            elif lower_v in ("false", "no", "off", "0", false_val.lower()):
                result = false_val
            # If already the target value, return as-is
            elif v in (true_val, false_val):
                result = v
            else:
                raise ValueError(f"Must be boolean-like value, got '{v}'")
        else:
            # For other types, convert to string and let Pydantic validate
            result = str(v)

        if logger.isEnabledFor(logging.DEBUG) and result != str(v):
            logger.debug(f"Boolean conversion ({true_val}/{false_val}): {v!r} -> {result!r}")

        return result

    # Set a helpful name for debugging
    validator.__name__ = f"boolean_{true_val}_{false_val}_validator"
    return validator


# Create specific validators using the generic one
boolean_01_validator = boolean_string_validator("1", "0")
boolean_true_false_validator = boolean_string_validator("true", "false")
boolean_yes_no_validator = boolean_string_validator("yes", "no")


def numeric_string_validator(v: Any) -> str:
    """
    Convert numeric values to strings for enum validation.

    Handles special cases:
    - Booleans (True -> "1", False -> "0")
    - Integers and floats -> string representation
    - Strings -> pass through for Pydantic validation
    """
    if isinstance(v, bool):
        # Handle boolean before int check since bool is subclass of int
        result = "1" if v else "0"
    elif isinstance(v, (int, float)):
        result = str(v)
    else:
        # For strings and other types, convert to string
        result = str(v)

    if logger.isEnabledFor(logging.DEBUG) and result != str(v):
        logger.debug(f"Numeric conversion: {v!r} ({type(v).__name__}) -> {result!r}")

    return result


def create_numeric_string_validator(
    minimum: Optional[float] = None, maximum: Optional[float] = None, integer_only: bool = False
) -> Callable[[Any], str]:
    """
    Create a validator for string parameters that should be numeric within constraints.

    Args:
        minimum: Minimum allowed value (inclusive)
        maximum: Maximum allowed value (inclusive)
        integer_only: If True, only accept integer values

    Returns:
        A validator function that validates numeric strings within constraints
    """

    def validate_numeric_string(value: Any) -> str:
        """Validate that a value is numeric and within constraints."""
        if value is None:
            return value

        # Convert to string if not already
        str_value = str(value)

        # Try to parse as number for validation
        try:
            if integer_only:
                numeric_value = int(float(str_value))  # Allow "60.0" -> 60
                if float(str_value) != numeric_value:
                    # Warn if decimal part is being truncated
                    logger.debug(f"Converting {str_value} to integer {numeric_value}")
            else:
                numeric_value = float(str_value)
        except ValueError:
            value_type = "an integer" if integer_only else "numeric"
            raise ValueError(f"Value must be {value_type}, got: {str_value}") from None

        # Check constraints
        if minimum is not None and numeric_value < minimum:
            raise ValueError(f"Value must be >= {minimum}, got: {numeric_value}")
        if maximum is not None and numeric_value > maximum:
            raise ValueError(f"Value must be <= {maximum}, got: {numeric_value}")

        # Return as string (as API expects)
        return str(int(numeric_value)) if integer_only else str_value

    # Set a helpful name for debugging
    type_name = "integer" if integer_only else "numeric"
    validate_numeric_string.__name__ = f"{type_name}_string_{minimum}_{maximum}_validator"
    return validate_numeric_string


def create_integer_string_validator(
    minimum: Optional[int] = None, maximum: Optional[int] = None
) -> Callable[[Any], str]:
    """
    Create a validator for string parameters that should be integers within constraints.

    This is a convenience wrapper around create_numeric_string_validator with integer_only=True.

    Args:
        minimum: Minimum allowed value (inclusive)
        maximum: Maximum allowed value (inclusive)

    Returns:
        A validator function that validates integer strings within constraints
    """
    return create_numeric_string_validator(minimum, maximum, integer_only=True)
