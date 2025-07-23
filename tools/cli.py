#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.7"
# dependencies = [
#     "click>=8.0",
#     "requests>=2.31.0",
#     "beautifulsoup4>=4.12.0",
#     "lxml>=4.9.0",
# ]
# ///
"""
VoIP.ms API Tools CLI

A unified command-line interface for VoIP.ms API development tools.
"""

import click


@click.group()
@click.version_option(version="1.0.0", prog_name="voipms-tools")
def cli():
    """VoIP.ms API development tools."""
    pass


@cli.command()
@click.option(
    "--stage",
    "-s",
    type=click.Choice(["all", "source", "quirks", "stubs"]),
    default="all",
    help="Which stage(s) to run",
)
@click.option("--wsdl-url", help="Override WSDL URL")
@click.option("--skip-html", is_flag=True, help="Skip HTML documentation parsing")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def generate(stage, wsdl_url, skip_html, verbose):
    """Generate API definitions and type stubs.

    By default, runs all stages:
    1. source: Generate source API definition from WSDL/HTML
    2. quirks: Apply quirks to create runtime API definition
    3. stubs: Generate Python type stubs

    Use --stage to run only specific stages for debugging.
    """
    import sys
    from pathlib import Path

    # Add tools directory to Python path for imports
    tools_dir = Path(__file__).parent
    sys.path.insert(0, str(tools_dir))

    src_dir = tools_dir.parent / "src" / "voipms"

    # Stage 1: Generate source API definition
    if stage in ("all", "source"):
        if verbose:
            click.echo("\n=== Stage 1: Generating source API definition ===")

        # Import and run the generator
        try:
            from .generate_api_definition import FinalVoIPMSJSONGenerator
        except ImportError:
            from generate_api_definition import FinalVoIPMSJSONGenerator

        generator = FinalVoIPMSJSONGenerator()

        # Check for HTML file
        html_file = None
        for possible_file in [
            tools_dir.parent / "resources" / "voipms_api_documentation.html",
            tools_dir / "voipms_api_documentation.html",
            "resources/voipms_api_documentation.html",
        ]:
            if possible_file.exists():
                html_file = str(possible_file)
                break

        if html_file and not skip_html:
            if verbose:
                click.echo(f"Using HTML documentation: {html_file}")
            api_def = generator.generate_with_documentation(html_file=html_file)
            if verbose:
                generator.show_enrichment_summary(api_def)
        else:
            if verbose:
                click.echo("Generating from WSDL only...")
            api_def = generator.generate_with_documentation()

        if stage == "source":
            return

    # Stage 2: Apply quirks
    if stage in ("all", "quirks"):
        if verbose:
            click.echo("\n=== Stage 2: Applying quirks to create runtime API definition ===")

        # Import and run apply_quirks
        try:
            from .apply_quirks import merge_corrections, load_json, save_json
        except ImportError:
            from apply_quirks import merge_corrections, load_json, save_json

        # Paths
        generated_dir = tools_dir / "generated"
        api_def_path = generated_dir / "api_definition_source.json"
        corrections_path = tools_dir / "config" / "api_corrections.json"
        enhanced_path = src_dir / "api_definition.json"

        if verbose:
            click.echo("Loading API definition and corrections...")

        api_def = load_json(api_def_path)
        
        if not corrections_path.exists():
            click.echo(f"Error: Corrections file not found: {corrections_path}", err=True)
            return
            
        corrections = load_json(corrections_path)

        if verbose:
            click.echo(f"Loaded {len(api_def.get('operations', {}))} operations")
            click.echo(f"Loaded corrections for {len(corrections.get('operations', {}))} operations")
            click.echo("\nApplying corrections...")

        enhanced = merge_corrections(api_def, corrections)

        if verbose:
            click.echo(f"\nSaving runtime API definition to {enhanced_path}")

        save_json(enhanced, enhanced_path)

        # Summary
        original_errors = len(api_def.get("error_codes", {}))
        enhanced_errors = len(enhanced.get("error_codes", {}))

        click.echo("\nSummary:")
        click.echo(
            f"  Error codes: {original_errors} → {enhanced_errors} (+{enhanced_errors - original_errors})"
        )
        click.echo(
            f"  Operations with corrections: {len([op for op in enhanced['operations'].values() if '_applied_corrections' in op])}"
        )
        click.echo(
            f"  Total corrections applied: {sum(len(op.get('_applied_corrections', [])) for op in enhanced['operations'].values())}"
        )

        if stage == "quirks":
            return

    # Stage 3: Generate type stubs
    if stage in ("all", "stubs"):
        if verbose:
            click.echo("\n=== Stage 3: Generating Python type stubs ===")

        # Import and run type stub generator
        from generate_type_stubs import generate_stubs

        # Use the runtime API definition (with quirks) for type stubs
        api_def_path = src_dir / "api_definition.json"

        if verbose:
            click.echo(f"Generating type stubs from {api_def_path}")

        generate_stubs(str(api_def_path), str(src_dir))

        click.echo(f"Generated type stubs in {src_dir}")

    if stage == "all" and verbose:
        click.echo("\n=== All stages completed successfully ===")


@cli.command()
@click.option(
    "--output-dir", "-o", default="docs/api", help="Output directory for downloaded documentation"
)
@click.option(
    "--methods",
    "-m",
    multiple=True,
    help="Specific methods to download (can be specified multiple times)",
)
@click.option("--headless", is_flag=True, help="Run browser in headless mode")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def download(output_dir, methods, headless, verbose):
    """Download API documentation pages."""
    from .commands.download import download_api_docs

    download_api_docs(output_dir, list(methods), headless, verbose)


@cli.command()
@click.option(
    "--discovery-dir",
    "-d",
    type=click.Path(exists=True),
    help="Directory containing discovery JSON files (default: ~/.voipms/discoveries)",
)
@click.option(
    "--output", "-o", type=click.Path(), help="Output file for aggregated results (default: stdout)"
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["json", "type-overrides", "summary"]),
    default="summary",
    help="Output format (json: raw data, type-overrides: for type_overrides.json, summary: human-readable)",
)
@click.option("--min-count", "-c", type=int, default=2, help="Minimum count to include in output")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def analyze_discoveries(discovery_dir, output, format, min_count, verbose):
    """Analyze type discovery files and suggest corrections.
    
    This command aggregates type discovery data from multiple sessions
    and identifies patterns that should be corrected:
    - Type overrides for tools/config/type_overrides.json
    - Behavioral quirks for src/voipms/api_quirks.json (manual review)
    """
    import json
    from collections import Counter, defaultdict
    from pathlib import Path
    from datetime import datetime
    
    # Helper function to categorize discoveries
    def categorize_discovery(expected_type, actual_type, sample_values=None):
        """Categorize whether this is a type override or behavioral quirk."""
        if sample_values is None:
            sample_values = []
            
        # Type overrides
        if expected_type == "integer" and actual_type == "string":
            # Check if values suggest it's really a string
            if any("_" in str(v) or not str(v).replace("-", "").replace("+", "").isdigit() 
                   for v in sample_values if v):
                return "type_override", "Parameter accepts string values"
        
        # Behavioral quirks
        if expected_type == "boolean" and actual_type == "string":
            if set(str(v).lower() for v in sample_values if v) <= {"yes", "no"}:
                return "yes_no_quirk", "Boolean parameter expects yes/no strings"
            elif set(str(v) for v in sample_values if v) <= {"0", "1"}:
                return "string_boolean_quirk", "Boolean parameter expects '0'/'1' strings"
        
        if expected_type == "array" and actual_type == "string":
            if any(";" in str(v) for v in sample_values if v):
                return "semicolon_list_quirk", "Array parameter expects semicolon-separated string"
        
        # Default to type override
        return "type_override", f"Expected {expected_type} but got {actual_type}"
    
    # Default discovery directory
    if not discovery_dir:
        discovery_dir = Path.home() / ".voipms" / "discoveries"
    else:
        discovery_dir = Path(discovery_dir)
    
    if not discovery_dir.exists():
        click.echo(f"Discovery directory not found: {discovery_dir}", err=True)
        return
    
    # Find all discovery JSON files
    discovery_files = list(discovery_dir.glob("discovery_*.json"))
    if not discovery_files:
        click.echo(f"No discovery files found in {discovery_dir}", err=True)
        return
    
    if verbose:
        click.echo(f"Found {len(discovery_files)} discovery files")
    
    # Aggregate discoveries
    type_mismatches = defaultdict(lambda: defaultdict(Counter))
    unknown_params = defaultdict(lambda: defaultdict(Counter))
    sample_values = defaultdict(lambda: defaultdict(set))
    
    for file_path in discovery_files:
        try:
            with open(file_path) as f:
                data = json.load(f)
            
            # Process type mismatches
            for entry in data.get("type_mismatches", []):
                method = entry["method"]
                param = entry["parameter"]
                key = (entry["expected_type"], entry["actual_type"])
                type_mismatches[method][param][key] += entry["count"]
                
                # Collect sample values
                if "sample_values" in entry:
                    for value in entry["sample_values"]:
                        sample_values[method][param].add(str(value))
            
            # Process unknown parameters
            for entry in data.get("unknown_parameters", []):
                method = entry["method"]
                param = entry["parameter"]
                actual_type = entry["actual_type"]
                unknown_params[method][param][actual_type] += entry["count"]
                
                # Collect sample values
                if "sample_values" in entry:
                    for value in entry["sample_values"]:
                        sample_values[method][param].add(str(value))
        
        except Exception as e:
            if verbose:
                click.echo(f"Error processing {file_path}: {e}", err=True)
    
    # Generate output based on format
    if format == "json":
        # Raw JSON output
        result = {
            "type_mismatches": {},
            "unknown_parameters": {}
        }
        
        # Convert type mismatches
        for method, params in type_mismatches.items():
            result["type_mismatches"][method] = {}
            for param, type_counts in params.items():
                total = sum(type_counts.values())
                if total >= min_count:
                    result["type_mismatches"][method][param] = [
                        {
                            "expected": expected,
                            "actual": actual,
                            "count": count
                        }
                        for (expected, actual), count in type_counts.items()
                    ]
        
        # Convert unknown parameters
        for method, params in unknown_params.items():
            result["unknown_parameters"][method] = {}
            for param, type_counts in params.items():
                total = sum(type_counts.values())
                if total >= min_count:
                    result["unknown_parameters"][method][param] = dict(type_counts)
        
        output_text = json.dumps(result, indent=2)
    
    elif format == "type-overrides":
        # Generate corrections for tools/config/api_corrections.json
        corrections = {
            "version": "1.0",
            "description": "Discovered corrections from type discovery",
            "error_codes": {},
            "operations": {}
        }
        
        # Process discoveries and categorize them
        for method, params in type_mismatches.items():
            for param, type_counts in params.items():
                # Get most common type mismatch
                for (expected, actual), count in type_counts.items():
                    if count < min_count:
                        continue
                        
                    samples = list(sample_values.get(method, {}).get(param, []))[:5]
                    category, reason = categorize_discovery(expected, actual, samples)
                    
                    # Initialize operation if needed
                    if method not in corrections["operations"]:
                        corrections["operations"][method] = {"parameters": {}}
                    
                    if category == "type_override":
                        # Type correction
                        corrections["operations"][method]["parameters"][param] = {
                            "type": actual,
                            "_type_override_reason": reason
                        }
                    elif category == "behavioral_quirk":
                        # Behavioral transform
                        if "yes/no" in reason:
                            corrections["operations"][method]["parameters"][param] = {
                                "type": "string",
                                "_transform": {
                                    "type": "boolean_to_yes_no",
                                    "from": "boolean",
                                    "to": "string",
                                    "mapping": {"true": "yes", "false": "no"}
                                }
                            }
                        elif "semicolon" in reason:
                            corrections["operations"][method]["parameters"][param] = {
                                "type": "string",
                                "_transform": {
                                    "type": "list_to_semicolon",
                                    "from": "array",
                                    "to": "string",
                                    "delimiter": ";"
                                }
                            }
        
        # Add metadata
        corrections["_metadata"] = {
            "generated_at": datetime.now().isoformat(),
            "files_analyzed": len(discovery_files),
            "min_count_threshold": min_count,
            "note": "Review and merge with tools/config/api_corrections.json"
        }
        
        output_text = json.dumps(corrections, indent=2)
    
    else:  # summary format
        lines = []
        lines.append("=== Type Discovery Analysis ===\n")
        
        # Categorize discoveries
        type_corrections = []
        behavioral_quirks = []
        
        for method, params in type_mismatches.items():
            for param, type_counts in params.items():
                total = sum(type_counts.values())
                if total >= min_count:
                    for (expected, actual), count in type_counts.items():
                        samples = list(sample_values.get(method, {}).get(param, []))[:5]
                        category, reason = categorize_discovery(expected, actual, samples)
                        
                        discovery = {
                            "method": method,
                            "param": param,
                            "expected": expected,
                            "actual": actual,
                            "count": count,
                            "samples": samples,
                            "reason": reason
                        }
                        
                        if category == "type_override":
                            type_corrections.append(discovery)
                        else:
                            behavioral_quirks.append(discovery)
        
        # Display type corrections
        if type_corrections:
            lines.append("Type Overrides (can be auto-merged to tools/config/api_corrections.json):")
            for disc in sorted(type_corrections, key=lambda x: (-x["count"], x["method"], x["param"])):
                lines.append(f"\n  {disc['method']}:")
                lines.append(f"    {disc['param']}: {disc['expected']} → {disc['actual']} ({disc['count']} times)")
                if disc['samples']:
                    lines.append(f"    Examples: {', '.join(repr(s) for s in disc['samples'][:3])}")
        
        # Display behavioral quirks
        if behavioral_quirks:
            lines.append("\n\nPotential Behavioral Quirks (review and manually add to tools/config/api_corrections.json if needed):")
            
            # Group by quirk type
            yes_no_quirks = [q for q in behavioral_quirks if "yes/no" in q["reason"]]
            semicolon_quirks = [q for q in behavioral_quirks if "semicolon" in q["reason"]]
            other_quirks = [q for q in behavioral_quirks if q not in yes_no_quirks + semicolon_quirks]
            
            if yes_no_quirks:
                lines.append("\n  Yes/No String Parameters:")
                for disc in sorted(yes_no_quirks, key=lambda x: (-x["count"], x["method"], x["param"])):
                    lines.append(f"    {disc['method']}.{disc['param']}: {disc['expected']} → {disc['actual']} ({disc['count']} times)")
                    lines.append(f"      Suggested quirk: Add to \"yes_no_strings\" list")
            
            if semicolon_quirks:
                lines.append("\n  Semicolon-Separated Lists:")
                for disc in sorted(semicolon_quirks, key=lambda x: (-x["count"], x["method"], x["param"])):
                    lines.append(f"    {disc['method']}.{disc['param']}: {disc['expected']} → {disc['actual']} ({disc['count']} times)")
                    if disc['samples']:
                        lines.append(f"      Example: {disc['samples'][0]}")
                    lines.append(f"      Suggested quirk: Add to \"list_to_semicolon\" list")
        
        # Unknown parameters summary
        if unknown_params:
            lines.append("\n\nUnknown Parameters (review for api_definition_source.json):")
            for method, params in sorted(unknown_params.items()):
                has_unknown = False
                for param, type_counts in sorted(params.items()):
                    total = sum(type_counts.values())
                    if total >= min_count:
                        if not has_unknown:
                            lines.append(f"\n  {method}:")
                            has_unknown = True
                        
                        types_str = ", ".join(f"{t}({c})" for t, c in sorted(type_counts.items(), key=lambda x: -x[1]))
                        lines.append(f"    {param}: {types_str}")
        
        # Add usage instructions
        if type_corrections:
            lines.append("\n\nTo apply type overrides:")
            lines.append("  voipms-cli analyze-discoveries --format type-overrides > discovered_overrides.json")
            lines.append("  # Then manually merge with tools/config/type_overrides.json")
        
        output_text = "\n".join(lines)
    
    # Output results
    if output:
        with open(output, "w") as f:
            f.write(output_text)
        if verbose:
            click.echo(f"Results written to {output}")
    else:
        click.echo(output_text)


if __name__ == "__main__":
    cli()
