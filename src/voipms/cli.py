#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "rich-click>=1.7.0",
#     "httpx>=0.24.0",
#     "pydantic>=2.0.0",
#     "python-dotenv>=1.0.0",
#     "rich>=13.0.0",
#     "dateparser>=1.1.0",
# ]
# ///
"""
Data-Driven VoIP.ms CLI - Dynamically generates commands from API definition
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import rich_click as click
from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

# Configure rich-click
click.rich_click.USE_RICH_MARKUP = True
click.rich_click.USE_MARKDOWN = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.STYLE_OPTION = "cyan"
click.rich_click.STYLE_SWITCH = "green"
click.rich_click.STYLE_ARGUMENT = "magenta"

# Try to load .env file
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# Add parent directory to path so we can import voipms
sys.path.insert(0, str(Path(__file__).parent.parent))

from voipms import VoIPMSClient, VoIPMSError  # noqa: E402


class VoIPMSCLI:
    """Data-driven CLI that generates commands from API definition."""

    def __init__(self):
        self.client = None
        self.api_definition = None
        self.console = Console()
        self.smart_defaults = self._load_smart_defaults()

    def _load_smart_defaults(self) -> Dict[str, Any]:
        """Load smart defaults configuration."""
        try:
            # Try to load from package resources
            import voipms

            config_path = Path(voipms.__file__).parent / "cli_smart_defaults.json"
            if config_path.exists():
                with open(config_path) as f:
                    return json.load(f)
        except Exception:
            pass

        # Return empty config if not found
        return {}

    def init_client(self, username: Optional[str] = None, password: Optional[str] = None):
        """Initialize the VoIP.ms client."""
        try:
            # Create a temporary context manager to load API definition
            with VoIPMSClient(username=username, password=password) as temp_client:
                self.api_definition = temp_client.api_definition
                # Store credentials for later use
                self.username = username
                self.password = password
        except Exception as e:
            click.echo(click.style(f"Error: Failed to initialize client: {e}", fg="red"), err=True)
            sys.exit(1)

    def format_json(self, data: Any, pretty: bool = True) -> str:
        """Format data as JSON."""
        if pretty:
            return json.dumps(data, indent=2, sort_keys=True)
        return json.dumps(data)

    def print_error(self, message: str):
        """Print error message to stderr."""
        self.console.print(f"[bold red]Error:[/bold red] {message}", style="red")

    def print_success(self, message: str):
        """Print success message."""
        self.console.print(message, style="bold green")

    def get_method_info(self, method_name: str) -> Optional[Dict[str, Any]]:
        """Get method information from API definition."""
        if not self.api_definition:
            return None
        operations = self.api_definition.get("operations", {})
        return operations.get(method_name)

    def call_method(self, method_name: str, params: Dict[str, Any], pretty: bool = True):
        """Call an API method with given parameters."""
        try:
            # Create a new client context for this method call
            with VoIPMSClient(username=self.username, password=self.password) as client:
                # Check if method exists
                if not hasattr(client, method_name):
                    self.print_error(f"Unknown method: {method_name}")
                    self.show_similar_methods(method_name)
                    sys.exit(1)

                # Call the method - let it use validation
                method = getattr(client, method_name)
                result = method(**params)

                # Format output
                if pretty:
                    self.console.print(JSON(json.dumps(result)))
                else:
                    click.echo(json.dumps(result))

        except VoIPMSError as e:
            self.print_error(f"API error: {e}")
            sys.exit(1)
        except Exception as e:
            self.print_error(str(e))
            sys.exit(1)

    def show_similar_methods(self, method_name: str):
        """Show methods with similar names."""
        if not self.api_definition:
            return

        operations = self.api_definition.get("operations", {})
        similar = []

        method_lower = method_name.lower()
        for op_name in operations:
            if method_lower in op_name.lower() or op_name.lower() in method_lower:
                similar.append(op_name)

        if similar:
            click.echo("\nDid you mean one of these?", err=True)
            for method in similar[:10]:
                click.echo(f"  - {method}", err=True)

    def _format_parameter_info(
        self, name: str, info: Dict[str, Any], show_defaults: bool = False
    ) -> tuple:
        """Format parameter information for display."""
        param_type = info.get("type", "string")
        desc = info.get("description", "No description")

        # Add enum values
        if enum_values := info.get("enum"):
            desc += f"\n[cyan]Options: {', '.join(enum_values)}[/cyan]"

        # Add constraint information
        constraints = []
        if "minimum" in info and "maximum" in info:
            constraints.append(f"Range: {info['minimum']}-{info['maximum']}")
        elif "minimum" in info:
            constraints.append(f"Min: {info['minimum']}")
        elif "maximum" in info:
            constraints.append(f"Max: {info['maximum']}")

        if "minLength" in info:
            constraints.append(f"MinLen: {info['minLength']}")
        if "maxLength" in info:
            constraints.append(f"MaxLen: {info['maxLength']}")

        if constraints:
            desc += f"\n[yellow]{' | '.join(constraints)}[/yellow]"

        # Add format information
        if format_info := info.get("format"):
            desc += f"\n[green]Format: {format_info}[/green]"

        # Add units
        if units := info.get("units"):
            desc += f"\n[blue]Units: {units}[/blue]"

        # Add default values (only for optional parameters)
        if show_defaults and (default := info.get("default")):
            desc += f"\n[magenta]Default: {default}[/magenta]"

        # Add example
        if "example" in info:
            desc += f"\n[dim]Example: {info['example']}[/dim]"

        return param_type, desc

    def list_methods(self, filter_text: Optional[str] = None):
        """List all available methods."""
        if not self.api_definition:
            self.print_error("No API definition loaded")
            return

        operations = self.api_definition.get("operations", {})

        # Filter if requested
        if filter_text:
            operations = {
                name: info
                for name, info in operations.items()
                if filter_text.lower() in name.lower()
                or filter_text.lower() in info.get("description", "").lower()
            }

        # Create a rich table
        table = Table(title=f"[bold]VoIP.ms API Methods[/bold] ({len(operations)} found)")
        table.add_column("Method", style="cyan", no_wrap=True, width=30)
        table.add_column("Description", style="white")
        table.add_column("Category", style="green", width=12)

        # Group and add methods
        for name, info in sorted(operations.items()):
            prefix = (
                name.split(next(c for c in name if c.isupper()))[0]
                if any(c.isupper() for c in name)
                else "other"
            )
            desc = info.get("description", "No description")
            table.add_row(name, desc, prefix.upper())

        self.console.print(table)

    def apply_smart_defaults(self, method_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Apply smart defaults based on method context."""
        result = params.copy()

        # Check each category of defaults
        for category, config in self.smart_defaults.items():
            if category == "method_descriptions":
                continue  # Skip descriptions

            if "methods" in config and method_name in config["methods"]:
                defaults = config.get("defaults", {})

                # Apply date-specific logic
                if category == "date_methods":
                    # Handle date parameter mapping
                    param_mapping = config.get("parameter_mapping", {})
                    mapping = param_mapping.get(method_name, param_mapping.get("default", {}))

                    # Default to last N days if no dates provided
                    date_range_days = defaults.get("date_range_days", 7)

                    # Check for date_from
                    from_param = mapping.get("from", "date_from")
                    if from_param not in result and not any(
                        p in result for p in ["from_date", "from"]
                    ):
                        result[from_param] = (
                            datetime.now() - timedelta(days=date_range_days)
                        ).strftime("%Y-%m-%d")
                        self.console.print(
                            f"[yellow]ℹ Added default {from_param}={result[from_param]}[/yellow]"
                        )

                    # Check for date_to
                    to_param = mapping.get("to", "date_to")
                    if to_param not in result and not any(p in result for p in ["to_date", "to"]):
                        result[to_param] = datetime.now().strftime("%Y-%m-%d")
                        self.console.print(
                            f"[yellow]ℹ Added default {to_param}={result[to_param]}[/yellow]"
                        )

                    # Apply other defaults (like timezone)
                    for param, value in defaults.items():
                        if param not in ["date_range_days"] and param not in result:
                            result[param] = value
                            self.console.print(f"[yellow]ℹ Added default {param}={value}[/yellow]")
                else:
                    # Apply all defaults for non-date methods
                    for param, value in defaults.items():
                        if param not in result:
                            result[param] = value
                            # Add description for certain defaults
                            desc = ""
                            if param == "billing_type" and value == 1:
                                desc = " (per minute)"
                            elif param == "pop":
                                desc = " (server location)"
                            elif param.endswith("_timeout") or param == "dialtime":
                                desc = " seconds"
                            self.console.print(
                                f"[yellow]ℹ Added default {param}={value}{desc}[/yellow]"
                            )

        return result

    def show_method_help(self, method_name: str):
        """Show detailed help for a method."""
        method_info = self.get_method_info(method_name)

        if not method_info:
            self.print_error(f"Unknown method: {method_name}")
            self.show_similar_methods(method_name)
            return

        # Create a panel for the method
        self.console.print(
            Panel(
                f"[bold cyan]{method_name}[/bold cyan]\n\n{method_info.get('description', 'No description available')}",
                title="[bold]API Method[/bold]",
                border_style="cyan",
            )
        )

        parameters = method_info.get("parameters", {})
        if parameters:
            # Create parameter tables
            required = [
                (name, info) for name, info in parameters.items() if info.get("required", False)
            ]
            optional = [
                (name, info) for name, info in parameters.items() if not info.get("required", False)
            ]

            if required:
                req_table = Table(title="[yellow]Required Parameters[/yellow]", show_header=True)
                req_table.add_column("Parameter", style="yellow", width=20)
                req_table.add_column("Type", style="cyan", width=10)
                req_table.add_column("Description", style="white")

                for name, info in required:
                    param_type, desc = self._format_parameter_info(name, info)
                    req_table.add_row(f"--{name}", param_type, desc)

                self.console.print(req_table)

            if optional:
                opt_table = Table(title="[green]Optional Parameters[/green]", show_header=True)
                opt_table.add_column("Parameter", style="green", width=20)
                opt_table.add_column("Type", style="cyan", width=10)
                opt_table.add_column("Description", style="white")

                for name, info in optional:
                    param_type, desc = self._format_parameter_info(name, info, show_defaults=True)
                    opt_table.add_row(f"--{name}", param_type, desc)

                self.console.print(opt_table)

        # Show smart defaults if applicable
        method_descriptions = self.smart_defaults.get("method_descriptions", {})
        if method_name in method_descriptions:
            self.console.print(
                Panel(
                    f"[green]{method_descriptions[method_name]}[/green]",
                    title="[bold green]Smart Defaults[/bold green]",
                    border_style="green",
                )
            )

        # Show example
        if parameters:
            required_params = [
                f"--{name}=<value>"
                for name, info in parameters.items()
                if info.get("required", False)
            ]
            example_cmd = f"voipms {method_name} {' '.join(required_params)}"
            self.console.print(
                Panel(
                    Syntax(example_cmd, "bash", theme="monokai"),
                    title="[bold]Example Usage[/bold]",
                    border_style="blue",
                )
            )


# Create global CLI instance
cli_instance = VoIPMSCLI()


@click.group(invoke_without_command=True)
@click.option("--username", envvar="VOIPMS_USERNAME", help="VoIP.ms username")
@click.option("--password", envvar="VOIPMS_API_PASSWORD", help="VoIP.ms API password")
@click.option("--pretty/--raw", default=True, help="Pretty print JSON output")
@click.pass_context
def cli(ctx, username: Optional[str], password: Optional[str], pretty: bool):
    """VoIP.ms API Client - Data-Driven CLI

    This CLI dynamically supports all VoIP.ms API methods based on the
    API definition. Methods and parameters are not hardcoded.

    \b
    Usage:
      voipms <method> [options]
      voipms list-methods [--filter=text]
      voipms help <method>

    \b
    Examples:
      voipms getBalance
      voipms getDIDsInfo --did=5551234567
      voipms sendSMS --did=5551234567 --destination=5559876543 --message="Hello"
    """
    # Initialize client
    cli_instance.init_client(username, password)

    # Store context
    ctx.ensure_object(dict)
    ctx.obj["pretty"] = pretty

    # If no command given, show help
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command("list-methods")
@click.option("--filter", "filter_text", help="Filter methods by name or description")
def list_methods_cmd(filter_text: Optional[str]):
    """List all available API methods."""
    cli_instance.list_methods(filter_text)


@cli.command("help")
@click.argument("method")
def help_cmd(method: str):
    """Show detailed help for a specific API method."""
    cli_instance.show_method_help(method)


@cli.command("api-info")
def api_info_cmd():
    """Show API definition information."""
    if not cli_instance.api_definition:
        cli_instance.print_error("No API definition loaded")
        return

    metadata = cli_instance.api_definition.get("metadata", {})
    operations = cli_instance.api_definition.get("operations", {})

    click.echo(click.style("VoIP.ms API Information", bold=True))
    click.echo(f"\nTotal operations: {len(operations)}")
    click.echo(f"Generated: {metadata.get('generated_at', 'Unknown')}")
    click.echo(f"Generator version: {metadata.get('generator_version', 'Unknown')}")
    click.echo(f"Documentation source: {metadata.get('documentation_source', 'Unknown')}")

    # Count by prefix
    prefixes = {}
    for name in operations:
        prefix = (
            name.split(next(c for c in name if c.isupper()))[0]
            if any(c.isupper() for c in name)
            else "other"
        )
        prefixes[prefix] = prefixes.get(prefix, 0) + 1

    click.echo("\nMethods by category:")
    for prefix, count in sorted(prefixes.items()):
        click.echo(f"  {prefix:<15} : {count:>3} methods")


# Dynamic command handler
@cli.command(
    context_settings={
        "ignore_unknown_options": True,
        "allow_extra_args": True,
    }
)
@click.argument("method")
@click.pass_context
def method_handler(ctx, method: str):
    """Dynamic handler for API methods."""
    # This is a catch-all that won't actually be used
    pass


# Store original invoke
original_invoke = cli.invoke


def custom_invoke(self, ctx):
    """Custom invoke to handle dynamic method calls."""
    # Get the full command line args
    import sys

    full_args = sys.argv[1:]  # Skip script name

    # Extract command name
    cmd_name = None
    cmd_args = []
    for i, arg in enumerate(full_args):
        if not arg.startswith("-"):
            cmd_name = arg
            cmd_args = full_args[i + 1 :]
            break

    # If it's a registered command, use normal Click handling
    if cmd_name in self.commands:
        return original_invoke(ctx)

    # Otherwise, treat it as an API method call
    if cmd_name:
        # Make sure client is initialized
        if not cli_instance.api_definition:
            cli_instance.init_client()

        method_info = cli_instance.get_method_info(cmd_name)
        if method_info:
            # Parse parameters from remaining arguments
            params = {}
            for arg in cmd_args:
                if arg.startswith("--"):
                    if "=" in arg:
                        key, value = arg[2:].split("=", 1)
                        # Convert types based on API definition
                        param_info = method_info.get("parameters", {}).get(key, {})
                        param_type = param_info.get("type", "string")

                        if param_type == "integer":
                            try:
                                value = int(value)
                            except ValueError:
                                cli_instance.print_error(f"Parameter {key} must be an integer")
                                sys.exit(1)
                        elif param_type == "number":
                            try:
                                value = float(value)
                            except ValueError:
                                cli_instance.print_error(f"Parameter {key} must be a number")
                                sys.exit(1)
                        elif param_type == "boolean":
                            value = value.lower() in ("true", "1", "yes", "on")
                        elif param_type == "string":
                            # Check for date parameters and parse flexible formats
                            if any(
                                keyword in key.lower()
                                for keyword in ["date", "_from", "_to", "start", "end"]
                            ):
                                try:
                                    import dateparser

                                    parsed_date = dateparser.parse(value)
                                    if parsed_date:
                                        # Convert to API-required YYYY-MM-DD format
                                        value = parsed_date.strftime("%Y-%m-%d")
                                except (ImportError, Exception):
                                    # Keep original value if dateparser unavailable or parsing fails
                                    pass

                            # Let the client handle boolean conversions via custom types
                            # Only validate non-boolean enums here
                            enum_values = param_info.get("enum", [])
                            if enum_values:
                                # Skip validation for boolean-like enums - they'll be handled by custom types
                                if set(enum_values) in [
                                    {"0", "1"},
                                    {"1", "0"},
                                    {"true", "false"},
                                    {"false", "true"},
                                    {"yes", "no"},
                                    {"no", "yes"},
                                ]:
                                    pass  # Custom types will handle conversion and validation
                                elif value not in enum_values:
                                    # General enum validation for non-boolean enums
                                    cli_instance.print_error(
                                        f"Parameter {key} must be one of: {', '.join(enum_values)}"
                                    )
                                    cli_instance.print_error(f"You provided: {value}")
                                    sys.exit(1)

                        params[key] = value
                    else:
                        cli_instance.print_error(f"Invalid parameter format: {arg}")
                        cli_instance.print_error("Use --param=value format")
                        sys.exit(1)

            # Apply smart defaults
            params = cli_instance.apply_smart_defaults(cmd_name, params)

            # Show HTML defaults that would be applied
            if cli_instance.api_definition:
                op_spec = cli_instance.api_definition.get("operations", {}).get(cmd_name, {})
                param_specs = op_spec.get("parameters", {})
                html_defaults = []
                for param_name, param_spec in param_specs.items():
                    if param_name not in params and param_spec.get("default") is not None:
                        default_val = param_spec["default"]
                        if default_val == "Today":
                            from datetime import datetime

                            default_val = datetime.now().strftime("%Y-%m-%d")
                        html_defaults.append(f"{param_name}={default_val}")

                if html_defaults:
                    cli_instance.console.print(
                        f"[cyan]ℹ HTML defaults will be applied: {', '.join(html_defaults)}[/cyan]"
                    )

            # Check required parameters (after applying defaults)
            required_params = [
                name
                for name, info in method_info.get("parameters", {}).items()
                if info.get("required", False)
            ]
            missing = [p for p in required_params if p not in params]
            if missing:
                cli_instance.print_error(f"Missing required parameters: {', '.join(missing)}")
                click.echo(f"\nUse 'voipms help {cmd_name}' for more information.")
                sys.exit(1)

            # Call the method
            pretty = ctx.obj.get("pretty", True) if ctx.obj else True
            cli_instance.call_method(cmd_name, params, pretty)
            return

    # If we get here, it's an unknown command
    if cmd_name:
        cli_instance.print_error(f"Unknown command: {cmd_name}")
        cli_instance.show_similar_methods(cmd_name)
        click.echo("\nUse 'voipms list-methods' to see all available methods.")
    else:
        click.echo(ctx.get_help())


# Monkey patch the invoke method
# pylint: disable=no-value-for-parameter
cli.invoke = custom_invoke.__get__(cli)
# pylint: enable=no-value-for-parameter


def main():
    """Main entry point."""
    # pylint: disable=no-value-for-parameter
    cli()
    # pylint: enable=no-value-for-parameter


if __name__ == "__main__":
    main()
