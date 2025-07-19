# VoIP.ms API WSDL Type Definition Fixes

## Summary

We have identified 54 parameters in the VoIP.ms WSDL that have incorrect type definitions. These parameters are defined as `integer` but actually accept string values according to the API documentation examples and descriptions.

## Impact

These type mismatches cause:
- Type validation errors in strongly-typed clients
- Confusion for developers implementing API integrations
- Failed API calls when clients enforce type safety

## Affected Parameters

### Account Parameters (10 instances)
These parameters accept account IDs like "100001_VoIP" but are defined as integer:
```xml
<!-- Current (incorrect) -->
<element name="account" type="xsd:int"/>

<!-- Should be -->
<element name="account" type="xsd:string"/>
```

Affected operations:
- connectDID
- connectFAX
- getRegistrationStatus
- orderDID
- orderDIDInternationalGeographic
- orderDIDInternationalNational
- orderDIDInternationalTollFree
- orderDIDVirtual
- orderTollFree
- orderVanity

### Boolean String Parameters (7 instances)
These parameters accept "yes"/"no" values but are defined as integer:
```xml
<!-- Current (incorrect) -->
<element name="say_callerid" type="xsd:int"/>

<!-- Should be -->
<element name="say_callerid" type="xsd:string"/>
```

Affected operations:
- createVoicemail (say_callerid)
- setVoicemail (say_callerid)
- setQueue (ring_inuse)
- markListenedVoicemailMessage (listened)
- markUrgentVoicemailMessage (urgent)
- getJoinWhenEmptyTypes (type)
- getReportEstimatedHoldTime (type)

### String Identifier Parameters (24 instances)
These parameters accept string codes/identifiers but are defined as integer:

Examples:
- createSubAccount.username accepts "VoIP" (not an integer)
- delMessages.folder accepts "INBOX" (not an integer)
- getAllowedCodecs.codec accepts "ulaw" (not an integer)
- getTimezones.timezone accepts "America/Buenos_Aires" (not an integer)

### Date Parameters (2 instances)
These parameters accept date strings in YYYY-MM-DD format:
- getLNPList.startDate
- getLNPList.endDate

### List Parameters (2 instances)
These parameters accept semicolon-separated lists:
- createSubAccount.allowed_codecs accepts "ulaw;g729;gsm"
- setSubAccount.allowed_codecs accepts "ulaw;g729;gsm"

### URL Parameter (1 instance)
- setSMS.url_callback accepts URLs like "http://mysite.com/callback"

## Complete List of Required Fixes

```
connectDID.account: integer → string
connectFAX.account: integer → string
getRegistrationStatus.account: integer → string
orderDID.account: integer → string
orderDIDInternationalGeographic.account: integer → string
orderDIDInternationalNational.account: integer → string
orderDIDInternationalTollFree.account: integer → string
orderDIDVirtual.account: integer → string
orderTollFree.account: integer → string
orderVanity.account: integer → string
createVoicemail.say_callerid: integer → string
setVoicemail.say_callerid: integer → string
setQueue.ring_inuse: integer → string
markListenedVoicemailMessage.listened: integer → string
markUrgentVoicemailMessage.urgent: integer → string
getJoinWhenEmptyTypes.type: integer → string
getReportEstimatedHoldTime.type: integer → string
createSubAccount.username: integer → string
delMessages.folder: integer → string
getAllowedCodecs.codec: integer → string
getCountries.country: integer → string
getDTMFModes.dtmf_mode: integer → string
getInternationalTypes.type: integer → string
getLanguages.language: integer → string
getLocales.locale: integer → string
getMusicOnHold.music_on_hold: integer → string
getNAT.nat: integer → string
getPlayInstructions.play_instructions: integer → string
getRingStrategies.strategy: integer → string
getTimezones.timezone: integer → string
getVoicemailAttachmentFormats.email_attachment_format: integer → string
setDIDInfo.pop: integer → string
setDIDPOP.pop: integer → string
setQueue.join_announcement: integer → string
setQueue.agent_announcement: integer → string
setQueue.voice_announcement: integer → string
setQueue.wrapup_time: integer → string
e911AddressTypes.type: integer → string
addLNPPort.country: integer → string
getLNPListStatus.portStatus: integer → string
setRingGroup.members: integer → string
getLNPList.startDate: integer → string
getLNPList.endDate: integer → string
createSubAccount.description: integer → string
setSubAccount.description: integer → string
createSubAccount.allowed_codecs: integer → string
setSubAccount.allowed_codecs: integer → string
getFaxProvinces.province: integer → string
getFaxStates.state: integer → string
getFaxRateCentersCAN.province: integer → string
getFaxRateCentersUSA.state: integer → string
setSMS.url_callback: integer → string
sendMMS.media2: integer → string
setRingGroup.language: integer → string
```

## Recommendation

Update the WSDL type definitions for these 54 parameters from `xsd:int` to `xsd:string` to match the actual API behavior and documentation examples.

## Additional Notes

1. These fixes are based on the examples provided in your own API documentation
2. We've implemented workarounds in our Python client, but fixing the WSDL would benefit all API consumers
3. This affects approximately 25% of all API operations

Thank you for considering these improvements to the WSDL.