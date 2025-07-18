# API Source Files

This directory contains the source files used to generate the API definition:

## Files

- **server.wsdl** - The official VoIP.ms SOAP/WSDL file that defines the API structure
- **VoIP.ms - API Documentation.html** - The HTML documentation from VoIP.ms that contains detailed parameter descriptions and examples

## Updating

To get the latest WSDL file:
1. Download from VoIP.ms API documentation page
2. Replace `server.wsdl` in this directory

To get the latest HTML documentation:
1. Use the fetch tool: `python ../tools/fetch_documentation_simple.py`
2. Or manually save the HTML from the VoIP.ms customer portal API documentation page

## Note

These files are the source of truth for the API definition. The JSON file in `src/voipms/` is generated from these files.