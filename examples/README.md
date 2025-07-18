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

## Account State Dumps

### Synchronous Versions

#### `dump_account_full.py`
Calls ALL 70+ read-only API methods to create a complete backup of your account state.
Takes ~30-40 seconds. Output can be several MB.

```bash
uv run dump_account_full.py --list  # See what would be called
uv run dump_account_full.py         # Run the full dump
```

#### `dump_account_categorized.py`
Same data as full dump but organized by category (Account Info, Phone Numbers, Billing, etc.)
for better readability.

```bash
uv run dump_account_categorized.py
```

### Async Versions (6-8x Faster!)

#### `dump_account_full_async.py`
Same as full dump but uses async/await to call all methods in parallel.
Completes in ~5 seconds instead of 30-40 seconds!

```bash
uv run dump_account_full_async.py
```

#### `dump_account_categorized_async.py`
Categorized dump using async. Much faster execution.

```bash
uv run dump_account_categorized_async.py
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