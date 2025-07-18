# VoIP.ms API Quirks Analysis Report
## Comprehensive Analysis of External Python-VoIPms Library

This report documents all parameter handling quirks, validation patterns, and API workarounds discovered in the external python-voipms library located at `/Users/akirby/Downloads/voipmsapi/external-voipms/voipms/entities/`.

## 1. Parameter Type Conversions

### 1.1 Boolean to String Conversions
The library extensively converts boolean values to strings ("1" or "0") for the API:

**Helper Function** (`helpers.py`):
```python
def convert_bool(boolean):
    if not isinstance(boolean, bool):
        raise ValueError("Needs to be a bool")
    if boolean:
        return "1"
    else:
        return "0"
```

**Methods Using Boolean Conversions**:
- `accounts.create.sub_account()`: `reseller_chargesetup` → convert_bool()
- `dids.set.sip_uri()`: `callerid_e164` → convert_bool()
- `dids.set.sms()`: `enable`, `email_enabled`, `sms_forward_enable`, `url_callback_enable`, `url_callback_retry` → convert_bool()
- `voicemail.set.voicemail()`: `skip_password` → convert_bool()
- `fax.send.fax_message()`: `send_email_enabled`, `test` → convert_bool()
- `helpers.order()`: `cnam`, `test` → convert_bool()

### 1.2 Integer Type Conversions
Several methods handle integers but pass them through helper functions or special processing:

**Special Cases**:
- `dids.order.*()` methods use a shared `order()` helper function that processes all parameters
- Phone numbers are consistently expected as integers despite being numeric strings in reality
- DIDs are expected as integers (e.g., 5552223333)

### 1.3 String Value Constraints
Many parameters accept only specific string values:

**"yes"/"no" String Values**:
- `voicemail.set.voicemail()`: `attach_message`, `delete_message`, `say_time`, `say_callerid` (validated to only accept "yes" or "no")
- `dids.set.queue()`: Various parameters like `join_when_empty`, `leave_when_empty`, `ring_inuse`
- `clients.set.conference_member()`: `admin`, `start_muted`, `announce_user_count`, etc.

## 2. Parameter Name Mappings

### 2.1 Parameter Aliases and Transformations
The library shows several parameter name transformations:

**Direct Name Changes**:
- `clients.set.client()`: `zip_code` (input) → `zip` (API parameter)
- `dids.set.caller_id_filtering()`: `filter_id` (input) → `filter` (API parameter)
- `dids.set.phonebook_group()`: Missing `number` parameter in method signature (bug)
- `accountscreate.sub_account()`: Typo in line 182 - checks `reseller_nextbilling` as int but expects string

### 2.2 Inconsistent Naming
Some methods show inconsistent parameter handling:

**Examples**:
- `dids.set.did_info()`: Uses kwargs update pattern instead of explicit parameter handling
- `dids.set.queue()`: Line 862 incorrectly validates `queue_number` as string when it should be int
- `calls.send.recording_email()`: References undefined `account` variable (line 38)

## 3. Validation Patterns

### 3.1 Email Validation
**Helper Function** (`helpers.py`):
```python
def validate_email(email):
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    if match:
        return True
    else:
        return False
```

Used in:
- `clients.set.client()`
- `clients.set.client_threshold()`
- `dids.set.sms()`
- `fax.send.fax_message()`

### 3.2 Date Validation
**Helper Function** (`helpers.py`):
```python
def validate_date(date_text):
    try:
        date_object = datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    return date_object
```

### 3.3 IP Address Validation
**Example** (`accountscreate.py`):
```python
if "ip" in kwargs:
    ip = kwargs["ip"]
    if not isinstance(ip, str):
        raise ValueError("Sub Account IP needs to be a str (For IP Authentication)")
    try:
        socket.inet_aton(ip)
    except socket.error:
        raise ValueError("The provided IP: {} is not in the correct format (Example: 127.0.0.1)".format(ip))
    parameters["ip"] = kwargs.pop("ip")
```

### 3.4 Range Validations
**Examples**:
- `clients.set.client_threshold()`: threshold must be between 1 and 250
- `dids.set.queue()`: 
  - `agent_ring_timeout`: 5 to 60 seconds
  - `retry_timer`: 5 to 60 seconds
  - `wrapup_time`: 1 to 60 seconds
  - `maximum_wait_time`: multiples of 30, max 1200
  - `frequency_announcement`: multiples of 15, max 1200

## 4. Required vs Optional Handling

### 4.1 Conditional Required Parameters
The `helpers.order()` function shows sophisticated conditional parameter requirements:

```python
required_fields = {
    "backOrderDIDUSA": ("quantity", "state", "ratecenter", "routing", "pop", "dialtime", "cnam", "billing_type"),
    "backOrderDIDCAN": ("quantity", "province", "ratecenter", "routing", "pop", "dialtime", "cnam", "billing_type"),
    "orderDID": did_fields,
    "orderDIDInternationalGeographic": international_fields,
    # ... etc
}
```

### 4.2 Parameter Presence Patterns
Most methods follow this pattern:
1. Validate required parameters
2. Check for optional parameters in kwargs
3. Validate and add optional parameters if present
4. Raise error if unknown parameters remain

## 5. Special Cases and Workarounds

### 5.1 Complex Parameter Handling
**DID Routing Format**:
Multiple methods accept routing parameters in special format:
```
routing can receive values in the following format => header:record_id
Where header could be: account, fwd, vm, sip, grp, ivr, sys, recording, queue, cb, tc, disa, none.

Examples:
'account:100001_VoIP'
'fwd:1026'
'vm:101'
'sys:echo'
'none:'
```

### 5.2 Special Value Handling
**"none" as Alternative Type**:
Several parameters accept either an integer or the string "none":
- `dids.set.queue()`: `join_announcement`, `agent_announcement`, `member_delay`, `voice_announcement`, etc.
- Can be integer (recording ID) or string "none"

**"unlimited" as Alternative**:
- `dids.set.queue()`: `maximum_wait_time`, `maximum_callers` can be integer or "unlimited"

### 5.3 List/Array Handling
**Semicolon-Separated Lists**:
- `accounts.create.sub_account()`: `allowed_codecs` - "ulaw;g729;gsm"
- `dids.set.ring_group()`: `members` - 'account:100001;fwd:16006'
- `dids.set.time_condition()`: Multiple parameters use semicolon separation

**JSON Array for Steps**:
- `clients.set.sequences()`: `steps` parameter expects a list that will be JSON-encoded

### 5.4 Duplicate Parameters
**Bug Found**:
- `voicemail.set.voicemail()`: Line 108 has duplicate `"attach_message": attach_message`

### 5.5 Missing StartMinute Parameter
- `dids.set.time_condition()`: Missing `startminute` in parameters dict (line 1442)

## 6. Error Handling Patterns

### 6.1 Comprehensive Error Messages
The library provides detailed error messages for validation failures, often including:
- Expected type
- Valid values or ranges
- References to other API methods for valid values

### 6.2 Parameter Cleanup Pattern
All methods follow this pattern:
```python
if len(kwargs) > 0:
    not_allowed_parameters = ""
    for key, value in kwargs.items():
        not_allowed_parameters += key + " "
    raise ValueError("Parameters not allowed: {}".format(not_allowed_parameters))
```

## 7. Recommendations for API Quirks System

### 7.1 Essential Quirks to Implement

1. **Boolean Conversion Quirk**:
   - Pattern: All boolean parameters → "1"/"0" strings
   - Affected methods: Most set/create methods

2. **Yes/No String Quirk**:
   - Pattern: Some parameters require "yes"/"no" instead of boolean
   - Affected: voicemail settings, queue settings, conference settings

3. **Integer as String Quirk**:
   - Pattern: Phone numbers/DIDs expected as integers
   - Consider: Should these be strings to preserve leading zeros?

4. **Special Value Quirk**:
   - Pattern: Parameters accepting int OR "none"/"unlimited"
   - Need type union handling

5. **Semicolon List Quirk**:
   - Pattern: Lists represented as semicolon-separated strings
   - Affected: codecs, members, time conditions

6. **Parameter Rename Quirk**:
   - Pattern: Input parameter name differs from API parameter
   - Examples: zip_code→zip, filter_id→filter

7. **Routing Format Quirk**:
   - Pattern: Special "header:record_id" format
   - Validation: Check header is valid, format is correct

### 7.2 Implementation Priority

**High Priority**:
1. Boolean to "1"/"0" conversion (very common)
2. Parameter name mappings (zip_code→zip)
3. Yes/no string values validation
4. Special routing format validation

**Medium Priority**:
1. Integer/string "none" union types
2. Semicolon-separated list handling
3. Range validations for specific parameters

**Low Priority**:
1. Complex conditional requirements
2. Email/IP/date format validations (can use standard validators)

### 7.3 Quirk System Architecture

Suggested quirk categories:
1. **Type Conversions**: bool→string, int→string
2. **Value Constraints**: enums, yes/no, ranges
3. **Parameter Transforms**: name changes, format changes
4. **Special Formats**: routing strings, semicolon lists
5. **Conditional Logic**: parameter dependencies

Each quirk should specify:
- Affected methods (regex or explicit list)
- Parameter names (regex or explicit list)
- Transformation/validation function
- Priority/order of application
- Error message template