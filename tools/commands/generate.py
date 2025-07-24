"""Generate commands for API definition and type stubs."""

import json
import sys
from pathlib import Path

# Import parsers from new location
sys.path.insert(0, str(Path(__file__).parent.parent))
from parsers.html_parser import parse_html_docs
from parsers.wsdl import parse_wsdl


def generate_api_definition(
    output_path: str, wsdl_url: str = None, skip_html: bool = False, verbose: bool = False
):
    """Generate API definition from WSDL and HTML documentation."""
    # Default WSDL URL
    if not wsdl_url:
        wsdl_url = "https://www.voip.ms/api/wsdl.php"

    if verbose:
        print(f"Parsing WSDL from {wsdl_url}...")

    # Parse WSDL
    operations, error_codes = parse_wsdl(wsdl_url)

    if verbose:
        print(f"Found {len(operations)} operations and {len(error_codes)} error codes")

    # Enrich with HTML docs if not skipped
    if not skip_html:
        if verbose:
            print("Enriching with HTML documentation...")
        operations = parse_html_docs(operations)

    # Load type overrides
    overrides_path = Path(__file__).parent.parent / "config" / "type_overrides.json"
    if overrides_path.exists():
        if verbose:
            print("Applying type overrides...")
        with open(overrides_path) as f:
            overrides_config = json.load(f)

        # Apply overrides from both core and extended sections
        all_overrides = {}
        all_overrides.update(overrides_config.get("overrides", {}).get("core", {}))
        all_overrides.update(overrides_config.get("overrides", {}).get("extended", {}))

        # Apply overrides
        for override_path, override_type in all_overrides.items():
            op_name, param_name = override_path.split(".")
            if op_name in operations and param_name in operations[op_name].get("parameters", {}):
                operations[op_name]["parameters"][param_name]["type"] = override_type
                if verbose:
                    print(f"  Override: {override_path} -> {override_type}")

    # Create final structure
    api_definition = {
        "version": "1.0",
        "base_url": "https://voip.ms/api/v1/rest.php",
        "operations": operations,
        "error_codes": error_codes,
    }

    # Save to file
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(api_definition, f, indent=2, sort_keys=True)

    if verbose:
        print(f"API definition saved to {output_path}")
    else:
        print(f"Generated {output_path}")


def generate_type_stubs(api_def_path: str, output_dir: str, verbose: bool = False):
    """Generate Python type stubs from API definition."""
    # Import the original generate_type_stubs logic
    import subprocess
    import sys

    # For now, call the original script
    # TODO: Refactor the script's logic into this function
    script_path = Path(__file__).parent.parent / "generate_type_stubs.py"

    cmd = [sys.executable, str(script_path), api_def_path, output_dir]
    if verbose:
        print(f"Running: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    if verbose:
        print(result.stdout)
    else:
        print(f"Generated type stubs in {output_dir}")
