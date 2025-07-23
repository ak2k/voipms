"""
Data-driven Hypothesis strategies for VoIP.ms API testing.

This module automatically generates Hypothesis testing strategies
from the API definition, requiring zero manual maintenance.
"""

from datetime import datetime, timedelta
from typing import Any, Dict

from hypothesis import strategies as st


class APIDefinitionStrategyFactory:
    """Factory for creating Hypothesis strategies from API definition parameters."""

    def __init__(self, api_definition: Dict[str, Any]):
        self.api_definition = api_definition
        self._strategy_cache = {}

    def build_parameter_strategy(
        self, param_spec: Dict[str, Any], include_invalid: bool = True
    ) -> st.SearchStrategy:
        """
        Build a Hypothesis strategy for a parameter specification.

        Args:
            param_spec: Parameter specification from API definition
            include_invalid: Whether to include invalid values for testing validation

        Returns:
            Hypothesis strategy that generates valid and optionally invalid values
        """
        param_type = param_spec.get("type", "string")
        required = param_spec.get("required", False)

        # Cache key for performance
        cache_key = (
            param_type,
            required,
            str(param_spec.get("enum")),
            param_spec.get("minimum"),
            param_spec.get("maximum"),
            param_spec.get("minLength"),
            param_spec.get("maxLength"),
            param_spec.get("pattern"),
            include_invalid,
        )

        if cache_key in self._strategy_cache:
            return self._strategy_cache[cache_key]

        if param_type == "string":
            strategy = self._build_string_strategy(param_spec, include_invalid)
        elif param_type == "integer":
            strategy = self._build_integer_strategy(param_spec, include_invalid)
        elif param_type == "number":
            strategy = self._build_number_strategy(param_spec, include_invalid)
        elif param_type == "boolean":
            strategy = self._build_boolean_strategy(param_spec, include_invalid)
        elif param_type == "array":
            strategy = self._build_array_strategy(param_spec, include_invalid)
        else:
            # Default to string for unknown types
            strategy = self._build_string_strategy(param_spec, include_invalid)

        # Handle optional parameters
        if not required:
            strategy = st.one_of(strategy, st.none())

        self._strategy_cache[cache_key] = strategy
        return strategy

    def _build_string_strategy(
        self, param_spec: Dict[str, Any], include_invalid: bool
    ) -> st.SearchStrategy:
        """Build strategy for string parameters."""
        strategies = []

        # Handle enum values
        if enum_values := param_spec.get("enum"):
            # Valid enum values
            strategies.append(st.sampled_from(enum_values))

            if include_invalid:
                # Invalid enum values - strings not in the enum
                invalid_enum = st.text().filter(lambda x: x not in enum_values and len(x) > 0)
                strategies.append(invalid_enum)
        else:
            # Regular string generation
            min_size = param_spec.get("minLength", 0)
            max_size = param_spec.get("maxLength", 100)  # Reasonable default

            # Valid strings within constraints
            strategies.append(st.text(min_size=min_size, max_size=max_size))

            if include_invalid and (min_size > 0 or max_size < 1000):
                # Invalid length strings
                if min_size > 0:
                    strategies.append(st.text(max_size=min_size - 1))
                if max_size < 1000:
                    strategies.append(st.text(min_size=max_size + 1, max_size=max_size + 50))

        # Handle pattern validation
        if pattern := param_spec.get("pattern"):
            try:
                # Generate strings that match the pattern
                # Note: This is simplified - full regex generation is complex
                if pattern == r"^\d+$":  # Common numeric string pattern
                    strategies.append(st.from_regex(r"\d{1,10}"))
                    if include_invalid:
                        strategies.append(
                            st.text().filter(lambda x: not x.isdigit() and len(x) > 0)
                        )
                elif pattern == r"^[a-zA-Z0-9]+$":  # Alphanumeric pattern
                    strategies.append(st.from_regex(r"[a-zA-Z0-9]{1,20}"))
                    if include_invalid:
                        strategies.append(
                            st.text().filter(lambda x: not x.isalnum() and len(x) > 0)
                        )
            except Exception:
                # If regex is too complex, fall back to basic text
                pass

        # Special string types based on parameter name
        param_name = param_spec.get("name", "").lower()
        if "email" in param_name:
            strategies.append(st.emails())
            if include_invalid:
                strategies.append(st.text().filter(lambda x: "@" not in x and len(x) > 0))
        elif "date" in param_name:
            # Date strings in YYYY-MM-DD format
            strategies.append(self._date_string_strategy())
            if include_invalid:
                strategies.append(st.sampled_from(["invalid-date", "2023-13-01", "2023-02-30"]))
        elif "timezone" in param_name:
            strategies.append(
                st.sampled_from(
                    [
                        "UTC",
                        "America/New_York",
                        "Europe/London",
                        "Asia/Tokyo",
                        "America/Los_Angeles",
                        "Australia/Sydney",
                    ]
                )
            )
            if include_invalid:
                strategies.append(st.sampled_from(["Invalid/Timezone", "Not_A_Zone"]))

        # Common edge cases for strings
        if include_invalid:
            strategies.extend(
                [
                    st.just(""),  # Empty string
                    st.just(" "),  # Whitespace only
                    st.just("\n\t"),  # Control characters
                    st.text().filter(lambda x: len(x) > 1000),  # Very long strings
                ]
            )

        return st.one_of(strategies) if len(strategies) > 1 else strategies[0]

    def _build_integer_strategy(
        self, param_spec: Dict[str, Any], include_invalid: bool
    ) -> st.SearchStrategy:
        """Build strategy for integer parameters."""
        minimum = param_spec.get("minimum", -1000)
        maximum = param_spec.get("maximum", 1000)

        strategies = [
            # Valid integers within range
            st.integers(min_value=minimum, max_value=maximum)
        ]

        if include_invalid:
            # Invalid integers outside range
            if minimum > -1000000:
                strategies.append(st.integers(min_value=minimum - 100, max_value=minimum - 1))
            if maximum < 1000000:
                strategies.append(st.integers(min_value=maximum + 1, max_value=maximum + 100))

        # Edge cases
        strategies.extend(
            [
                st.just(0),  # Zero
                st.just(minimum) if minimum is not None else st.just(-1),  # Boundary values
                st.just(maximum) if maximum is not None else st.just(1),
            ]
        )

        return st.one_of(strategies)

    def _build_number_strategy(
        self, param_spec: Dict[str, Any], include_invalid: bool
    ) -> st.SearchStrategy:
        """Build strategy for number (float) parameters."""
        minimum = param_spec.get("minimum", -1000.0)
        maximum = param_spec.get("maximum", 1000.0)

        strategies = [
            # Valid floats within range
            st.floats(min_value=minimum, max_value=maximum, allow_nan=False, allow_infinity=False)
        ]

        if include_invalid:
            # Invalid floats outside range
            if minimum > -1000000:
                strategies.append(st.floats(min_value=minimum - 100, max_value=minimum - 0.01))
            if maximum < 1000000:
                strategies.append(st.floats(min_value=maximum + 0.01, max_value=maximum + 100))

            # Special invalid values
            strategies.extend(
                [
                    st.just(float("nan")),
                    st.just(float("inf")),
                    st.just(float("-inf")),
                ]
            )

        return st.one_of(strategies)

    def _build_boolean_strategy(
        self, param_spec: Dict[str, Any], include_invalid: bool
    ) -> st.SearchStrategy:
        """Build strategy for boolean parameters."""
        strategies = [
            st.booleans(),  # True/False
        ]

        # Boolean-like values that should be accepted
        boolean_like_values = [
            1,
            0,  # Integer booleans
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

        strategies.append(st.sampled_from(boolean_like_values))

        if include_invalid:
            # Invalid boolean values
            invalid_booleans = [
                "maybe",
                "sometimes",
                "2",
                "-1",
                "TRUE",
                "FALSE",
                "YES",
                "NO",
                "enabled",
                "disabled",
            ]
            strategies.append(st.sampled_from(invalid_booleans))

        return st.one_of(strategies)

    def _build_array_strategy(
        self, param_spec: Dict[str, Any], include_invalid: bool
    ) -> st.SearchStrategy:
        """Build strategy for array parameters."""
        # Most VoIP.ms arrays are simple lists of strings or numbers
        item_type = param_spec.get("items", {}).get("type", "string")

        if item_type == "string":
            item_strategy = st.text(min_size=1, max_size=20)
        elif item_type == "integer":
            item_strategy = st.integers()
        else:
            item_strategy = st.text()

        strategies = [
            st.lists(item_strategy, min_size=0, max_size=10),  # Valid arrays
        ]

        if include_invalid:
            # Invalid array types (if the API expects arrays but gets other types)
            strategies.extend(
                [
                    st.text(),  # String instead of array
                    st.integers(),  # Integer instead of array
                    st.dictionaries(st.text(), st.text()),  # Dict instead of array
                ]
            )

        return st.one_of(strategies)

    def _date_string_strategy(self) -> st.SearchStrategy:
        """Generate valid date strings in YYYY-MM-DD format."""
        return st.dates(
            min_value=datetime(2020, 1, 1).date(), max_value=datetime(2030, 12, 31).date()
        ).map(lambda d: d.strftime("%Y-%m-%d"))

    def build_operation_strategy(
        self, op_name: str, include_invalid: bool = True
    ) -> st.SearchStrategy:
        """
        Build a strategy that generates parameter dictionaries for an operation.

        Args:
            op_name: Operation name from API definition
            include_invalid: Whether to include invalid parameter combinations

        Returns:
            Strategy that generates parameter dictionaries
        """
        if op_name not in self.api_definition.get("operations", {}):
            raise ValueError(f"Operation {op_name} not found in API definition")

        op_spec = self.api_definition["operations"][op_name]
        parameters = op_spec.get("parameters", {})

        if not parameters:
            # Operation has no parameters
            return st.just({})

        # Build strategies for each parameter
        param_strategies = {}
        required_params = []
        optional_params = []

        for param_name, param_spec in parameters.items():
            # Skip API credentials (handled by client)
            if param_name in ["api_username", "api_password"]:
                continue

            strategy = self.build_parameter_strategy(param_spec, include_invalid)
            param_strategies[param_name] = strategy

            if param_spec.get("required", False):
                required_params.append(param_name)
            else:
                optional_params.append(param_name)

        # Generate parameter combinations
        @st.composite
        def parameter_dict(draw):
            params = {}

            # Always include required parameters
            for param_name in required_params:
                params[param_name] = draw(param_strategies[param_name])

            # Randomly include optional parameters
            for param_name in optional_params:
                if draw(st.booleans()):  # 50% chance to include each optional param
                    value = draw(param_strategies[param_name])
                    if value is not None:  # Don't include None values
                        params[param_name] = value

            return params

        return parameter_dict()

    def build_cross_parameter_strategy(self, op_name: str) -> st.SearchStrategy:
        """
        Build strategies that test cross-parameter validation (e.g., date ranges).

        Args:
            op_name: Operation name from API definition

        Returns:
            Strategy that generates parameter combinations that test relationships
        """
        if op_name not in self.api_definition.get("operations", {}):
            return st.just({})

        op_spec = self.api_definition["operations"][op_name]
        parameters = op_spec.get("parameters", {})

        # Look for common cross-parameter patterns
        has_date_range = "date_from" in parameters and "date_to" in parameters
        has_pagination = any(p in parameters for p in ["limit", "offset", "start", "count"])

        strategies = []

        if has_date_range:
            strategies.append(self._build_date_range_strategy())

        if has_pagination:
            strategies.append(self._build_pagination_strategy(parameters))

        # Default to regular operation strategy
        if not strategies:
            return self.build_operation_strategy(op_name, include_invalid=False)

        return st.one_of(strategies)

    def _build_date_range_strategy(self) -> st.SearchStrategy:
        """Build strategy for testing date range parameters."""

        @st.composite
        def date_range_params(draw):
            # Generate two dates
            base_date = draw(
                st.dates(
                    min_value=datetime(2020, 1, 1).date(), max_value=datetime(2030, 12, 31).date()
                )
            )

            # Sometimes generate valid ranges, sometimes invalid
            if draw(st.booleans()):
                # Valid range: date_from <= date_to
                days_diff = draw(st.integers(min_value=0, max_value=365))
                date_from = base_date
                date_to = base_date + timedelta(days=days_diff)
            else:
                # Invalid range: date_from > date_to
                days_diff = draw(st.integers(min_value=1, max_value=30))
                date_from = base_date + timedelta(days=days_diff)
                date_to = base_date

            return {
                "date_from": date_from.strftime("%Y-%m-%d"),
                "date_to": date_to.strftime("%Y-%m-%d"),
            }

        return date_range_params()

    def _build_pagination_strategy(self, parameters: Dict[str, Any]) -> st.SearchStrategy:
        """Build strategy for testing pagination parameters."""

        @st.composite
        def pagination_params(draw):
            params = {}

            if "limit" in parameters:
                # Test various limit values
                limit = draw(
                    st.one_of(
                        st.integers(min_value=1, max_value=1000),  # Valid limits
                        st.integers(min_value=-10, max_value=0),  # Invalid limits
                        st.just(0),  # Edge case
                    )
                )
                params["limit"] = limit

            if "offset" in parameters:
                # Offset should be non-negative
                offset = draw(
                    st.one_of(
                        st.integers(min_value=0, max_value=10000),  # Valid offsets
                        st.integers(min_value=-100, max_value=-1),  # Invalid offsets
                    )
                )
                params["offset"] = offset

            return params

        return pagination_params()
