"""
Dynamic method generation for VoIP.ms API client.

This module handles creation of API methods from the API definition.
"""

import logging
from functools import wraps
from typing import Any, Callable, Dict

from pydantic import ValidationError

from .validation import ModelFactory

logger = logging.getLogger(__name__)


class MethodFactory:
    """Factory for creating API methods dynamically."""

    def __init__(self, client_instance, debug: bool = False, is_async: bool = False):
        self.client = client_instance
        self.debug = debug
        self.is_async = is_async
        self.model_factory = ModelFactory()

    def create_method(self, op_name: str, op_spec: Dict[str, Any]) -> Callable:
        """Create a method for an API operation."""
        if self.is_async:
            return self._create_async_method(op_name, op_spec)
        else:
            return self._create_sync_method(op_name, op_spec)

    def _process_parameters(
        self, op_name: str, op_spec: Dict[str, Any], validate: bool, kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process and validate parameters for a method call."""
        if validate:
            # Get or create Pydantic model for this operation
            param_model = self.model_factory.get_or_create_model(op_name, op_spec)

            try:
                # Validate and coerce types using Pydantic
                validated_params = param_model(**kwargs)
                # Convert to dict, excluding None values
                params_dict = validated_params.model_dump(exclude_none=True)
            except ValidationError as e:
                # Format errors with constraint suggestions
                errors = self._format_validation_errors(e, op_spec)
                raise ValueError(
                    f"Parameter validation failed for {op_name}:\n  " + "\n  ".join(errors)
                ) from None
        else:
            # Skip validation, use raw parameters
            params_dict = {k: v for k, v in kwargs.items() if v is not None}

        # Apply extracted HTML defaults before transforms
        params_dict = self._apply_html_defaults(op_name, params_dict, op_spec)

        # Apply parameter transforms from api_definition
        params_dict = self._apply_transforms(op_name, params_dict, op_spec)

        return params_dict

    def _create_sync_method(self, op_name: str, op_spec: Dict[str, Any]) -> Callable:
        """Create a synchronous method."""

        @wraps(self.client._execute)
        def method(validate=True, **kwargs):
            # Start discovery tracking
            if hasattr(self.client, "_type_discovery"):
                self.client._type_discovery.start_call(op_name)

                # Log parameters before validation
                expected_params = op_spec.get("parameters", {})
                for param_name, param_value in kwargs.items():
                    if param_name in expected_params:
                        expected_type = expected_params[param_name].get("type", "string")
                        self.client._type_discovery.log_parameter(
                            param_name, param_value, expected_type
                        )

            params_dict = self._process_parameters(op_name, op_spec, validate, kwargs)

            # Apply retry decorator if enabled
            if self.client.enable_retries and self.client._retry_decorator:
                execute_func = self.client._retry_decorator(self.client._execute)
                return execute_func(op_name, **params_dict)
            else:
                return self.client._execute(op_name, **params_dict)

        # Add docstring
        method.__doc__ = self._generate_method_doc(op_name, op_spec)
        method.__name__ = op_name

        return method

    def _create_async_method(self, op_name: str, op_spec: Dict[str, Any]) -> Callable:
        """Create an asynchronous method."""

        async def method(validate=True, **kwargs):
            # Start discovery tracking
            if hasattr(self.client, "_type_discovery"):
                self.client._type_discovery.start_call(op_name)

                # Log parameters before validation
                expected_params = op_spec.get("parameters", {})
                for param_name, param_value in kwargs.items():
                    if param_name in expected_params:
                        expected_type = expected_params[param_name].get("type", "string")
                        self.client._type_discovery.log_parameter(
                            param_name, param_value, expected_type
                        )

            params_dict = self._process_parameters(op_name, op_spec, validate, kwargs)

            # Apply retry decorator if enabled
            if self.client.enable_retries and self.client._retry_decorator:
                execute_func = self.client._retry_decorator(self.client._execute)
                return await execute_func(op_name, **params_dict)
            else:
                return await self.client._execute(op_name, **params_dict)

        # Add docstring
        method.__doc__ = self._generate_method_doc(op_name, op_spec)
        method.__name__ = op_name

        return method

    def _format_validation_errors(self, e: ValidationError, op_spec: Dict[str, Any]) -> list:
        """Format Pydantic validation errors with helpful constraint information."""
        errors = []
        for error in e.errors():
            field = error["loc"][0]
            msg = error["msg"]

            # Add constraint suggestions based on parameter spec
            param_spec = op_spec.get("parameters", {}).get(field, {})
            constraint_hints = []

            # Add enum suggestions
            if enum_values := param_spec.get("enum"):
                constraint_hints.append(f"valid options: {', '.join(enum_values)}")

            # Add range suggestions
            if "minimum" in param_spec and "maximum" in param_spec:
                constraint_hints.append(f"range: {param_spec['minimum']}-{param_spec['maximum']}")
            elif "minimum" in param_spec:
                constraint_hints.append(f"minimum: {param_spec['minimum']}")
            elif "maximum" in param_spec:
                constraint_hints.append(f"maximum: {param_spec['maximum']}")

            # Add length suggestions
            if "minLength" in param_spec:
                constraint_hints.append(f"min length: {param_spec['minLength']}")
            if "maxLength" in param_spec:
                constraint_hints.append(f"max length: {param_spec['maxLength']}")

            # Add format suggestions
            if format_info := param_spec.get("format"):
                constraint_hints.append(f"format: {format_info}")

            # Combine message with hints
            error_msg = f"{field}: {msg}"
            if constraint_hints:
                error_msg += f" ({'; '.join(constraint_hints)})"

            errors.append(error_msg)

        return errors

    def _apply_html_defaults(
        self, op_name: str, params_dict: Dict[str, Any], op_spec: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply default values extracted from HTML documentation."""
        param_specs = op_spec.get("parameters", {})
        result = params_dict.copy()

        for param_name, param_spec in param_specs.items():
            # Skip if parameter is already provided
            if param_name in result:
                continue

            # Check if parameter has a default value from HTML
            default_value = param_spec.get("default")
            if default_value is not None:
                # Handle special default values
                if default_value == "Today":
                    from datetime import datetime, timezone

                    # Use UTC to ensure consistent behavior across timezones
                    result[param_name] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
                    if self.debug:
                        logger.debug(
                            f"HTML default: {op_name}.{param_name} = {result[param_name]} (today's date)"
                        )
                elif default_value == "50" and param_name in ["limit", "count", "records"]:
                    # Numeric defaults for common pagination parameters
                    result[param_name] = int(default_value)
                    if self.debug:
                        logger.debug(f"HTML default: {op_name}.{param_name} = {result[param_name]}")
                elif isinstance(default_value, str) and default_value.isdigit():
                    # Handle string numeric defaults based on parameter type
                    param_type = param_spec.get("type", "string")
                    if param_type == "integer":
                        result[param_name] = int(default_value)
                    else:
                        result[param_name] = default_value
                    if self.debug:
                        logger.debug(f"HTML default: {op_name}.{param_name} = {result[param_name]}")
                else:
                    # Use default as-is
                    result[param_name] = default_value
                    if self.debug:
                        logger.debug(f"HTML default: {op_name}.{param_name} = {result[param_name]}")

        return result

    def _apply_transforms(
        self, op_name: str, params_dict: Dict[str, Any], op_spec: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply parameter transforms defined in api_definition."""
        param_specs = op_spec.get("parameters", {})
        result = params_dict.copy()
        
        # Apply parameter-level transforms
        for param_name, value in list(result.items()):
            if param_name not in param_specs:
                continue
                
            param_spec = param_specs[param_name]
            if "_transform" not in param_spec:
                continue
                
            transform = param_spec["_transform"]
            transformed_value = self._apply_parameter_transform(param_name, value, transform)
            
            if transformed_value != value:
                result[param_name] = transformed_value
                if self.debug:
                    logger.debug(
                        f"Transform {op_name}.{param_name}: {value} -> {transformed_value} "
                        f"(type: {transform['type']})"
                    )
        
        # Apply operation-level transforms (aliases, defaults, etc.)
        if "_parameter_aliases" in op_spec:
            for old_name, new_name in op_spec["_parameter_aliases"].items():
                if old_name in result:
                    value = result.pop(old_name)
                    result[new_name] = value
                    if self.debug:
                        logger.debug(f"Alias {op_name}: {old_name} -> {new_name}")
        
        if "_smart_defaults" in op_spec:
            for param_name, default_value in op_spec["_smart_defaults"].items():
                if param_name not in result:
                    result[param_name] = default_value
                    if self.debug:
                        logger.debug(f"Smart default {op_name}.{param_name} = {default_value}")
        
        # Apply date validations if present
        if "_date_validations" in op_spec:
            self._validate_dates(op_name, result, op_spec["_date_validations"])
        
        return result
    
    def _apply_parameter_transform(self, param_name: str, value: Any, transform: dict) -> Any:
        """Apply a single parameter transform."""
        transform_type = transform["type"]
        
        if transform_type == "boolean_to_yes_no":
            if isinstance(value, bool):
                return "yes" if value else "no"
        
        elif transform_type == "list_to_semicolon":
            if isinstance(value, list):
                return ";".join(str(item) for item in value)
        
        elif transform_type == "special_value_mapping":
            mapping = transform.get("mapping", {})
            # Handle None values (represented as "__none__" in JSON)
            if value is None and "__none__" in mapping:
                return mapping["__none__"]
            # Handle other mapped values
            elif str(value) in mapping:
                return mapping[str(value)]
        
        return value
    
    def _validate_dates(self, op_name: str, params: Dict[str, Any], date_config: Dict[str, Any]) -> None:
        """Validate date parameters."""
        if "date_from" in params and "date_to" in params:
            try:
                from datetime import datetime
                
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

    def _generate_method_doc(self, op_name: str, op_spec: Dict[str, Any]) -> str:
        """Generate method documentation from spec."""
        doc_parts = [op_spec.get("description", f"Execute {op_name} operation")]

        # Add parameters
        params = op_spec.get("parameters", {})
        if params:
            doc_parts.append("\nParameters:")
            for param_name, param_spec in params.items():
                required = "*" if param_spec.get("required", False) else ""
                param_type = param_spec.get("type", "string")
                description = param_spec.get("description", "")
                doc_parts.append(f"    {param_name}{required} ({param_type}): {description}")

        # Add returns
        returns = op_spec.get("returns", {})
        if returns:
            doc_parts.append(f"\nReturns:\n    {returns.get('description', 'API response')}")

        # Add errors
        errors = op_spec.get("errors", [])
        if errors:
            doc_parts.append(f"\nPossible errors: {', '.join(errors)}")

        return "\n".join(doc_parts)
