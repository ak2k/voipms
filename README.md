# voipms

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern, type-safe Python client for the VoIP.ms API with Pydantic validation, async support, and a rich CLI.

## Features

- 🚀 **Complete API Coverage**: All 200+ VoIP.ms API methods dynamically generated from the official WSDL
- 🔍 **Full Type Safety**: Pydantic models with comprehensive type hints and validation
- ⚡ **Async Support**: Both sync and async clients for optimal performance
- 🎨 **Rich CLI**: Beautiful command-line interface with auto-completion and formatted output
- 📝 **Smart Validation**: Automatic type coercion, date parsing, and constraint validation
- 🔧 **IDE Friendly**: Generated .pyi stubs for perfect auto-completion
- 📊 **Data-Driven**: Two-stage API definition - source from WSDL/HTML, runtime with quirks

## Installation

```bash
pip install voipms
```

Or install from source:

```bash
git clone https://github.com/your-username/voipms.git
cd voipms
pip install -e .
```

## Quick Start

1. **Set your credentials:**

```bash
# Get your API credentials from https://voip.ms/m/api.php
export VOIPMS_USERNAME='your-email@example.com'
export VOIPMS_API_PASSWORD='your-api-password'
```

2. **Use the client:**

```python
from voipms import VoIPMSClient

# Create client (credentials from environment)
client = VoIPMSClient()

# Get account balance
balance = client.getBalance()
print(f"Balance: ${balance['balance']['current_balance']}")

# Get CDR (with automatic date range)
cdr = client.getCDR(answered=True)
print(f"Found {len(cdr['cdr'])} calls")
```

3. **Async example:**

```python
from voipms import VoIPMSClientAsync
import asyncio

async def main():
    async with VoIPMSClientAsync() as client:
        balance = await client.getBalance()
        print(f"Balance: ${balance['balance']['current_balance']}")

asyncio.run(main())
```

4. **CLI usage:**

```bash
# After installation
voipms getBalance
voipms getServersInfo
voipms getCDR --answered=true --days=7

# Get help
voipms --help
voipms list-methods
voipms help getCDR
```

## Advanced Features

### String-Numeric Validation

The client properly validates string parameters that represent numeric values:

```python
# These all work correctly:
client.setDIDInfo(did="5551234567", callerid_prefix="1")  # Valid: "1" is numeric
client.setDIDInfo(did="5551234567", callerid_prefix=1)    # Also valid: converts to "1"

# This raises ValidationError:
client.setDIDInfo(did="5551234567", callerid_prefix="abc")  # Invalid: not numeric
```

### Date Parsing

The client uses dateparser for flexible date inputs:

```python
# All of these work:
client.getCDR(date_from="2025-01-01", date_to="2025-01-31")
client.getCDR(date_from="yesterday", date_to="today")
client.getCDR(date_from="1 week ago", date_to="now")
```

### Complete Type Hints

Every method has full type hints with detailed parameter information:

```python
# Your IDE will show:
def getCDR(
    self,
    date_from: Annotated[str, Field(description="Start date for CDR retrieval")],
    date_to: Annotated[str, Field(description="End date for CDR retrieval")],
    answered: Annotated[Literal["0", "1"], Field(description="Include answered calls")] = None,
    # ... all parameters with descriptions and constraints
) -> Dict[str, Any]:
```

## Project Structure

```
voipms/
├── src/voipms/          # Main package
│   ├── __init__.py
│   ├── base_client.py   # Base client with shared functionality
│   ├── client.py        # Synchronous client implementation
│   ├── async_client.py  # Asynchronous client implementation
│   ├── method_factory.py # Dynamic method generation
│   ├── validation.py    # Pydantic model factory
│   ├── types.py         # Type validators and converters
│   ├── api_quirks.py    # API-specific quirk handling
│   ├── cli.py           # Rich CLI interface
│   ├── api_definition.json    # Complete API metadata
│   ├── api_quirks.json        # API quirks configuration
│   ├── cli_smart_defaults.json # CLI smart defaults
│   └── *.pyi            # Generated type stubs
├── resources/           # Source files for API definition
│   ├── server.wsdl      # VoIP.ms WSDL file
│   └── voipms_api_documentation.html  # HTML docs
├── tools/               # API definition generation tools
│   ├── cli.py           # Unified tools CLI
│   ├── commands/        # CLI command implementations
│   ├── parsers/         # WSDL and HTML parsers
│   ├── config/          # Tool configurations
│   ├── generate_api_definition.py
│   ├── generate_type_stubs.py
│   └── download_api_docs.py
├── examples/            # Example scripts
│   ├── basic_usage.py
│   ├── async_usage.py
│   └── backup_account_complete.py
└── tests/              # Test suite

## Regenerating the API Definitions

### Quick Regeneration

To regenerate all API definitions and type stubs:

```bash
# Regenerate everything (recommended)
uv run tools/cli.py generate
```

This runs three stages automatically:
1. **Source Generation**: Creates `api_definition_source.json` from WSDL/HTML
2. **Quirks Application**: Creates `api_definition.json` with runtime adjustments
3. **Type Stubs**: Updates `.pyi` files for IDE support

### When to Regenerate

Regenerate the API definitions when:

1. **VoIP.ms Updates Their API**:
   ```bash
   # First, update HTML documentation
   cp /path/to/voipms_api_documentation.html resources/
   
   # Then regenerate
   uv run tools/cli.py generate
   ```

2. **You Add New Quirks**:
   ```bash
   # Edit src/voipms/api_quirks.json
   # Then regenerate (only stages 2-3 needed)
   uv run tools/cli.py generate --stage=quirks
   uv run tools/cli.py generate --stage=stubs
   ```

3. **You Update Type Overrides**:
   ```bash
   # Edit tools/config/type_overrides.json
   # Then regenerate everything
   uv run tools/cli.py generate
   ```

### Individual Stages (for debugging)

```bash
# Stage 1: Generate source definition from WSDL/HTML
uv run tools/cli.py generate --stage=source

# Stage 2: Apply quirks to source definition
uv run tools/cli.py generate --stage=quirks

# Stage 3: Generate Python type stubs
uv run tools/cli.py generate --stage=stubs
```

### API Definition Files

The system uses a two-stage approach:

| File | Purpose | Generated By |
|------|---------|-------------|
| `api_definition_source.json` | Pure API definition from WSDL/HTML | `--stage=source` |
| `api_definition.json` | Runtime definition with quirks applied | `--stage=quirks` |
| `api_quirks.json` | Behavioral adjustments and fixes | Manually edited |

The client loads `api_definition.json` at runtime, which includes all quirks and adjustments.

## Development

This project uses [uv](https://github.com/astral-sh/uv) for dependency management:

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Run linting
uv run ruff check .
uv run mypy src/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This is an independent project and is not affiliated with or endorsed by VoIP.ms.