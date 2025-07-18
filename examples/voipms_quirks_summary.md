# VoIP.ms API Quirks Summary

## ✅ Implemented Quirks

### 1. Boolean to String "1"/"0" Conversion
**Methods**: 20+ methods including getCDR, getSMS, getMMS, orderDID, createSubAccount, setSIPURI, setSMS, setVoicemail, sendFax
```python
answered=True → "1"
cnam=False → "0"
```

### 2. Boolean to "yes"/"no" String Conversion  
**Methods**: setVoicemail, setQueue, setConferenceMember
```python
attach_message=True → "yes"
delete_message=False → "no"
```

### 3. Parameter Name Aliases
**Methods**: getCallRecordings, getSMS, getMMS, setCallerIDFiltering, setClient
```python
from_date → date_from
to_date → date_to
zip_code → zip
filter_id → filter
```

### 4. Required Defaults
**Methods**: getCDR
```python
timezone: "1" (added automatically)
```

### 5. Special Value Mapping
**Methods**: setQueue
```python
join_announcement=None → "none"
maximum_wait_time=None → "unlimited"
maximum_callers=-1 → "unlimited"
```

### 6. List to Semicolon String Conversion
**Methods**: createSubAccount, setRingGroup, setTimeCondition
```python
allowed_codecs=["ulaw", "g729", "gsm"] → "ulaw;g729;gsm"
members=["account:100001", "fwd:16006"] → "account:100001;fwd:16006"
```

## ❌ Not Yet Implemented Quirks

### 1. Routing Format Validation
**Pattern**: "header:record_id"
**Valid headers**: account, fwd, vm, sip, grp, ivr, sys, recording, queue, cb, tc, disa, none
```python
"account:100001_VoIP"
"vm:101"
"sys:echo"
"none:"
```

### 2. Range Validations
**Methods**: setQueue, setClientThreshold
- agent_ring_timeout: 5-60 seconds
- retry_timer: 5-60 seconds  
- wrapup_time: 1-60 seconds
- maximum_wait_time: multiples of 30, max 1200
- frequency_announcement: multiples of 15, max 1200
- threshold: 1-250

### 3. Conditional Required Parameters
**Methods**: orderDID variants
```python
"backOrderDIDUSA": requires (quantity, state, ratecenter, routing, pop, dialtime, cnam, billing_type)
"backOrderDIDCAN": requires (quantity, province, ratecenter, routing, pop, dialtime, cnam, billing_type)
```

### 4. Phone Number/DID Type Handling
- DIDs expected as integers (5551234567)
- Preserving leading zeros might need strings

### 5. Date Business Logic
- CDR limited to 92 days
- No future dates allowed
- Start date must be before end date

### 6. Email/IP Validation
- Email regex validation
- IP address format validation using socket.inet_aton

### 7. Complex Type Unions
- Parameters accepting int OR string ("none", "unlimited")
- Need more sophisticated type handling

## Usage Examples

### Basic Usage with Quirks
```python
# Boolean conversions happen automatically
result = await client.getCDR(
    validate=False,
    date_from="2025-07-17",
    date_to="2025-07-17", 
    answered=True,    # Converts to "1"
    noanswer=False    # Converts to "0"
)

# Parameter aliases work transparently  
recordings = await client.getCallRecordings(
    account="110414",
    from_date="2025-07-17",  # Aliased to date_from
    to_date="2025-07-17"     # Aliased to date_to
)

# Special values and lists
await client.setQueue(
    queue="101",
    join_announcement=None,                           # Converts to "none"
    maximum_wait_time=-1,                            # Converts to "unlimited"  
    join_when_empty=True                             # Converts to "yes"
)

await client.createSubAccount(
    username="test",
    allowed_codecs=["ulaw", "g729", "gsm"],         # Converts to "ulaw;g729;gsm"
    reseller_chargesetup=True                        # Converts to "1"
)
```

### Debug Helper Usage
```python
# See what parameters a method expects and what quirks apply
client.debug_method_params(
    "getCDR",
    date_from="2025-07-17",
    answered=True
)
```

## Benefits

1. **Natural Python Usage**: Use True/False, lists, None - quirks handle conversion
2. **Automatic Handling**: No need to remember API-specific formats
3. **Debug Support**: Built-in helpers show transformations
4. **Systematic Approach**: All 217 methods benefit from improvements
5. **Future-Proof**: New quirks can be added without changing client code