# VoIP.ms API Tools

This directory contains tools for maintaining and updating the VoIP.ms API client definition.

## Main Tools

### 1. `generate_api_definition.py` 
**Main generator that creates the comprehensive API definition**

```bash
uv run tools/generate_api_definition.py
```

This tool:
- Fetches the WSDL from VoIP.ms API
- Parses HTML documentation for enhanced metadata
- Generates `src/voipms/api_definition.json` with:
  - All 217 API operations
  - Parameter constraints (ranges, enums, formats)
  - Error codes and descriptions
  - Default values and units
  - Required/optional parameter information

### 2. `generate_type_stubs.py`
**Generates Python type stub files (.pyi) for IDE support**

```bash
uv run tools/generate_type_stubs.py --api-definition=src/voipms/api_definition.json
```

This creates:
- `src/voipms/client.pyi` - Type annotations for all API methods
- `src/voipms/__init__.pyi` - Package type exports
- Includes enhanced Annotated types with constraint information

## Supporting Tools

### `parse_wsdl.py`
- Parses VoIP.ms WSDL to extract API structure
- Handles complex types and nested parameters
- Called by `generate_api_definition.py`

### `parse_html_docs.py` 
- Extracts enhanced metadata from HTML documentation
- Detects constraints, enums, formats, units
- Parses error codes and descriptions
- Called by `generate_api_definition.py`

### `download_api_docs.py`
- Downloads VoIP.ms HTML documentation (requires login)
- Uses Playwright for browser automation
- Useful when documentation updates are needed

### `extract_php_examples.py`
- Extracts test data from VoIP.ms PHP examples
- Creates test fixtures for validation
- Optional utility for test generation

## Workflow for API Updates

When VoIP.ms updates their API:

1. **Regenerate the API definition**:
   ```bash
   uv run tools/generate_api_definition.py
   ```

2. **Regenerate type stubs**:
   ```bash
   uv run tools/generate_type_stubs.py
   ```

3. **Test the changes**:
   ```bash
   # Run any validation tests
   uv run python -m pytest tests/
   ```

## Notes

- The API definition is automatically loaded by the client
- WSDL is fetched directly from VoIP.ms (no authentication needed)
- HTML documentation parsing uses the local copy in `resources/`
- All tools use PEP 723 inline dependencies (uv handles installation)