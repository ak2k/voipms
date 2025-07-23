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
        from apply_quirks import apply_quirks_to_definition, load_json, save_json

        # Paths
        api_def_path = src_dir / "api_definition_source.json"
        quirks_path = src_dir / "api_quirks.json"
        enhanced_path = src_dir / "api_definition.json"

        if verbose:
            click.echo("Loading API definition and quirks...")

        api_def = load_json(api_def_path)
        quirks_config = load_json(quirks_path)

        if verbose:
            click.echo(f"Loaded {len(api_def.get('operations', {}))} operations")
            click.echo(f"Loaded {len(quirks_config.get('quirks', {}))} method quirks")
            click.echo("\nApplying quirks...")

        enhanced = apply_quirks_to_definition(api_def, quirks_config)

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
            f"  Methods with quirks: {len([op for op in enhanced['operations'].values() if '_applied_quirks' in op])}"
        )
        click.echo(
            f"  Total quirks applied: {sum(len(op.get('_applied_quirks', [])) for op in enhanced['operations'].values())}"
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


if __name__ == "__main__":
    cli()
