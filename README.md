# VoIP.ms Python Client

A modern, data-driven Python client for the VoIP.ms API that dynamically creates methods from a JSON API definition.

## Features

- **Data-Driven Architecture**: All API details stored in JSON, no code generation needed
- **Dynamic Method Creation**: Methods created at runtime from API definition
- **Full Documentation**: Rich parameter descriptions from HTML documentation
- **Type Validation**: Pydantic-based validation with automatic type coercion
- **Async/Sync Support**: Both synchronous and asynchronous clients
- **Auto-completion Friendly**: Supports both camelCase and snake_case method names
- **Easy Updates**: Just regenerate the JSON when the API changes
- **CLI Support**: Command-line interface for all API methods

## Installation

```bash
pip install voipms-python
```

Or install from source:

```bash
git clone https://github.com/yourusername/voipms-python.git
cd voipms-python
pip install -e .
```

## Quick Start

1. **Set your credentials:**

Option A: Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
# Edit .env with your credentials
```

Option B: Export environment variables:
```bash
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

# Get server info
servers = client.getServersInfo()
print(f"Found {len(servers['servers'])} servers")
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
voipms getDIDsInfo --did=5551234567

# Get help
voipms --help
voipms list-methods
voipms help getBalance
```

## Project Structure

```
voipms-python/
├── src/voipms/          # Main package
│   ├── __init__.py
│   ├── client.py        # Data-driven client implementation
│   └── voipms_api_enriched.json  # API definition
├── resources/           # Source files for API definition
│   ├── server.wsdl      # VoIP.ms WSDL file
│   └── VoIP.ms - API Documentation.html  # HTML docs
├── tools/               # Generation tools
│   ├── enhanced_json_generator.py
│   ├── json_api_generator.py
│   ├── html_documentation_parser.py
│   └── fetch_documentation_simple.py
├── examples/            # Example scripts
│   ├── simple_example.py
│   ├── async_example.py
│   └── example_usage.py
├── tests/              # Unit tests
│   └── test_client.py
└── docs/               # Documentation

## Updating the API Definition

When VoIP.ms updates their API:

```bash
cd tools
# With existing HTML documentation
python enhanced_json_generator.py

# Copy updated definition to package
cp voipms_api_enriched.json ../src/voipms/
```

## Architecture Benefits

1. **No Code Generation**: Methods are created dynamically at runtime
2. **Single Source of Truth**: All API details in one JSON file
3. **Easy Maintenance**: Update JSON without touching client code
4. **Full Introspection**: Query available methods and their documentation
5. **Type Safety**: Parameters validated against schema

## Technical Notes

- VoIP.ms REST API uses GET requests with query parameters (not POST)
- All 217+ API methods are dynamically available without code generation
- Pydantic handles type coercion (e.g., string "123" → int 123 for CLI usage)
- The API definition JSON contains parameter types, descriptions, and requirements

## Dependencies

- httpx (for HTTP requests)
- pydantic (for data validation and type coercion)
- click (for CLI functionality)
- python-dotenv (for environment variable support)
- beautifulsoup4 (for HTML parsing, only needed for generation)
- requests (for fetching docs, only needed for generation)

## License

This is a community project, not affiliated with VoIP.ms.