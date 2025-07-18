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

1. **Update the HTML documentation in resources/**:
   
   The generator fetches WSDL automatically, but you need to update the HTML documentation:
   
   **HTML Documentation** (Requires VoIP.ms login):
   ```bash
   # Option 1: Use the download tool (requires credentials)
   export VOIPMS_USERNAME='your-email@example.com'
   export VOIPMS_PASSWORD='your-website-password'
   uv run tools/download_api_docs.py
   cp api_docs_redirected.html resources/voipms_api_documentation.html
   
   # Option 2: Manual download
   # 1. Login to https://voip.ms
   # 2. Navigate to https://voip.ms/m/apidocs.php
   # 3. Save the page as resources/voipms_api_documentation.html
   ```

2. **Regenerate the API definition**:
   ```bash
   uv run tools/generate_api_definition.py
   ```
   
   This will:
   - Parse the WSDL from `resources/server.wsdl`
   - Extract metadata from `resources/voipms_api_documentation.html`
   - Generate `src/voipms/api_definition.json`

3. **Regenerate type stubs**:
   ```bash
   uv run tools/generate_type_stubs.py
   ```

4. **Test the changes**:
   ```bash
   # Verify the client still works
   uv run python -c "from src.voipms import VoIPMSClient; print(f'Loaded {len(VoIPMSClient().get_available_methods())} methods')"
   ```

## Notes

- The API definition is automatically loaded by the client from `src/voipms/api_definition.json`
- WSDL is fetched automatically from https://voip.ms/api/v1/server.wsdl
- HTML documentation must be manually updated in `resources/voipms_api_documentation.html`
- HTML docs require VoIP.ms login to access (https://voip.ms/m/apidocs.php)
- All tools use PEP 723 inline dependencies (uv handles installation automatically)