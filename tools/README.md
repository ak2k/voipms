# VoIP.ms API Tools

This directory contains tools for maintaining and updating the VoIP.ms API client.

## Essential Tools

### 1. `download_api_docs.py`
Downloads the latest API documentation from VoIP.ms using Playwright.

```bash
# Install Playwright browser first (one-time setup)
uv run --with playwright playwright install chromium

# Run the downloader (dependencies handled automatically)
./download_api_docs.py
```

This will:
- Open a browser window
- Login to VoIP.ms automatically (using VOIPMS_USERNAME and VOIPMS_PASSWORD env vars)
- Navigate to the API documentation
- Save it as `api_docs_redirected.html`

### 2. `generate_api_json.py`
Generates the enriched API definition by combining WSDL and HTML documentation.

```bash
./generate_api_json.py
```

This creates `api_definition.json` with:
- All API operations from the WSDL
- Enhanced descriptions from HTML docs
- Parameter requirements and types

## Supporting Files

- `parse_wsdl.py` - WSDL parser that extracts API structure
- `parse_html_docs.py` - HTML documentation parser for descriptions
- `extract_php_examples.py` - Extracts test data from PHP examples

## Workflow

When VoIP.ms updates their API:

1. **Download latest documentation**:
   ```bash
   # Set credentials
   export VOIPMS_USERNAME='your-email@example.com'
   export VOIPMS_PASSWORD='your-website-password'
   
   # Download docs
   ./download_api_docs.py
   
   # Copy to resources
   cp api_docs_redirected.html ../resources/voipms_api_documentation.html
   ```

2. **Regenerate API definition**:
   ```bash
   ./generate_api_json.py
   ```

3. **The client will automatically use the updated definition**

## Important Notes

- The HTML documentation requires authentication to access
- The documentation contains `[Required]` and `[Optional]` markers for parameters
- The WSDL provides structure but not parameter requirements
- Always test after regenerating the API definition