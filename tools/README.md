# VoIP.ms API Tools

This directory contains tools for generating and maintaining the VoIP.ms API definition.

## Tools

### 1. enhanced_json_generator.py
Main tool that combines WSDL structure with HTML documentation to create a comprehensive API definition.

```bash
# Generate API definition using existing HTML documentation
python enhanced_json_generator.py

# Output: voipms_api_enriched.json
```

### 2. fetch_documentation_simple.py
Downloads the authenticated API documentation from VoIP.ms website.

```bash
# Set credentials
export VOIPMS_USERNAME='your-email@example.com'
export VOIPMS_PASSWORD='your-password'

# Test fetching documentation
python test_fetch_docs.py
```

**Note**: The fetcher performs these steps:
1. Gets the login page
2. Logs in with your credentials
3. Fetches the API documentation page
4. Saves it as HTML

### 3. json_api_generator.py
Base generator that parses WSDL to extract API structure.

### 4. html_documentation_parser.py
Parses HTML documentation to extract parameter descriptions and requirements.

### 5. extract_test_data.py
Extracts test cases from PHP example files.

## Workflow

To update the API definition:

1. **Fetch latest documentation** (optional):
   ```bash
   export VOIPMS_USERNAME='your-email@example.com'
   export VOIPMS_PASSWORD='your-password'
   python test_fetch_docs.py
   ```

2. **Generate enriched API definition**:
   ```bash
   python enhanced_json_generator.py
   ```

3. **Copy to package**:
   ```bash
   cp voipms_api_enriched.json ../src/voipms/
   ```

4. **Run tests**:
   ```bash
   cd ..
   uv run --with pytest --with pytest-asyncio pytest -v
   ```

## Important Notes

- The HTML documentation requires authentication to access
- The documentation contains `[Required]` and `[Optional]` markers for parameters
- The WSDL provides structure but not parameter requirements
- Always test after regenerating the API definition