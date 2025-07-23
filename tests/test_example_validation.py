"""
Test that examples in the API definition pass validation.

This test ensures that the examples we show in our API definition
actually work with the parameter types we declare.
"""

import json
from pathlib import Path

import pytest

from voipms.config import VoIPMSConfig
from voipms.validation import ModelFactory


class TestExampleValidation:
    """Test that API definition examples pass their own validation."""

    @pytest.fixture(scope="class")
    def api_definition(self):
        """Load the API definition once for all tests."""
        api_def_path = Path(__file__).parent.parent / "src" / "voipms" / "api_definition.json"
        with open(api_def_path) as f:
            return json.load(f)

    @pytest.fixture(scope="class")
    def model_factory(self):
        """Create a model factory for validation."""
        return ModelFactory()

    def test_all_examples_validate(self, api_definition, model_factory):
        """Test that all parameter examples pass validation."""
        failures = []
        tested_count = 0

        # Check all operations
        for op_name, op_spec in api_definition["operations"].items():
            params = op_spec.get("parameters", {})
            
            # Skip if no parameters
            if not params:
                continue
                
            # Get the validation model for this operation
            try:
                param_model = model_factory.get_or_create_model(op_name, op_spec)
            except Exception as e:
                failures.append({
                    "operation": op_name,
                    "error": f"Failed to create model: {e}",
                    "type": "model_creation"
                })
                continue

            # Test each parameter that has examples
            for param_name, param_spec in params.items():
                examples = param_spec.get("examples", [])
                if not examples:
                    continue

                param_type = param_spec.get("type", "string")
                
                for example in examples:
                    tested_count += 1
                    
                    # Try to validate a minimal call with just this parameter
                    # (we can't test all required params, just this one)
                    test_params = {param_name: example}
                    
                    # Add other required params with dummy values if needed
                    for other_param, other_spec in params.items():
                        if other_param != param_name and other_spec.get("required", False):
                            # Use a reasonable default based on type
                            other_type = other_spec.get("type", "string")
                            if other_type == "integer":
                                test_params[other_param] = 1
                            elif other_type == "boolean":
                                test_params[other_param] = True
                            else:
                                test_params[other_param] = "test"
                    
                    # Try validation
                    try:
                        param_model(**test_params)
                    except Exception as e:
                        # Check if it's specifically about our example parameter
                        error_str = str(e)
                        if param_name in error_str:
                            failures.append({
                                "operation": op_name,
                                "parameter": param_name,
                                "example": example,
                                "declared_type": param_type,
                                "error": error_str,
                                "type": "validation"
                            })

        # Report results
        if failures:
            # Group by error type
            validation_failures = [f for f in failures if f["type"] == "validation"]
            model_failures = [f for f in failures if f["type"] == "model_creation"]
            
            failure_report = [f"\nFound {len(failures)} total failures out of {tested_count} examples tested:"]
            
            if validation_failures:
                failure_report.append(f"\n{len(validation_failures)} validation failures:")
                # Group by similar issues
                type_mismatches = {}
                for f in validation_failures[:20]:  # Show first 20
                    key = f["declared_type"]
                    if key not in type_mismatches:
                        type_mismatches[key] = []
                    type_mismatches[key].append(f)
                
                for declared_type, failures_list in type_mismatches.items():
                    failure_report.append(f"\n  Type '{declared_type}' with string examples:")
                    for f in failures_list[:5]:  # Show first 5 of each type
                        failure_report.append(
                            f"    {f['operation']}.{f['parameter']} = {f['example']!r}"
                        )
                    if len(failures_list) > 5:
                        failure_report.append(f"    ... and {len(failures_list) - 5} more")
            
            if model_failures:
                failure_report.append(f"\n{len(model_failures)} model creation failures:")
                for f in model_failures[:5]:
                    failure_report.append(f"  {f['operation']}: {f['error']}")

            pytest.fail("\n".join(failure_report))

    def test_common_parameter_type_consistency(self, api_definition):
        """Test that common parameters have consistent types across operations."""
        # Track parameter types across operations
        param_types = {}
        
        for op_name, op_spec in api_definition["operations"].items():
            params = op_spec.get("parameters", {})
            for param_name, param_spec in params.items():
                param_type = param_spec.get("type", "string")
                
                if param_name not in param_types:
                    param_types[param_name] = {}
                
                if param_type not in param_types[param_name]:
                    param_types[param_name][param_type] = []
                
                param_types[param_name][param_type].append(op_name)
        
        # Check for inconsistencies in common parameters
        inconsistencies = []
        common_params = ["account", "did", "client", "id", "number", "type"]
        
        for param_name in common_params:
            if param_name in param_types:
                types = param_types[param_name]
                if len(types) > 1:
                    inconsistencies.append({
                        "parameter": param_name,
                        "types": {t: len(ops) for t, ops in types.items()},
                        "operations": {t: ops[:3] for t, ops in types.items()}  # First 3 examples
                    })
        
        if inconsistencies:
            report = ["\nFound type inconsistencies in common parameters:"]
            for inc in inconsistencies:
                report.append(f"\n  Parameter '{inc['parameter']}':")
                for ptype, count in inc['types'].items():
                    report.append(f"    - {ptype}: {count} operations")
                    examples = inc['operations'][ptype]
                    report.append(f"      Examples: {', '.join(examples)}")
            
            # This is informational, not a failure
            print("\n".join(report))