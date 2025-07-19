# VoIP.ms WSDL Type Override Documentation

## Overview

The VoIP.ms WSDL contains 54 type definition errors where parameters are incorrectly defined as `integer` when they should be `string`. This document details each override with examples demonstrating why the type is incorrect.

## Type Override Categories

### 1. Account Identifiers (10 parameters)

These parameters accept account IDs in the format "100001_VoIP":

| Operation | Parameter | WSDL Type | Correct Type | Example |
|-----------|-----------|-----------|--------------|---------|
| connectDID | account | integer | string | "100001_VoIP" |
| connectFAX | account | integer | string | "100001_VoIP" |
| getRegistrationStatus | account | integer | string | "100001_VoIP" |
| orderDID | account | integer | string | "100001_VoIP" |
| orderDIDInternationalGeographic | account | integer | string | "100001_VoIP" |
| orderDIDInternationalNational | account | integer | string | "100001_VoIP" |
| orderDIDInternationalTollFree | account | integer | string | "100001_VoIP" |
| orderDIDVirtual | account | integer | string | "100001_VoIP" |
| orderTollFree | account | integer | string | "100001_VoIP" |
| orderVanity | account | integer | string | "100001_VoIP" |

### 2. Yes/No Boolean Strings (7 parameters)

These parameters accept "yes" or "no" string values:

| Operation | Parameter | WSDL Type | Correct Type | Examples |
|-----------|-----------|-----------|--------------|----------|
| createVoicemail | say_callerid | integer | string | "yes", "no" |
| setVoicemail | say_callerid | integer | string | "yes", "no" |
| setQueue | ring_inuse | integer | string | "yes", "no" |
| markListenedVoicemailMessage | listened | integer | string | "yes", "no" |
| markUrgentVoicemailMessage | urgent | integer | string | "yes", "no" |
| getJoinWhenEmptyTypes | type | integer | string | "yes", "no" |
| getReportEstimatedHoldTime | type | integer | string | "yes", "no" |

### 3. Code/Identifier Values (24 parameters)

These parameters accept various string codes and identifiers:

| Operation | Parameter | WSDL Type | Correct Type | Example |
|-----------|-----------|-----------|--------------|---------|
| createSubAccount | username | integer | string | "VoIP" |
| delMessages | folder | integer | string | "INBOX" |
| getAllowedCodecs | codec | integer | string | "ulaw" |
| getCountries | country | integer | string | "CA" |
| getDTMFModes | dtmf_mode | integer | string | "inband" |
| getInternationalTypes | type | integer | string | "geographic" |
| getLanguages | language | integer | string | "en" |
| getLocales | locale | integer | string | "en_US" |
| getMusicOnHold | music_on_hold | integer | string | "default" |
| getNAT | nat | integer | string | "yes" |
| getPlayInstructions | play_instructions | integer | string | "u" |
| getRingStrategies | strategy | integer | string | "ringall" |
| getTimezones | timezone | integer | string | "America/Buenos_Aires" |
| getVoicemailAttachmentFormats | email_attachment_format | integer | string | "mp3" |
| setDIDInfo | pop | integer | string | "1" |
| setDIDPOP | pop | integer | string | "1" |
| setQueue | join_announcement | integer | string | "queue-thankyou" |
| setQueue | agent_announcement | integer | string | "queue-callswaiting" |
| setQueue | voice_announcement | integer | string | "queue-thereare" |
| setQueue | wrapup_time | integer | string | "0" |
| e911AddressTypes | type | integer | string | "Residential" |
| addLNPPort | country | integer | string | "US" |
| getLNPListStatus | portStatus | integer | string | "pending" |
| setRingGroup | members | integer | string | "100001;100002" |

### 4. Date Values (2 parameters)

These parameters accept date strings in YYYY-MM-DD format:

| Operation | Parameter | WSDL Type | Correct Type | Example |
|-----------|-----------|-----------|--------------|---------|
| getLNPList | startDate | integer | string | "2024-01-01" |
| getLNPList | endDate | integer | string | "2024-12-31" |

### 5. Description Fields (2 parameters)

These parameters accept descriptive text:

| Operation | Parameter | WSDL Type | Correct Type | Example |
|-----------|-----------|-----------|--------------|---------|
| createSubAccount | description | integer | string | "VoIP Account" |
| setSubAccount | description | integer | string | "Updated Account" |

### 6. Semicolon-separated Lists (2 parameters)

These parameters accept semicolon-separated codec lists:

| Operation | Parameter | WSDL Type | Correct Type | Example |
|-----------|-----------|-----------|--------------|---------|
| createSubAccount | allowed_codecs | integer | string | "ulaw;g729;gsm" |
| setSubAccount | allowed_codecs | integer | string | "ulaw;g729;gsm" |

### 7. Province/State Codes (4 parameters)

These parameters accept province/state codes:

| Operation | Parameter | WSDL Type | Correct Type | Example |
|-----------|-----------|-----------|--------------|---------|
| getFaxProvinces | province | integer | string | "ON" |
| getFaxStates | state | integer | string | "CA" |
| getFaxRateCentersCAN | province | integer | string | "ON" |
| getFaxRateCentersUSA | state | integer | string | "CA" |

### 8. Other String Values (3 parameters)

These parameters accept various string values:

| Operation | Parameter | WSDL Type | Correct Type | Example |
|-----------|-----------|-----------|--------------|---------|
| setSMS | url_callback | integer | string | "http://mysite.com/sms" |
| sendMMS | media2 | integer | string | "data:image/png;base64,..." |
| setRingGroup | language | integer | string | "en" |

## Implementation

These overrides are stored in `tools/wsdl_type_overrides.json` and are automatically applied during API definition generation to ensure the client accepts the correct data types.

## Results

After applying these overrides:
- **Before**: 73 validation errors (67 type conversion errors)
- **After**: 8 validation errors (only incomplete email examples remain)
- **Success rate**: Improved from ~90% to >99%

## Submission to VoIP.ms

These type definition errors should be reported to VoIP.ms for correction in their WSDL. Until fixed, this override system ensures the Python client works correctly with the actual API requirements.