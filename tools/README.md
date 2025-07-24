# VoIP.ms API Tools

This directory contains tools for maintaining and updating the VoIP.ms API client definition.

## Quick Start: Regenerating API Definitions

```bash
# Regenerate everything (recommended)
uv run tools/cli.py generate

# This automatically runs all three stages:
# 1. source: Generate api_definition_source.json from WSDL/HTML
# 2. quirks: Apply quirks to create api_definition.json
# 3. stubs: Generate Python type stubs (.pyi files)
```

## Unified CLI Interface

### Generate Command

The `generate` command handles all API definition generation:

```bash
# Full regeneration (all stages)
uv run tools/cli.py generate

# Individual stages for specific updates:
uv run tools/cli.py generate --stage=source  # Update from WSDL/HTML
uv run tools/cli.py generate --stage=quirks  # Reapply quirks only
uv run tools/cli.py generate --stage=stubs   # Regenerate type stubs only

# Verbose output for debugging
uv run tools/cli.py generate --verbose
```

### Other Commands

```bash
# Show all available commands
uv run tools/cli.py --help

# Download API documentation (requires login)
uv run tools/cli.py download
```

## Main Tools

### Understanding the Three-Stage Generation Process

#### Stage 1: Source Generation (`--stage=source`)
**What it does**: Creates a pure API definition from official sources

- Fetches WSDL from https://voip.ms/api/v1/server.wsdl
- Parses HTML documentation from `resources/voipms_api_documentation.html`
- Extracts cross-references (_values_from) from documentation
- Applies type corrections from `tools/config/api_corrections.json`
- **Output**: `tools/generated/api_definition_source.json`

**When to run**: When VoIP.ms updates their API or you update type overrides

#### Stage 2: Quirks Application (`--stage=quirks`)
**What it does**: Applies behavioral adjustments to create runtime definition

- Reads `tools/generated/api_definition_source.json`
- Applies corrections from `tools/config/api_corrections.json`:
  - Parameter type conversions (boolean → yes/no)
  - Parameter aliases (date_from → from)
  - Smart defaults
  - Additional error codes
  - Special value mappings
  - Cross-reference (_values_from) information
- **Output**: `src/voipms/api_definition.json` (used by the client)

**When to run**: When you add/modify quirks or after stage 1

#### Stage 3: Type Stub Generation (`--stage=stubs`)
**What it does**: Creates Python type hints for IDE support

- Reads `src/voipms/api_definition.json` (with quirks applied)
- Generates `.pyi` stub files
- **Output**: `src/voipms/client.pyi`, `src/voipms/__init__.pyi`

**When to run**: After stages 1-2 or when stub generation logic changes

### 2. API Definition Files

The system uses two API definition files:

- **`tools/generated/api_definition_source.json`**: Pure API definition from WSDL/HTML documentation
- **`src/voipms/api_definition.json`**: Runtime API definition with quirks applied (used by the client)

Corrections are behavioral adjustments discovered through testing, stored in `api_corrections.json`:
- Parameter type conversions (e.g., boolean → yes/no strings)
- Parameter aliases (e.g., `date_from` → `from`)
- Smart defaults
- Additional error codes not in documentation
- Special value mappings
- Cross-reference information (_values_from) for decoding numeric codes

### 3. Documentation Downloader
**Downloads VoIP.ms HTML documentation (requires login)**

```bash
uv run tools/cli.py download
# Or directly: uv run tools/download_api_docs.py
```

Options:
- `--headless` - Run browser in headless mode
- `--methods` - Download specific method pages

## Project Structure

```
tools/
├── cli.py              # Unified CLI interface
├── commands/           # CLI command implementations
│   ├── generate.py     # API and stub generation commands
│   └── download.py     # Documentation download command
├── parsers/            # Parsing modules
│   ├── wsdl.py        # WSDL parser (from parse_wsdl.py)
│   └── html_parser.py # HTML parser (from parse_html_docs.py)
├── config/            # Configuration files
│   └── api_corrections.json  # API corrections and type overrides
├── generate_api_definition.py  # Legacy direct script
├── generate_type_stubs.py      # Legacy direct script
└── download_api_docs.py        # Legacy direct script
```

## Configuration Files

### `config/api_corrections.json`
Contains all API corrections and overrides:
- Type corrections for WSDL errors
- Parameter transformations (boolean → yes/no)
- Smart defaults for methods
- Cross-reference information (_values_from)
- Additional error codes
- Category overrides for proper documentation organization

## Common Regeneration Scenarios

### 1. When VoIP.ms Updates Their API

```bash
# Step 1: Update HTML documentation
# Option A: Use the download tool
export VOIPMS_USERNAME='your-email@example.com'
export VOIPMS_PASSWORD='your-website-password'
uv run tools/cli.py download
cp api_docs_redirected.html resources/voipms_api_documentation.html

# Option B: Manual download
# 1. Login to https://voip.ms
# 2. Navigate to https://voip.ms/m/apidocs.php
# 3. Save page as resources/voipms_api_documentation.html

# Step 2: Regenerate everything
uv run tools/cli.py generate
```

### 2. When You Discover New Quirks

```bash
# Step 1: Edit tools/config/api_corrections.json
# Add your correction to the appropriate method

# Step 2: Regenerate (only stages 2-3 needed)
uv run tools/cli.py generate --stage=quirks  # Apply updated corrections
uv run tools/cli.py generate --stage=stubs   # Update type stubs
```

### 3. When You Fix Type Overrides

```bash
# Step 1: Edit tools/config/api_corrections.json
# Add type correction for WSDL errors

# Step 2: Regenerate everything (source needs updating)
uv run tools/cli.py generate
```

### 4. Quick Regeneration After Code Changes

```bash
# If you only changed quirks handling logic
uv run tools/cli.py generate --stage=quirks

# If you changed type stub generation logic
uv run tools/cli.py generate --stage=stubs
```

3. **Test the changes**:
   ```bash
   # Verify the client still works
   uv run python -c "from voipms import VoIPMSClient; print(f'Loaded {len(VoIPMSClient().get_available_methods())} methods')"
   ```

## Architecture Notes

- **Data-Driven Design**: All API metadata is stored in JSON, no hardcoded methods
- **Type Safety**: Comprehensive type overrides fix WSDL inconsistencies
- **Modular Parsers**: WSDL and HTML parsers are separate modules
- **Configuration-Based**: Type overrides and other settings are externalized

## Adding New Type Overrides

If you discover new type errors in the WSDL:

1. Add the override to `tools/config/api_corrections.json`:
   ```json
   {
     "operations": {
       "methodName": {
         "parameters": {
           "parameterName": {
             "type": "string",
             "_type_override_reason": "Explain why this override is needed"
           }
         }
       }
     }
   }
   ```

2. Document the reason in the appropriate category

3. Regenerate the API definition:
   ```bash
   uv run tools/cli.py generate api
   ```

## Key Files

- **`tools/generated/api_definition_source.json`**: Pure API definition from WSDL/HTML
- **`src/voipms/api_definition.json`**: Runtime API definition with corrections (loaded by client)
- **`tools/config/api_corrections.json`**: Behavioral adjustments, fixes, and type overrides
- **`resources/voipms_api_documentation.html`**: Cached HTML documentation

## Troubleshooting Regeneration

### Regenerated files seem unchanged?
```bash
# Check if quirks are being applied
jq '._metadata' src/voipms/api_definition.json
# Should show: "quirks_applied": true

# Check specific quirks
jq '.operations.setVoicemail._applied_quirks' src/voipms/api_definition.json
```

### Type stubs not updating?
```bash
# Force regenerate stubs only
uv run tools/cli.py generate --stage=stubs

# Check if py.typed exists
ls src/voipms/py.typed
```

### Need to verify changes?
```bash
# Compare source vs runtime definitions
diff -u <(jq '.operations.getCDR.parameters' tools/generated/api_definition_source.json) \
        <(jq '.operations.getCDR.parameters' src/voipms/api_definition.json)
```

## Notes

- The client loads `api_definition.json` (with quirks) at runtime
- WSDL is fetched automatically from https://voip.ms/api/v1/server.wsdl
- HTML documentation must be manually updated in `resources/voipms_api_documentation.html`
- HTML docs require VoIP.ms login to access (https://voip.ms/m/apidocs.php)
- All tools use PEP 723 inline dependencies (uv handles installation automatically)