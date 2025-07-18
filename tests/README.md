# Test Suite

This directory contains tests for the VoIP.ms Python client.

## Test Files

- **test_client.py** - Unit tests for the client functionality (mocked)
- **test_api_examples.py** - Tests based on official PHP examples (mocked)
- **test_fixtures.json** - Test data extracted from PHP examples

## Test Categories

### Unit Tests (test_client.py)
- Client initialization
- Dynamic method creation
- Parameter validation
- Error handling
- Async client functionality

### API Example Tests (test_api_examples.py)
Generated from the official VoIP.ms PHP examples, these tests ensure our client handles the same use cases as the official examples:
- `getLanguages` - Basic API call
- `getRegistrationStatus` - With account parameter
- `getClients` - With email filtering
- `getSubAccounts` - Account management
- `getVoicemails` - Mailbox queries
- `getCDR` - Call detail records
- And more...

These tests validate that:
1. Methods accept the expected parameters
2. Responses contain the expected fields
3. Error handling works as documented

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=voipms tests/

# Run specific test file
pytest tests/test_client.py

# Run in verbose mode
pytest -v
```

## Value of PHP Example Tests

The PHP examples provide real-world usage patterns that help ensure:
- Our dynamic method generation creates the right methods
- Parameters are named correctly
- Response structures match what the actual API returns
- Common use cases work as expected

While these tests are mocked (not hitting the real API), they validate that our client structure aligns with official usage patterns.