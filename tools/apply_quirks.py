#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""
Enhance API definition with quirks to create runtime version.

This tool takes the pure API definition and applies quirks to create
an enhanced version used at runtime.
"""

import json
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    """Load JSON file."""
    with open(path) as f:
        return json.load(f)


def save_json(data: dict, path: Path):
    """Save JSON file."""
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, sort_keys=True)


def apply_quirks_to_definition(api_def: dict, quirks_config: dict) -> dict:
    """Apply quirks to API definition to create enhanced version."""
    # Deep copy to avoid modifying original
    import copy
    enhanced = copy.deepcopy(api_def)
    
    # Add version info
    enhanced['_metadata'] = {
        'generated_from': 'api_definition_source.json',
        'quirks_applied': True,
        'quirks_version': quirks_config.get('version', '1.0'),
        'description': 'Runtime API definition with quirks applied'
    }
    
    # Apply error code additions
    if error_additions := quirks_config.get('error_code_additions', {}):
        print(f"Adding {len(error_additions)} error codes...")
        for error_id, error_info in error_additions.items():
            enhanced.setdefault('error_codes', {})[error_id] = error_info['message']
    
    # Apply method quirks
    quirks = quirks_config.get('quirks', {})
    operations = enhanced.get('operations', {})
    
    for method_name, method_quirks in quirks.items():
        if method_name not in operations:
            print(f"Warning: Method {method_name} has quirks but not in API definition")
            continue
            
        operation = operations[method_name]
        parameters = operation.get('parameters', {})
        
        # Apply parameter-level quirks
        applied_quirks = []
        
        # Handle yes/no string conversions
        for param_name in method_quirks.get('yes_no_strings', []):
            if param_name in parameters:
                parameters[param_name]['_quirks'] = {
                    'type': 'yes_no_string',
                    'description': 'Converts boolean to yes/no string'
                }
                # Keep original type for documentation, quirks handler will convert
                applied_quirks.append(f"{param_name}: boolean → yes/no")
        
        # Handle list to semicolon conversions
        for param_name in method_quirks.get('list_to_semicolon', []):
            if param_name in parameters:
                parameters[param_name]['_quirks'] = {
                    'type': 'list_to_semicolon',
                    'description': 'Converts list to semicolon-separated string'
                }
                applied_quirks.append(f"{param_name}: list → semicolon string")
        
        # Handle parameter aliases
        if aliases := method_quirks.get('aliases', {}):
            operation['_parameter_aliases'] = aliases
            for old_name, new_name in aliases.items():
                applied_quirks.append(f"alias: {old_name} → {new_name}")
        
        # Handle special value mappings
        if special_values := method_quirks.get('special_values', {}):
            for param_name, mappings in special_values.items():
                if param_name in parameters:
                    parameters[param_name]['_value_mappings'] = mappings
                    applied_quirks.append(f"{param_name}: special value mappings")
        
        # Handle defaults
        if defaults := method_quirks.get('defaults', {}):
            operation['_smart_defaults'] = defaults
            for param_name, default_value in defaults.items():
                if param_name in parameters and 'default' not in parameters[param_name]:
                    # Add as metadata, not actual default
                    parameters[param_name]['_smart_default'] = default_value
                    applied_quirks.append(f"{param_name}: smart default = {default_value}")
        
        # Handle date validations
        if date_validations := method_quirks.get('date_validations', {}):
            operation['_date_validations'] = date_validations
            applied_quirks.append(f"date validations: {date_validations}")
        
        # Add summary of applied quirks
        if applied_quirks:
            operation['_applied_quirks'] = applied_quirks
            print(f"  {method_name}: {len(applied_quirks)} quirks applied")
    
    return enhanced


def main():
    """Main entry point."""
    # Paths
    src_dir = Path(__file__).parent.parent / 'src' / 'voipms'
    
    # Input files
    api_def_path = src_dir / 'api_definition_source.json'
    quirks_path = src_dir / 'api_quirks.json'
    
    # Output file
    enhanced_path = src_dir / 'api_definition.json'
    
    print("Loading API definition and quirks...")
    api_def = load_json(api_def_path)
    quirks_config = load_json(quirks_path)
    
    print(f"Loaded {len(api_def.get('operations', {}))} operations")
    print(f"Loaded {len(quirks_config.get('quirks', {}))} method quirks")
    
    print("\nApplying quirks...")
    enhanced = apply_quirks_to_definition(api_def, quirks_config)
    
    print(f"\nSaving runtime API definition to {enhanced_path}")
    save_json(enhanced, enhanced_path)
    
    # Summary
    original_errors = len(api_def.get('error_codes', {}))
    enhanced_errors = len(enhanced.get('error_codes', {}))
    
    print(f"\nSummary:")
    print(f"  Error codes: {original_errors} → {enhanced_errors} (+{enhanced_errors - original_errors})")
    print(f"  Methods with quirks: {len([op for op in enhanced['operations'].values() if '_applied_quirks' in op])}")
    print(f"  Total quirks applied: {sum(len(op.get('_applied_quirks', [])) for op in enhanced['operations'].values())}")


if __name__ == '__main__':
    main()