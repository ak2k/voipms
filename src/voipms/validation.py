"""
Parameter validation and Pydantic model creation for VoIP.ms API.

This module handles dynamic creation of Pydantic models for API operations
and parameter validation.
"""

import logging
from typing import Annotated, Any, Dict, Optional, Type

from pydantic import BaseModel, BeforeValidator, Field, create_model

from .types import (
    boolean_01_validator,
    boolean_true_false_validator,
    boolean_yes_no_validator,
    create_integer_string_validator,
    create_numeric_string_validator,
    numeric_string_validator,
)

logger = logging.getLogger(__name__)


class ModelFactory:
    """Factory for creating Pydantic models for API operations."""

    # Type mapping from JSON schema to Python types
    TYPE_MAP = {
        "string": str,
        "integer": int,
        "number": float,
        "boolean": bool,
        "array": list,
        "object": dict,
    }

    def __init__(self):
        self._model_cache: Dict[str, Type[BaseModel]] = {}

    def get_or_create_model(self, op_name: str, op_spec: Dict[str, Any]) -> Type[BaseModel]:
        """Get or create a Pydantic model for operation parameters."""
        if op_name in self._model_cache:
            return self._model_cache[op_name]

        # Build field definitions
        fields = {}
        param_specs = op_spec.get("parameters", {})

        for param_name, param_spec in param_specs.items():
            fields[param_name] = self._create_field(param_name, param_spec)

        # Create the model dynamically with configuration
        model = create_model(
            f"{op_name}Params",
            __base__=BaseModel,
            __config__={
                "extra": "forbid",  # Don't allow extra fields
                "validate_assignment": True,
                "use_enum_values": True,
                "str_strip_whitespace": True,  # Auto-strip whitespace from strings
            },
            **fields,
        )

        self._model_cache[op_name] = model
        return model

    def _create_field(self, param_name: str, param_spec: Dict[str, Any]) -> tuple:
        """Create a Pydantic field definition from parameter specification."""
        # Get the Python type
        param_type = param_spec.get("type", "string")
        python_type = self.TYPE_MAP.get(param_type, str)

        # Create field with validation
        field_kwargs = {
            "description": param_spec.get("description", ""),
        }

        # Add pattern validation if specified
        if pattern := param_spec.get("pattern"):
            field_kwargs["pattern"] = pattern

        # Add string length constraints
        if "minLength" in param_spec:
            field_kwargs["min_length"] = param_spec["minLength"]
        if "maxLength" in param_spec:
            field_kwargs["max_length"] = param_spec["maxLength"]

        # Handle numeric constraints
        if param_type in ["integer", "number"]:
            if "minimum" in param_spec:
                field_kwargs["ge"] = param_spec["minimum"]
            if "maximum" in param_spec:
                field_kwargs["le"] = param_spec["maximum"]
        # For string parameters with numeric constraints
        elif param_type == "string" and ("minimum" in param_spec or "maximum" in param_spec):
            python_type = self._create_numeric_string_type(param_spec)

        # Handle enum validation
        if enum_values := param_spec.get("enum"):
            python_type = self._create_enum_type(python_type, enum_values, field_kwargs)

        # Set default based on required status
        if param_spec.get("required", False):
            field_kwargs["default"] = ...  # Required field
        else:
            field_kwargs["default"] = None
            python_type = Optional[python_type]

        return (python_type, Field(**field_kwargs))

    def _create_numeric_string_type(self, param_spec: Dict[str, Any]) -> Any:
        """Create appropriate numeric string validator type."""
        minimum = param_spec.get("minimum")
        maximum = param_spec.get("maximum")

        # Determine if this should be integer or float validation
        examples = param_spec.get("examples", [])
        use_integer = (
            isinstance(minimum, int)
            and isinstance(maximum, int)
            and all(str(ex).replace(".", "").isdigit() for ex in examples if ex)
        )

        if use_integer:
            validator = create_integer_string_validator(minimum, maximum)
        else:
            validator = create_numeric_string_validator(minimum, maximum)

        # Use Annotated type with BeforeValidator
        return Annotated[str, BeforeValidator(validator)]

    def _create_enum_type(
        self, base_type: Type, enum_values: list, field_kwargs: Dict[str, Any]
    ) -> Any:
        """Create appropriate enum type with validators."""
        # For string enums, we can use Literal type for better validation
        if base_type is str and all(isinstance(v, str) for v in enum_values):
            from typing import Literal

            # Check for boolean-like enums and add validators
            if set(enum_values) == {"0", "1"} or set(enum_values) == {"1", "0"}:
                # Use Literal type with BeforeValidator for conversions
                field_kwargs["description"] = (
                    field_kwargs.get("description", "")
                    + " (accepts: true/false, yes/no, on/off, 0/1, boolean)"
                )
                return Annotated[Literal[tuple(enum_values)], BeforeValidator(boolean_01_validator)]

            elif set(enum_values) == {"true", "false"} or set(enum_values) == {"false", "true"}:
                field_kwargs["description"] = (
                    field_kwargs.get("description", "")
                    + " (accepts: true/false, yes/no, on/off, 1/0, boolean)"
                )
                return Annotated[
                    Literal[tuple(enum_values)], BeforeValidator(boolean_true_false_validator)
                ]

            elif set(enum_values) == {"yes", "no"} or set(enum_values) == {"no", "yes"}:
                field_kwargs["description"] = (
                    field_kwargs.get("description", "")
                    + " (accepts: yes/no, true/false, on/off, 1/0, boolean)"
                )
                return Annotated[
                    Literal[tuple(enum_values)], BeforeValidator(boolean_yes_no_validator)
                ]

            elif all(v.isdigit() for v in enum_values):
                # For numeric string enums like ["1", "2", "3"], accept integers
                field_kwargs["description"] = (
                    field_kwargs.get("description", "") + " (accepts: numeric values)"
                )
                return Annotated[
                    Literal[tuple(enum_values)], BeforeValidator(numeric_string_validator)
                ]
            else:
                return Literal[tuple(enum_values)]

        return base_type
