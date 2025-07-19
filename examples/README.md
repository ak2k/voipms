# VoIP.ms Python Client Examples

All examples use safe, read-only operations unless noted otherwise.

## Basic Examples

### `basic_usage.py`
The simplest starting point - shows how to get balance, registration status, and servers.

### `async_usage.py`
Same as basic_usage but using the async client.

## Account Information

### `account_summary.py`
Comprehensive account overview including sub-accounts, voicemail boxes, and registration status.

## Complete Account Backups

### `backup_account_simple.py`
Simple backup of all account configuration that doesn't require parameters.
Perfect for regular configuration backups. Backs up ~50 settings in categories.

```bash
uv run backup_account_simple.py
# Creates: voipms_backup_simple_YYYY-MM-DD.json
```

### `backup_account_complete.py`
Comprehensive backup including call history, SMS/MMS, and per-DID settings.
More complex but captures everything possible.

```bash
uv run backup_account_complete.py --days 90  # Last 90 days of history
uv run backup_account_complete.py --days 7   # Last week only
```

### `backup_complete_categorized.py`
Same data as backup_account_complete but organized by category (Account Info, Phone Numbers, Billing, etc.)
for better readability. Uses async for 6-8x faster execution (~5 seconds vs 30-40 seconds).

```bash
uv run backup_complete_categorized.py
```

## Advanced Examples

### `inspect_call_recordings.py`
Analyzes call recordings metadata and compares with CDR (Call Detail Records).
Can optionally download actual recording files.

```bash
uv run inspect_call_recordings.py --days 30
uv run inspect_call_recordings.py --download  # Downloads audio files
```

## Running Examples

All examples can be run directly with `uv`:

```bash
# Set your credentials
export VOIPMS_USERNAME='your-email@example.com'
export VOIPMS_API_PASSWORD='your-api-password'

# Run any example
uv run basic_usage.py
```

Or if you've installed the package:

```bash
python3 basic_usage.py
```

## Notes

- All examples require environment variables `VOIPMS_USERNAME` and `VOIPMS_API_PASSWORD`
- The API password is different from your web login password
- Set your API password at: https://voip.ms/m/api.php
- All examples use PEP-723 inline script dependencies