# API Source Files

This directory contains source documentation used to enhance the API definition.

## Files

- **server.wsdl** - VoIP.ms WSDL file (kept for reference, but fetched automatically during generation)
- **voipms_api_documentation.html** - HTML documentation with detailed parameter metadata

## Updating Documentation

### WSDL (Automatic)
The WSDL is automatically fetched from https://voip.ms/api/v1/server.wsdl when running the generator.
No manual update needed.

### HTML Documentation (Manual)
The HTML documentation requires VoIP.ms login and must be updated manually:

**Option 1: Using the download tool**
```bash
export VOIPMS_USERNAME='your-email@example.com'
export VOIPMS_PASSWORD='your-website-password'
uv run tools/download_api_docs.py
cp api_docs_redirected.html resources/voipms_api_documentation.html
```

**Option 2: Manual download**
1. Login to https://voip.ms
2. Navigate to https://voip.ms/m/apidocs.php
3. Save the complete page as `voipms_api_documentation.html` in this directory

## Usage

After updating the HTML documentation, regenerate the API definition:
```bash
uv run tools/generate_api_definition.py
```

This combines:
- Fresh WSDL structure (fetched automatically)
- Enhanced metadata from the HTML documentation (constraints, enums, error codes)

## Note

The HTML documentation is essential for:
- Parameter constraints (min/max values, string lengths)
- Enum values (valid options for parameters)
- Error code descriptions
- Default values and units
- Required/optional parameter detection