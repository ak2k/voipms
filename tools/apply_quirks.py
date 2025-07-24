#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""
Enhance API definition with corrections to create runtime version.

This tool takes the pure API definition and applies corrections to create
an enhanced version used at runtime.
"""

import json
from pathlib import Path
from typing import Optional


def load_json(path: Path) -> dict:
    """Load JSON file."""
    with open(path) as f:
        return json.load(f)


def save_json(data: dict, path: Path):
    """Save JSON file."""
    with open(path, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)


def resolve_type_sources(param_spec: dict, quirk_type: Optional[str] = None) -> None:
    """Resolve final parameter type from all sources."""
    sources = param_spec.get("_type_sources", {})
    
    if not sources:
        return
    
    # Add quirk if provided
    if quirk_type:
        sources["quirk"] = quirk_type
    
    # Determine final type by priority
    if quirk_type:
        final_type = quirk_type
        resolution = "quirk"
    elif sources.get("html_example_inference"):
        final_type = sources["html_example_inference"]
        resolution = "html_example_inference"
    elif sources.get("html_declaration"):
        final_type = sources["html_declaration"]
        resolution = "html_declaration"
    else:
        final_type = sources.get("wsdl", "string")
        resolution = "wsdl"
    
    # Check for conflicts
    unique_types = set(v for k, v in sources.items() if v and k != "quirk")
    conflict = len(unique_types) > 1
    
    # Update sources with resolution info
    sources.update({
        "final": final_type,
        "conflict": conflict,
        "resolution": resolution
    })
    
    # Update the parameter type
    param_spec["type"] = final_type


def merge_corrections(api_def: dict, corrections: dict) -> dict:
    """Merge corrections into API definition."""
    # Deep copy to avoid modifying original
    import copy

    enhanced = copy.deepcopy(api_def)

    # Add version info
    enhanced["_metadata"] = {
        "generated_from": "api_definition_source.json",
        "corrections_applied": True,
        "corrections_version": corrections.get("version", "1.0"),
        "description": "Runtime API definition with corrections applied",
    }

    # Merge error codes directly
    if error_codes := corrections.get("error_codes", {}):
        print(f"Merging {len(error_codes)} error codes...")
        enhanced.setdefault("error_codes", {}).update(error_codes)
    
    # Merge decoder overrides
    if decoder_overrides := corrections.get("decoder_overrides", {}):
        print(f"Adding {len(decoder_overrides)} decoder overrides...")
        enhanced.setdefault("_metadata", {})["decoder_overrides"] = decoder_overrides

    # Apply operation corrections
    corrections_operations = corrections.get("operations", {})
    operations = enhanced.get("operations", {})
    
    # First, resolve type sources for ALL parameters (even without corrections)
    for op_name, operation in operations.items():
        for param_name, param_spec in operation.get("parameters", {}).items():
            if "_type_sources" in param_spec and "final" not in param_spec.get("_type_sources", {}):
                resolve_type_sources(param_spec)

    # Process each operation correction
    for operation_name, operation_corrections in corrections_operations.items():
        if operation_name not in operations:
            print(f"Warning: Operation {operation_name} has corrections but not in API definition")
            continue
            
        operation = operations[operation_name]
        applied_corrections = []
        
        # Merge parameter corrections
        if param_corrections := operation_corrections.get("parameters", {}):
            operation_params = operation.setdefault("parameters", {})
            
            for param_name, param_correction in param_corrections.items():
                if param_name not in operation_params:
                    # New parameter from corrections
                    operation_params[param_name] = param_correction
                    applied_corrections.append(f"Added parameter: {param_name}")
                else:
                    # Merge corrections into existing parameter
                    # Using dict unpacking to create merged dict
                    original = operation_params[param_name]
                    operation_params[param_name] = {**original, **param_correction}
                    
                    # Track what was changed
                    for key in param_correction:
                        if key not in original or original.get(key) != param_correction[key]:
                            applied_corrections.append(f"{param_name}.{key}")
                    
                    # Resolve type if overridden
                    if "type" in param_correction:
                        resolve_type_sources(operation_params[param_name], param_correction["type"])
        
        # Merge operation-level metadata
        for key, value in operation_corrections.items():
            if key != "parameters" and key.startswith("_"):
                operation[key] = value
                applied_corrections.append(f"Added {key}")
        
        # Add summary of applied corrections
        if applied_corrections:
            operation["_applied_corrections"] = applied_corrections
            print(f"  {operation_name}: {len(applied_corrections)} corrections applied")
        
        # Final type resolution for all parameters
        for param_name, param_spec in operation.get("parameters", {}).items():
            if "_type_sources" in param_spec and "final" not in param_spec.get("_type_sources", {}):
                resolve_type_sources(param_spec)

    # Add get/set method linkages for cross-reference decoding
    _add_method_linkages(enhanced)
    
    return enhanced


def _add_method_linkages(api_def: dict):
    """Add linkages between get and set methods for cross-reference decoding."""
    operations = api_def.get("operations", {})
    
    # Check for manual decoder overrides in corrections
    decoder_overrides = {}
    if "_metadata" in api_def and "decoder_overrides" in api_def["_metadata"]:
        decoder_overrides = api_def["_metadata"]["decoder_overrides"]
    
    # Find all set methods with _values_from parameters
    set_methods_with_values_from = {}
    for name, op in operations.items():
        if name.startswith("set"):
            params_with_values_from = []
            for param_name, param_data in op.get("parameters", {}).items():
                if "_values_from" in param_data:
                    params_with_values_from.append(param_name)
            if params_with_values_from:
                set_methods_with_values_from[name] = params_with_values_from
    
    # Find matching get methods for each set method
    get_method_mappings = {}
    
    # Start with manual overrides
    for get_method, set_methods in decoder_overrides.items():
        if get_method in operations:
            if isinstance(set_methods, str):
                set_methods = [set_methods]
            get_method_mappings[get_method] = set_methods
    
    # Then do automatic discovery for remaining set methods
    mapped_set_methods = set()
    for sets in get_method_mappings.values():
        mapped_set_methods.update(sets)
    
    for set_method in set_methods_with_values_from.keys():
        if set_method in mapped_set_methods:
            continue  # Already mapped by override
            
        # Try different patterns to find matching get method
        potential_gets = [
            set_method.replace("set", "get"),           # setSubAccount -> getSubAccount
            set_method.replace("set", "get") + "s",     # setSubAccount -> getSubAccounts
            set_method.replace("set", "getDIDs") if set_method.startswith("setDID") else None,  # setDIDInfo -> getDIDsInfo
        ]
        
        for potential_get in potential_gets:
            if potential_get and potential_get in operations:
                # Don't override existing mappings
                if potential_get not in get_method_mappings:
                    get_method_mappings[potential_get] = []
                get_method_mappings[potential_get].append(set_method)
                break
    
    # Add the mappings to each get method's metadata
    for get_method, set_methods in get_method_mappings.items():
        if get_method in operations:
            operations[get_method]["_decoder_set_methods"] = set_methods
    
    # Add summary to metadata
    if "_metadata" not in api_def:
        api_def["_metadata"] = {}
    
    api_def["_metadata"]["decoder_mappings"] = {
        "total_get_methods_with_decoding": len(get_method_mappings),
        "total_set_methods_with_values_from": len(set_methods_with_values_from),
        "mappings": {get: sets for get, sets in get_method_mappings.items()}
    }




def main():
    """Main entry point."""
    # Paths
    tools_dir = Path(__file__).parent
    src_dir = tools_dir.parent / "src" / "voipms"
    config_dir = tools_dir / "config"
    generated_dir = tools_dir / "generated"

    # Input files
    api_def_path = generated_dir / "api_definition_source.json"
    corrections_path = config_dir / "api_corrections.json"

    # Output file
    enhanced_path = src_dir / "api_definition.json"

    print("Loading API definition and corrections...")
    api_def = load_json(api_def_path)
    
    if not corrections_path.exists():
        print(f"Error: Corrections file not found: {corrections_path}")
        return 1
    
    corrections = load_json(corrections_path)

    print(f"Loaded {len(api_def.get('operations', {}))} operations")
    print(f"Loaded corrections for {len(corrections.get('operations', {}))} operations")

    print("\nApplying corrections...")
    enhanced = merge_corrections(api_def, corrections)

    print(f"\nSaving runtime API definition to {enhanced_path}")
    save_json(enhanced, enhanced_path)

    # Summary
    original_errors = len(api_def.get("error_codes", {}))
    enhanced_errors = len(enhanced.get("error_codes", {}))

    print("\nSummary:")
    print(
        f"  Error codes: {original_errors} → {enhanced_errors} (+{enhanced_errors - original_errors})"
    )
    print(
        f"  Operations with corrections: {len([op for op in enhanced['operations'].values() if '_applied_corrections' in op])}"
    )
    print(
        f"  Total corrections applied: {sum(len(op.get('_applied_corrections', [])) for op in enhanced['operations'].values())}"
    )


if __name__ == "__main__":
    main()
