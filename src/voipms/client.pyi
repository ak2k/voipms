"""
Type stubs for VoIP.ms Client

Generated from api_definition.json on 2025-07-22
DO NOT EDIT MANUALLY - This file is auto-generated
"""

from typing import Dict, Any, Optional, List, Union, Literal, Annotated
from pathlib import Path


class VoIPMSError(Exception):
    """VoIP.ms API error"""
    code: str
    message: str
    response: Optional[Dict[str, Any]]
    def __init__(self, code: str, message: str, response: Optional[Dict[str, Any]] = None) -> None: ...


class VoIPMSClient:
    """Data-driven VoIP.ms client that dynamically creates methods from JSON definition."""
    
    api_definition: Dict[str, Any]
    username: Optional[str]
    password: Optional[str]
    base_url: str
    timeout: float
    max_retries: int
    verify_ssl: bool
    debug: bool
    
    def __init__(
        self,
        api_definition_path: str = "api_definition.json",
        username: Optional[str] = None,
        password: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        verify_ssl: bool = True,
        debug: bool = False
    ) -> None: ...
    
    def close(self) -> None: ...
    def __enter__(self) -> "VoIPMSClient": ...
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...
    
    def get_available_methods(self) -> List[str]: ...
    def get_method_info(self, method_name: str) -> Optional[Dict[str, Any]]: ...
    def debug_method_params(self, op_name: str, **kwargs: Any) -> None: ...

    # API Methods

    def addCharge(
        self,
        validate: bool = True,
        *,
        charge: str,
        client: int,
        description: Optional[str] = None,
        test: Optional[Literal["true", "false"]] = None,
    ) -> Dict[str, Any]:
        """Add new charge

        Args:
            validate: Whether to validate parameters with Pydantic
            charge: Amount of money that will be Debited from the customer (Example: 4.99) (required)
            client: ID for a specific Reseller Client (Example: 561115) (required)
            description: Charge Description
            test: Set to true if testing how adding charges works (accepts: true/false, yes/no, on/off, 1/0, boolean)

        Returns:
            Response from addCharge operation
        """
        ...

    def addLNPFile(
        self,
        validate: bool = True,
        *,
        file: int,
        portid: int,
    ) -> Dict[str, Any]:
        """Add new lnp file

        Args:
            validate: Whether to validate parameters with Pydantic
            file: Base 64 code of the file to be attached (required)
            portid: ID of the port previously created. (required)

        Returns:
            Response from addLNPFile operation
        """
        ...

    def addLNPPort(
        self,
        validate: bool = True,
        *,
        address1: str,
        city: str,
        country: int,
        firstName: str,
        lastName: str,
        numbers: int,
        portType: str,
        providerAccount: int,
        providerName: int,
        state: str,
        statementName: str,
        zip: int,
        address2: Optional[str] = None,
        btn: Optional[Annotated[str, "Format: phone"]] = None,
        isMobile: Optional[Literal["1", "0"]] = None,
        isPartial: Optional[int] = None,
        locationType: Optional[Literal["1", "0"]] = None,
        notes: Optional[int] = None,
        pin: Optional[str] = None,
        services: Optional[str] = None,
        tfType: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Add new lnp port

        Args:
            validate: Whether to validate parameters with Pydantic
            address1: This is the "Customer Address" as it appears on the CSR (Customer Service Record) of the losing carrier. (required)
            address2: Optional Address information (e.g: Suite 343)
            btn: [Required If isMobile = 1] BTN: It is the phone number to which all the other numbers of the customer are charged, in a consolidated telephone bill (instead of showing separate charges for each number you own). Please try to find the BTN on your invoice, and if you are unable to do so please contact the current provider to obtain it.
            city: This is the "City" as it appears on the CSR (Customer Service Record) of the losing carrier. (required)
            country: This is the "Country" as it appears on the CSR (Customer Service Record) of the losing carrier. (required)
            firstName: This is the "Customer First Name" as it appears on  the CSR (Customer Service Record) of the losing carrier. Please Enter the first name of the owner of the number or the autorized contact. No company name must be entered in the field. (required)
            isMobile: - (Values: 1 = All the numbers are mobile numbers, 0 = false) - Default: 0 (accepts: true/false, yes/no, on/off, 0/1, boolean)
            isPartial: If you have more then 1 number with your current carrier and not porting them all, choose yes. If you are porting all the numbers, choose no. Please note that you still need to include all numbers you want to port. If you have 2 numbers and want to port both, you need to include both numbers in the list of numbers to port. - (Values: 1 = true, 0 = false) - Default: 0
            lastName: This is the "Customer Last Name" as it appears on  the CSR (Customer Service Record) of the losing carrier. Please Enter the last name of the owner of the number or the autorized contact. No company name must be entered in the field (required)
            locationType: - (Values: 1 = Business, 0 = Residential) - Default: 0 (accepts: true/false, yes/no, on/off, 0/1, boolean)
            notes: - If you would like to include additional information regarding this port, you can use this parameter.
            numbers: DID(s) to port into VoIP.ms network (Example: 5552341234,5552341233). If you are porting more than one number, please separate them with commas. (required)
            pin: PIN Number
            portType: Digits from 1 to 4: 1: United States Local numbers 2: Canadian Local Numbers 3: US/CA Toll Free Numbers 4: United States Fax numbers 5: Canadian Fax Numbers (required)
            providerAccount: Your Account with your current service provider. (required)
            providerName: The name of your current service provider. (required)
            services: [Required If isMobile = 1] Please be specific and describe ALL remaining services with the current carrier. This includes DSL/Data services, Hunt Group services, etc. Any services NOT listed below may be disconnected upon completion of this port order.
            state: This is the "State or Province" as it appears on the CSR (Customer Service Record) of the losing carrier. (required)
            statementName: This is for Business numbers only. Please type your Company Name if applicable, otherwise leave it blank. (required)
            tfType: [Required If portType = 3] Values: 1 - American Carrier, American Callers Only, 2 - American Carrier, American and Canadian Callers allowed, 3 - Canadian Carrier
            zip: This is the "ZIP or Postal Code" as it appears on the CSR (Customer Service Record) of the losing carrier. (required)

        Returns:
            Response from addLNPPort operation
        """
        ...

    def addMemberToConference(
        self,
        validate: bool = True,
        *,
        conference: int,
        member: int,
    ) -> Dict[str, Any]:
        """Add new member to conference

        Args:
            validate: Whether to validate parameters with Pydantic
            conference: Specific Conference ID (Example: 234) (required)
            member: Specific Member ID (Example: 6547) (required)

        Returns:
            Response from addMemberToConference operation
        """
        ...

    def addPayment(
        self,
        validate: bool = True,
        *,
        client: int,
        payment: str,
        description: Optional[str] = None,
        test: Optional[Literal["true", "false"]] = None,
    ) -> Dict[str, Any]:
        """Add new payment

        Args:
            validate: Whether to validate parameters with Pydantic
            client: ID for a specific Reseller Client (Example: 561115) (required)
            description: Payment Description
            payment: Amount of money that will be Credited to the customer (Example: 4.99) (required)
            test: Set to true if testing how adding payments works (accepts: true/false, yes/no, on/off, 1/0, boolean)

        Returns:
            Response from addPayment operation
        """
        ...

    def assignDIDvPRI(
        self,
        validate: bool = True,
        *,
        did: int,
        vpri: int,
    ) -> Dict[str, Any]:
        """Assign di dv pri

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID Number to be assign into our Vpri (Example: 561115) (required)
            vpri: Id for specific Vpri (required)

        Returns:
            Response from assignDIDvPRI operation
        """
        ...

    def backOrderDIDCAN(
        self,
        validate: bool = True,
        *,
        billing_type: Literal["1", "2"],
        cnam: Literal["0", "1"],
        dialtime: int,
        pop: int,
        province: str,
        quantity: int,
        ratecenter: str,
        routing: int,
        callerid_prefix: Optional[int] = None,
        failover_busy: Optional[int] = None,
        failover_noanswer: Optional[int] = None,
        failover_unreachable: Optional[int] = None,
        note: Optional[int] = None,
        test: Optional[Literal["true", "false"]] = None,
        voicemail: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Backorder didcan

        Args:
            validate: Whether to validate parameters with Pydantic
            billing_type: Billing type for the DID (1 = Per Minute, 2 = Flat) (required)
            callerid_prefix: Caller ID Prefix for the DID
            cnam: CNAM for the DID (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean) (required)
            dialtime: Dial Time Out for the DID (Example: 60 -> in seconds) (required)
            failover_busy: Busy Routing for the DID
            failover_noanswer: NoAnswer Routing for the DID
            failover_unreachable: Unreachable Routing for the DID
            note: Note for the DID
            pop: Point of Presence for the DID (Example: 5) (required)
            province: Canadian Province (values from getProvinces) (required)
            quantity: Number of DIDs to be Ordered (Example: 3) (required)
            ratecenter: USA Ratecenter (Values from getRateCentersUSA) (required)
            routing: Main Routing for the DID (required)
            test: Set to true if testing how Orders work - Orders can not be undone - When testing, no Orders are made (accepts: true/false, yes/no, on/off, 1/0, boolean)
            voicemail: Voicemail for the DID (Example: 101)

        Returns:
            Response from backOrderDIDCAN operation

        Note:
            CNAM parameter is converted to '1'/'0' string
        """
        ...

    def backOrderDIDUSA(
        self,
        validate: bool = True,
        *,
        billing_type: Literal["1", "2"],
        cnam: Literal["0", "1"],
        dialtime: int,
        pop: int,
        quantity: int,
        ratecenter: str,
        routing: int,
        state: str,
        callerid_prefix: Optional[int] = None,
        failover_busy: Optional[int] = None,
        failover_noanswer: Optional[int] = None,
        failover_unreachable: Optional[int] = None,
        note: Optional[int] = None,
        test: Optional[Literal["true", "false"]] = None,
        voicemail: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Backorder didusa

        Args:
            validate: Whether to validate parameters with Pydantic
            billing_type: Billing type for the DID (1 = Per Minute, 2 = Flat) (required)
            callerid_prefix: Caller ID Prefix for the DID
            cnam: CNAM for the DID (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean) (required)
            dialtime: Dial Time Out for the DID (Example: 60 -> in seconds) (required)
            failover_busy: Busy Routing for the DID
            failover_noanswer: NoAnswer Routing for the DID
            failover_unreachable: Unreachable Routing for the DID
            note: Note for the DID
            pop: Point of Presence for the DID (Example: 5) (required)
            quantity: Number of DIDs to be Ordered (Example: 3) (required)
            ratecenter: USA Ratecenter (Values from getRateCentersUSA) (required)
            routing: Main Routing for the DID (required)
            state: USA State (values from getStates) (required)
            test: Set to true if testing how Orders work - Orders can not be undone - When testing, no Orders are made (accepts: true/false, yes/no, on/off, 1/0, boolean)
            voicemail: Voicemail for the DID (Example: 101)

        Returns:
            Response from backOrderDIDUSA operation

        Note:
            CNAM parameter is converted to '1'/'0' string
        """
        ...

    def cancelDID(
        self,
        validate: bool = True,
        *,
        did: int,
        cancelcomment: Optional[int] = None,
        portout: Optional[Literal["true", "false"]] = None,
        test: Optional[Literal["true", "false"]] = None,
    ) -> Dict[str, Any]:
        """Cancel did

        Args:
            validate: Whether to validate parameters with Pydantic
            cancelcomment: Comment for DID cancellation
            did: DID to be canceled and deleted (Example: 5551234567) (required)
            portout: Set to true if the DID is being ported out (accepts: true/false, yes/no, on/off, 1/0, boolean)
            test: Set to true if testing how cancellation works - Cancellation can not be undone - When testing, no changes are made (accepts: true/false, yes/no, on/off, 1/0, boolean)

        Returns:
            Response from cancelDID operation
        """
        ...

    def cancelFaxNumber(
        self,
        validate: bool = True,
        *,
        id_: int,
        test: Optional[Literal["true", "false"]] = None,
    ) -> Dict[str, Any]:
        """Cancel fax number

        Args:
            validate: Whether to validate parameters with Pydantic
            id_: ID for a specific Fax Number (Example: 923) (required)
            test: Set to true if testing how cancel a Fax Number (accepts: true/false, yes/no, on/off, 1/0, boolean)

        Returns:
            Response from cancelFaxNumber operation
        """
        ...

    def connectDID(
        self,
        validate: bool = True,
        *,
        account: int,
        did: int,
        minute: Annotated[str, "Units: minutes"],
        monthly: str,
        setup: str,
        dont_charge_monthly: Optional[str] = None,
        dont_charge_setup: Optional[str] = None,
        next_billing: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Connect did

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Reseller Sub Account (Example: '100001_VoIP') (required)
            did: DID to be Connected to Reseler Sub Account (Example: 5551234567) (required)
            dont_charge_monthly: If set to true, the monthly value will not be charged after Connect
            dont_charge_setup: If set to true, the setup value will not be charged after Connect
            minute: Minute Rate for Reseller Client (Example: 0.03) (required)
            monthly: Montly Fee for Reseller Client (Example: 3.50) (required)
            next_billing: Next billing date (Example: '2014-03-30')
            setup: Setup Fee for Reseller Client (Example: 1.99) (required)

        Returns:
            Response from connectDID operation
        """
        ...

    def connectFAX(
        self,
        validate: bool = True,
        *,
        account: int,
        did: int,
        minute: Annotated[str, "Units: minutes"],
        monthly: str,
        setup: str,
        dont_charge_monthly: Optional[str] = None,
        dont_charge_setup: Optional[str] = None,
        next_billing: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Connect fax

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Reseller Sub Account (Example: '100001_VoIP') (required)
            did: FAX DID to be Connected to Reseller Sub Account (Example: 5551234567) (required)
            dont_charge_monthly: If set to true, the monthly value will not be charged after Connect
            dont_charge_setup: If set to true, the setup value will not be charged after Connect
            minute: Minute Rate for Reseller Client (Example: 0.03) (required)
            monthly: Montly Fee for Reseller Client (Example: 3.50) (required)
            next_billing: Next billing date (Example: '2014-03-30')
            setup: Setup Fee for Reseller Client (Example: 1.99) (required)

        Returns:
            Response from connectFAX operation
        """
        ...

    def createSubAccount(
        self,
        validate: bool = True,
        *,
        allowed_codecs: int,
        auth_type: int,
        device_type: int,
        dtmf_mode: int,
        international_route: int,
        lock_international: int,
        music_on_hold: int,
        nat: int,
        protocol: int,
        username: int,
        callerid_number: Optional[int] = None,
        canada_routing: Optional[int] = None,
        description: Optional[int] = None,
        dialing_mode: Optional[Literal["0", "1", "2"]] = None,
        enable_internal_cnam: Optional[int] = None,
        enable_ip_restriction: Optional[Literal["0", "1"]] = None,
        enable_pop_restriction: Optional[Literal["0", "1"]] = None,
        internal_cnam: Optional[int] = None,
        internal_dialtime: Optional[int] = None,
        internal_extension: Optional[int] = None,
        internal_voicemail: Optional[int] = None,
        ip: Optional[int] = None,
        ip_restriction: Optional[str] = None,
        language: Optional[int] = None,
        max_expiry: Optional[Annotated[str, "Range: 60-3600"]] = None,
        password: Optional[int] = None,
        pop_restriction: Optional[str] = None,
        record_calls: Optional[Literal["0", "1"]] = None,
        reseller_chargesetup: Optional[str] = None,
        reseller_client: Optional[int] = None,
        reseller_nextbilling: Optional[str] = None,
        reseller_package: Optional[str] = None,
        rtp_hold_timeout: Optional[Annotated[str, "Range: 1-3600"]] = None,
        rtp_timeout: Optional[Annotated[str, "Range: 1-3600"]] = None,
        send_bye: Optional[Literal["0", "1"]] = None,
        sip_traffic: Optional[Literal["0", "1"]] = None,
        tfcarrier: Optional[Literal["-1", "0", "1", "2"]] = None,
        transcribe: Optional[Literal["0", "1"]] = None,
        transcription_email: Optional[str] = None,
        transcription_locale: Optional[str] = None,
        transcription_start_delay: Optional[Annotated[str, "Range: 0-60; Units: seconds"]] = None,
    ) -> Dict[str, Any]:
        """Create new sub account

        Args:
            validate: Whether to validate parameters with Pydantic
            allowed_codecs: List of Allowed Codecs (Values from getAllowedCodecs) Codecs separated by semicolon (Example: ulaw;g729;gsm) (required)
            auth_type: Authorization Type Code (Values from getAuthTypes) (required)
            callerid_number: Caller ID Override
            canada_routing: Route Code (Values from getRoutes)
            description: Sub Account Description (Example: 'VoIP Account')
            device_type: Device Type Code (Values from getDeviceTypes) (required)
            dialing_mode: Allows you to dial outgoing calls using either the NANPA configuration or the E164 configuration. (Values: 0 = Use Main Account Setting, 1 = E164, 2 = NANPA)
            dtmf_mode: DTMF Mode Code (Values from getDTMFModes) (required)
            enable_internal_cnam: Enable Internal CallerID
            enable_ip_restriction: Enable IP Restriction (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            enable_pop_restriction: Enable POP Restriction (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            internal_cnam: Internal CallerID Name
            internal_dialtime: Sub Account Internal Dialtime (Example: 60 -> seconds)
            internal_extension: Sub Account Internal Extension (Example: 1 -> Creates 101)
            internal_voicemail: Sub Account Internal Voicemail (Example: 101)
            international_route: Route Code (Values from getRoutes) (required)
            ip: Sub Account IP (For IP Authentication)
            ip_restriction: List of IP Addresses, IP Addresses/Netmask, or Fully Qualified Domain Names to allow outgoing calls separated by commas (Example: 123.45.3.21,10.255.12.0/22,device.mydomain.com)
            language: Language for system messages, such as "Invalid Option" (Values from getLanguages)
            lock_international: Lock International Code (Values from getLockInternational) (required)
            max_expiry: Max Expiry between 60 and 3600 (Example: 3000)
            music_on_hold: Music on Hold Code (Values from getMusicOnHold) (required)
            nat: NAT Mode Code (Values from getNAT) (required)
            password: Sub Account Password (For Password Authentication)
            pop_restriction: List of POP Servers to allow outgoing calls separated by commas (values from getServersInfo. Example: 10,23,45)
            protocol: Protocol used for the Sub Account (Values from getProtocols) (required)
            record_calls: Record Calls (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            reseller_chargesetup: True if you want to charge Package Setup Fee after Save
            reseller_client: Reseller Account ID (Example: 561115)
            reseller_nextbilling: Reseller Next Billing Date (Example: '2012-12-31')
            reseller_package: Reseller Package (Example: 92364)
            rtp_hold_timeout: RTP Hold Time Out between 1 and 3600 (Example: 600)
            rtp_timeout: RTP Time Out between 1 and 3600 (Example: 60)
            send_bye: Send BYE on successful transfer (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            sip_traffic: Encrypted SIP Traffic (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            tfcarrier: This allows you to select the carrier to be used for outgoing calls to toll-free numbers. (Values: -1 = Use main account settings, 0 = Default server setting, 1 = US carrier, 2 = Canadian carrier)
            transcribe: Enable Call Transcription (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            transcription_email: Call Transcription Email
            transcription_locale: Call Transcription Locale (values from getLocales)
            transcription_start_delay: Call Transcription Delay Seconds between 0 and 60, Increments of 5 (Example: 10 -> seconds)
            username: Username for the Sub Account (Example: 'VoIP') (required)

        Returns:
            Response from createSubAccount operation
        """
        ...

    def createVoicemail(
        self,
        validate: bool = True,
        *,
        attach_message: Annotated[str, "Format: wav"],
        delete_message: str,
        digits: Annotated[str, "Range: 1-10"],
        language: int,
        name: str,
        password: str,
        play_instructions: int,
        say_callerid: int,
        say_time: str,
        skip_password: Literal["0", "1"],
        timezone: str,
        email: Optional[Annotated[str, "Format: email"]] = None,
        email_attachment_format: Optional[int] = None,
        transcription: Optional[str] = None,
        transcription_locale: Optional[int] = None,
        unavailable_message_recording: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create new voicemail

        Args:
            validate: Whether to validate parameters with Pydantic
            attach_message: Yes for Attaching WAV files to Message (Values: 'yes'/'no') (required)
            delete_message: Yes for Deleting Messages (Values: 'yes'/'no') (required)
            digits: Digits used to create the voicemail (Example: 01) Minimum 1 digit, maximum 10 digits (required)
            email: Email address for receiving messages, multiple email addresses are allowed if separated by a comma
            email_attachment_format: Code for Email Attachment format (Values from getVoicemailAttachmentFormats)
            language: Code for Language (Values from getLanguages) (required)
            name: Name for the Mailbox (required)
            password: Password for the Mailbox (required)
            play_instructions: Code for Play Instructions Setting (Values from getPlayInstructions) (required)
            say_callerid: Yes for Saying the Caller ID (Values: 'yes'/'no') (required)
            say_time: Yes for Saying Time Stamp (Values: 'yes'/'no') (required)
            skip_password: True if Skipping Password (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean) (required)
            timezone: Time Zone for Mailbox (Values from getTimeZones) (required)
            transcription: Voicemail Transcription
            transcription_locale: Transcription locale code (values from getLocales)
            unavailable_message_recording: Recording for the Unavailable Message (values from getRecordings)

        Returns:
            Response from createVoicemail operation
        """
        ...

    def delCallHunting(
        self,
        validate: bool = True,
        *,
        callhunting: int,
    ) -> Dict[str, Any]:
        """Delete call hunting

        Args:
            validate: Whether to validate parameters with Pydantic
            callhunting: ID for a specific Call Hunting (Example: 323) (required)

        Returns:
            Response from delCallHunting operation
        """
        ...

    def delCallParking(
        self,
        validate: bool = True,
        *,
        callparking: int,
    ) -> Dict[str, Any]:
        """Delete call parking

        Args:
            validate: Whether to validate parameters with Pydantic
            callparking: ID for a specific Call Parking (Example: 323) (required)

        Returns:
            Response from delCallParking operation
        """
        ...

    def delCallRecording(
        self,
        validate: bool = True,
        *,
        account: int,
        callrecording: str,
    ) -> Dict[str, Any]:
        """Delete call recording

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Filter Call Recordings by Account (Values from getCallAccounts) (required)
            callrecording: Call Recording (Values from getCallRecordings) (required)

        Returns:
            Response from delCallRecording operation
        """
        ...

    def delCallback(
        self,
        validate: bool = True,
        *,
        callback: int,
    ) -> Dict[str, Any]:
        """Delete callback

        Args:
            validate: Whether to validate parameters with Pydantic
            callback: ID for a specific Callback (Example: 19183) (required)

        Returns:
            Response from delCallback operation
        """
        ...

    def delCallerIDFiltering(
        self,
        validate: bool = True,
        *,
        filtering: int,
    ) -> Dict[str, Any]:
        """Delete caller id filtering

        Args:
            validate: Whether to validate parameters with Pydantic
            filtering: ID for a specific CallerID Filtering (Example: 19183) (required)

        Returns:
            Response from delCallerIDFiltering operation
        """
        ...

    def delClient(
        self,
        validate: bool = True,
        *,
        client: int,
    ) -> Dict[str, Any]:
        """Delete client

        Args:
            validate: Whether to validate parameters with Pydantic
            client: ID for a specific Reseller Client (Example: 1998) (required)

        Returns:
            Response from delClient operation
        """
        ...

    def delConference(
        self,
        validate: bool = True,
        *,
        conference: int,
    ) -> Dict[str, Any]:
        """Delete conference

        Args:
            validate: Whether to validate parameters with Pydantic
            conference: ID for a specific Conference (Example: 737) (required)

        Returns:
            Response from delConference operation
        """
        ...

    def delConferenceMember(
        self,
        validate: bool = True,
        *,
        member: int,
    ) -> Dict[str, Any]:
        """Delete conference member

        Args:
            validate: Whether to validate parameters with Pydantic
            member: ID for a specific Member Profile (Example: 737) (required)

        Returns:
            Response from delConferenceMember operation
        """
        ...

    def delDISA(
        self,
        validate: bool = True,
        *,
        disa: int,
    ) -> Dict[str, Any]:
        """Delete disa

        Args:
            validate: Whether to validate parameters with Pydantic
            disa: ID for a specific DISA (Example: 19183) (required)

        Returns:
            Response from delDISA operation
        """
        ...

    def delEmailToFax(
        self,
        validate: bool = True,
        *,
        id_: int,
        test: Optional[Literal["true", "false"]] = None,
    ) -> Dict[str, Any]:
        """Delete email to fax

        Args:
            validate: Whether to validate parameters with Pydantic
            id_: ID for a specific "Email To Fax Configuration" (Example: 923) (required)
            test: Set to true if testing how cancel a "Email To Fax Configuration" (accepts: true/false, yes/no, on/off, 1/0, boolean)

        Returns:
            Response from delEmailToFax operation
        """
        ...

    def delFaxFolder(
        self,
        validate: bool = True,
        *,
        id_: int,
        test: Optional[Literal["true", "false"]] = None,
    ) -> Dict[str, Any]:
        """Delete fax folder

        Args:
            validate: Whether to validate parameters with Pydantic
            id_: ID for a specific Fax Folder (Example: 923) (required)
            test: Set to true if testing how to delete a Fax Folder (accepts: true/false, yes/no, on/off, 1/0, boolean)

        Returns:
            Response from delFaxFolder operation
        """
        ...

    def delForwarding(
        self,
        validate: bool = True,
        *,
        forwarding: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Delete forwarding

        Args:
            validate: Whether to validate parameters with Pydantic
            forwarding: ID for a specific Forwarding (Example: 19183)

        Returns:
            Response from delForwarding operation
        """
        ...

    def delIVR(
        self,
        validate: bool = True,
        *,
        ivr: int,
    ) -> Dict[str, Any]:
        """Delete ivr

        Args:
            validate: Whether to validate parameters with Pydantic
            ivr: ID for a specific IVR (Example: 19183) (required)

        Returns:
            Response from delIVR operation
        """
        ...

    def delMemberFromConference(
        self,
        validate: bool = True,
        *,
        member: int,
        conference: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Delete member from conference

        Args:
            validate: Whether to validate parameters with Pydantic
            conference: ID for a specific Conference (Example: 3829)
            member: ID for a specific Member (Example: 101) (required)

        Returns:
            Response from delMemberFromConference operation
        """
        ...

    def delMessages(
        self,
        validate: bool = True,
        *,
        mailbox: int,
        folder: Optional[int] = None,
        message_num: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Delete messages

        Args:
            validate: Whether to validate parameters with Pydantic
            folder: Name for specific Folder (Required if message id is passed, Example: 'INBOX', values from: getVoicemailFolders)
            mailbox: ID for a specific Mailbox (Example: 1001) (required)
            message_num: ID for specific Voicemail Message (Required if folder is passed, Example: 1)

        Returns:
            Response from delMessages operation
        """
        ...

    def delMusicOnHold(
        self,
        validate: bool = True,
        *,
        music_on_hold: str,
    ) -> Dict[str, Any]:
        """Delete music on hold

        Args:
            validate: Whether to validate parameters with Pydantic
            music_on_hold: Music on Hold Name (Values from getMusicOnHold) (required)

        Returns:
            Response from delMusicOnHold operation
        """
        ...

    def delPhonebook(
        self,
        validate: bool = True,
        *,
        phonebook: int,
    ) -> Dict[str, Any]:
        """Delete phonebook

        Args:
            validate: Whether to validate parameters with Pydantic
            phonebook: ID for a specific Phonebook (Example: 19183) (required)

        Returns:
            Response from delPhonebook operation
        """
        ...

    def delPhonebookGroup(
        self,
        validate: bool = True,
        *,
        group: int,
    ) -> Dict[str, Any]:
        """Delete phonebook group

        Args:
            validate: Whether to validate parameters with Pydantic
            group: ID for a specific Phonebook group (required)

        Returns:
            Response from delPhonebookGroup operation
        """
        ...

    def delQueue(
        self,
        validate: bool = True,
        *,
        queue: int,
    ) -> Dict[str, Any]:
        """Delete queue

        Args:
            validate: Whether to validate parameters with Pydantic
            queue: ID for a specific Queue (Example: 13183) (required)

        Returns:
            Response from delQueue operation
        """
        ...

    def delRecording(
        self,
        validate: bool = True,
        *,
        recording: int,
    ) -> Dict[str, Any]:
        """Delete recording

        Args:
            validate: Whether to validate parameters with Pydantic
            recording: ID for a specific Recording (Example: 19183) (required)

        Returns:
            Response from delRecording operation
        """
        ...

    def delRingGroup(
        self,
        validate: bool = True,
        *,
        ringgroup: int,
    ) -> Dict[str, Any]:
        """Delete ring group

        Args:
            validate: Whether to validate parameters with Pydantic
            ringgroup: ID for a specific Ring Group (Example: 19183) (required)

        Returns:
            Response from delRingGroup operation
        """
        ...

    def delSIPURI(
        self,
        validate: bool = True,
        *,
        sipuri: int,
    ) -> Dict[str, Any]:
        """Delete sipuri

        Args:
            validate: Whether to validate parameters with Pydantic
            sipuri: ID for a specific SIP URI (Example: 19183) (required)

        Returns:
            Response from delSIPURI operation
        """
        ...

    def delStaticMember(
        self,
        validate: bool = True,
        *,
        member: int,
        queue: int,
    ) -> Dict[str, Any]:
        """Delete static member

        Args:
            validate: Whether to validate parameters with Pydantic
            member: ID for a specific Member Queue (Example: 1918) (required)
            queue: ID for a specific Queue (Example: 27183) (required)

        Returns:
            Response from delStaticMember operation
        """
        ...

    def delSubAccount(
        self,
        validate: bool = True,
        *,
        id_: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Delete sub account

        Args:
            validate: Whether to validate parameters with Pydantic
            id_: ID for a specific Sub Account (Example: 99785)

        Returns:
            Response from delSubAccount operation
        """
        ...

    def delTimeCondition(
        self,
        validate: bool = True,
        *,
        timecondition: int,
    ) -> Dict[str, Any]:
        """Delete time condition

        Args:
            validate: Whether to validate parameters with Pydantic
            timecondition: ID for a specific Time Condition (Example: 19183) (required)

        Returns:
            Response from delTimeCondition operation
        """
        ...

    def delVoicemail(
        self,
        validate: bool = True,
        *,
        mailbox: int,
    ) -> Dict[str, Any]:
        """Delete voicemail

        Args:
            validate: Whether to validate parameters with Pydantic
            mailbox: ID for a specific Mailbox (Example: 1001) (required)

        Returns:
            Response from delVoicemail operation
        """
        ...

    def deleteFaxMessage(
        self,
        validate: bool = True,
        *,
        id_: int,
        test: Optional[Literal["true", "false"]] = None,
    ) -> Dict[str, Any]:
        """Delete ete fax message

        Args:
            validate: Whether to validate parameters with Pydantic
            id_: ID for a specific Fax Message (Example: 923) (required)
            test: Set to true if testing how cancel a Fax Message (accepts: true/false, yes/no, on/off, 1/0, boolean)

        Returns:
            Response from deleteFaxMessage operation
        """
        ...

    def deleteMMS(
        self,
        validate: bool = True,
        *,
        id_: int,
    ) -> Dict[str, Any]:
        """Delete ete mms

        Args:
            validate: Whether to validate parameters with Pydantic
            id_: ID for a specific MMS (Example: 1918) (required)

        Returns:
            Response from deleteMMS operation
        """
        ...

    def deleteSMS(
        self,
        validate: bool = True,
        *,
        id_: int,
    ) -> Dict[str, Any]:
        """Delete ete sms

        Args:
            validate: Whether to validate parameters with Pydantic
            id_: ID for a specific SMS (Example: 1918) (required)

        Returns:
            Response from deleteSMS operation
        """
        ...

    def e911AddressTypes(
        self,
        validate: bool = True,
        *,
        type_: Optional[int] = None,
    ) -> Dict[str, Any]:
        """E address types

        Args:
            validate: Whether to validate parameters with Pydantic
            type_: Code for a specific Address Type (Example: Apartment)

        Returns:
            Response from e911AddressTypes operation
        """
        ...

    def e911Cancel(
        self,
        validate: bool = True,
        *,
        did: int,
    ) -> Dict[str, Any]:
        """E cancel

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID to be canceled. (required)

        Returns:
            Response from e911Cancel operation
        """
        ...

    def e911Info(
        self,
        validate: bool = True,
        *,
        did: int,
    ) -> Dict[str, Any]:
        """E info

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID with e911 enabled / in process. (required)

        Returns:
            Response from e911Info operation
        """
        ...

    def e911Provision(
        self,
        validate: bool = True,
        *,
        city: str,
        country: int,
        did: int,
        full_name: str,
        language: str,
        state: str,
        street_name: str,
        street_number: str,
        zip: str,
        address_number: Optional[str] = None,
        address_type: Optional[str] = None,
        other_info: Optional[str] = None,
    ) -> Dict[str, Any]:
        """E provision

        Args:
            validate: Whether to validate parameters with Pydantic
            address_number: Address Number that will be sent to the e911 service.
            address_type: Address Type that will be sent to the e911 service (Values from e911AddressTypes).
            city: City that will be sent to the e911 service. (required)
            country: Country that will be sent to the e911 service. Value can be US (United states) or CA (Canada). (required)
            did: DID that will be sent to the e911 service. (required)
            full_name: Full Name that will be sent to the e911 service. (required)
            language: Language that will be sent to the e911 service. Only available for addresses from Canada. Value can be EN (English) or FR (French). (required)
            other_info: Additional Address Information that will be sent to the e911 service. Only available for addresses from Canada.
            state: State / Province that will be sent to the e911 service. (required)
            street_name: Street Name that will be sent to the e911 service. (required)
            street_number: Street Number that will be sent to the e911 service. (required)
            zip:  (required)

        Returns:
            Response from e911Provision operation
        """
        ...

    def e911ProvisionManually(
        self,
        validate: bool = True,
        *,
        city: str,
        country: int,
        did: int,
        full_name: str,
        language: str,
        state: str,
        street_name: str,
        street_number: str,
        zip: str,
        address_number: Optional[str] = None,
        address_type: Optional[str] = None,
        other_info: Optional[str] = None,
    ) -> Dict[str, Any]:
        """E provision manually

        Args:
            validate: Whether to validate parameters with Pydantic
            address_number: Address Number that will be sent to the e911 service.
            address_type: Address Type that will be sent to the e911 service (Values from e911AddressTypes).
            city: City that will be sent to the e911 service. (required)
            country: Country that will be sent to the e911 service. Value can be US (United states) or CA (Canada). (required)
            did: DID that will be sent to the e911 service. (required)
            full_name: Full Name that will be sent to the e911 service. (required)
            language: Language that will be sent to the e911 service. Only available for addresses from Canada. Value can be EN (English) or FR (French). (required)
            other_info: Additional Address Information that will be sent to the e911 service. Only available for addresses from Canada.
            state: State / Province that will be sent to the e911 service. (required)
            street_name: Street Name that will be sent to the e911 service. (required)
            street_number: Street Number that will be sent to the e911 service. (required)
            zip:  (required)

        Returns:
            Response from e911ProvisionManually operation
        """
        ...

    def e911Update(
        self,
        validate: bool = True,
        *,
        city: str,
        country: int,
        did: int,
        full_name: str,
        language: str,
        state: str,
        street_name: str,
        street_number: str,
        zip: str,
        address_number: Optional[str] = None,
        address_type: Optional[str] = None,
        other_info: Optional[str] = None,
    ) -> Dict[str, Any]:
        """E update

        Args:
            validate: Whether to validate parameters with Pydantic
            address_number: Address Number that will be updated to the e911 service.
            address_type: Address Type that will be updated to the e911 service (Values from e911AddressTypes).
            city: City that will be updated to the e911 service. (required)
            country: Country that will be updated to the e911 service. Value can be US (United states) or CA (Canada). (required)
            did: DID with e911 enabled / in process. (required)
            full_name: Full Name that will be updated to the e911 service. (required)
            language: Language that will be updated to the e911 service. Only available for addresses from Canada. Value can be EN (English) or FR (French). (required)
            other_info: Additional Address Information that will be updated to the e911 service. Only available for addresses from Canada.
            state: State / Province that will be updated to the e911 service. (required)
            street_name: Street Name that will be updated to the e911 service. (required)
            street_number: Street Number that will be updated to the e911 service. (required)
            zip:  (required)

        Returns:
            Response from e911Update operation
        """
        ...

    def e911Validate(
        self,
        validate: bool = True,
        *,
        city: int,
        country: int,
        did: int,
        full_name: int,
        state: int,
        street_name: int,
        street_number: int,
        zip: str,
        address_number: Optional[int] = None,
        address_type: Optional[int] = None,
        language: Optional[int] = None,
        other_info: Optional[int] = None,
    ) -> Dict[str, Any]:
        """E validate

        Args:
            validate: Whether to validate parameters with Pydantic
            address_number: Address Number that will be validated.
            address_type: Address Type that will be validated (Values from e911AddressTypes).
            city: City that will be validated. (required)
            country: Country that will be validated. Value can be US (United states) or CA (Canada). (required)
            did: DID with e911 enabled / in process. (required)
            full_name: Full Name that will be validated. (required)
            language: Language that will be validated. Only available for addresses from Canada. Value can be EN (English) or FR (French).
            other_info: Additional Address Information that will be validated. Only available for addresses from Canada.
            state: State / Province that will be validated. (required)
            street_name: Street Name that will be validated. (required)
            street_number: Street Number that will be validated. (required)
            zip:  (required)

        Returns:
            Response from e911Validate operation
        """
        ...

    def getAllowedCodecs(
        self,
        validate: bool = True,
        *,
        codec: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve allowed codecs information

        Args:
            validate: Whether to validate parameters with Pydantic
            codec: Code for a specific Codec (Example: 'ulaw')

        Returns:
            Response from getAllowedCodecs operation
        """
        ...

    def getAuthTypes(
        self,
        validate: bool = True,
        *,
        type_: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve auth types information

        Args:
            validate: Whether to validate parameters with Pydantic
            type_: Code for a specific Authorization Type (Example: 2)

        Returns:
            Response from getAuthTypes operation
        """
        ...

    def getBackOrders(
        self,
        validate: bool = True,
        *,
        id_: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve back orders information

        Args:
            validate: Whether to validate parameters with Pydantic
            id_: ID for a specific backorder DID

        Returns:
            Response from getBackOrders operation
        """
        ...

    def getBalance(
        self,
        validate: bool = True,
        *,
        advanced: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve balance information

        Args:
            validate: Whether to validate parameters with Pydantic
            advanced: True for Calls Statistics

        Returns:
            Response from getBalance operation
        """
        ...

    def getBalanceManagement(
        self,
        validate: bool = True,
        *,
        balance_management: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve balance management information

        Args:
            validate: Whether to validate parameters with Pydantic
            balance_management: Code for a specific Balance Management Setting (Example: 1)

        Returns:
            Response from getBalanceManagement operation
        """
        ...

    def getCDR(
        self,
        validate: bool = True,
        *,
        date_from: str,
        date_to: str,
        timezone: str,
        account: Optional[int] = None,
        answered: Optional[Literal["0", "1"]] = None,
        busy: Optional[Literal["0", "1"]] = None,
        callbilling: Optional[str] = None,
        calltype: Optional[str] = None,
        failed: Optional[Literal["0", "1"]] = None,
        noanswer: Optional[Literal["0", "1"]] = None,
    ) -> Dict[str, Any]:
        """Retrieve cdr information

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Filter CDR by Account (Values from getCallAccounts)
            answered: Include Answered Calls to CDR (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            busy: Include Busy Calls to CDR (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            callbilling: Filter CDR by Call Billing (Values from getCallBilling)
            calltype: Filters CDR by Call Type (Values from getCallTypes)
            date_from: Start Date for Filtering CDR (Example: '2010-11-30') (required)
            date_to: End Date for Filtering CDR (Example: '2010-11-30') (required)
            failed: Include Failed Calls to CDR (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            noanswer: Include NoAnswered calls to CDR (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            timezone: Adjust time of calls according to Timezome (Numeric: -12 to 13) (required)

        Returns:
            Response from getCDR operation

        Note:
            Date range limited to 92 days
            Boolean parameters are converted to '1'/'0' strings
            Timezone defaults to '1' if not provided
        """
        ...

    def getCallAccounts(
        self,
        validate: bool = True,
    ) -> Dict[str, Any]:
        """Retrieve call accounts information

        Returns:
            Response from getCallAccounts operation
        """
        ...

    def getCallBilling(
        self,
        validate: bool = True,
    ) -> Dict[str, Any]:
        """Retrieve call billing information

        Returns:
            Response from getCallBilling operation
        """
        ...

    def getCallHuntings(
        self,
        validate: bool = True,
        *,
        callhunting: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve call huntings information

        Args:
            validate: Whether to validate parameters with Pydantic
            callhunting: ID for a specific Call Hunting (Example: 323)

        Returns:
            Response from getCallHuntings operation
        """
        ...

    def getCallParking(
        self,
        validate: bool = True,
        *,
        callparking: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve call parking information

        Args:
            validate: Whether to validate parameters with Pydantic
            callparking: ID for a specific Call Parking (Example: 737)

        Returns:
            Response from getCallParking operation
        """
        ...

    def getCallRecording(
        self,
        validate: bool = True,
        *,
        account: int,
        callrecording: str,
    ) -> Dict[str, Any]:
        """Retrieve call recording information

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Main Account or Sub Account related to the call recording (Values from getCallRecordings) (required)
            callrecording: Call Recording (Values from getCallRecordings) (required)

        Returns:
            Response from getCallRecording operation
        """
        ...

    def getCallRecordings(
        self,
        validate: bool = True,
        *,
        account: int,
        date_from: str,
        date_to: str,
        length: Optional[int] = None,
        start: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve call recordings information

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Filter Call Recordings by Account (Values from getCallAccounts) (required)
            date_from: Start Date for Filtering Call Recording (Example:'2018-11-01') (required)
            date_to: End Date for Filtering Call Recording (Example:'2018-12-01') (required)
            length: Number of records to show
            start: Number of records shown previously, used for pages

        Returns:
            Response from getCallRecordings operation
        """
        ...

    def getCallTypes(
        self,
        validate: bool = True,
        *,
        client: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve call types information

        Args:
            validate: Whether to validate parameters with Pydantic
            client: ID for a specific Reseller Client (Example: 561115)

        Returns:
            Response from getCallTypes operation
        """
        ...

    def getCallbacks(
        self,
        validate: bool = True,
        *,
        callback: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve callbacks information

        Args:
            validate: Whether to validate parameters with Pydantic
            callback: ID for a specific Callback (Example: 2359)

        Returns:
            Response from getCallbacks operation
        """
        ...

    def getCallerIDFiltering(
        self,
        validate: bool = True,
        *,
        did: Optional[int] = None,
        filtering: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve caller id filtering information

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID for a specific CallerID Filtering (Example: 5551234567)
            filtering: ID for a specific CallerID Filtering (Example: 18915)

        Returns:
            Response from getCallerIDFiltering operation
        """
        ...

    def getCarriers(
        self,
        validate: bool = True,
        *,
        carrier: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve carriers information

        Args:
            validate: Whether to validate parameters with Pydantic
            carrier: Code for a specific Carrier (Example: 2)

        Returns:
            Response from getCarriers operation
        """
        ...

    def getCharges(
        self,
        validate: bool = True,
        *,
        client: int,
    ) -> Dict[str, Any]:
        """Retrieve charges information

        Args:
            validate: Whether to validate parameters with Pydantic
            client: ID for a specific Reseller Client (Example: 561115) (required)

        Returns:
            Response from getCharges operation
        """
        ...

    def getClientPackages(
        self,
        validate: bool = True,
        *,
        client: int,
    ) -> Dict[str, Any]:
        """Retrieve client packages information

        Args:
            validate: Whether to validate parameters with Pydantic
            client: ID for a specific Reseller Client (Example: 561115) (required)

        Returns:
            Response from getClientPackages operation
        """
        ...

    def getClientThreshold(
        self,
        validate: bool = True,
        *,
        client: int,
    ) -> Dict[str, Any]:
        """Retrieve client threshold information

        Args:
            validate: Whether to validate parameters with Pydantic
            client: ID for a specific Reseller Client (Example: 561115) (required)

        Returns:
            Response from getClientThreshold operation
        """
        ...

    def getClients(
        self,
        validate: bool = True,
        *,
        client: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve clients information

        Args:
            validate: Whether to validate parameters with Pydantic
            client: Parameter could have the following values: * Empty Value [Not Required] * Specific Reseller Client ID (Example: 561115) * Specific Reseller Client e-mail  (Example: 'john.doe@mydomain.com')

        Returns:
            Response from getClients operation
        """
        ...

    def getConference(
        self,
        validate: bool = True,
        *,
        conference: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve conference information

        Args:
            validate: Whether to validate parameters with Pydantic
            conference: Code for a specific Conference (Example: 1599)

        Returns:
            Response from getConference operation
        """
        ...

    def getConferenceMembers(
        self,
        validate: bool = True,
        *,
        member: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve conference members information

        Args:
            validate: Whether to validate parameters with Pydantic
            member: Code for a specific Member profile (Example: 1599)

        Returns:
            Response from getConferenceMembers operation
        """
        ...

    def getConferenceRecordingFile(
        self,
        validate: bool = True,
        *,
        conference: int,
        recording: int,
    ) -> Dict[str, Any]:
        """Retrieve conference recording file information

        Args:
            validate: Whether to validate parameters with Pydantic
            conference: ID for a specific Conference (Example: 5356) (required)
            recording: ID for a specific Conference Recording (Example: 1543338379) (required)

        Returns:
            Response from getConferenceRecordingFile operation
        """
        ...

    def getConferenceRecordings(
        self,
        validate: bool = True,
        *,
        conference: int,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve conference recordings information

        Args:
            validate: Whether to validate parameters with Pydantic
            conference: ID for a specific Conference (Example: 5356) (required)
            date_from: Start Date for Filtering Transactions (Example: '2016-06-03')
            date_to: End Date for Filtering Transactions (Example: '2016-06-04')

        Returns:
            Response from getConferenceRecordings operation
        """
        ...

    def getCountries(
        self,
        validate: bool = True,
        *,
        country: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve countries information

        Args:
            validate: Whether to validate parameters with Pydantic
            country: Code for a specific Country (Example: 'CA')

        Returns:
            Response from getCountries operation
        """
        ...

    def getDIDCountries(
        self,
        validate: bool = True,
        *,
        type_: int,
        country_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve did countries information

        Args:
            validate: Whether to validate parameters with Pydantic
            country_id: ID for a specific country (Example: 205)
            type_: Type of International DID (Values from getInternationalTypes) (required)

        Returns:
            Response from getDIDCountries operation
        """
        ...

    def getDIDsCAN(
        self,
        validate: bool = True,
        *,
        province: str,
        ratecenter: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve di ds can information

        Args:
            validate: Whether to validate parameters with Pydantic
            province: Canadian Province (Values from getProvinces) (required)
            ratecenter: Canadian Ratecenter (Values from getRateCentersCAN)

        Returns:
            Response from getDIDsCAN operation
        """
        ...

    def getDIDsInfo(
        self,
        validate: bool = True,
        *,
        client: Optional[str] = None,
        did: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve di ds info information

        Args:
            validate: Whether to validate parameters with Pydantic
            client: Parameter could have the following values: * Empty Value [Not Required] * Specific Reseller Client ID (Example: 561115) * Specific Sub Account (Example: '100001_VoIP')
            did: DID from Client or Sub Account (Example: 5551234567)

        Returns:
            Response from getDIDsInfo operation
        """
        ...

    def getDIDsInternationalGeographic(
        self,
        validate: bool = True,
        *,
        country_id: int,
    ) -> Dict[str, Any]:
        """Retrieve di ds international geographic information

        Args:
            validate: Whether to validate parameters with Pydantic
            country_id: ID for a specific Country (Values from getDIDCountries) (required)

        Returns:
            Response from getDIDsInternationalGeographic operation
        """
        ...

    def getDIDsInternationalNational(
        self,
        validate: bool = True,
        *,
        country_id: int,
    ) -> Dict[str, Any]:
        """Retrieve di ds international national information

        Args:
            validate: Whether to validate parameters with Pydantic
            country_id: ID for a specific Country (Values from getDIDCountries) (required)

        Returns:
            Response from getDIDsInternationalNational operation
        """
        ...

    def getDIDsInternationalTollFree(
        self,
        validate: bool = True,
        *,
        country_id: int,
    ) -> Dict[str, Any]:
        """Retrieve di ds international toll free information

        Args:
            validate: Whether to validate parameters with Pydantic
            country_id: ID for a specific Country (Values from getDIDCountries) (required)

        Returns:
            Response from getDIDsInternationalTollFree operation
        """
        ...

    def getDIDsUSA(
        self,
        validate: bool = True,
        *,
        state: str,
        ratecenter: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve di ds usa information

        Args:
            validate: Whether to validate parameters with Pydantic
            ratecenter: United States Ratecenter (Values from getRateCentersUSA)
            state: United States State (Values from getStates) (required)

        Returns:
            Response from getDIDsUSA operation
        """
        ...

    def getDIDvPRI(
        self,
        validate: bool = True,
        *,
        vpri: int,
    ) -> Dict[str, Any]:
        """Retrieve di dv pri information

        Args:
            validate: Whether to validate parameters with Pydantic
            vpri: Id for specific Vpri (required)

        Returns:
            Response from getDIDvPRI operation
        """
        ...

    def getDISAs(
        self,
        validate: bool = True,
        *,
        disa: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve dis as information

        Args:
            validate: Whether to validate parameters with Pydantic
            disa: ID for a specific DISA (Example: 2114)

        Returns:
            Response from getDISAs operation
        """
        ...

    def getDTMFModes(
        self,
        validate: bool = True,
        *,
        dtmf_mode: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve dtmf modes information

        Args:
            validate: Whether to validate parameters with Pydantic
            dtmf_mode: Code for a specific DTMF Mode (Example: 'inband')

        Returns:
            Response from getDTMFModes operation
        """
        ...

    def getDeposits(
        self,
        validate: bool = True,
        *,
        client: int,
    ) -> Dict[str, Any]:
        """Retrieve deposits information

        Args:
            validate: Whether to validate parameters with Pydantic
            client: ID for a specific Reseller Client (Example: 561115) (required)

        Returns:
            Response from getDeposits operation
        """
        ...

    def getDeviceTypes(
        self,
        validate: bool = True,
        *,
        device_type: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve device types information

        Args:
            validate: Whether to validate parameters with Pydantic
            device_type: Code for a specific Device Type (Example: 1)

        Returns:
            Response from getDeviceTypes operation
        """
        ...

    def getEmailToFax(
        self,
        validate: bool = True,
        *,
        id_: int,
    ) -> Dict[str, Any]:
        """Retrieve email to fax information

        Args:
            validate: Whether to validate parameters with Pydantic
            id_:  (required)

        Returns:
            Response from getEmailToFax operation
        """
        ...

    def getFaxFolders(
        self,
        validate: bool = True,
        *,
        id_: int,
    ) -> Dict[str, Any]:
        """Retrieve fax folders information

        Args:
            validate: Whether to validate parameters with Pydantic
            id_:  (required)

        Returns:
            Response from getFaxFolders operation
        """
        ...

    def getFaxMessagePDF(
        self,
        validate: bool = True,
        *,
        id_: int,
    ) -> Dict[str, Any]:
        """Retrieve fax message pdf information

        Args:
            validate: Whether to validate parameters with Pydantic
            id_: ID of the Fax Message requested (Values from getFaxMessages) (required)

        Returns:
            Response from getFaxMessagePDF operation
        """
        ...

    def getFaxMessages(
        self,
        validate: bool = True,
        *,
        folder: Optional[str] = None,
        from_: Optional[str] = None,
        id_: Optional[int] = None,
        to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve fax messages information

        Args:
            validate: Whether to validate parameters with Pydantic
            folder: Name of specific Fax Folder (Example: SENT) - Default value: ALL
            from_: Start Date for Filtering Fax Messages (Example: '2014-03-30') - Default value: Today
            id_: ID for a Specific Fax Message (Example: 23434)
            to: End Date for Filtering Fax Messages (Example: '2014-03-30') - Default value: Today

        Returns:
            Response from getFaxMessages operation
        """
        ...

    def getFaxNumbersInfo(
        self,
        validate: bool = True,
        *,
        did: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve fax numbers info information

        Args:
            validate: Whether to validate parameters with Pydantic
            did: Fax Number to retrieves the information of a single number, or not send if you want retrieves the information of all your Fax Numbers.

        Returns:
            Response from getFaxNumbersInfo operation
        """
        ...

    def getFaxNumbersPortability(
        self,
        validate: bool = True,
        *,
        did: int,
    ) -> Dict[str, Any]:
        """Retrieve fax numbers portability information

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID Number to be ported into our network (Example: 5552341234) (required)

        Returns:
            Response from getFaxNumbersPortability operation
        """
        ...

    def getFaxProvinces(
        self,
        validate: bool = True,
        *,
        province: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve fax provinces information

        Args:
            validate: Whether to validate parameters with Pydantic
            province: CODE for a specific Province (Example: AB)

        Returns:
            Response from getFaxProvinces operation
        """
        ...

    def getFaxRateCentersCAN(
        self,
        validate: bool = True,
        *,
        province: int,
    ) -> Dict[str, Any]:
        """Retrieve fax rate centers can information

        Args:
            validate: Whether to validate parameters with Pydantic
            province: Province two letters code (Example: AB) (required)

        Returns:
            Response from getFaxRateCentersCAN operation
        """
        ...

    def getFaxRateCentersUSA(
        self,
        validate: bool = True,
        *,
        state: int,
    ) -> Dict[str, Any]:
        """Retrieve fax rate centers usa information

        Args:
            validate: Whether to validate parameters with Pydantic
            state: Province two letters code (Example: AL) (required)

        Returns:
            Response from getFaxRateCentersUSA operation
        """
        ...

    def getFaxStates(
        self,
        validate: bool = True,
        *,
        state: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve fax states information

        Args:
            validate: Whether to validate parameters with Pydantic
            state: CODE for a specific State (Example: AL)

        Returns:
            Response from getFaxStates operation
        """
        ...

    def getForwardings(
        self,
        validate: bool = True,
        *,
        forwarding: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve forwardings information

        Args:
            validate: Whether to validate parameters with Pydantic
            forwarding: ID for a specific Forwarding (Example: 18635)

        Returns:
            Response from getForwardings operation
        """
        ...

    def getIP(
        self,
        validate: bool = True,
    ) -> Dict[str, Any]:
        """Retrieve ip information

        Returns:
            Response from getIP operation
        """
        ...

    def getIVRs(
        self,
        validate: bool = True,
        *,
        ivr: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve iv rs information

        Args:
            validate: Whether to validate parameters with Pydantic
            ivr: ID for a specific IVR (Example: 4636)

        Returns:
            Response from getIVRs operation
        """
        ...

    def getInternationalTypes(
        self,
        validate: bool = True,
        *,
        type_: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve international types information

        Args:
            validate: Whether to validate parameters with Pydantic
            type_: Code for a specific International Type (Example: 'NATIONAL')

        Returns:
            Response from getInternationalTypes operation
        """
        ...

    def getJoinWhenEmptyTypes(
        self,
        validate: bool = True,
        *,
        type_: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve join when empty types information

        Args:
            validate: Whether to validate parameters with Pydantic
            type_: Code for a specific 'JoinWhenEmpty' Type (Example: 'yes')

        Returns:
            Response from getJoinWhenEmptyTypes operation
        """
        ...

    def getLNPAttach(
        self,
        validate: bool = True,
        *,
        attachid: int,
    ) -> Dict[str, Any]:
        """Retrieve lnp attach information

        Args:
            validate: Whether to validate parameters with Pydantic
            attachid: ID of the invoice (attachment) previously uploaded. (required)

        Returns:
            Response from getLNPAttach operation
        """
        ...

    def getLNPAttachList(
        self,
        validate: bool = True,
        *,
        portid: int,
    ) -> Dict[str, Any]:
        """Retrieve lnp attach list information

        Args:
            validate: Whether to validate parameters with Pydantic
            portid: ID of the port previously created. (required)

        Returns:
            Response from getLNPAttachList operation
        """
        ...

    def getLNPDetails(
        self,
        validate: bool = True,
        *,
        portid: int,
    ) -> Dict[str, Any]:
        """Retrieve lnp details information

        Args:
            validate: Whether to validate parameters with Pydantic
            portid: ID of the port previously created. (required)

        Returns:
            Response from getLNPDetails operation
        """
        ...

    def getLNPList(
        self,
        validate: bool = True,
        *,
        portid: int,
        endDate: Optional[int] = None,
        portStatus: Optional[int] = None,
        startDate: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve lnp list information

        Args:
            validate: Whether to validate parameters with Pydantic
            endDate: End Date for filtering Ports. (Example: '2014-03-30')
            portStatus: Status code to filtering Ports. Example: precessing. (You can use the values returned by the method getLNPListStatus)
            portid: ID of the port previously created. (required)
            startDate: Start Date for filtering Ports. (Example: '2014-03-30')

        Returns:
            Response from getLNPList operation
        """
        ...

    def getLNPListStatus(
        self,
        validate: bool = True,
    ) -> Dict[str, Any]:
        """Retrieve lnp list status information

        Returns:
            Response from getLNPListStatus operation
        """
        ...

    def getLNPNotes(
        self,
        validate: bool = True,
        *,
        portid: int,
    ) -> Dict[str, Any]:
        """Retrieve lnp notes information

        Args:
            validate: Whether to validate parameters with Pydantic
            portid: ID of the port previously created. (required)

        Returns:
            Response from getLNPNotes operation
        """
        ...

    def getLNPStatus(
        self,
        validate: bool = True,
        *,
        portid: int,
    ) -> Dict[str, Any]:
        """Retrieve lnp status information

        Args:
            validate: Whether to validate parameters with Pydantic
            portid: ID of the port previously created. (required)

        Returns:
            Response from getLNPStatus operation
        """
        ...

    def getLanguages(
        self,
        validate: bool = True,
        *,
        language: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve languages information

        Args:
            validate: Whether to validate parameters with Pydantic
            language: Code for a specific Language (Example: 'en')

        Returns:
            Response from getLanguages operation
        """
        ...

    def getLocales(
        self,
        validate: bool = True,
        *,
        locale: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve locales information

        Args:
            validate: Whether to validate parameters with Pydantic
            locale: Code for a specific Locale Code (Example: 'en-US')

        Returns:
            Response from getLocales operation
        """
        ...

    def getLockInternational(
        self,
        validate: bool = True,
        *,
        lock_international: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve lock international information

        Args:
            validate: Whether to validate parameters with Pydantic
            lock_international: Code for a specific Lock International Mode (Example: 1)

        Returns:
            Response from getLockInternational operation
        """
        ...

    def getMMS(
        self,
        validate: bool = True,
        *,
        all_messages: Optional[int] = None,
        contact: Optional[str] = None,
        did: Optional[int] = None,
        from_: Optional[str] = None,
        limit: Optional[int] = None,
        mms: Optional[int] = None,
        timezone: Optional[str] = None,
        to: Optional[str] = None,
        type_: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve mms information

        Args:
            validate: Whether to validate parameters with Pydantic
            all_messages: Filter to recive all MMSs and SMSs, 1 recive all SMS and MMS, 0 if only need MMS, important: the sms ID must be 0
            contact: Contact number for Filtering MMSs (Example: 5551234567)
            did: DID number for Filtering MMSs (Example: 5551234567)
            from_: Start Date for Filtering MMSs (Example: '2014-03-30') - Default value: Today
            limit: Number of records to be displayed (Example: 20) - Default value: 50
            mms: ID for a specific MMS (Example: 1918)
            timezone: Adjust time of MMSs according to Timezome (Numeric: -12 to 13)
            to: End Date for Filtering MMSs (Example: '2014-03-30') - Default value: Today
            type_: Filter MMSs by Type (Boolean: 1 = received / 0 = sent)

        Returns:
            Response from getMMS operation

        Note:
            Date parameters use 'from' and 'to' instead of 'date_from' and 'date_to'
        """
        ...

    def getMediaMMS(
        self,
        validate: bool = True,
        *,
        id_: Optional[int] = None,
        media_as_array: Optional[Annotated[str, "Format: json"]] = None,
    ) -> Dict[str, Any]:
        """Retrieve media mms information

        Args:
            validate: Whether to validate parameters with Pydantic
            id_: ID for a specific MMS (Example: 1918)
            media_as_array: Return the list of media attachments as an Array if the value is 1 or as a JSON Object if the value is 0 (Default: 0)

        Returns:
            Response from getMediaMMS operation
        """
        ...

    def getMusicOnHold(
        self,
        validate: bool = True,
        *,
        music_on_hold: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve music on hold information

        Args:
            validate: Whether to validate parameters with Pydantic
            music_on_hold: Code for a specific Music on Hold (Example: 'jazz')

        Returns:
            Response from getMusicOnHold operation
        """
        ...

    def getNAT(
        self,
        validate: bool = True,
        *,
        nat: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve nat information

        Args:
            validate: Whether to validate parameters with Pydantic
            nat: Code for a specific NAT Option (Example: 'route')

        Returns:
            Response from getNAT operation
        """
        ...

    def getPackages(
        self,
        validate: bool = True,
        *,
        package: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve packages information

        Args:
            validate: Whether to validate parameters with Pydantic
            package: Code for a specific Package (Example: 8378)

        Returns:
            Response from getPackages operation
        """
        ...

    def getPhonebook(
        self,
        validate: bool = True,
        *,
        group: Optional[int] = None,
        group_name: Optional[str] = None,
        name: Optional[str] = None,
        phonebook: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve phonebook information

        Args:
            validate: Whether to validate parameters with Pydantic
            group: ID for a specific Phonebook group
            group_name: Group Name
            name: Name to be searched in database   (Example: 'jane')
            phonebook: ID for a specific Phonebook entry (Example: 32207)

        Returns:
            Response from getPhonebook operation
        """
        ...

    def getPhonebookGroups(
        self,
        validate: bool = True,
        *,
        group: Optional[int] = None,
        name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve phonebook groups information

        Args:
            validate: Whether to validate parameters with Pydantic
            group: ID for a specific Phonebook group
            name: Group Name

        Returns:
            Response from getPhonebookGroups operation
        """
        ...

    def getPlayInstructions(
        self,
        validate: bool = True,
        *,
        play_instructions: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve play instructions information

        Args:
            validate: Whether to validate parameters with Pydantic
            play_instructions: Code for a specific Play Instructions setting (Example: 'u')

        Returns:
            Response from getPlayInstructions operation
        """
        ...

    def getPortability(
        self,
        validate: bool = True,
        *,
        did: int,
    ) -> Dict[str, Any]:
        """Retrieve portability information

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID Number to be ported into our network (Example: 5552341234) (required)

        Returns:
            Response from getPortability operation
        """
        ...

    def getProtocols(
        self,
        validate: bool = True,
        *,
        protocol: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve protocols information

        Args:
            validate: Whether to validate parameters with Pydantic
            protocol: Code for a specific Protocol (Example: 3)

        Returns:
            Response from getProtocols operation
        """
        ...

    def getProvinces(
        self,
        validate: bool = True,
    ) -> Dict[str, Any]:
        """Retrieve provinces information

        Returns:
            Response from getProvinces operation
        """
        ...

    def getQueues(
        self,
        validate: bool = True,
        *,
        queue: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve queues information

        Args:
            validate: Whether to validate parameters with Pydantic
            queue: ID for a specific Queue (Example: 4764)

        Returns:
            Response from getQueues operation
        """
        ...

    def getRateCentersCAN(
        self,
        validate: bool = True,
        *,
        province: str,
    ) -> Dict[str, Any]:
        """Retrieve rate centers can information

        Args:
            validate: Whether to validate parameters with Pydantic
            province: Canadian Province (Values from getProvinces) (required)

        Returns:
            Response from getRateCentersCAN operation
        """
        ...

    def getRateCentersUSA(
        self,
        validate: bool = True,
        *,
        state: str,
    ) -> Dict[str, Any]:
        """Retrieve rate centers usa information

        Args:
            validate: Whether to validate parameters with Pydantic
            state: United States State (Values from getStates) (required)

        Returns:
            Response from getRateCentersUSA operation
        """
        ...

    def getRates(
        self,
        validate: bool = True,
        *,
        package: int,
        query: str,
    ) -> Dict[str, Any]:
        """Retrieve rates information

        Args:
            validate: Whether to validate parameters with Pydantic
            package: ID for a specific Package (Example: 92364) (required)
            query: Query for searching rates (Example: 'Canada') (required)

        Returns:
            Response from getRates operation
        """
        ...

    def getRecordingFile(
        self,
        validate: bool = True,
        *,
        recording: int,
    ) -> Dict[str, Any]:
        """Retrieve recording file information

        Args:
            validate: Whether to validate parameters with Pydantic
            recording: ID for a specific Recording (Example: 7567) (required)

        Returns:
            Response from getRecordingFile operation
        """
        ...

    def getRecordings(
        self,
        validate: bool = True,
        *,
        recording: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve recordings information

        Args:
            validate: Whether to validate parameters with Pydantic
            recording: ID for a specific Recording (Example: 7567)

        Returns:
            Response from getRecordings operation
        """
        ...

    def getRegistrationStatus(
        self,
        validate: bool = True,
        *,
        account: int,
    ) -> Dict[str, Any]:
        """Retrieve registration status information

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Specific Account (Example: '100001_VoIP') (required)

        Returns:
            Response from getRegistrationStatus operation
        """
        ...

    def getReportEstimatedHoldTime(
        self,
        validate: bool = True,
        *,
        type_: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve report estimated hold time information

        Args:
            validate: Whether to validate parameters with Pydantic
            type_: Code for a specific 'ReportEstimatedHoldTime' Type (Example: 'yes')

        Returns:
            Response from getReportEstimatedHoldTime operation
        """
        ...

    def getResellerBalance(
        self,
        validate: bool = True,
        *,
        client: int,
    ) -> Dict[str, Any]:
        """Retrieve reseller balance information

        Args:
            validate: Whether to validate parameters with Pydantic
            client: ID for a specific Reseller Client (Example: 561115) (required)

        Returns:
            Response from getResellerBalance operation
        """
        ...

    def getResellerCDR(
        self,
        validate: bool = True,
        *,
        client: int,
        date_from: str,
        date_to: str,
        timezone: str,
        account: Optional[int] = None,
        answered: Optional[Literal["0", "1"]] = None,
        busy: Optional[Literal["0", "1"]] = None,
        callbilling: Optional[str] = None,
        calltype: Optional[str] = None,
        failed: Optional[Literal["0", "1"]] = None,
        noanswer: Optional[Literal["0", "1"]] = None,
    ) -> Dict[str, Any]:
        """Retrieve reseller cdr information

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Filter CDR by Account (Values from getCallAccounts)
            answered: Include Answered Calls to CDR (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            busy: Include Busy Calls to CDR (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            callbilling: Filter CDR by Call Billing (Values from getCallBilling)
            calltype: Filters CDR by Call Type (Values from getCallTypes)
            client: ID for a specific Reseller Client (Example: 561115) (required)
            date_from: Start Date for Filtering CDR (Example: '2010-11-30') (required)
            date_to: End Date for Filtering CDR (Example: '2010-11-30') (required)
            failed: Include Failed Calls to CDR (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            noanswer: Include NoAnswered calls to CDR (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            timezone: Adjust time of calls according to Timezome (Numeric: -12 to 13) (required)

        Returns:
            Response from getResellerCDR operation
        """
        ...

    def getResellerMMS(
        self,
        validate: bool = True,
        *,
        client: int,
        mms: int,
        all_messages: Optional[int] = None,
        contact: Optional[str] = None,
        did: Optional[int] = None,
        from_: Optional[str] = None,
        limit: Optional[int] = None,
        timezone: Optional[str] = None,
        to: Optional[str] = None,
        type_: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve reseller mms information

        Args:
            validate: Whether to validate parameters with Pydantic
            all_messages: Filter to recive all SMSs and MMSs, 1 recive all SMS and MMS, 0 if only need SMS, important: the sms ID must be 0
            client:  (required)
            contact: Contact number for Filtering MMSs (Example: 5551234567)
            did: DID number for Filtering MMSs (Example: 5551234567)
            from_: Start Date for Filtering SMSs (Example: '2014-03-30') - Default value: Today
            limit: Number of records to be displayed (Example: 20) - Default value: 50
            mms:  (required)
            timezone: Adjust time of MMSs according to Timezome (Numeric: -12 to 13)
            to: End Date for Filtering MMSs (Example: '2014-03-30')
            type_: Filter SMSs by Type (Boolean: 1 = received / 0 = sent)

        Returns:
            Response from getResellerMMS operation
        """
        ...

    def getResellerSMS(
        self,
        validate: bool = True,
        *,
        client: int,
        all_messages: Optional[int] = None,
        contact: Optional[str] = None,
        did: Optional[int] = None,
        from_: Optional[str] = None,
        limit: Optional[int] = None,
        sms: Optional[int] = None,
        timezone: Optional[str] = None,
        to: Optional[str] = None,
        type_: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve reseller sms information

        Args:
            validate: Whether to validate parameters with Pydantic
            all_messages: Filter to recive all SMSs and MMSs, 1 recive all SMS and MMS, 0 if only need SMS, important: the sms ID must be 0
            client:  (required)
            contact: Contact number for Filtering SMSs (Example: 5551234567)
            did: DID number for Filtering SMSs (Example: 5551234567)
            from_: Start Date for Filtering SMSs (Example: '2014-03-30') - Default value: Today
            limit: Number of records to be displayed (Example: 20) - Default value: 50
            sms: ID for a specific SMS (Example: 5853)
            timezone: Adjust time of SMSs according to Timezome (Numeric: -12 to 13)
            to: End Date for Filtering SMSs (Example: '2014-03-30')
            type_: Filter SMSs by Type (Boolean: 1 = received / 0 = sent)

        Returns:
            Response from getResellerSMS operation
        """
        ...

    def getRingGroups(
        self,
        validate: bool = True,
        *,
        ring_group: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve ring groups information

        Args:
            validate: Whether to validate parameters with Pydantic
            ring_group: ID for a specific Ring Group (Example: 4768)

        Returns:
            Response from getRingGroups operation
        """
        ...

    def getRingStrategies(
        self,
        validate: bool = True,
        *,
        strategy: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve ring strategies information

        Args:
            validate: Whether to validate parameters with Pydantic
            strategy: ID for a specific Ring Strategy (Example: 'rrmemory')

        Returns:
            Response from getRingStrategies operation
        """
        ...

    def getRoutes(
        self,
        validate: bool = True,
        *,
        route: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve routes information

        Args:
            validate: Whether to validate parameters with Pydantic
            route: Code for a specific Route (Example: 2)

        Returns:
            Response from getRoutes operation
        """
        ...

    def getSIPURIs(
        self,
        validate: bool = True,
        *,
        sipuri: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve sipur is information

        Args:
            validate: Whether to validate parameters with Pydantic
            sipuri: ID for a specific SIP URI (Example: 6199)

        Returns:
            Response from getSIPURIs operation
        """
        ...

    def getSMS(
        self,
        validate: bool = True,
        *,
        all_messages: Optional[int] = None,
        contact: Optional[str] = None,
        did: Optional[int] = None,
        from_: Optional[str] = None,
        limit: Optional[int] = None,
        sms: Optional[int] = None,
        timezone: Optional[str] = None,
        to: Optional[str] = None,
        type_: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve sms information

        Args:
            validate: Whether to validate parameters with Pydantic
            all_messages: Filter to recive all SMSs and MMSs, 1 recive all SMS and MMS, 0 if only need SMS, important: the sms ID must be 0
            contact: Contact number for Filtering SMSs (Example: 5551234567)
            did: DID number for Filtering SMSs (Example: 5551234567)
            from_: Start Date for Filtering SMSs (Example: '2014-03-30') - Default value: Today
            limit: Number of records to be displayed (Example: 20) - Default value: 50
            sms: ID for a specific SMS (Example: 5853)
            timezone: Adjust time of SMSs according to Timezome (Numeric: -12 to 13)
            to: End Date for Filtering SMSs (Example: '2014-03-30') - Default value: Today
            type_: Filter SMSs by Type (Boolean: 1 = received / 0 = sent)

        Returns:
            Response from getSMS operation

        Note:
            Date parameters use 'from' and 'to' instead of 'date_from' and 'date_to'
        """
        ...

    def getServersInfo(
        self,
        validate: bool = True,
        *,
        server_pop: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve servers info information

        Args:
            validate: Whether to validate parameters with Pydantic
            server_pop: POP for a specific Server (Example: 1)

        Returns:
            Response from getServersInfo operation
        """
        ...

    def getStates(
        self,
        validate: bool = True,
    ) -> Dict[str, Any]:
        """Retrieve states information

        Returns:
            Response from getStates operation
        """
        ...

    def getStaticMembers(
        self,
        validate: bool = True,
        *,
        queue: int,
        member: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve static members information

        Args:
            validate: Whether to validate parameters with Pydantic
            member: ID for a specific Static Member (Example: 163) - The Member must belong to the queue provided
            queue: ID for a specific Queue (Example: 4136) (required)

        Returns:
            Response from getStaticMembers operation
        """
        ...

    def getSubAccounts(
        self,
        validate: bool = True,
        *,
        account: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve sub accounts information

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Parameter could have the following values: * Empty Value [Not Required] * Specific Sub Account (Example: '100000_VoIP') * Specific Reseller Client ID (Example: 561115)

        Returns:
            Response from getSubAccounts operation
        """
        ...

    def getTerminationRates(
        self,
        validate: bool = True,
        *,
        query: str,
        route: int,
    ) -> Dict[str, Any]:
        """Retrieve termination rates information

        Args:
            validate: Whether to validate parameters with Pydantic
            query: Query for searching rates (Example: 'Canada') (required)
            route: Route Code (Values from getRoutes)(Example: '2') (required)

        Returns:
            Response from getTerminationRates operation
        """
        ...

    def getTimeConditions(
        self,
        validate: bool = True,
        *,
        timecondition: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve time conditions information

        Args:
            validate: Whether to validate parameters with Pydantic
            timecondition: ID for a specific Time Condition (Example: 1830)

        Returns:
            Response from getTimeConditions operation
        """
        ...

    def getTimezones(
        self,
        validate: bool = True,
        *,
        timezone: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve timezones information

        Args:
            validate: Whether to validate parameters with Pydantic
            timezone: Code for a specific Time Zone (Example: 'America/Buenos_Aires')

        Returns:
            Response from getTimezones operation
        """
        ...

    def getTransactionHistory(
        self,
        validate: bool = True,
        *,
        date_from: str,
        date_to: str,
    ) -> Dict[str, Any]:
        """Retrieve transaction history information

        Args:
            validate: Whether to validate parameters with Pydantic
            date_from: Start Date for Filtering Transactions (Example: '2016-06-03') (required)
            date_to: End Date for Filtering Transactions (Example: '2016-06-04') (required)

        Returns:
            Response from getTransactionHistory operation
        """
        ...

    def getVPRIs(
        self,
        validate: bool = True,
    ) -> Dict[str, Any]:
        """Retrieve vpr is information

        Returns:
            Response from getVPRIs operation
        """
        ...

    def getVoicemailAttachmentFormats(
        self,
        validate: bool = True,
        *,
        email_attachment_format: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve voicemail attachment formats information

        Args:
            validate: Whether to validate parameters with Pydantic
            email_attachment_format: ID for a specific attachment format (Example: wav49)

        Returns:
            Response from getVoicemailAttachmentFormats operation
        """
        ...

    def getVoicemailFolders(
        self,
        validate: bool = True,
        *,
        folder: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve voicemail folders information

        Args:
            validate: Whether to validate parameters with Pydantic
            folder: Folder Name (Example: 'INBOX')

        Returns:
            Response from getVoicemailFolders operation
        """
        ...

    def getVoicemailMessageFile(
        self,
        validate: bool = True,
        *,
        folder: str,
        mailbox: int,
        message_num: int,
    ) -> Dict[str, Any]:
        """Retrieve voicemail message file information

        Args:
            validate: Whether to validate parameters with Pydantic
            folder: Name for specific Folder (Example: 'INBOX', values from: getVoicemailFolders) (required)
            mailbox: ID for specific Mailbox (Example: 1001) (required)
            message_num: ID for specific Voicemail Message (Example: 1) (required)

        Returns:
            Response from getVoicemailMessageFile operation
        """
        ...

    def getVoicemailMessages(
        self,
        validate: bool = True,
        *,
        mailbox: int,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        folder: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve voicemail messages information

        Args:
            validate: Whether to validate parameters with Pydantic
            date_from: Start Date for Filtering Voicemail Messages (Example: '2016-01-30')
            date_to: End Date for Filtering Voicemail Messages (Example: '2016-01-30')
            folder: Name for specific Folder (Example: 'INBOX', values from: getVoicemailFolders)
            mailbox: ID for specific Mailbox (Example: 1001) (required)

        Returns:
            Response from getVoicemailMessages operation
        """
        ...

    def getVoicemailSetups(
        self,
        validate: bool = True,
        *,
        voicemailsetup: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve voicemail setups information

        Args:
            validate: Whether to validate parameters with Pydantic
            voicemailsetup: ID for a specific Voicemail Setup (Example: 2)

        Returns:
            Response from getVoicemailSetups operation
        """
        ...

    def getVoicemails(
        self,
        validate: bool = True,
        *,
        mailbox: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve voicemails information

        Args:
            validate: Whether to validate parameters with Pydantic
            mailbox: ID for specific Mailbox (Example: 1001)

        Returns:
            Response from getVoicemails operation
        """
        ...

    def mailFaxMessagePDF(
        self,
        validate: bool = True,
        *,
        email: Annotated[str, "Format: email"],
        id_: int,
    ) -> Dict[str, Any]:
        """Mail fax message pdf

        Args:
            validate: Whether to validate parameters with Pydantic
            email: Destination email adreess (example: yourname@company.com) (required)
            id_: ID of the Fax Message requested (Values from getFaxMessages) (required)

        Returns:
            Response from mailFaxMessagePDF operation
        """
        ...

    def markListenedVoicemailMessage(
        self,
        validate: bool = True,
        *,
        folder: str,
        listened: int,
        mailbox: int,
        message_num: int,
    ) -> Dict[str, Any]:
        """Mark listened voicemail message

        Args:
            validate: Whether to validate parameters with Pydantic
            folder: Name for specific Folder (Example: 'INBOX', values from: getVoicemailFolders) (required)
            listened: Code for mark voicemail as listened or not-listened (Values: 'yes'/'no') (required)
            mailbox: ID for specific Mailbox (Example: 1001) (required)
            message_num: ID for specific Voicemail Message (Example: 1) (required)

        Returns:
            Response from markListenedVoicemailMessage operation
        """
        ...

    def markUrgentVoicemailMessage(
        self,
        validate: bool = True,
        *,
        folder: str,
        mailbox: int,
        message_num: int,
        urgent: int,
    ) -> Dict[str, Any]:
        """Mark urgent voicemail message

        Args:
            validate: Whether to validate parameters with Pydantic
            folder: Name for specific Folder (Example: 'INBOX', values from: getVoicemailFolders) (required)
            mailbox: ID for specific Mailbox (Example: 1001) (required)
            message_num: ID for specific Voicemail Message (Example: 1) (required)
            urgent: Code for mark voicemail as urgent or not-urgent (Values: 'yes'/'no') (required)

        Returns:
            Response from markUrgentVoicemailMessage operation
        """
        ...

    def moveFaxMessage(
        self,
        validate: bool = True,
        *,
        fax_id: int,
        folder_id: int,
        test: Optional[Literal["true", "false"]] = None,
    ) -> Dict[str, Any]:
        """Move fax message

        Args:
            validate: Whether to validate parameters with Pydantic
            fax_id: ID of the Fax Message requested (Values from getFaxMessages) (required)
            folder_id: ID of the destination Fax Folder (Values from getFaxFolders) (required)
            test: Set to true if testing how to move a Fax Message (accepts: true/false, yes/no, on/off, 1/0, boolean)

        Returns:
            Response from moveFaxMessage operation
        """
        ...

    def moveFolderVoicemailMessage(
        self,
        validate: bool = True,
        *,
        folder: str,
        mailbox: int,
        message_num: int,
        new_folder: str,
    ) -> Dict[str, Any]:
        """Move folder voicemail message

        Args:
            validate: Whether to validate parameters with Pydantic
            folder: Name for specific Folder (Example: 'INBOX', values from: getVoicemailFolders) (required)
            mailbox: ID for specific Mailbox (Example: 1001) (required)
            message_num: ID for specific Voicemail Message (Example: 1) (required)
            new_folder: Destination Folder (Example: 'Urgent', values from: getVoicemailFolders) (required)

        Returns:
            Response from moveFolderVoicemailMessage operation
        """
        ...

    def orderDID(
        self,
        validate: bool = True,
        *,
        billing_type: Literal["1", "2"],
        cnam: Literal["0", "1"],
        dialtime: int,
        did: int,
        pop: int,
        routing: int,
        account: Optional[int] = None,
        callerid_prefix: Optional[int] = None,
        failover_busy: Optional[int] = None,
        failover_noanswer: Optional[int] = None,
        failover_unreachable: Optional[int] = None,
        minute: Optional[Annotated[str, "Units: minutes"]] = None,
        monthly: Optional[str] = None,
        note: Optional[int] = None,
        setup: Optional[str] = None,
        test: Optional[Literal["true", "false"]] = None,
        voicemail: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Order did

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Reseller Sub Account (Example: '100001_VoIP')
            billing_type: Billing type for the DID (1 = Per Minute, 2 = Flat) (required)
            callerid_prefix: Caller ID Prefix for the DID
            cnam: CNAM for the DID (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean) (required)
            dialtime: Dial Time Out for the DID (Example: 60 -> in seconds) (required)
            did: DID to be Ordered (Example: 5552223333) (required)
            failover_busy: Busy Routing for the DID
            failover_noanswer: NoAnswer Routing for the DID
            failover_unreachable: Unreachable Routing for the DID
            minute: Minute Rate for Reseller Client (Example: 0.03)
            monthly: Montly Fee for Reseller Client (Example: 3.50)
            note: Note for the DID
            pop: Point of Presence for the DID (Example: 5) (required)
            routing: Main Routing for the DID (required)
            setup: Setup Fee for Reseller Client (Example: 1.99)
            test: Set to true if testing how Orders work - Orders can not be undone - When testing, no Orders are made (accepts: true/false, yes/no, on/off, 1/0, boolean)
            voicemail: Voicemail for the DID (Example: 101)

        Returns:
            Response from orderDID operation

        Note:
            CNAM parameter is converted to '1'/'0' string
        """
        ...

    def orderDIDInternationalGeographic(
        self,
        validate: bool = True,
        *,
        billing_type: Literal["1", "2"],
        cnam: Literal["0", "1"],
        dialtime: int,
        location_id: int,
        pop: int,
        quantity: int,
        routing: int,
        account: Optional[int] = None,
        callerid_prefix: Optional[int] = None,
        failover_busy: Optional[int] = None,
        failover_noanswer: Optional[int] = None,
        failover_unreachable: Optional[int] = None,
        minute: Optional[Annotated[str, "Units: minutes"]] = None,
        monthly: Optional[str] = None,
        note: Optional[int] = None,
        setup: Optional[str] = None,
        test: Optional[Literal["true", "false"]] = None,
        voicemail: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Order did international geographic

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Reseller Sub Account (Example: '100001_VoIP')
            billing_type: Billing type for the DID (1 = Per Minute, 2 = Flat) (required)
            callerid_prefix: Caller ID Prefix for the DID
            cnam: CNAM for the DID (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean) (required)
            dialtime: Dial Time Out for the DID (Example: 60 -> in seconds) (required)
            failover_busy: Busy Routing for the DID
            failover_noanswer: NoAnswer Routing for the DID
            failover_unreachable: Unreachable Routing for the DID
            location_id: ID for a specific International Location (Values from getDIDsInternationalGeographic) (required)
            minute: Minute Rate for Reseller Client (Example: 0.03)
            monthly: Montly Fee for Reseller Client (Example: 3.50)
            note: Note for the DID
            pop: Point of Presence for the DID (Example: 5) (required)
            quantity: Number of dids to be purchased (Example: 2) (required)
            routing: Main Routing for the DID (required)
            setup: Setup Fee for Reseller Client (Example: 1.99)
            test: Set to true if testing how Orders work - Orders can not be undone - When testing, no Orders are made (accepts: true/false, yes/no, on/off, 1/0, boolean)
            voicemail: Voicemail for the DID (Example: 101)

        Returns:
            Response from orderDIDInternationalGeographic operation
        """
        ...

    def orderDIDInternationalNational(
        self,
        validate: bool = True,
        *,
        billing_type: Literal["1", "2"],
        cnam: Literal["0", "1"],
        dialtime: int,
        location_id: int,
        pop: int,
        quantity: int,
        routing: int,
        account: Optional[int] = None,
        callerid_prefix: Optional[int] = None,
        failover_busy: Optional[int] = None,
        failover_noanswer: Optional[int] = None,
        failover_unreachable: Optional[int] = None,
        minute: Optional[Annotated[str, "Units: minutes"]] = None,
        monthly: Optional[str] = None,
        note: Optional[int] = None,
        setup: Optional[str] = None,
        test: Optional[Literal["true", "false"]] = None,
        voicemail: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Order did international national

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Reseller Sub Account (Example: '100001_VoIP')
            billing_type: Billing type for the DID (1 = Per Minute, 2 = Flat) (required)
            callerid_prefix: Caller ID Prefix for the DID
            cnam: CNAM for the DID (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean) (required)
            dialtime: Dial Time Out for the DID (Example: 60 -> in seconds) (required)
            failover_busy: Busy Routing for the DID
            failover_noanswer: NoAnswer Routing for the DID
            failover_unreachable: Unreachable Routing for the DID
            location_id: ID for a specific International Location (Values from getDIDsInternationalNational) (required)
            minute: Minute Rate for Reseller Client (Example: 0.03)
            monthly: Montly Fee for Reseller Client (Example: 3.50)
            note: Note for the DID
            pop: Point of Presence for the DID (Example: 5) (required)
            quantity: Number of dids to be purchased (Example: 2) (required)
            routing: Main Routing for the DID (required)
            setup: Setup Fee for Reseller Client (Example: 1.99)
            test: Set to true if testing how Orders work - Orders can not be undone - When testing, no Orders are made (accepts: true/false, yes/no, on/off, 1/0, boolean)
            voicemail: Voicemail for the DID (Example: 101)

        Returns:
            Response from orderDIDInternationalNational operation
        """
        ...

    def orderDIDInternationalTollFree(
        self,
        validate: bool = True,
        *,
        cnam: Literal["0", "1"],
        dialtime: int,
        location_id: int,
        pop: int,
        quantity: int,
        routing: int,
        account: Optional[int] = None,
        callerid_prefix: Optional[int] = None,
        failover_busy: Optional[int] = None,
        failover_noanswer: Optional[int] = None,
        failover_unreachable: Optional[int] = None,
        minute: Optional[Annotated[str, "Units: minutes"]] = None,
        monthly: Optional[str] = None,
        note: Optional[int] = None,
        setup: Optional[str] = None,
        test: Optional[Literal["true", "false"]] = None,
        voicemail: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Order did international toll free

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Reseller Sub Account (Example: '100001_VoIP')
            callerid_prefix: Caller ID Prefix for the DID
            cnam: CNAM for the DID (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean) (required)
            dialtime: Dial Time Out for the DID (Example: 60 -> in seconds) (required)
            failover_busy: Busy Routing for the DID
            failover_noanswer: NoAnswer Routing for the DID
            failover_unreachable: Unreachable Routing for the DID
            location_id: ID for a specific International Location (Values from getDIDsInternationalTollFree) (required)
            minute: Minute Rate for Reseller Client (Example: 0.03)
            monthly: Montly Fee for Reseller Client (Example: 3.50)
            note: Note for the DID
            pop: Point of Presence for the DID (Example: 5) (required)
            quantity: Number of dids to be purchased (Example: 2) (required)
            routing: Main Routing for the DID (required)
            setup: Setup Fee for Reseller Client (Example: 1.99)
            test: Set to true if testing how Orders work - Orders can not be undone - When testing, no Orders are made (accepts: true/false, yes/no, on/off, 1/0, boolean)
            voicemail: Voicemail for the DID (Example: 101)

        Returns:
            Response from orderDIDInternationalTollFree operation
        """
        ...

    def orderDIDVirtual(
        self,
        validate: bool = True,
        *,
        cnam: Literal["0", "1"],
        dialtime: int,
        digits: int,
        pop: int,
        routing: int,
        account: Optional[int] = None,
        callerid_prefix: Optional[int] = None,
        failover_busy: Optional[int] = None,
        failover_noanswer: Optional[int] = None,
        failover_unreachable: Optional[int] = None,
        minute: Optional[Annotated[str, "Units: minutes"]] = None,
        monthly: Optional[str] = None,
        note: Optional[int] = None,
        setup: Optional[str] = None,
        test: Optional[Literal["true", "false"]] = None,
        voicemail: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Order did virtual

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Reseller Sub Account (Example: '100001_VoIP')
            callerid_prefix: Caller ID Prefix for the DID
            cnam: CNAM for the DID (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean) (required)
            dialtime: Dial Time Out for the DID (Example: 60 -> in seconds) (required)
            digits: Three Digits for the new Virtual DID (Example: 001) (required)
            failover_busy: Busy Routing for the DID
            failover_noanswer: NoAnswer Routing for the DID
            failover_unreachable: Unreachable Routing for the DID
            minute: Minute Rate for Reseller Client (Example: 0.03)
            monthly: Montly Fee for Reseller Client (Example: 3.50)
            note: Note for the DID
            pop: Point of Presence for the DID (Example: 5) (required)
            routing: Main Routing for the DID (required)
            setup: Setup Fee for Reseller Client (Example: 1.99)
            test: Set to true if testing how Orders work - Orders can not be undone - When testing, no Orders are made (accepts: true/false, yes/no, on/off, 1/0, boolean)
            voicemail: Voicemail for the DID (Example: 101)

        Returns:
            Response from orderDIDVirtual operation
        """
        ...

    def orderFaxNumber(
        self,
        validate: bool = True,
        *,
        location: int,
        quantity: str,
        email: Optional[Annotated[str, "Format: email"]] = None,
        email_attach_file: Optional[Annotated[str, "Format: pdf"]] = None,
        email_enable: Optional[str] = None,
        test: Optional[Literal["true", "false"]] = None,
        url_callback: Optional[str] = None,
        url_callback_enable: Optional[str] = None,
        url_callback_retry: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Order fax number

        Args:
            validate: Whether to validate parameters with Pydantic
            email: Email address where send notifications when receive Fax Messages - (Example: yourname@company.com)
            email_attach_file: Flag to enable attach the Fax Message as a PDF file in the notifications. - (Values: 1 = true, 0 = false) - Default: 0
            email_enable: Flag to enable the email notifications. - (Values: 1 = true, 0 = false) - Default: 0
            location: Location ID of the Fax Number (Values from getFaxRateCentersCAN/getFaxRateCentersUSA) (required)
            quantity: Quantity of Fax Numbers to order (Example: 3) (required)
            test: Set to true if testing how Orders work - Orders can not be undone - When testing, no Orders are made (accepts: true/false, yes/no, on/off, 1/0, boolean)
            url_callback: URL where make a POST when you receive a Fax Message.
            url_callback_enable: Flag to enable the URL Callback functionality. - (Values: 1 = true, 0 = false) - Default: 0
            url_callback_retry: Flag to enable retry the POST action in case we don't receive "ok".

        Returns:
            Response from orderFaxNumber operation
        """
        ...

    def orderTollFree(
        self,
        validate: bool = True,
        *,
        cnam: Literal["0", "1"],
        dialtime: int,
        did: int,
        pop: int,
        routing: int,
        account: Optional[int] = None,
        callerid_prefix: Optional[int] = None,
        failover_busy: Optional[int] = None,
        failover_noanswer: Optional[int] = None,
        failover_unreachable: Optional[int] = None,
        minute: Optional[Annotated[str, "Units: minutes"]] = None,
        monthly: Optional[str] = None,
        note: Optional[int] = None,
        setup: Optional[str] = None,
        test: Optional[Literal["true", "false"]] = None,
        voicemail: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Order toll free

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Reseller Sub Account (Example: '100001_VoIP')
            callerid_prefix: Caller ID Prefix for the DID
            cnam: CNAM for the DID (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean) (required)
            dialtime: Dial Time Out for the DID (Example: 60 -> in seconds) (required)
            did: DID to be Ordered (Example: 8772223333) (required)
            failover_busy: Busy Routing for the DID
            failover_noanswer: NoAnswer Routing for the DID
            failover_unreachable: Unreachable Routing for the DID
            minute: Minute Rate for Reseller Client (Example: 0.03)
            monthly: Montly Fee for Reseller Client (Example: 3.50)
            note: Note for the DID
            pop: Point of Presence for the DID (Example: 5) (required)
            routing: Main Routing for the DID (required)
            setup: Setup Fee for Reseller Client (Example: 1.99)
            test: Set to true if testing how Orders work - Orders can not be undone - When testing, no Orders are made (accepts: true/false, yes/no, on/off, 1/0, boolean)
            voicemail: Voicemail for the DID (Example: 101)

        Returns:
            Response from orderTollFree operation
        """
        ...

    def orderVanity(
        self,
        validate: bool = True,
        *,
        carrier: int,
        cnam: Literal["0", "1"],
        dialtime: int,
        did: int,
        pop: int,
        routing: int,
        account: Optional[int] = None,
        callerid_prefix: Optional[int] = None,
        failover_busy: Optional[int] = None,
        failover_noanswer: Optional[int] = None,
        failover_unreachable: Optional[int] = None,
        minute: Optional[Annotated[str, "Units: minutes"]] = None,
        monthly: Optional[str] = None,
        note: Optional[int] = None,
        setup: Optional[str] = None,
        test: Optional[Literal["true", "false"]] = None,
        voicemail: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Order vanity

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Reseller Sub Account (Example: '100001_VoIP')
            callerid_prefix: Caller ID Prefix for the DID
            carrier: Carrier for the DID (Values from getCarriers) (required)
            cnam: CNAM for the DID (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean) (required)
            dialtime: Dial Time Out for the DID (Example: 60 -> in seconds) (required)
            did: DID to be Ordered (Example: 8772223333) (required)
            failover_busy: Busy Routing for the DID
            failover_noanswer: NoAnswer Routing for the DID
            failover_unreachable: Unreachable Routing for the DID
            minute: Minute Rate for Reseller Client (Example: 0.03)
            monthly: Montly Fee for Reseller Client (Example: 3.50)
            note: Note for the DID
            pop: Point of Presence for the DID (Example: 5) (required)
            routing: Main Routing for the DID (required)
            setup: Setup Fee for Reseller Client (Example: 1.99)
            test: Set to true if testing how Orders work - Orders can not be undone - When testing, no Orders are made (accepts: true/false, yes/no, on/off, 1/0, boolean)
            voicemail: Voicemail for the DID (Example: 101)

        Returns:
            Response from orderVanity operation
        """
        ...

    def removeDIDvPRI(
        self,
        validate: bool = True,
        *,
        did: int,
        vpri: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Remove di dv pri

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID Number to be remove from our Vpri (Example: 561115) (required)
            vpri: Id for specific Vpri

        Returns:
            Response from removeDIDvPRI operation
        """
        ...

    def searchDIDsCAN(
        self,
        validate: bool = True,
        *,
        query: str,
        type_: str,
        province: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Search for di ds can

        Args:
            validate: Whether to validate parameters with Pydantic
            province: Canadian Province (Values from getProvinces)
            query: Query for searching (Examples: 'JOHN', '555', '123ABC') (required)
            type_: Type of search (Values: 'starts', 'contains', 'ends') (required)

        Returns:
            Response from searchDIDsCAN operation
        """
        ...

    def searchDIDsUSA(
        self,
        validate: bool = True,
        *,
        query: str,
        type_: str,
        state: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Search for di ds usa

        Args:
            validate: Whether to validate parameters with Pydantic
            query: Query for searching (Examples: 'JOHN', '555', '123ABC') (required)
            state: United States State (Values from getStates)
            type_: Type of search (Values: 'starts', 'contains', 'ends') (required)

        Returns:
            Response from searchDIDsUSA operation
        """
        ...

    def searchFaxAreaCodeCAN(
        self,
        validate: bool = True,
        *,
        area_code: int,
    ) -> Dict[str, Any]:
        """Search for fax area code can

        Args:
            validate: Whether to validate parameters with Pydantic
            area_code: Area code number, as the initial of the Fax Number you looking for. (values from getFaxRateCentersCAN) (required)

        Returns:
            Response from searchFaxAreaCodeCAN operation
        """
        ...

    def searchFaxAreaCodeUSA(
        self,
        validate: bool = True,
        *,
        area_code: int,
    ) -> Dict[str, Any]:
        """Search for fax area code usa

        Args:
            validate: Whether to validate parameters with Pydantic
            area_code: Area code number, as the initial of the Fax Number you looking for. (values from getFaxRateCentersUSA) (required)

        Returns:
            Response from searchFaxAreaCodeUSA operation
        """
        ...

    def searchTollFreeCanUS(
        self,
        validate: bool = True,
        *,
        query: Optional[str] = None,
        type_: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Search for toll free can us

        Args:
            validate: Whether to validate parameters with Pydantic
            query: Query for searching (Examples: 'JOHN', '555', '123ABC')
            type_: Type of search (Values: 'starts', 'contains', 'ends')

        Returns:
            Response from searchTollFreeCanUS operation
        """
        ...

    def searchTollFreeUSA(
        self,
        validate: bool = True,
        *,
        query: Optional[str] = None,
        type_: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Search for toll free usa

        Args:
            validate: Whether to validate parameters with Pydantic
            query: Query for searching (Examples: 'JOHN', '555', '123ABC')
            type_: Type of search (Values: 'starts', 'contains', 'ends')

        Returns:
            Response from searchTollFreeUSA operation
        """
        ...

    def searchVanity(
        self,
        validate: bool = True,
        *,
        query: str,
        type_: str,
    ) -> Dict[str, Any]:
        """Search for vanity

        Args:
            validate: Whether to validate parameters with Pydantic
            query: Query for searching : 7 Chars Examples: '***JHON', '**555**', '**HELLO' (required)
            type_: Type of Vanity Number Values: '8**', '800', '833', '844', '855', '866', '877', '888' (required)

        Returns:
            Response from searchVanity operation
        """
        ...

    def sendCallRecordingEmail(
        self,
        validate: bool = True,
        *,
        account: int,
        callrecording: str,
        email: str,
    ) -> Dict[str, Any]:
        """Send call recording email

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Filter Call Recordings by Account (Values from getCallAccounts) (required)
            callrecording: Call Recording (Values from getCallRecordings) (required)
            email: Email to send call recording (required)

        Returns:
            Response from sendCallRecordingEmail operation
        """
        ...

    def sendFaxMessage(
        self,
        validate: bool = True,
        *,
        file: int,
        from_name: str,
        from_number: int,
        to_number: int,
        send_email: Optional[Annotated[str, "Format: email"]] = None,
        send_email_enabled: Optional[str] = None,
        station_id: Optional[int] = None,
        test: Optional[Literal["true", "false"]] = None,
    ) -> Dict[str, Any]:
        """Send fax message

        Args:
            validate: Whether to validate parameters with Pydantic
            file: The file must be encoded in Base64, and in one of the following formats: pdf, txt, jpg, gif, png, tif (required)
            from_name: Name of the sender (Example: 5552341234) (required)
            from_number: DID number of the Fax sender (required)
            send_email: Email address where you want send a copy of your Fax.
            send_email_enabled: Flag to enable the send of a copy of your Fax via email. - (Values: 1 = true, 0 = false) - Default: 0
            station_id: An word to identify a equipment or department sending the Fax.
            test: Set to true if testing how to send a Fax Message (accepts: true/false, yes/no, on/off, 1/0, boolean)
            to_number: Destination DID Number (Example: 5552341234) (required)

        Returns:
            Response from sendFaxMessage operation
        """
        ...

    def sendMMS(
        self,
        validate: bool = True,
        *,
        did: int,
        dst: str,
        message: str,
        media1: Optional[Annotated[str, "Units: milliseconds"]] = None,
        media2: Optional[int] = None,
        media3: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Send mms

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID Numbers which is sending the message (Example: 5551234567) (required)
            dst: Destination Number (Example: 5551234568) (required)
            media1: [Optional]  Url to media file (Example: 'https://voip.ms/themes/voipms/assets/img/talent.jpg?v=2'
            media2: [Optional] Base 64 image encode (Example: data:image/png;base64,iVBORw0KGgoAAAANSUh...)
            media3: [Optional] Empty value (Example: '' )
            message: Message to be sent (Example: 'hello John Smith' max chars: 2048) (required)

        Returns:
            Response from sendMMS operation
        """
        ...

    def sendSMS(
        self,
        validate: bool = True,
        *,
        did: int,
        dst: str,
        message: str,
    ) -> Dict[str, Any]:
        """Send sms

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID Numbers which is sending the message (Example: 5551234567) (required)
            dst: Destination Number (Example: 5551234568) (required)
            message: Message to be sent (Example: 'hello John Smith' max chars: 160) (required)

        Returns:
            Response from sendSMS operation
        """
        ...

    def sendVoicemailEmail(
        self,
        validate: bool = True,
        *,
        email_address: Annotated[str, "Format: email"],
        folder: str,
        mailbox: int,
        message_num: int,
    ) -> Dict[str, Any]:
        """Send voicemail email

        Args:
            validate: Whether to validate parameters with Pydantic
            email_address: Destination Email address (Example: john.doe@my-domain.com) (required)
            folder: Name for specific Folder (Example: 'INBOX', values from: getVoicemailFolders) (required)
            mailbox: ID for specific Mailbox (Example: 1001) (required)
            message_num: ID for specific Voicemail Message (Example: 1) (required)

        Returns:
            Response from sendVoicemailEmail operation
        """
        ...

    def setCallHunting(
        self,
        validate: bool = True,
        *,
        description: str,
        language: str,
        members: str,
        music: int,
        order: str,
        press: str,
        recording: str,
        ring_time: str,
        callhunting: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update call hunting settings

        Args:
            validate: Whether to validate parameters with Pydantic
            callhunting: ID for a specific Call Hunting (Example: 235 / Leave empty to create a new one)
            description: Description for the Call Hunting (required)
            language: Language for the Call Hunting (values from getLanguages) (required)
            members: The list of members assigned to the call hunting (required)
            music: Music on Hold Code (Values from getMusicOnHold) (required)
            order: The members will be called in follow or random order (values follow or random) (required)
            press: This option confirm if the member will take the call by pressing 1 * ring_time and press parameters need to have the same amount of items as the members parameter, one for each member. (required)
            recording: Recording for the Call Hunting (values from getRecordings) (required)
            ring_time: The Maximum amount of time the call will ring the member (required)

        Returns:
            Response from setCallHunting operation
        """
        ...

    def setCallParking(
        self,
        validate: bool = True,
        *,
        delay: int,
        destination: int,
        failover: str,
        language: str,
        music: int,
        name: str,
        timeout: int,
        callparking: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update call parking settings

        Args:
            validate: Whether to validate parameters with Pydantic
            callparking: ID for a specific Call Parking (Example: 235 / Leave empty to create a new one)
            delay: The number of seconds before the Announce Destination receives an automatic call from the system to announce the extension of the parked call (required)
            destination: The system will make an automatic call to this destination to announce the extension of the parked call. (Values: parker, main account or sub-accounts) (required)
            failover: Final destination where the call will be forwarded if it isn’t answered. (Values: callback, system:hangup, vm:mailbox) (required)
            language: Language for the Call Parking (values from getLanguages) (required)
            music: Music on Hold Code (Values from getMusicOnHold) (required)
            name: Name for the Call Parking (required)
            timeout: The number of seconds a call will stay parked before it is forwarded to the Failover Destination (required)

        Returns:
            Response from setCallParking operation
        """
        ...

    def setCallback(
        self,
        validate: bool = True,
        *,
        delay_before: str,
        description: str,
        digit_timeout: str,
        number: str,
        response_timeout: str,
        callback: Optional[int] = None,
        callerid_number: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update callback settings

        Args:
            validate: Whether to validate parameters with Pydantic
            callback: ID for a specific Callback (Example: 2359 / Leave empty to create a new one)
            callerid_number: Caller ID Override for the callback
            delay_before: Delay befor calling back (required)
            description: Description for the Callback (required)
            digit_timeout: Time between digits input (required)
            number: Number that will be called back (required)
            response_timeout: Time before hanging up for incomplete input (required)

        Returns:
            Response from setCallback operation
        """
        ...

    def setCallerIDFiltering(
        self,
        validate: bool = True,
        *,
        callerid: int,
        did: int,
        routing: str,
        failover_busy: Optional[str] = None,
        failover_noanswer: Optional[str] = None,
        failover_unreachable: Optional[str] = None,
        filter: Optional[int] = None,
        note: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update caller id filtering settings

        Args:
            validate: Whether to validate parameters with Pydantic
            callerid: Caller ID that triggers the Filter (i = Not North American format, 0 = Anonymous, NPANXXXXXX, s or sb or sc = STIR/SHAKEN Attestation Level, p = All Phone Book, p:XXXX = Specific Phone Book Group) (required)
            did: DIDs affected by the filter (all, NPANXXXXXX) (required)
            failover_busy: Route the call follows when busy
            failover_noanswer: Route the call follows when noanswer
            failover_unreachable: Route the call follows when unreachable
            filter: ID for a specific Caller ID Filtering (Example: 18915 / Leave empty to create a new one)
            note: Note for the Caller ID Filtering
            routing: Route the call follows when filter is triggered (required)

        Returns:
            Response from setCallerIDFiltering operation
        """
        ...

    def setClient(
        self,
        validate: bool = True,
        *,
        client: int,
        email: str,
        firstname: str,
        lastname: str,
        password: str,
        phone_number: Annotated[str, "Format: phone"],
        address: Optional[str] = None,
        balance_management: Optional[str] = None,
        city: Optional[str] = None,
        company: Optional[str] = None,
        country: Optional[int] = None,
        state: Optional[str] = None,
        zip: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update client settings

        Args:
            validate: Whether to validate parameters with Pydantic
            address: Client's Address
            balance_management: Balance Management for Client (Values from getBalanceManagement)
            city: Client's City
            client: ID for a specific Reseller Client (Example: 561115) (required)
            company: Client's Company
            country: Client's Country (Values from getCountries)
            email: Client's e-mail (required)
            firstname: Client's Firstname (required)
            lastname: Client's Lastname (required)
            password: Client's Password (required)
            phone_number: Client's Phone Number (required)
            state: Client's State
            zip: Client's Zip Code

        Returns:
            Response from setClient operation
        """
        ...

    def setClientThreshold(
        self,
        validate: bool = True,
        *,
        client: int,
        threshold: Annotated[str, "Range: 1-250"],
        email: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update client threshold settings

        Args:
            validate: Whether to validate parameters with Pydantic
            client: ID for a specific Reseller Client (Example: 561115) (required)
            email: Client's e-mail for balance threshold notification
            threshold: Threshold amount between 1 and 250 (Example: 10) (required)

        Returns:
            Response from setClientThreshold operation
        """
        ...

    def setConference(
        self,
        validate: bool = True,
        *,
        conference: int,
        description: str,
        max_members: str,
        name: str,
        language: Optional[str] = None,
        members: Optional[str] = None,
        sound_error_menu: Optional[str] = None,
        sound_get_pin: Optional[str] = None,
        sound_has_joined: Optional[str] = None,
        sound_has_left: Optional[str] = None,
        sound_invalid_pin: Optional[int] = None,
        sound_join: Optional[str] = None,
        sound_kicked: Optional[str] = None,
        sound_leave: Optional[str] = None,
        sound_locked: Optional[str] = None,
        sound_locked_now: Optional[str] = None,
        sound_muted: Optional[str] = None,
        sound_only_one: Optional[str] = None,
        sound_only_person: Optional[str] = None,
        sound_other_in_party: Optional[int] = None,
        sound_participants_muted: Optional[str] = None,
        sound_participants_unmuted: Optional[str] = None,
        sound_place_into_conference: Optional[str] = None,
        sound_there_are: Optional[str] = None,
        sound_unlocked_now: Optional[str] = None,
        sound_unmuted: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update conference settings

        Args:
            validate: Whether to validate parameters with Pydantic
            conference: ID for a specific Conference (Example: 5356) (required)
            description: Conference description (required)
            language: Conference Language (Values from getLanguages)
            max_members: Members Max Value (required)
            members: Conference Members
            name: Conference name (required)
            sound_error_menu: The recording played when there is an error on the menu. (Values from getRecordings)
            sound_get_pin: The recording played when prompting for a conference PIN (Values from getRecordings)
            sound_has_joined: The recording played as a user intro (Values from getRecordings)
            sound_has_left: The recording played as a user leaves the conference (Values from getRecordings)
            sound_invalid_pin: The recording played when an invalid PIN is entered too many (3) times (Values from getRecordings)
            sound_join: The recording played when a user joins, typically some kind of beep sound (Values from getRecordings)
            sound_kicked: The recording played to a user who has been kicked from the conference (Values from getRecordings)
            sound_leave: The recording played when a user leaves, typically some kind of beep sound (Values from getRecordings)
            sound_locked: The recording played to a user trying to join a locked conference (Values from getRecordings)
            sound_locked_now: The recording played to an Admin-level user after toggling the conference to locked mode (Values from getRecordings)
            sound_muted: The recording played to a user when the mute option is toggled on (Values from getRecordings)
            sound_only_one: The recording played to a user when there is only one other person in the conference. (Values from getRecordings)
            sound_only_person: The recording played when a user is the only person in the conference (Values from getRecordings)
            sound_other_in_party: The recording used in conjunction with the There are option, used like There are (number of participants) Other in party (Values from getRecordings)
            sound_participants_muted: The recording played when all non-admin participants are muted. (Values from getRecordings)
            sound_participants_unmuted: The recording played when all non-admin participants are unmuted. (Values from getRecordings)
            sound_place_into_conference: The recording played when a user is placed into a conference that cannot start until a marked user enters (Values from getRecordings)
            sound_there_are: The recording played when announcing how many users there are in a conference. (Values from getRecordings)
            sound_unlocked_now: The recording played to an Admin-level user after toggling the conference to unlocked mode (Values from getRecordings)
            sound_unmuted: The recording played to a user when the mute option is toggled off (Values from getRecordings)

        Returns:
            Response from setConference operation
        """
        ...

    def setConferenceMember(
        self,
        validate: bool = True,
        *,
        conference: int,
        member: int,
        name: str,
        admin: Optional[Literal["yes", "no"]] = None,
        announce_join_leave: Optional[Literal["yes", "no"]] = None,
        announce_only_user: Optional[Literal["yes", "no"]] = None,
        announce_user_count: Optional[Literal["yes", "no"]] = None,
        announcement: Optional[str] = None,
        description: Optional[str] = None,
        drop_silence: Optional[Literal["yes", "no"]] = None,
        jitter_buffer: Optional[Literal["yes", "no"]] = None,
        moh_when_empty: Optional[str] = None,
        pin: Optional[str] = None,
        quiet: Optional[Literal["yes", "no"]] = None,
        silence_threshold: Optional[Literal["2000", "2100", "2200", "2300", "2400", "2500", "2600", "2700", "2800", "2900"]] = None,
        start_muted: Optional[Literal["yes", "no"]] = None,
        talk_detection: Optional[Literal["yes", "no"]] = None,
        talking_threshold: Optional[Literal["100", "120", "140", "160", "180", "200", "220", "240"]] = None,
    ) -> Dict[str, Any]:
        """Update conference member settings

        Args:
            validate: Whether to validate parameters with Pydantic
            admin: Sets if the member is an admin or not (yes/no). (accepts: yes/no, true/false, on/off, 1/0, boolean)
            announce_join_leave: Sets if the conference recording when a member joins or leaves will be played (yes/no). (accepts: yes/no, true/false, on/off, 1/0, boolean)
            announce_only_user: Sets if the "only user" announcement should be played when a caller enters an empty conference (yes/no). (accepts: yes/no, true/false, on/off, 1/0, boolean)
            announce_user_count: Sets if the number of members in the conference should be announced to the caller as he joins (yes/no). (accepts: yes/no, true/false, on/off, 1/0, boolean)
            announcement: If set, this recording will be heard only by the user as he joins the conference (Values from getRecordings).
            conference: ID for a specific Conference (Example: 5356) (required)
            description: Member description.
            drop_silence: The system will drop what is detected as silence from entering into the conference (yes/no). (accepts: yes/no, true/false, on/off, 1/0, boolean)
            jitter_buffer: When set to YES, the system will place a jitter buffer on the caller's audio stream before any audio mixing is performed (yes/no). (accepts: yes/no, true/false, on/off, 1/0, boolean)
            member: ID for a specific Member profile (Example: 5356) (required)
            moh_when_empty: Sets whether music on hold (MOH) should be played when only one person is in the conference (Values from getMusicOnHold).
            name: Member name. (required)
            pin: Assigned PIN.
            quiet: When set to "yes", enter/leave prompts and user introductions are not played (yes/no). (accepts: yes/no, true/false, on/off, 1/0, boolean)
            silence_threshold: The time, in milliseconds, that silence needs to be present in the user’s sound stream before the system can consider it to be in fact silent and close the audio (allowed values are 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900 or 3000).
            start_muted: Sets if the member should start out muted after entering the conference (yes/no). (accepts: yes/no, true/false, on/off, 1/0, boolean)
            talk_detection: If set to YES, the conference dashboard will display a notification when a participant starts and stops talking (yes/no). (accepts: yes/no, true/false, on/off, 1/0, boolean)
            talking_threshold: The time, in milliseconds, that a users needs to be sending sound or voice before the system can consider them to be talking (allowed values are 100, 120, 140, 160, 180, 200, 220, 240 or 250).

        Returns:
            Response from setConferenceMember operation
        """
        ...

    def setDIDBillingType(
        self,
        validate: bool = True,
        *,
        billing_type: Literal["1", "2"],
        did: int,
    ) -> Dict[str, Any]:
        """Update did billing type settings

        Args:
            validate: Whether to validate parameters with Pydantic
            billing_type: Billing type for the DID (1 = Per Minute, 2 = Flat) (required)
            did: DID affected by the new billing plan (required)

        Returns:
            Response from setDIDBillingType operation
        """
        ...

    def setDIDInfo(
        self,
        validate: bool = True,
        *,
        billing_type: Literal["1", "2"],
        cnam: Literal["0", "1"],
        dialtime: int,
        did: int,
        pop: int,
        routing: int,
        callerid_prefix: Optional[int] = None,
        failover_busy: Optional[int] = None,
        failover_noanswer: Optional[int] = None,
        failover_unreachable: Optional[int] = None,
        note: Optional[int] = None,
        port_out_pin: Optional[int] = None,
        record_calls: Optional[Literal["0", "1"]] = None,
        transcribe: Optional[Literal["0", "1"]] = None,
        transcription_email: Optional[str] = None,
        transcription_locale: Optional[str] = None,
        transcription_start_delay: Optional[Annotated[str, "Range: 0-60; Units: seconds"]] = None,
        voicemail: Optional[int] = None,
        voicemail_threshold: Optional[Annotated[str, "Range: 0-60; Units: seconds"]] = None,
    ) -> Dict[str, Any]:
        """Update did info settings

        Args:
            validate: Whether to validate parameters with Pydantic
            billing_type: Billing type for the DID (1 = Per Minute, 2 = Flat) (required)
            callerid_prefix: Caller ID Prefix for the DID
            cnam: CNAM for the DID (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean) (required)
            dialtime: Dial Time Out for the DID (Example: 60 -> in seconds) (required)
            did: DID to be Updated (Example: 5551234567) (required)
            failover_busy: Busy Routing for the DID
            failover_noanswer: NoAnswer Routing for the DID
            failover_unreachable: Unreachable Routing for the DID
            note: Note for the DID
            pop: Point of Presence for the DID ("server_pop" values from getServersInfo. Example: 3) (required)
            port_out_pin: Port Out PIN protection is used as a means of authorizing outgoing portability (only for selected US numbers with the lock icon)
            record_calls: Record Calls (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            routing: Main Routing for the DID (required)
            transcribe: Enable Call Transcription (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            transcription_email: Call Transcription Email
            transcription_locale: Call Transcription Locale (values from getLocales)
            transcription_start_delay: Call Transcription Delay Seconds between 0 and 60, Increments of 5 (Example: 10 -> seconds)
            voicemail: Voicemail for the DID
            voicemail_threshold: Voicemail Threshold Seconds between 0 and 60, Increments of 5 (Example: 10 -> seconds)

        Returns:
            Response from setDIDInfo operation
        """
        ...

    def setDIDPOP(
        self,
        validate: bool = True,
        *,
        did: int,
        pop: int,
    ) -> Dict[str, Any]:
        """Update didpop settings

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID to be Updated (Example: 5551234567) (required)
            pop: Point of Presence for the DID ("server_pop" values from getServersInfo. Example: 3) (required)

        Returns:
            Response from setDIDPOP operation
        """
        ...

    def setDIDRouting(
        self,
        validate: bool = True,
        *,
        did: int,
        routing: int,
    ) -> Dict[str, Any]:
        """Update did routing settings

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID to be Updated (Example: 5551234567) (required)
            routing: Main Routing for the DID (required)

        Returns:
            Response from setDIDRouting operation
        """
        ...

    def setDIDVoicemail(
        self,
        validate: bool = True,
        *,
        did: int,
        voicemail: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update did voicemail settings

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID to be Updated (Example: 5551234567) (required)
            voicemail: Mailbox for the DID

        Returns:
            Response from setDIDVoicemail operation
        """
        ...

    def setDISA(
        self,
        validate: bool = True,
        *,
        digit_timeout: str,
        name: str,
        pin: str,
        callerid_override: Optional[int] = None,
        disa: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update disa settings

        Args:
            validate: Whether to validate parameters with Pydantic
            callerid_override: Caller ID Override for the DISA
            digit_timeout: Time between digits (required)
            disa: ID for a specific DISA (Example: 2114 / Leave empty to create a new one)
            name: Name for the DISA (required)
            pin: Password for the DISA (required)

        Returns:
            Response from setDISA operation
        """
        ...

    def setEmailToFax(
        self,
        validate: bool = True,
        *,
        auth_email: Annotated[str, "Format: email"],
        from_number_id: str,
        security_code: int,
        enabled: Optional[Literal["0", "1"]] = None,
        id_: Optional[int] = None,
        security_code_enabled: Optional[Literal["0", "1"]] = None,
        test: Optional[Literal["true", "false"]] = None,
    ) -> Dict[str, Any]:
        """Update email to fax settings

        Args:
            validate: Whether to validate parameters with Pydantic
            auth_email: Email address from you will sent Fax Messages (required)
            enabled: If Enable, we will send Fax Message when we receive an email from the provided address. (Values:1=Enable / 0=Disable) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            from_number_id: Fax number that will appear as fax sender. (values from getFaxNumbersInfo) (required)
            id_: [Only for updates] ID of the "Email to Fax" to edit (Values from getEmailToFax)
            security_code: An alphanumeric code to identify your emails before send as Fax. (required)
            security_code_enabled: If Enable, we will check the mail subject if this include a Security Code before send the Fax. (Values:1=Enable / 0=Disable) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            test: Set to true if testing. (accepts: true/false, yes/no, on/off, 1/0, boolean)

        Returns:
            Response from setEmailToFax operation
        """
        ...

    def setFaxFolder(
        self,
        validate: bool = True,
        *,
        name: str,
        id_: Optional[int] = None,
        test: Optional[Literal["true", "false"]] = None,
    ) -> Dict[str, Any]:
        """Update fax folder settings

        Args:
            validate: Whether to validate parameters with Pydantic
            id_: [Only for updates] ID of the Fax Folder to edit (Values from getFaxFolders)
            name: Name of the Fax Folder to create or update (Example: FAMILY) (required)
            test: Set to true if testing how to create/update a Fax Folder (accepts: true/false, yes/no, on/off, 1/0, boolean)

        Returns:
            Response from setFaxFolder operation
        """
        ...

    def setFaxNumberEmail(
        self,
        validate: bool = True,
        *,
        did: int,
        email: Optional[Annotated[str, "Format: email"]] = None,
        email_attach_file: Optional[Annotated[str, "Format: pdf"]] = None,
        email_enable: Optional[str] = None,
        test: Optional[Literal["true", "false"]] = None,
    ) -> Dict[str, Any]:
        """Update fax number email settings

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID Number to be ported into our network (Example: 5552341234) (required)
            email: Email address where send notifications when receive Fax Messages - (Example: yourname@company.com)
            email_attach_file: Flag to enable attach the Fax Message as a PDF file in the notifications. - (Values: 1 = true, 0 = false) - Default: 0
            email_enable: Flag to enable the email notifications. - (Values: 1 = true, 0 = false) - Default: 0
            test: Set to true if testing how to set the email of a Fax Number (accepts: true/false, yes/no, on/off, 1/0, boolean)

        Returns:
            Response from setFaxNumberEmail operation
        """
        ...

    def setFaxNumberInfo(
        self,
        validate: bool = True,
        *,
        did: int,
        email: Optional[Annotated[str, "Format: email"]] = None,
        email_attach_file: Optional[Annotated[str, "Format: pdf"]] = None,
        email_enable: Optional[str] = None,
        test: Optional[Literal["true", "false"]] = None,
        url_callback: Optional[str] = None,
        url_callback_enable: Optional[str] = None,
        url_callback_retry: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update fax number info settings

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID Number to be ported into our network (Example: 5552341234) (required)
            email: Email address where send notifications when receive Fax Messages - (Example: yourname@company.com)
            email_attach_file: Flag to enable attach the Fax Message as a PDF file in the notifications. - (Values: 1 = true, 0 = false) - Default: 0
            email_enable: Flag to enable the email notifications. - (Values: 1 = true, 0 = false) - Default: 0
            test: Set to true if testing how to update the information of a Fax Number (accepts: true/false, yes/no, on/off, 1/0, boolean)
            url_callback: URL where make a POST when you receive a Fax Message.
            url_callback_enable: Flag to enable the URL Callback functionality. - (Values: 1 = true, 0 = false) - Default: 0
            url_callback_retry: Flag to enable retry the POST action in case we don't receive "ok".

        Returns:
            Response from setFaxNumberInfo operation
        """
        ...

    def setFaxNumberURLCallback(
        self,
        validate: bool = True,
        *,
        did: int,
        test: Optional[Literal["true", "false"]] = None,
        url_callback: Optional[str] = None,
        url_callback_enable: Optional[str] = None,
        url_callback_retry: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update fax number url callback settings

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID Number to be ported into our network (Example: 5552341234) (required)
            test: Set to true if testing how to set the URL callback of a Fax Number (accepts: true/false, yes/no, on/off, 1/0, boolean)
            url_callback: URL where make a POST when you receive a Fax Message.
            url_callback_enable: Flag to enable the URL Callback functionality. - (Values: 1 = true, 0 = false) - Default: 0
            url_callback_retry: Flag to enable retry the POST action in case we don't receive "ok".

        Returns:
            Response from setFaxNumberURLCallback operation
        """
        ...

    def setForwarding(
        self,
        validate: bool = True,
        *,
        phone_number: Annotated[str, "Format: phone"],
        callerid_override: Optional[int] = None,
        description: Optional[str] = None,
        diversion_header: Optional[str] = None,
        dtmf_digits: Optional[str] = None,
        forwarding: Optional[int] = None,
        pause: Optional[Annotated[str, "Units: seconds"]] = None,
    ) -> Dict[str, Any]:
        """Update forwarding settings

        Args:
            validate: Whether to validate parameters with Pydantic
            callerid_override: Caller ID Override for the Forwarding
            description: Description for the Forwarding
            diversion_header: If enabled, we will add a Diversion Header to your forwarded call
            dtmf_digits: Send DTMF digits when call is answered
            forwarding: ID for a specific Forwarding (Example: 19183 / Leave empty to create a new one)
            pause: Pause (seconds) when call is answered before sending digits (Example: 1.5 / Values: 0 to 10 in increments of 0.5)
            phone_number: Phone Number for the Forwarding (required)

        Returns:
            Response from setForwarding operation
        """
        ...

    def setIVR(
        self,
        validate: bool = True,
        *,
        choices: str,
        language: str,
        name: str,
        recording: str,
        timeout: str,
        voicemailsetup: str,
        ivr: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update ivr settings

        Args:
            validate: Whether to validate parameters with Pydantic
            choices: Choices for the IVR (Example: '1=sip:5096 ; 2=fwd:20222') (required)
            ivr: ID for a specific IVR (Example: 4636 / Leave empty to create a new one)
            language: Language for the IVR (values from getLanguages) (required)
            name: Name for the IVR (required)
            recording: Recording for the IVR (values from getRecordings) (required)
            timeout: Maximum time for type in a choice after recording (required)
            voicemailsetup: Voicemail Setup for the IVR (values from getVoicemailSetups) (required)

        Returns:
            Response from setIVR operation
        """
        ...

    def setMusicOnHold(
        self,
        validate: bool = True,
        *,
        description: str,
        recordings: Literal["1234", "1235", "1236"],
        name: Optional[str] = None,
        sort: Optional[str] = None,
        volume: Optional[Literal["0", "1"]] = None,
    ) -> Dict[str, Any]:
        """Update music on hold settings

        Args:
            validate: Whether to validate parameters with Pydantic
            description: Music on Hold Description (required)
            name: Music on Hold Name (Values from getMusicOnHold)
            recordings: Selected recordings separated by commas (Values from getRecordings, example: (1234,1235,1236) (required)
            sort: Selected recordings sort mode (Example: "alpha", "random")
            volume: Music on Hold Quiet Volume (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)

        Returns:
            Response from setMusicOnHold operation
        """
        ...

    def setPhonebook(
        self,
        validate: bool = True,
        *,
        name: Annotated[str, "Format: phone"],
        number: str,
        callerid: Optional[int] = None,
        group: Optional[int] = None,
        note: Optional[Annotated[str, "Format: phone"]] = None,
        phonebook: Optional[int] = None,
        speed_dial: Optional[Annotated[str, "Format: phone"]] = None,
    ) -> Dict[str, Any]:
        """Update phonebook settings

        Args:
            validate: Whether to validate parameters with Pydantic
            callerid: Caller ID Override when dialing via Speed Dial
            group: ID for a specific Phonebook group
            name: Name for the Phonebook Entry (required)
            note: Note for the phonebook entry
            number: Number or SIP for the Phonebook entry (Example: 'sip:2563' or '5552223333') (required)
            phonebook: ID for a specific Phonebook entry (Example: 32207 / Leave empty to create a new one)
            speed_dial: Speed Dial for the Phonebook entry

        Returns:
            Response from setPhonebook operation
        """
        ...

    def setPhonebookGroup(
        self,
        validate: bool = True,
        *,
        name: Annotated[str, "Format: phone"],
        phonebook: str,
        group: Optional[int] = None,
        members: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update phonebook group settings

        Args:
            validate: Whether to validate parameters with Pydantic
            group: ID for a specific Phonebook group (Example: 32207 / Leave empty to create a new one)
            members: Phonebook entry codes associated to this group separated by a semicolon
            name: Name for the Phonebook group (required)
            phonebook:  (required)

        Returns:
            Response from setPhonebookGroup operation
        """
        ...

    def setQueue(
        self,
        validate: bool = True,
        *,
        join_when_empty: str,
        leave_when_empty: str,
        priority_weight: str,
        queue_language: int,
        queue_name: str,
        queue_number: str,
        report_hold_time_agent: int,
        ring_inuse: int,
        ring_strategy: str,
        agent_announcement: Optional[int] = None,
        agent_ring_timeout: Optional[int] = None,
        announce_position_frecuency: Optional[Annotated[str, "Units: seconds"]] = None,
        announce_round_seconds: Optional[Annotated[str, "Units: seconds"]] = None,
        callerid_prefix: Optional[int] = None,
        fail_over_routing_full: Optional[str] = None,
        fail_over_routing_join_empty: Optional[str] = None,
        fail_over_routing_join_unavail: Optional[str] = None,
        fail_over_routing_leave_empty: Optional[str] = None,
        fail_over_routing_leave_unavail: Optional[str] = None,
        fail_over_routing_timeout: Optional[str] = None,
        frequency_announcement: Optional[Annotated[str, "Units: seconds"]] = None,
        if_announce_position_enabled_report_estimated_hold_time: Optional[str] = None,
        join_announcement: Optional[int] = None,
        maximum_callers: Optional[str] = None,
        maximum_wait_time: Optional[Annotated[str, "Units: seconds"]] = None,
        member_delay: Optional[Annotated[str, "Units: seconds"]] = None,
        music_on_hold: Optional[int] = None,
        queue: Optional[int] = None,
        queue_password: Optional[str] = None,
        retry_timer: Optional[Annotated[str, "Units: seconds"]] = None,
        thankyou_for_your_patience: Optional[str] = None,
        voice_announcement: Optional[int] = None,
        wrapup_time: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update queue settings

        Args:
            validate: Whether to validate parameters with Pydantic
            agent_announcement: Recording Code (Values from getRecordings or 'none')
            agent_ring_timeout: Number of seconds to ring an agent (Values 5 to 60)
            announce_position_frecuency: How often to make any periodic announcement (Values in seconds: multiples of 15, max value: 1200 or 'none' = No announcement)
            announce_round_seconds: Announce seconds (Values in seconds: 1 to 60  or 'none' = Do not announce)
            callerid_prefix: Caller ID Prefix for queue
            fail_over_routing_full: Failover routing to Maximum callers reached
            fail_over_routing_join_empty: A call was sent to the queue but the queue had no members (Only works when Join when Empty is set to no)
            fail_over_routing_join_unavail: Same as routingjoinempty, except that there were still queue members, but all were status unavailable
            fail_over_routing_leave_empty: The last agent was removed form the queue before alls calls were handled (Only works when Leave when Empty is set to yes)
            fail_over_routing_leave_unavail: Same as routingleaveempty, except that there were still queue members, but all were status unavailable
            fail_over_routing_timeout: Failover routing to Maximum wait time reached
            frequency_announcement: Periodic interval to play voice announce recording (Values in seconds: multiples of 15, max value: 1200 or 'none' = No announcement)
            if_announce_position_enabled_report_estimated_hold_time:  Include estimated hold time in position announcements (Values 'yes'/'no'/'once')
            join_announcement: Recording Code (Values from getRecordings or 'none')
            join_when_empty: How caller join to the queue (Values from getJoinWhenEmptyTypes) Examples: yes     Callers can join a queue with no members or only unavailable members no      Callers cannot join a queue with no members strict  Callers cannot join a queue with no members or only unavailable members (required)
            leave_when_empty: How caller leave the queue (Values 'yes'/'no'/'strict') Examples: yes     Callers are sent to failover when there are no members no      Callers will remain in the queue even if there are no members strict  Callers are sent to failover if there are members but none of them is available. (required)
            maximum_callers: Maximum callers (Values: 1 to 60 or 'unlimited')
            maximum_wait_time: Ammount of time a caller can wait in queue (Values in seconds: multiples of 30, max value: 1200 or 'unlimited')
            member_delay: Member delay when the agent is connected to the caller (Values 1 to 15 in seconds or 'none')
            music_on_hold: Music on Hold Code (Values from getMusicOnHold)
            priority_weight: weight/priority of queue (Values 1 to 60) (required)
            queue: ID for a specific Queue entry (Example: 32208 / Leave empty to create a new one)
            queue_language: Language Code (Values from getLanguages) (required)
            queue_name: Queue entry name (required)
            queue_number: Queue entry number (required)
            queue_password: Queue Password
            report_hold_time_agent: Report hold time to agent (Values from getReportEstimatedHoldTime) (required)
            retry_timer: How long do we wait before trying all the members again (Values 5 to 60 seconds or 'none'= No Delay)
            ring_inuse: If you want the queue to avoid sending calls to members (Values 'yes'/'no') (required)
            ring_strategy: Ring strategy (Values from getRingStrategies) (required)
            thankyou_for_your_patience: Yes to say "Thank you for your patience" immediatly after announcing Queue Position and Estimated hold time left (Values 'yes'/'no')
            voice_announcement: Code for Recording (Values from getRecordings or 'none')
            wrapup_time: After a successful call, the number of seconds to wait before sending a free agent another call (Values 1 to 60 seconds or 'none'= No Delay)

        Returns:
            Response from setQueue operation

        Note:
            None values for certain parameters convert to 'none' or 'unlimited'
            Boolean parameters use 'yes'/'no' strings
        """
        ...

    def setRecording(
        self,
        validate: bool = True,
        *,
        file: int,
        name: str,
        recording: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update recording settings

        Args:
            validate: Whether to validate parameters with Pydantic
            file: Base64 encoded file (Provide Recording ID and file if you want update the file only) (required)
            name: Name for the Recording Entry (Example: 'recording1') (Provide Recording ID and name if you want update the name only) (Provide Recording ID, file and name if you want update both parameters at the same time) (required)
            recording: ID for a specific Phonebook entry (Example: 33221 / Leave empty to create a new one)

        Returns:
            Response from setRecording operation
        """
        ...

    def setRingGroup(
        self,
        validate: bool = True,
        *,
        members: int,
        name: str,
        voicemail: str,
        caller_announcement: Optional[int] = None,
        language: Optional[int] = None,
        music_on_hold: Optional[int] = None,
        ring_group: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update ring group settings

        Args:
            validate: Whether to validate parameters with Pydantic
            caller_announcement: Recording Code (Values from getRecordings)
            language: Code for Language (Values from getLanguages) "members" can receive the following routing headers: account     Used to route the call to an Account or a Sub Account fwd         Used to route the call to a Forwarding entry sip         Used to route the call to a SIP URI Each member can a specific ring time and press1 values, you can add those to the routing header as follow: Example: 'account:100001,25,0;fwd:16006,10,1' 25 = Default ring time value (Values from 1 to 60 sec) 0  = Default press1 value (Values allowed 0 and 1)
            members: Members for the Ring Group (Example: 'account:100001;fwd:16006') (required)
            music_on_hold: Music on Hold Code (Values from getMusicOnHold)
            name: Name for the Ring Group (required)
            ring_group: ID for a specific Ring Group (Example: 4768 / Leave empty to create a new one)
            voicemail: Voicemail for the Ring Group (Values from getVoicemails) (required)

        Returns:
            Response from setRingGroup operation
        """
        ...

    def setSIPURI(
        self,
        validate: bool = True,
        *,
        uri: Annotated[str, "Format: email; Units: milliseconds"],
        callerid_e164: Optional[int] = None,
        callerid_override: Optional[int] = None,
        description: Optional[str] = None,
        sipuri: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update sipuri settings

        Args:
            validate: Whether to validate parameters with Pydantic
            callerid_e164: If this option is Enabled, then your CallerID will be E164 compliant.
            callerid_override: This setting is optional.  You can  configure a 'CallerID Number Override'. Your default CallerID number will be changed to the override you have configured here when using this SIP URI.
            description: Description for the SIP URI
            sipuri: ID for a specific SIP URI (Example: 6199 / Leave empty to create a new one)
            uri: SIP URI (Example: '5552223333@sip.voip.ms') (required)

        Returns:
            Response from setSIPURI operation
        """
        ...

    def setSMS(
        self,
        validate: bool = True,
        *,
        did: int,
        enable: Literal["0", "1"],
        email_address: Optional[int] = None,
        email_enabled: Optional[int] = None,
        sms_forward: Optional[int] = None,
        sms_forward_enable: Optional[int] = None,
        sms_sipaccount: Optional[int] = None,
        sms_sipaccount_enabled: Optional[int] = None,
        url_callback: Optional[int] = None,
        url_callback_enable: Optional[int] = None,
        url_callback_retry: Optional[Annotated[str, "Units: minutes"]] = None,
    ) -> Dict[str, Any]:
        """Update sms settings

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID to be Updated (Example: 5551234567) (required)
            email_address: SMS Messages received by your DID will be sent to the email address provided
            email_enabled: If Enable, SMS Messages received by your DID will be sent to the email address provided (Values:1=Enable / 0=Disable)
            enable: Enable/Disable the DID to receive SMS Messages (Values:1=Enable / 0=Disable) (accepts: true/false, yes/no, on/off, 0/1, boolean) (required)
            sms_forward: SMS Messages received by your DID will be forwarded to the phone number provided (Example: 5551234567)
            sms_forward_enable: If Enable, SMS Messages received by your DID will be forwarded to the phone number provided (Values:1=Enable / 0=Disable)
            sms_sipaccount: SIP account or sub-account that will receive the SMS Messages
            sms_sipaccount_enabled: If Enable, SMS Messages received by your DID will be sent to the specified SIP account or sub-account (Values:1=Enable / 0=Disable)
            url_callback: SMS Messages received by your DID will be send a GET request to the URL callback provided Available Variables for your URL {FROM}    The phone number that sent you the message. {TO}      The DID number that received the message. {MESSAGE} The content of the message. Example: http://mysite.com/sms.php?to={TO}&from={FROM}&message={MESSAGE}
            url_callback_enable: If Enable, SMS Messages received by your DID will be send a GET request to the URL callback provided (Values:1=Enable / 0=Disable)
            url_callback_retry: Enable URL callback Retry (Values:1=Enable / 0=Disable) we will be expecting an 'ok' output (without quotes) from your URL callback page as an indicator that you have received the message correctly. If we don\'t receive the 'ok' letters (wihtout quotes) from your callback page, we will keep sending you the same message every 30 minutes.

        Returns:
            Response from setSMS operation
        """
        ...

    def setStaticMember(
        self,
        validate: bool = True,
        *,
        member_name: str,
        priority: str,
        queue: int,
        account: Optional[str] = None,
        member: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update static member settings

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Static Member Routing to receive calls - You can get all sub accounts using the getSubAccounts function
            member: ID for a specific Member (Example: 619 / Leave empty to create a new one)
            member_name: Member Description (required)
            priority: Values for get calls first (Example: 0) (required)
            queue: ID for a specific Queue (required)

        Returns:
            Response from setStaticMember operation
        """
        ...

    def setSubAccount(
        self,
        validate: bool = True,
        *,
        allowed_codecs: int,
        auth_type: int,
        device_type: int,
        dtmf_mode: int,
        id_: int,
        international_route: int,
        lock_international: int,
        music_on_hold: int,
        nat: int,
        transcribe: int,
        transcription_email: str,
        transcription_locale: str,
        callerid_number: Optional[int] = None,
        canada_routing: Optional[int] = None,
        default_e911: Optional[int] = None,
        description: Optional[int] = None,
        dialing_mode: Optional[Literal["0", "1", "2"]] = None,
        enable_ip_restriction: Optional[Literal["0", "1"]] = None,
        enable_pop_restriction: Optional[Literal["0", "1"]] = None,
        internal_dialtime: Optional[int] = None,
        internal_extension: Optional[int] = None,
        internal_voicemail: Optional[int] = None,
        ip: Optional[int] = None,
        ip_restriction: Optional[str] = None,
        language: Optional[int] = None,
        max_expiry: Optional[Annotated[str, "Range: 60-3600"]] = None,
        password: Optional[int] = None,
        pop_restriction: Optional[str] = None,
        record_calls: Optional[Literal["0", "1"]] = None,
        reseller_chargesetup: Optional[str] = None,
        reseller_client: Optional[int] = None,
        reseller_nextbilling: Optional[str] = None,
        reseller_package: Optional[str] = None,
        rtp_hold_timeout: Optional[Annotated[str, "Range: 1-3600"]] = None,
        rtp_timeout: Optional[Annotated[str, "Range: 1-3600"]] = None,
        send_bye: Optional[Literal["0", "1"]] = None,
        sip_traffic: Optional[Literal["0", "1"]] = None,
        tfcarrier: Optional[Literal["-1", "0", "1", "2"]] = None,
        transcription_start_delay: Optional[Annotated[str, "Range: 0-60; Units: seconds"]] = None,
    ) -> Dict[str, Any]:
        """Update sub account settings

        Args:
            validate: Whether to validate parameters with Pydantic
            allowed_codecs: List of Allowed Codecs (Values from getAllowedCodecs) Codecs separated by semicolon (Example: ulaw;g729;gsm) (required)
            auth_type: Authorization Type Code (Values from getAuthTypes) (required)
            callerid_number: Caller ID Override
            canada_routing: Route Code (Values from getRoutes)
            default_e911: e911 Default CallerID
            description: Sub Account Description (Example: 'VoIP Account')
            device_type: Device Type Code (Values from getDeviceTypes) (required)
            dialing_mode: Allows you to dial outgoing calls using either the NANPA configuration or the E164 configuration. (Values: 0 = Use Main Account Setting, 1 = E164, 2 = NANPA)
            dtmf_mode: DTMF Mode Code (Values from getDTMFModes) (required)
            enable_ip_restriction: Enable IP Restriction (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            enable_pop_restriction: Enable POP Restriction (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            id_: Sub Account ID (Example: 10236) (required)
            internal_dialtime: Sub Account Internal Dialtime (Example: 60 -> seconds)
            internal_extension: Sub Account Internal Extension (Example: 1 -> Creates 101)
            internal_voicemail: Sub Account Internal Voicemail (Example: 101)
            international_route: Route Code (Values from getRoutes) (required)
            ip: Sub Account IP (For IP Authentication)
            ip_restriction: List of IP/Netmask to allow outgoing calls separated by commas (Example: 123.45.3.21,10.255.12.0/22,device.mydomain.com)
            language: Language for system messages, such as "Invalid Option" (Values from getLanguages)
            lock_international: Lock International Code (Values from getLockInternational) (required)
            max_expiry: Max Expiry between 60 and 3600 (Example: 3000)
            music_on_hold: Music on Hold Code (Values from getMusicOnHold) (required)
            nat: NAT Mode Code (Values from getNAT) (required)
            password: Sub Account Password (For Password Authentication)
            pop_restriction: List of POP Servers to allow outgoing calls separated by commas (values from getServersInfo. Example: 10,23,45)
            record_calls: Record Calls (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            reseller_chargesetup: True if you want to charge Package Setup Fee after Save
            reseller_client: Reseller Account ID (Example: 561115)
            reseller_nextbilling: Reseller Next Billing Date (Example: '2012-12-31')
            reseller_package: Reseller Package (Example: 92364)
            rtp_hold_timeout: RTP Hold Time Out between 1 and 3600 (Example: 600)
            rtp_timeout: RTP Time Out between 1 and 3600 (Example: 60)
            send_bye: Send BYE on successful transfer (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            sip_traffic: Encrypted SIP Traffic (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            tfcarrier: This allows you to select the carrier to be used for outgoing calls to toll-free numbers. (Values: -1 = Use main account settings, 0 = Default server setting, 1 = US carrier, 2 = Canadian carrier)
            transcribe:  (required)
            transcription_email:  (required)
            transcription_locale:  (required)
            transcription_start_delay: Call Transcription Delay Seconds between 0 and 60, Increments of 5 (Example: 10 -> seconds)

        Returns:
            Response from setSubAccount operation
        """
        ...

    def setTimeCondition(
        self,
        validate: bool = True,
        *,
        endhour: Annotated[str, "Units: hours"],
        endminute: Annotated[str, "Units: minutes"],
        name: str,
        routing_match: str,
        routing_nomatch: str,
        starthour: Annotated[str, "Units: hours"],
        startminute: Annotated[str, "Units: minutes"],
        weekdayend: Annotated[str, "Units: days"],
        weekdaystart: Annotated[str, "Units: days"],
        timecondition: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update time condition settings

        Args:
            validate: Whether to validate parameters with Pydantic
            endhour: All the End Hour Conditions (Example: '16;12') (required)
            endminute: All the End Minute Conditions (Example: '0;0') (required)
            name: Name for the Time Condition (required)
            routing_match: Routing for the Call when condition matches (required)
            routing_nomatch: Routing for the Call when condition does not matche (required)
            starthour: All the Start Hour Conditions (Example: '8;8') (required)
            startminute: All the Start Minute Conditions (Example: '0;0') (required)
            timecondition: ID for a specific Time Condition (Example: 1830 / Leave empty to create a new one)
            weekdayend: All the Week Day End Conditions (Example: 'fri;sat') (required)
            weekdaystart: All the Week Day Start Conditions (Example: 'mon;sat') (required)

        Returns:
            Response from setTimeCondition operation
        """
        ...

    def setVoicemail(
        self,
        validate: bool = True,
        *,
        attach_message: Annotated[str, "Format: wav"],
        delete_message: str,
        language: int,
        mailbox: int,
        name: str,
        password: str,
        play_instructions: int,
        say_callerid: int,
        say_time: str,
        skip_password: Literal["0", "1"],
        timezone: str,
        email: Optional[Annotated[str, "Format: email"]] = None,
        email_attachment_format: Optional[int] = None,
        transcription: Optional[str] = None,
        transcription_locale: Optional[int] = None,
        unavailable_message_recording: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update voicemail settings

        Args:
            validate: Whether to validate parameters with Pydantic
            attach_message: Yes for Attaching WAV files to Message (Values: 'yes'/'no') (required)
            delete_message: Yes for Deleting Messages (Values: 'yes'/'no') (required)
            email: Email address for receiving messages, multiple email addresses are allowed if separated by a comma
            email_attachment_format: Code for Email Attachment format (Values from getVoicemailAttachmentFormats)
            language: Code for Language (Values from getLanguages) (required)
            mailbox: ID for a specific Mailbox (Example: 1001) (required)
            name: Name for the Mailbox (required)
            password: Password for the Mailbox (required)
            play_instructions: Code for Play Instructions Setting (Values from getPlayInstructions) (required)
            say_callerid: Yes for Saying the Caller ID (Values: 'yes'/'no') (required)
            say_time: Yes for Saying Time Stamp (Values: 'yes'/'no') (required)
            skip_password: True if Skipping Password (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean) (required)
            timezone: Time Zone for Mailbox (Values from getTimeZones) (required)
            transcription: Voicemail Transcription
            transcription_locale: Transcription locale code (values from getLocales)
            unavailable_message_recording: Recording for the Unavailable Message (values from getRecordings)

        Returns:
            Response from setVoicemail operation

        Note:
            Boolean parameters like attach_message use 'yes'/'no' strings
            skip_password uses '1'/'0' string
        """
        ...

    def signupClient(
        self,
        validate: bool = True,
        *,
        address: str,
        city: str,
        confirm_email: str,
        confirm_password: str,
        country: int,
        email: str,
        firstname: str,
        lastname: str,
        password: str,
        phone_number: Annotated[str, "Format: phone"],
        state: str,
        zip: int,
        activate: Optional[Literal["0", "1"]] = None,
        balance_management: Optional[str] = None,
        company: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Sign up client

        Args:
            validate: Whether to validate parameters with Pydantic
            activate: Activates Client (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            address: Client's Address (required)
            balance_management: Balance Management for Client (Values from getBalanceManagement)
            city: Client's City (required)
            company: Client's Company
            confirm_email: Client's Confirmation e-mail (required)
            confirm_password: Client's Confirmation Password (required)
            country: Client's Country (Values from getCountries) (required)
            email: Client's e-mail (required)
            firstname: Client's Firstname (required)
            lastname: Client's Lastname (required)
            password: Client's Password (required)
            phone_number: Client's Phone Number (required)
            state: Client's State (required)
            zip: Client's Zip Code (required)

        Returns:
            Response from signupClient operation
        """
        ...

    def unconnectDID(
        self,
        validate: bool = True,
        *,
        did: int,
    ) -> Dict[str, Any]:
        """Unconnect did

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID to be Unconnected from Reseller Sub Account(Example: 5551234567) (required)

        Returns:
            Response from unconnectDID operation
        """
        ...

    def unconnectFAX(
        self,
        validate: bool = True,
        *,
        did: int,
    ) -> Dict[str, Any]:
        """Unconnect fax

        Args:
            validate: Whether to validate parameters with Pydantic
            did: FAX DID to be Unconnected from Reseller Sub Account (Example: 5551234567) (required)

        Returns:
            Response from unconnectFAX operation
        """
        ...


class VoIPMSClientAsync(VoIPMSClient):
    """Asynchronous data-driven VoIP.ms client."""
    
    async def __aenter__(self) -> "VoIPMSClientAsync": ...
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...
    async def close(self) -> None: ...

    # Async API Methods

    async def addCharge(
        self,
        validate: bool = True,
        *,
        charge: str,
        client: int,
        description: Optional[str] = None,
        test: Optional[Literal["true", "false"]] = None,
    ) -> Dict[str, Any]:
        """Add new charge

        Args:
            validate: Whether to validate parameters with Pydantic
            charge: Amount of money that will be Debited from the customer (Example: 4.99) (required)
            client: ID for a specific Reseller Client (Example: 561115) (required)
            description: Charge Description
            test: Set to true if testing how adding charges works (accepts: true/false, yes/no, on/off, 1/0, boolean)

        Returns:
            Response from addCharge operation
        """
        ...

    async def addLNPFile(
        self,
        validate: bool = True,
        *,
        file: int,
        portid: int,
    ) -> Dict[str, Any]:
        """Add new lnp file

        Args:
            validate: Whether to validate parameters with Pydantic
            file: Base 64 code of the file to be attached (required)
            portid: ID of the port previously created. (required)

        Returns:
            Response from addLNPFile operation
        """
        ...

    async def addLNPPort(
        self,
        validate: bool = True,
        *,
        address1: str,
        city: str,
        country: int,
        firstName: str,
        lastName: str,
        numbers: int,
        portType: str,
        providerAccount: int,
        providerName: int,
        state: str,
        statementName: str,
        zip: int,
        address2: Optional[str] = None,
        btn: Optional[Annotated[str, "Format: phone"]] = None,
        isMobile: Optional[Literal["1", "0"]] = None,
        isPartial: Optional[int] = None,
        locationType: Optional[Literal["1", "0"]] = None,
        notes: Optional[int] = None,
        pin: Optional[str] = None,
        services: Optional[str] = None,
        tfType: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Add new lnp port

        Args:
            validate: Whether to validate parameters with Pydantic
            address1: This is the "Customer Address" as it appears on the CSR (Customer Service Record) of the losing carrier. (required)
            address2: Optional Address information (e.g: Suite 343)
            btn: [Required If isMobile = 1] BTN: It is the phone number to which all the other numbers of the customer are charged, in a consolidated telephone bill (instead of showing separate charges for each number you own). Please try to find the BTN on your invoice, and if you are unable to do so please contact the current provider to obtain it.
            city: This is the "City" as it appears on the CSR (Customer Service Record) of the losing carrier. (required)
            country: This is the "Country" as it appears on the CSR (Customer Service Record) of the losing carrier. (required)
            firstName: This is the "Customer First Name" as it appears on  the CSR (Customer Service Record) of the losing carrier. Please Enter the first name of the owner of the number or the autorized contact. No company name must be entered in the field. (required)
            isMobile: - (Values: 1 = All the numbers are mobile numbers, 0 = false) - Default: 0 (accepts: true/false, yes/no, on/off, 0/1, boolean)
            isPartial: If you have more then 1 number with your current carrier and not porting them all, choose yes. If you are porting all the numbers, choose no. Please note that you still need to include all numbers you want to port. If you have 2 numbers and want to port both, you need to include both numbers in the list of numbers to port. - (Values: 1 = true, 0 = false) - Default: 0
            lastName: This is the "Customer Last Name" as it appears on  the CSR (Customer Service Record) of the losing carrier. Please Enter the last name of the owner of the number or the autorized contact. No company name must be entered in the field (required)
            locationType: - (Values: 1 = Business, 0 = Residential) - Default: 0 (accepts: true/false, yes/no, on/off, 0/1, boolean)
            notes: - If you would like to include additional information regarding this port, you can use this parameter.
            numbers: DID(s) to port into VoIP.ms network (Example: 5552341234,5552341233). If you are porting more than one number, please separate them with commas. (required)
            pin: PIN Number
            portType: Digits from 1 to 4: 1: United States Local numbers 2: Canadian Local Numbers 3: US/CA Toll Free Numbers 4: United States Fax numbers 5: Canadian Fax Numbers (required)
            providerAccount: Your Account with your current service provider. (required)
            providerName: The name of your current service provider. (required)
            services: [Required If isMobile = 1] Please be specific and describe ALL remaining services with the current carrier. This includes DSL/Data services, Hunt Group services, etc. Any services NOT listed below may be disconnected upon completion of this port order.
            state: This is the "State or Province" as it appears on the CSR (Customer Service Record) of the losing carrier. (required)
            statementName: This is for Business numbers only. Please type your Company Name if applicable, otherwise leave it blank. (required)
            tfType: [Required If portType = 3] Values: 1 - American Carrier, American Callers Only, 2 - American Carrier, American and Canadian Callers allowed, 3 - Canadian Carrier
            zip: This is the "ZIP or Postal Code" as it appears on the CSR (Customer Service Record) of the losing carrier. (required)

        Returns:
            Response from addLNPPort operation
        """
        ...

    async def addMemberToConference(
        self,
        validate: bool = True,
        *,
        conference: int,
        member: int,
    ) -> Dict[str, Any]:
        """Add new member to conference

        Args:
            validate: Whether to validate parameters with Pydantic
            conference: Specific Conference ID (Example: 234) (required)
            member: Specific Member ID (Example: 6547) (required)

        Returns:
            Response from addMemberToConference operation
        """
        ...

    async def addPayment(
        self,
        validate: bool = True,
        *,
        client: int,
        payment: str,
        description: Optional[str] = None,
        test: Optional[Literal["true", "false"]] = None,
    ) -> Dict[str, Any]:
        """Add new payment

        Args:
            validate: Whether to validate parameters with Pydantic
            client: ID for a specific Reseller Client (Example: 561115) (required)
            description: Payment Description
            payment: Amount of money that will be Credited to the customer (Example: 4.99) (required)
            test: Set to true if testing how adding payments works (accepts: true/false, yes/no, on/off, 1/0, boolean)

        Returns:
            Response from addPayment operation
        """
        ...

    async def assignDIDvPRI(
        self,
        validate: bool = True,
        *,
        did: int,
        vpri: int,
    ) -> Dict[str, Any]:
        """Assign di dv pri

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID Number to be assign into our Vpri (Example: 561115) (required)
            vpri: Id for specific Vpri (required)

        Returns:
            Response from assignDIDvPRI operation
        """
        ...

    async def backOrderDIDCAN(
        self,
        validate: bool = True,
        *,
        billing_type: Literal["1", "2"],
        cnam: Literal["0", "1"],
        dialtime: int,
        pop: int,
        province: str,
        quantity: int,
        ratecenter: str,
        routing: int,
        callerid_prefix: Optional[int] = None,
        failover_busy: Optional[int] = None,
        failover_noanswer: Optional[int] = None,
        failover_unreachable: Optional[int] = None,
        note: Optional[int] = None,
        test: Optional[Literal["true", "false"]] = None,
        voicemail: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Backorder didcan

        Args:
            validate: Whether to validate parameters with Pydantic
            billing_type: Billing type for the DID (1 = Per Minute, 2 = Flat) (required)
            callerid_prefix: Caller ID Prefix for the DID
            cnam: CNAM for the DID (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean) (required)
            dialtime: Dial Time Out for the DID (Example: 60 -> in seconds) (required)
            failover_busy: Busy Routing for the DID
            failover_noanswer: NoAnswer Routing for the DID
            failover_unreachable: Unreachable Routing for the DID
            note: Note for the DID
            pop: Point of Presence for the DID (Example: 5) (required)
            province: Canadian Province (values from getProvinces) (required)
            quantity: Number of DIDs to be Ordered (Example: 3) (required)
            ratecenter: USA Ratecenter (Values from getRateCentersUSA) (required)
            routing: Main Routing for the DID (required)
            test: Set to true if testing how Orders work - Orders can not be undone - When testing, no Orders are made (accepts: true/false, yes/no, on/off, 1/0, boolean)
            voicemail: Voicemail for the DID (Example: 101)

        Returns:
            Response from backOrderDIDCAN operation

        Note:
            CNAM parameter is converted to '1'/'0' string
        """
        ...

    async def backOrderDIDUSA(
        self,
        validate: bool = True,
        *,
        billing_type: Literal["1", "2"],
        cnam: Literal["0", "1"],
        dialtime: int,
        pop: int,
        quantity: int,
        ratecenter: str,
        routing: int,
        state: str,
        callerid_prefix: Optional[int] = None,
        failover_busy: Optional[int] = None,
        failover_noanswer: Optional[int] = None,
        failover_unreachable: Optional[int] = None,
        note: Optional[int] = None,
        test: Optional[Literal["true", "false"]] = None,
        voicemail: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Backorder didusa

        Args:
            validate: Whether to validate parameters with Pydantic
            billing_type: Billing type for the DID (1 = Per Minute, 2 = Flat) (required)
            callerid_prefix: Caller ID Prefix for the DID
            cnam: CNAM for the DID (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean) (required)
            dialtime: Dial Time Out for the DID (Example: 60 -> in seconds) (required)
            failover_busy: Busy Routing for the DID
            failover_noanswer: NoAnswer Routing for the DID
            failover_unreachable: Unreachable Routing for the DID
            note: Note for the DID
            pop: Point of Presence for the DID (Example: 5) (required)
            quantity: Number of DIDs to be Ordered (Example: 3) (required)
            ratecenter: USA Ratecenter (Values from getRateCentersUSA) (required)
            routing: Main Routing for the DID (required)
            state: USA State (values from getStates) (required)
            test: Set to true if testing how Orders work - Orders can not be undone - When testing, no Orders are made (accepts: true/false, yes/no, on/off, 1/0, boolean)
            voicemail: Voicemail for the DID (Example: 101)

        Returns:
            Response from backOrderDIDUSA operation

        Note:
            CNAM parameter is converted to '1'/'0' string
        """
        ...

    async def cancelDID(
        self,
        validate: bool = True,
        *,
        did: int,
        cancelcomment: Optional[int] = None,
        portout: Optional[Literal["true", "false"]] = None,
        test: Optional[Literal["true", "false"]] = None,
    ) -> Dict[str, Any]:
        """Cancel did

        Args:
            validate: Whether to validate parameters with Pydantic
            cancelcomment: Comment for DID cancellation
            did: DID to be canceled and deleted (Example: 5551234567) (required)
            portout: Set to true if the DID is being ported out (accepts: true/false, yes/no, on/off, 1/0, boolean)
            test: Set to true if testing how cancellation works - Cancellation can not be undone - When testing, no changes are made (accepts: true/false, yes/no, on/off, 1/0, boolean)

        Returns:
            Response from cancelDID operation
        """
        ...

    async def cancelFaxNumber(
        self,
        validate: bool = True,
        *,
        id_: int,
        test: Optional[Literal["true", "false"]] = None,
    ) -> Dict[str, Any]:
        """Cancel fax number

        Args:
            validate: Whether to validate parameters with Pydantic
            id_: ID for a specific Fax Number (Example: 923) (required)
            test: Set to true if testing how cancel a Fax Number (accepts: true/false, yes/no, on/off, 1/0, boolean)

        Returns:
            Response from cancelFaxNumber operation
        """
        ...

    async def connectDID(
        self,
        validate: bool = True,
        *,
        account: int,
        did: int,
        minute: Annotated[str, "Units: minutes"],
        monthly: str,
        setup: str,
        dont_charge_monthly: Optional[str] = None,
        dont_charge_setup: Optional[str] = None,
        next_billing: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Connect did

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Reseller Sub Account (Example: '100001_VoIP') (required)
            did: DID to be Connected to Reseler Sub Account (Example: 5551234567) (required)
            dont_charge_monthly: If set to true, the monthly value will not be charged after Connect
            dont_charge_setup: If set to true, the setup value will not be charged after Connect
            minute: Minute Rate for Reseller Client (Example: 0.03) (required)
            monthly: Montly Fee for Reseller Client (Example: 3.50) (required)
            next_billing: Next billing date (Example: '2014-03-30')
            setup: Setup Fee for Reseller Client (Example: 1.99) (required)

        Returns:
            Response from connectDID operation
        """
        ...

    async def connectFAX(
        self,
        validate: bool = True,
        *,
        account: int,
        did: int,
        minute: Annotated[str, "Units: minutes"],
        monthly: str,
        setup: str,
        dont_charge_monthly: Optional[str] = None,
        dont_charge_setup: Optional[str] = None,
        next_billing: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Connect fax

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Reseller Sub Account (Example: '100001_VoIP') (required)
            did: FAX DID to be Connected to Reseller Sub Account (Example: 5551234567) (required)
            dont_charge_monthly: If set to true, the monthly value will not be charged after Connect
            dont_charge_setup: If set to true, the setup value will not be charged after Connect
            minute: Minute Rate for Reseller Client (Example: 0.03) (required)
            monthly: Montly Fee for Reseller Client (Example: 3.50) (required)
            next_billing: Next billing date (Example: '2014-03-30')
            setup: Setup Fee for Reseller Client (Example: 1.99) (required)

        Returns:
            Response from connectFAX operation
        """
        ...

    async def createSubAccount(
        self,
        validate: bool = True,
        *,
        allowed_codecs: int,
        auth_type: int,
        device_type: int,
        dtmf_mode: int,
        international_route: int,
        lock_international: int,
        music_on_hold: int,
        nat: int,
        protocol: int,
        username: int,
        callerid_number: Optional[int] = None,
        canada_routing: Optional[int] = None,
        description: Optional[int] = None,
        dialing_mode: Optional[Literal["0", "1", "2"]] = None,
        enable_internal_cnam: Optional[int] = None,
        enable_ip_restriction: Optional[Literal["0", "1"]] = None,
        enable_pop_restriction: Optional[Literal["0", "1"]] = None,
        internal_cnam: Optional[int] = None,
        internal_dialtime: Optional[int] = None,
        internal_extension: Optional[int] = None,
        internal_voicemail: Optional[int] = None,
        ip: Optional[int] = None,
        ip_restriction: Optional[str] = None,
        language: Optional[int] = None,
        max_expiry: Optional[Annotated[str, "Range: 60-3600"]] = None,
        password: Optional[int] = None,
        pop_restriction: Optional[str] = None,
        record_calls: Optional[Literal["0", "1"]] = None,
        reseller_chargesetup: Optional[str] = None,
        reseller_client: Optional[int] = None,
        reseller_nextbilling: Optional[str] = None,
        reseller_package: Optional[str] = None,
        rtp_hold_timeout: Optional[Annotated[str, "Range: 1-3600"]] = None,
        rtp_timeout: Optional[Annotated[str, "Range: 1-3600"]] = None,
        send_bye: Optional[Literal["0", "1"]] = None,
        sip_traffic: Optional[Literal["0", "1"]] = None,
        tfcarrier: Optional[Literal["-1", "0", "1", "2"]] = None,
        transcribe: Optional[Literal["0", "1"]] = None,
        transcription_email: Optional[str] = None,
        transcription_locale: Optional[str] = None,
        transcription_start_delay: Optional[Annotated[str, "Range: 0-60; Units: seconds"]] = None,
    ) -> Dict[str, Any]:
        """Create new sub account

        Args:
            validate: Whether to validate parameters with Pydantic
            allowed_codecs: List of Allowed Codecs (Values from getAllowedCodecs) Codecs separated by semicolon (Example: ulaw;g729;gsm) (required)
            auth_type: Authorization Type Code (Values from getAuthTypes) (required)
            callerid_number: Caller ID Override
            canada_routing: Route Code (Values from getRoutes)
            description: Sub Account Description (Example: 'VoIP Account')
            device_type: Device Type Code (Values from getDeviceTypes) (required)
            dialing_mode: Allows you to dial outgoing calls using either the NANPA configuration or the E164 configuration. (Values: 0 = Use Main Account Setting, 1 = E164, 2 = NANPA)
            dtmf_mode: DTMF Mode Code (Values from getDTMFModes) (required)
            enable_internal_cnam: Enable Internal CallerID
            enable_ip_restriction: Enable IP Restriction (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            enable_pop_restriction: Enable POP Restriction (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            internal_cnam: Internal CallerID Name
            internal_dialtime: Sub Account Internal Dialtime (Example: 60 -> seconds)
            internal_extension: Sub Account Internal Extension (Example: 1 -> Creates 101)
            internal_voicemail: Sub Account Internal Voicemail (Example: 101)
            international_route: Route Code (Values from getRoutes) (required)
            ip: Sub Account IP (For IP Authentication)
            ip_restriction: List of IP Addresses, IP Addresses/Netmask, or Fully Qualified Domain Names to allow outgoing calls separated by commas (Example: 123.45.3.21,10.255.12.0/22,device.mydomain.com)
            language: Language for system messages, such as "Invalid Option" (Values from getLanguages)
            lock_international: Lock International Code (Values from getLockInternational) (required)
            max_expiry: Max Expiry between 60 and 3600 (Example: 3000)
            music_on_hold: Music on Hold Code (Values from getMusicOnHold) (required)
            nat: NAT Mode Code (Values from getNAT) (required)
            password: Sub Account Password (For Password Authentication)
            pop_restriction: List of POP Servers to allow outgoing calls separated by commas (values from getServersInfo. Example: 10,23,45)
            protocol: Protocol used for the Sub Account (Values from getProtocols) (required)
            record_calls: Record Calls (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            reseller_chargesetup: True if you want to charge Package Setup Fee after Save
            reseller_client: Reseller Account ID (Example: 561115)
            reseller_nextbilling: Reseller Next Billing Date (Example: '2012-12-31')
            reseller_package: Reseller Package (Example: 92364)
            rtp_hold_timeout: RTP Hold Time Out between 1 and 3600 (Example: 600)
            rtp_timeout: RTP Time Out between 1 and 3600 (Example: 60)
            send_bye: Send BYE on successful transfer (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            sip_traffic: Encrypted SIP Traffic (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            tfcarrier: This allows you to select the carrier to be used for outgoing calls to toll-free numbers. (Values: -1 = Use main account settings, 0 = Default server setting, 1 = US carrier, 2 = Canadian carrier)
            transcribe: Enable Call Transcription (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            transcription_email: Call Transcription Email
            transcription_locale: Call Transcription Locale (values from getLocales)
            transcription_start_delay: Call Transcription Delay Seconds between 0 and 60, Increments of 5 (Example: 10 -> seconds)
            username: Username for the Sub Account (Example: 'VoIP') (required)

        Returns:
            Response from createSubAccount operation
        """
        ...

    async def createVoicemail(
        self,
        validate: bool = True,
        *,
        attach_message: Annotated[str, "Format: wav"],
        delete_message: str,
        digits: Annotated[str, "Range: 1-10"],
        language: int,
        name: str,
        password: str,
        play_instructions: int,
        say_callerid: int,
        say_time: str,
        skip_password: Literal["0", "1"],
        timezone: str,
        email: Optional[Annotated[str, "Format: email"]] = None,
        email_attachment_format: Optional[int] = None,
        transcription: Optional[str] = None,
        transcription_locale: Optional[int] = None,
        unavailable_message_recording: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create new voicemail

        Args:
            validate: Whether to validate parameters with Pydantic
            attach_message: Yes for Attaching WAV files to Message (Values: 'yes'/'no') (required)
            delete_message: Yes for Deleting Messages (Values: 'yes'/'no') (required)
            digits: Digits used to create the voicemail (Example: 01) Minimum 1 digit, maximum 10 digits (required)
            email: Email address for receiving messages, multiple email addresses are allowed if separated by a comma
            email_attachment_format: Code for Email Attachment format (Values from getVoicemailAttachmentFormats)
            language: Code for Language (Values from getLanguages) (required)
            name: Name for the Mailbox (required)
            password: Password for the Mailbox (required)
            play_instructions: Code for Play Instructions Setting (Values from getPlayInstructions) (required)
            say_callerid: Yes for Saying the Caller ID (Values: 'yes'/'no') (required)
            say_time: Yes for Saying Time Stamp (Values: 'yes'/'no') (required)
            skip_password: True if Skipping Password (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean) (required)
            timezone: Time Zone for Mailbox (Values from getTimeZones) (required)
            transcription: Voicemail Transcription
            transcription_locale: Transcription locale code (values from getLocales)
            unavailable_message_recording: Recording for the Unavailable Message (values from getRecordings)

        Returns:
            Response from createVoicemail operation
        """
        ...

    async def delCallHunting(
        self,
        validate: bool = True,
        *,
        callhunting: int,
    ) -> Dict[str, Any]:
        """Delete call hunting

        Args:
            validate: Whether to validate parameters with Pydantic
            callhunting: ID for a specific Call Hunting (Example: 323) (required)

        Returns:
            Response from delCallHunting operation
        """
        ...

    async def delCallParking(
        self,
        validate: bool = True,
        *,
        callparking: int,
    ) -> Dict[str, Any]:
        """Delete call parking

        Args:
            validate: Whether to validate parameters with Pydantic
            callparking: ID for a specific Call Parking (Example: 323) (required)

        Returns:
            Response from delCallParking operation
        """
        ...

    async def delCallRecording(
        self,
        validate: bool = True,
        *,
        account: int,
        callrecording: str,
    ) -> Dict[str, Any]:
        """Delete call recording

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Filter Call Recordings by Account (Values from getCallAccounts) (required)
            callrecording: Call Recording (Values from getCallRecordings) (required)

        Returns:
            Response from delCallRecording operation
        """
        ...

    async def delCallback(
        self,
        validate: bool = True,
        *,
        callback: int,
    ) -> Dict[str, Any]:
        """Delete callback

        Args:
            validate: Whether to validate parameters with Pydantic
            callback: ID for a specific Callback (Example: 19183) (required)

        Returns:
            Response from delCallback operation
        """
        ...

    async def delCallerIDFiltering(
        self,
        validate: bool = True,
        *,
        filtering: int,
    ) -> Dict[str, Any]:
        """Delete caller id filtering

        Args:
            validate: Whether to validate parameters with Pydantic
            filtering: ID for a specific CallerID Filtering (Example: 19183) (required)

        Returns:
            Response from delCallerIDFiltering operation
        """
        ...

    async def delClient(
        self,
        validate: bool = True,
        *,
        client: int,
    ) -> Dict[str, Any]:
        """Delete client

        Args:
            validate: Whether to validate parameters with Pydantic
            client: ID for a specific Reseller Client (Example: 1998) (required)

        Returns:
            Response from delClient operation
        """
        ...

    async def delConference(
        self,
        validate: bool = True,
        *,
        conference: int,
    ) -> Dict[str, Any]:
        """Delete conference

        Args:
            validate: Whether to validate parameters with Pydantic
            conference: ID for a specific Conference (Example: 737) (required)

        Returns:
            Response from delConference operation
        """
        ...

    async def delConferenceMember(
        self,
        validate: bool = True,
        *,
        member: int,
    ) -> Dict[str, Any]:
        """Delete conference member

        Args:
            validate: Whether to validate parameters with Pydantic
            member: ID for a specific Member Profile (Example: 737) (required)

        Returns:
            Response from delConferenceMember operation
        """
        ...

    async def delDISA(
        self,
        validate: bool = True,
        *,
        disa: int,
    ) -> Dict[str, Any]:
        """Delete disa

        Args:
            validate: Whether to validate parameters with Pydantic
            disa: ID for a specific DISA (Example: 19183) (required)

        Returns:
            Response from delDISA operation
        """
        ...

    async def delEmailToFax(
        self,
        validate: bool = True,
        *,
        id_: int,
        test: Optional[Literal["true", "false"]] = None,
    ) -> Dict[str, Any]:
        """Delete email to fax

        Args:
            validate: Whether to validate parameters with Pydantic
            id_: ID for a specific "Email To Fax Configuration" (Example: 923) (required)
            test: Set to true if testing how cancel a "Email To Fax Configuration" (accepts: true/false, yes/no, on/off, 1/0, boolean)

        Returns:
            Response from delEmailToFax operation
        """
        ...

    async def delFaxFolder(
        self,
        validate: bool = True,
        *,
        id_: int,
        test: Optional[Literal["true", "false"]] = None,
    ) -> Dict[str, Any]:
        """Delete fax folder

        Args:
            validate: Whether to validate parameters with Pydantic
            id_: ID for a specific Fax Folder (Example: 923) (required)
            test: Set to true if testing how to delete a Fax Folder (accepts: true/false, yes/no, on/off, 1/0, boolean)

        Returns:
            Response from delFaxFolder operation
        """
        ...

    async def delForwarding(
        self,
        validate: bool = True,
        *,
        forwarding: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Delete forwarding

        Args:
            validate: Whether to validate parameters with Pydantic
            forwarding: ID for a specific Forwarding (Example: 19183)

        Returns:
            Response from delForwarding operation
        """
        ...

    async def delIVR(
        self,
        validate: bool = True,
        *,
        ivr: int,
    ) -> Dict[str, Any]:
        """Delete ivr

        Args:
            validate: Whether to validate parameters with Pydantic
            ivr: ID for a specific IVR (Example: 19183) (required)

        Returns:
            Response from delIVR operation
        """
        ...

    async def delMemberFromConference(
        self,
        validate: bool = True,
        *,
        member: int,
        conference: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Delete member from conference

        Args:
            validate: Whether to validate parameters with Pydantic
            conference: ID for a specific Conference (Example: 3829)
            member: ID for a specific Member (Example: 101) (required)

        Returns:
            Response from delMemberFromConference operation
        """
        ...

    async def delMessages(
        self,
        validate: bool = True,
        *,
        mailbox: int,
        folder: Optional[int] = None,
        message_num: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Delete messages

        Args:
            validate: Whether to validate parameters with Pydantic
            folder: Name for specific Folder (Required if message id is passed, Example: 'INBOX', values from: getVoicemailFolders)
            mailbox: ID for a specific Mailbox (Example: 1001) (required)
            message_num: ID for specific Voicemail Message (Required if folder is passed, Example: 1)

        Returns:
            Response from delMessages operation
        """
        ...

    async def delMusicOnHold(
        self,
        validate: bool = True,
        *,
        music_on_hold: str,
    ) -> Dict[str, Any]:
        """Delete music on hold

        Args:
            validate: Whether to validate parameters with Pydantic
            music_on_hold: Music on Hold Name (Values from getMusicOnHold) (required)

        Returns:
            Response from delMusicOnHold operation
        """
        ...

    async def delPhonebook(
        self,
        validate: bool = True,
        *,
        phonebook: int,
    ) -> Dict[str, Any]:
        """Delete phonebook

        Args:
            validate: Whether to validate parameters with Pydantic
            phonebook: ID for a specific Phonebook (Example: 19183) (required)

        Returns:
            Response from delPhonebook operation
        """
        ...

    async def delPhonebookGroup(
        self,
        validate: bool = True,
        *,
        group: int,
    ) -> Dict[str, Any]:
        """Delete phonebook group

        Args:
            validate: Whether to validate parameters with Pydantic
            group: ID for a specific Phonebook group (required)

        Returns:
            Response from delPhonebookGroup operation
        """
        ...

    async def delQueue(
        self,
        validate: bool = True,
        *,
        queue: int,
    ) -> Dict[str, Any]:
        """Delete queue

        Args:
            validate: Whether to validate parameters with Pydantic
            queue: ID for a specific Queue (Example: 13183) (required)

        Returns:
            Response from delQueue operation
        """
        ...

    async def delRecording(
        self,
        validate: bool = True,
        *,
        recording: int,
    ) -> Dict[str, Any]:
        """Delete recording

        Args:
            validate: Whether to validate parameters with Pydantic
            recording: ID for a specific Recording (Example: 19183) (required)

        Returns:
            Response from delRecording operation
        """
        ...

    async def delRingGroup(
        self,
        validate: bool = True,
        *,
        ringgroup: int,
    ) -> Dict[str, Any]:
        """Delete ring group

        Args:
            validate: Whether to validate parameters with Pydantic
            ringgroup: ID for a specific Ring Group (Example: 19183) (required)

        Returns:
            Response from delRingGroup operation
        """
        ...

    async def delSIPURI(
        self,
        validate: bool = True,
        *,
        sipuri: int,
    ) -> Dict[str, Any]:
        """Delete sipuri

        Args:
            validate: Whether to validate parameters with Pydantic
            sipuri: ID for a specific SIP URI (Example: 19183) (required)

        Returns:
            Response from delSIPURI operation
        """
        ...

    async def delStaticMember(
        self,
        validate: bool = True,
        *,
        member: int,
        queue: int,
    ) -> Dict[str, Any]:
        """Delete static member

        Args:
            validate: Whether to validate parameters with Pydantic
            member: ID for a specific Member Queue (Example: 1918) (required)
            queue: ID for a specific Queue (Example: 27183) (required)

        Returns:
            Response from delStaticMember operation
        """
        ...

    async def delSubAccount(
        self,
        validate: bool = True,
        *,
        id_: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Delete sub account

        Args:
            validate: Whether to validate parameters with Pydantic
            id_: ID for a specific Sub Account (Example: 99785)

        Returns:
            Response from delSubAccount operation
        """
        ...

    async def delTimeCondition(
        self,
        validate: bool = True,
        *,
        timecondition: int,
    ) -> Dict[str, Any]:
        """Delete time condition

        Args:
            validate: Whether to validate parameters with Pydantic
            timecondition: ID for a specific Time Condition (Example: 19183) (required)

        Returns:
            Response from delTimeCondition operation
        """
        ...

    async def delVoicemail(
        self,
        validate: bool = True,
        *,
        mailbox: int,
    ) -> Dict[str, Any]:
        """Delete voicemail

        Args:
            validate: Whether to validate parameters with Pydantic
            mailbox: ID for a specific Mailbox (Example: 1001) (required)

        Returns:
            Response from delVoicemail operation
        """
        ...

    async def deleteFaxMessage(
        self,
        validate: bool = True,
        *,
        id_: int,
        test: Optional[Literal["true", "false"]] = None,
    ) -> Dict[str, Any]:
        """Delete ete fax message

        Args:
            validate: Whether to validate parameters with Pydantic
            id_: ID for a specific Fax Message (Example: 923) (required)
            test: Set to true if testing how cancel a Fax Message (accepts: true/false, yes/no, on/off, 1/0, boolean)

        Returns:
            Response from deleteFaxMessage operation
        """
        ...

    async def deleteMMS(
        self,
        validate: bool = True,
        *,
        id_: int,
    ) -> Dict[str, Any]:
        """Delete ete mms

        Args:
            validate: Whether to validate parameters with Pydantic
            id_: ID for a specific MMS (Example: 1918) (required)

        Returns:
            Response from deleteMMS operation
        """
        ...

    async def deleteSMS(
        self,
        validate: bool = True,
        *,
        id_: int,
    ) -> Dict[str, Any]:
        """Delete ete sms

        Args:
            validate: Whether to validate parameters with Pydantic
            id_: ID for a specific SMS (Example: 1918) (required)

        Returns:
            Response from deleteSMS operation
        """
        ...

    async def e911AddressTypes(
        self,
        validate: bool = True,
        *,
        type_: Optional[int] = None,
    ) -> Dict[str, Any]:
        """E address types

        Args:
            validate: Whether to validate parameters with Pydantic
            type_: Code for a specific Address Type (Example: Apartment)

        Returns:
            Response from e911AddressTypes operation
        """
        ...

    async def e911Cancel(
        self,
        validate: bool = True,
        *,
        did: int,
    ) -> Dict[str, Any]:
        """E cancel

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID to be canceled. (required)

        Returns:
            Response from e911Cancel operation
        """
        ...

    async def e911Info(
        self,
        validate: bool = True,
        *,
        did: int,
    ) -> Dict[str, Any]:
        """E info

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID with e911 enabled / in process. (required)

        Returns:
            Response from e911Info operation
        """
        ...

    async def e911Provision(
        self,
        validate: bool = True,
        *,
        city: str,
        country: int,
        did: int,
        full_name: str,
        language: str,
        state: str,
        street_name: str,
        street_number: str,
        zip: str,
        address_number: Optional[str] = None,
        address_type: Optional[str] = None,
        other_info: Optional[str] = None,
    ) -> Dict[str, Any]:
        """E provision

        Args:
            validate: Whether to validate parameters with Pydantic
            address_number: Address Number that will be sent to the e911 service.
            address_type: Address Type that will be sent to the e911 service (Values from e911AddressTypes).
            city: City that will be sent to the e911 service. (required)
            country: Country that will be sent to the e911 service. Value can be US (United states) or CA (Canada). (required)
            did: DID that will be sent to the e911 service. (required)
            full_name: Full Name that will be sent to the e911 service. (required)
            language: Language that will be sent to the e911 service. Only available for addresses from Canada. Value can be EN (English) or FR (French). (required)
            other_info: Additional Address Information that will be sent to the e911 service. Only available for addresses from Canada.
            state: State / Province that will be sent to the e911 service. (required)
            street_name: Street Name that will be sent to the e911 service. (required)
            street_number: Street Number that will be sent to the e911 service. (required)
            zip:  (required)

        Returns:
            Response from e911Provision operation
        """
        ...

    async def e911ProvisionManually(
        self,
        validate: bool = True,
        *,
        city: str,
        country: int,
        did: int,
        full_name: str,
        language: str,
        state: str,
        street_name: str,
        street_number: str,
        zip: str,
        address_number: Optional[str] = None,
        address_type: Optional[str] = None,
        other_info: Optional[str] = None,
    ) -> Dict[str, Any]:
        """E provision manually

        Args:
            validate: Whether to validate parameters with Pydantic
            address_number: Address Number that will be sent to the e911 service.
            address_type: Address Type that will be sent to the e911 service (Values from e911AddressTypes).
            city: City that will be sent to the e911 service. (required)
            country: Country that will be sent to the e911 service. Value can be US (United states) or CA (Canada). (required)
            did: DID that will be sent to the e911 service. (required)
            full_name: Full Name that will be sent to the e911 service. (required)
            language: Language that will be sent to the e911 service. Only available for addresses from Canada. Value can be EN (English) or FR (French). (required)
            other_info: Additional Address Information that will be sent to the e911 service. Only available for addresses from Canada.
            state: State / Province that will be sent to the e911 service. (required)
            street_name: Street Name that will be sent to the e911 service. (required)
            street_number: Street Number that will be sent to the e911 service. (required)
            zip:  (required)

        Returns:
            Response from e911ProvisionManually operation
        """
        ...

    async def e911Update(
        self,
        validate: bool = True,
        *,
        city: str,
        country: int,
        did: int,
        full_name: str,
        language: str,
        state: str,
        street_name: str,
        street_number: str,
        zip: str,
        address_number: Optional[str] = None,
        address_type: Optional[str] = None,
        other_info: Optional[str] = None,
    ) -> Dict[str, Any]:
        """E update

        Args:
            validate: Whether to validate parameters with Pydantic
            address_number: Address Number that will be updated to the e911 service.
            address_type: Address Type that will be updated to the e911 service (Values from e911AddressTypes).
            city: City that will be updated to the e911 service. (required)
            country: Country that will be updated to the e911 service. Value can be US (United states) or CA (Canada). (required)
            did: DID with e911 enabled / in process. (required)
            full_name: Full Name that will be updated to the e911 service. (required)
            language: Language that will be updated to the e911 service. Only available for addresses from Canada. Value can be EN (English) or FR (French). (required)
            other_info: Additional Address Information that will be updated to the e911 service. Only available for addresses from Canada.
            state: State / Province that will be updated to the e911 service. (required)
            street_name: Street Name that will be updated to the e911 service. (required)
            street_number: Street Number that will be updated to the e911 service. (required)
            zip:  (required)

        Returns:
            Response from e911Update operation
        """
        ...

    async def e911Validate(
        self,
        validate: bool = True,
        *,
        city: int,
        country: int,
        did: int,
        full_name: int,
        state: int,
        street_name: int,
        street_number: int,
        zip: str,
        address_number: Optional[int] = None,
        address_type: Optional[int] = None,
        language: Optional[int] = None,
        other_info: Optional[int] = None,
    ) -> Dict[str, Any]:
        """E validate

        Args:
            validate: Whether to validate parameters with Pydantic
            address_number: Address Number that will be validated.
            address_type: Address Type that will be validated (Values from e911AddressTypes).
            city: City that will be validated. (required)
            country: Country that will be validated. Value can be US (United states) or CA (Canada). (required)
            did: DID with e911 enabled / in process. (required)
            full_name: Full Name that will be validated. (required)
            language: Language that will be validated. Only available for addresses from Canada. Value can be EN (English) or FR (French).
            other_info: Additional Address Information that will be validated. Only available for addresses from Canada.
            state: State / Province that will be validated. (required)
            street_name: Street Name that will be validated. (required)
            street_number: Street Number that will be validated. (required)
            zip:  (required)

        Returns:
            Response from e911Validate operation
        """
        ...

    async def getAllowedCodecs(
        self,
        validate: bool = True,
        *,
        codec: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve allowed codecs information

        Args:
            validate: Whether to validate parameters with Pydantic
            codec: Code for a specific Codec (Example: 'ulaw')

        Returns:
            Response from getAllowedCodecs operation
        """
        ...

    async def getAuthTypes(
        self,
        validate: bool = True,
        *,
        type_: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve auth types information

        Args:
            validate: Whether to validate parameters with Pydantic
            type_: Code for a specific Authorization Type (Example: 2)

        Returns:
            Response from getAuthTypes operation
        """
        ...

    async def getBackOrders(
        self,
        validate: bool = True,
        *,
        id_: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve back orders information

        Args:
            validate: Whether to validate parameters with Pydantic
            id_: ID for a specific backorder DID

        Returns:
            Response from getBackOrders operation
        """
        ...

    async def getBalance(
        self,
        validate: bool = True,
        *,
        advanced: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve balance information

        Args:
            validate: Whether to validate parameters with Pydantic
            advanced: True for Calls Statistics

        Returns:
            Response from getBalance operation
        """
        ...

    async def getBalanceManagement(
        self,
        validate: bool = True,
        *,
        balance_management: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve balance management information

        Args:
            validate: Whether to validate parameters with Pydantic
            balance_management: Code for a specific Balance Management Setting (Example: 1)

        Returns:
            Response from getBalanceManagement operation
        """
        ...

    async def getCDR(
        self,
        validate: bool = True,
        *,
        date_from: str,
        date_to: str,
        timezone: str,
        account: Optional[int] = None,
        answered: Optional[Literal["0", "1"]] = None,
        busy: Optional[Literal["0", "1"]] = None,
        callbilling: Optional[str] = None,
        calltype: Optional[str] = None,
        failed: Optional[Literal["0", "1"]] = None,
        noanswer: Optional[Literal["0", "1"]] = None,
    ) -> Dict[str, Any]:
        """Retrieve cdr information

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Filter CDR by Account (Values from getCallAccounts)
            answered: Include Answered Calls to CDR (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            busy: Include Busy Calls to CDR (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            callbilling: Filter CDR by Call Billing (Values from getCallBilling)
            calltype: Filters CDR by Call Type (Values from getCallTypes)
            date_from: Start Date for Filtering CDR (Example: '2010-11-30') (required)
            date_to: End Date for Filtering CDR (Example: '2010-11-30') (required)
            failed: Include Failed Calls to CDR (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            noanswer: Include NoAnswered calls to CDR (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            timezone: Adjust time of calls according to Timezome (Numeric: -12 to 13) (required)

        Returns:
            Response from getCDR operation

        Note:
            Date range limited to 92 days
            Boolean parameters are converted to '1'/'0' strings
            Timezone defaults to '1' if not provided
        """
        ...

    async def getCallAccounts(
        self,
        validate: bool = True,
    ) -> Dict[str, Any]:
        """Retrieve call accounts information

        Returns:
            Response from getCallAccounts operation
        """
        ...

    async def getCallBilling(
        self,
        validate: bool = True,
    ) -> Dict[str, Any]:
        """Retrieve call billing information

        Returns:
            Response from getCallBilling operation
        """
        ...

    async def getCallHuntings(
        self,
        validate: bool = True,
        *,
        callhunting: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve call huntings information

        Args:
            validate: Whether to validate parameters with Pydantic
            callhunting: ID for a specific Call Hunting (Example: 323)

        Returns:
            Response from getCallHuntings operation
        """
        ...

    async def getCallParking(
        self,
        validate: bool = True,
        *,
        callparking: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve call parking information

        Args:
            validate: Whether to validate parameters with Pydantic
            callparking: ID for a specific Call Parking (Example: 737)

        Returns:
            Response from getCallParking operation
        """
        ...

    async def getCallRecording(
        self,
        validate: bool = True,
        *,
        account: int,
        callrecording: str,
    ) -> Dict[str, Any]:
        """Retrieve call recording information

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Main Account or Sub Account related to the call recording (Values from getCallRecordings) (required)
            callrecording: Call Recording (Values from getCallRecordings) (required)

        Returns:
            Response from getCallRecording operation
        """
        ...

    async def getCallRecordings(
        self,
        validate: bool = True,
        *,
        account: int,
        date_from: str,
        date_to: str,
        length: Optional[int] = None,
        start: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve call recordings information

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Filter Call Recordings by Account (Values from getCallAccounts) (required)
            date_from: Start Date for Filtering Call Recording (Example:'2018-11-01') (required)
            date_to: End Date for Filtering Call Recording (Example:'2018-12-01') (required)
            length: Number of records to show
            start: Number of records shown previously, used for pages

        Returns:
            Response from getCallRecordings operation
        """
        ...

    async def getCallTypes(
        self,
        validate: bool = True,
        *,
        client: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve call types information

        Args:
            validate: Whether to validate parameters with Pydantic
            client: ID for a specific Reseller Client (Example: 561115)

        Returns:
            Response from getCallTypes operation
        """
        ...

    async def getCallbacks(
        self,
        validate: bool = True,
        *,
        callback: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve callbacks information

        Args:
            validate: Whether to validate parameters with Pydantic
            callback: ID for a specific Callback (Example: 2359)

        Returns:
            Response from getCallbacks operation
        """
        ...

    async def getCallerIDFiltering(
        self,
        validate: bool = True,
        *,
        did: Optional[int] = None,
        filtering: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve caller id filtering information

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID for a specific CallerID Filtering (Example: 5551234567)
            filtering: ID for a specific CallerID Filtering (Example: 18915)

        Returns:
            Response from getCallerIDFiltering operation
        """
        ...

    async def getCarriers(
        self,
        validate: bool = True,
        *,
        carrier: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve carriers information

        Args:
            validate: Whether to validate parameters with Pydantic
            carrier: Code for a specific Carrier (Example: 2)

        Returns:
            Response from getCarriers operation
        """
        ...

    async def getCharges(
        self,
        validate: bool = True,
        *,
        client: int,
    ) -> Dict[str, Any]:
        """Retrieve charges information

        Args:
            validate: Whether to validate parameters with Pydantic
            client: ID for a specific Reseller Client (Example: 561115) (required)

        Returns:
            Response from getCharges operation
        """
        ...

    async def getClientPackages(
        self,
        validate: bool = True,
        *,
        client: int,
    ) -> Dict[str, Any]:
        """Retrieve client packages information

        Args:
            validate: Whether to validate parameters with Pydantic
            client: ID for a specific Reseller Client (Example: 561115) (required)

        Returns:
            Response from getClientPackages operation
        """
        ...

    async def getClientThreshold(
        self,
        validate: bool = True,
        *,
        client: int,
    ) -> Dict[str, Any]:
        """Retrieve client threshold information

        Args:
            validate: Whether to validate parameters with Pydantic
            client: ID for a specific Reseller Client (Example: 561115) (required)

        Returns:
            Response from getClientThreshold operation
        """
        ...

    async def getClients(
        self,
        validate: bool = True,
        *,
        client: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve clients information

        Args:
            validate: Whether to validate parameters with Pydantic
            client: Parameter could have the following values: * Empty Value [Not Required] * Specific Reseller Client ID (Example: 561115) * Specific Reseller Client e-mail  (Example: 'john.doe@mydomain.com')

        Returns:
            Response from getClients operation
        """
        ...

    async def getConference(
        self,
        validate: bool = True,
        *,
        conference: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve conference information

        Args:
            validate: Whether to validate parameters with Pydantic
            conference: Code for a specific Conference (Example: 1599)

        Returns:
            Response from getConference operation
        """
        ...

    async def getConferenceMembers(
        self,
        validate: bool = True,
        *,
        member: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve conference members information

        Args:
            validate: Whether to validate parameters with Pydantic
            member: Code for a specific Member profile (Example: 1599)

        Returns:
            Response from getConferenceMembers operation
        """
        ...

    async def getConferenceRecordingFile(
        self,
        validate: bool = True,
        *,
        conference: int,
        recording: int,
    ) -> Dict[str, Any]:
        """Retrieve conference recording file information

        Args:
            validate: Whether to validate parameters with Pydantic
            conference: ID for a specific Conference (Example: 5356) (required)
            recording: ID for a specific Conference Recording (Example: 1543338379) (required)

        Returns:
            Response from getConferenceRecordingFile operation
        """
        ...

    async def getConferenceRecordings(
        self,
        validate: bool = True,
        *,
        conference: int,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve conference recordings information

        Args:
            validate: Whether to validate parameters with Pydantic
            conference: ID for a specific Conference (Example: 5356) (required)
            date_from: Start Date for Filtering Transactions (Example: '2016-06-03')
            date_to: End Date for Filtering Transactions (Example: '2016-06-04')

        Returns:
            Response from getConferenceRecordings operation
        """
        ...

    async def getCountries(
        self,
        validate: bool = True,
        *,
        country: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve countries information

        Args:
            validate: Whether to validate parameters with Pydantic
            country: Code for a specific Country (Example: 'CA')

        Returns:
            Response from getCountries operation
        """
        ...

    async def getDIDCountries(
        self,
        validate: bool = True,
        *,
        type_: int,
        country_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve did countries information

        Args:
            validate: Whether to validate parameters with Pydantic
            country_id: ID for a specific country (Example: 205)
            type_: Type of International DID (Values from getInternationalTypes) (required)

        Returns:
            Response from getDIDCountries operation
        """
        ...

    async def getDIDsCAN(
        self,
        validate: bool = True,
        *,
        province: str,
        ratecenter: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve di ds can information

        Args:
            validate: Whether to validate parameters with Pydantic
            province: Canadian Province (Values from getProvinces) (required)
            ratecenter: Canadian Ratecenter (Values from getRateCentersCAN)

        Returns:
            Response from getDIDsCAN operation
        """
        ...

    async def getDIDsInfo(
        self,
        validate: bool = True,
        *,
        client: Optional[str] = None,
        did: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve di ds info information

        Args:
            validate: Whether to validate parameters with Pydantic
            client: Parameter could have the following values: * Empty Value [Not Required] * Specific Reseller Client ID (Example: 561115) * Specific Sub Account (Example: '100001_VoIP')
            did: DID from Client or Sub Account (Example: 5551234567)

        Returns:
            Response from getDIDsInfo operation
        """
        ...

    async def getDIDsInternationalGeographic(
        self,
        validate: bool = True,
        *,
        country_id: int,
    ) -> Dict[str, Any]:
        """Retrieve di ds international geographic information

        Args:
            validate: Whether to validate parameters with Pydantic
            country_id: ID for a specific Country (Values from getDIDCountries) (required)

        Returns:
            Response from getDIDsInternationalGeographic operation
        """
        ...

    async def getDIDsInternationalNational(
        self,
        validate: bool = True,
        *,
        country_id: int,
    ) -> Dict[str, Any]:
        """Retrieve di ds international national information

        Args:
            validate: Whether to validate parameters with Pydantic
            country_id: ID for a specific Country (Values from getDIDCountries) (required)

        Returns:
            Response from getDIDsInternationalNational operation
        """
        ...

    async def getDIDsInternationalTollFree(
        self,
        validate: bool = True,
        *,
        country_id: int,
    ) -> Dict[str, Any]:
        """Retrieve di ds international toll free information

        Args:
            validate: Whether to validate parameters with Pydantic
            country_id: ID for a specific Country (Values from getDIDCountries) (required)

        Returns:
            Response from getDIDsInternationalTollFree operation
        """
        ...

    async def getDIDsUSA(
        self,
        validate: bool = True,
        *,
        state: str,
        ratecenter: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve di ds usa information

        Args:
            validate: Whether to validate parameters with Pydantic
            ratecenter: United States Ratecenter (Values from getRateCentersUSA)
            state: United States State (Values from getStates) (required)

        Returns:
            Response from getDIDsUSA operation
        """
        ...

    async def getDIDvPRI(
        self,
        validate: bool = True,
        *,
        vpri: int,
    ) -> Dict[str, Any]:
        """Retrieve di dv pri information

        Args:
            validate: Whether to validate parameters with Pydantic
            vpri: Id for specific Vpri (required)

        Returns:
            Response from getDIDvPRI operation
        """
        ...

    async def getDISAs(
        self,
        validate: bool = True,
        *,
        disa: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve dis as information

        Args:
            validate: Whether to validate parameters with Pydantic
            disa: ID for a specific DISA (Example: 2114)

        Returns:
            Response from getDISAs operation
        """
        ...

    async def getDTMFModes(
        self,
        validate: bool = True,
        *,
        dtmf_mode: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve dtmf modes information

        Args:
            validate: Whether to validate parameters with Pydantic
            dtmf_mode: Code for a specific DTMF Mode (Example: 'inband')

        Returns:
            Response from getDTMFModes operation
        """
        ...

    async def getDeposits(
        self,
        validate: bool = True,
        *,
        client: int,
    ) -> Dict[str, Any]:
        """Retrieve deposits information

        Args:
            validate: Whether to validate parameters with Pydantic
            client: ID for a specific Reseller Client (Example: 561115) (required)

        Returns:
            Response from getDeposits operation
        """
        ...

    async def getDeviceTypes(
        self,
        validate: bool = True,
        *,
        device_type: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve device types information

        Args:
            validate: Whether to validate parameters with Pydantic
            device_type: Code for a specific Device Type (Example: 1)

        Returns:
            Response from getDeviceTypes operation
        """
        ...

    async def getEmailToFax(
        self,
        validate: bool = True,
        *,
        id_: int,
    ) -> Dict[str, Any]:
        """Retrieve email to fax information

        Args:
            validate: Whether to validate parameters with Pydantic
            id_:  (required)

        Returns:
            Response from getEmailToFax operation
        """
        ...

    async def getFaxFolders(
        self,
        validate: bool = True,
        *,
        id_: int,
    ) -> Dict[str, Any]:
        """Retrieve fax folders information

        Args:
            validate: Whether to validate parameters with Pydantic
            id_:  (required)

        Returns:
            Response from getFaxFolders operation
        """
        ...

    async def getFaxMessagePDF(
        self,
        validate: bool = True,
        *,
        id_: int,
    ) -> Dict[str, Any]:
        """Retrieve fax message pdf information

        Args:
            validate: Whether to validate parameters with Pydantic
            id_: ID of the Fax Message requested (Values from getFaxMessages) (required)

        Returns:
            Response from getFaxMessagePDF operation
        """
        ...

    async def getFaxMessages(
        self,
        validate: bool = True,
        *,
        folder: Optional[str] = None,
        from_: Optional[str] = None,
        id_: Optional[int] = None,
        to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve fax messages information

        Args:
            validate: Whether to validate parameters with Pydantic
            folder: Name of specific Fax Folder (Example: SENT) - Default value: ALL
            from_: Start Date for Filtering Fax Messages (Example: '2014-03-30') - Default value: Today
            id_: ID for a Specific Fax Message (Example: 23434)
            to: End Date for Filtering Fax Messages (Example: '2014-03-30') - Default value: Today

        Returns:
            Response from getFaxMessages operation
        """
        ...

    async def getFaxNumbersInfo(
        self,
        validate: bool = True,
        *,
        did: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve fax numbers info information

        Args:
            validate: Whether to validate parameters with Pydantic
            did: Fax Number to retrieves the information of a single number, or not send if you want retrieves the information of all your Fax Numbers.

        Returns:
            Response from getFaxNumbersInfo operation
        """
        ...

    async def getFaxNumbersPortability(
        self,
        validate: bool = True,
        *,
        did: int,
    ) -> Dict[str, Any]:
        """Retrieve fax numbers portability information

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID Number to be ported into our network (Example: 5552341234) (required)

        Returns:
            Response from getFaxNumbersPortability operation
        """
        ...

    async def getFaxProvinces(
        self,
        validate: bool = True,
        *,
        province: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve fax provinces information

        Args:
            validate: Whether to validate parameters with Pydantic
            province: CODE for a specific Province (Example: AB)

        Returns:
            Response from getFaxProvinces operation
        """
        ...

    async def getFaxRateCentersCAN(
        self,
        validate: bool = True,
        *,
        province: int,
    ) -> Dict[str, Any]:
        """Retrieve fax rate centers can information

        Args:
            validate: Whether to validate parameters with Pydantic
            province: Province two letters code (Example: AB) (required)

        Returns:
            Response from getFaxRateCentersCAN operation
        """
        ...

    async def getFaxRateCentersUSA(
        self,
        validate: bool = True,
        *,
        state: int,
    ) -> Dict[str, Any]:
        """Retrieve fax rate centers usa information

        Args:
            validate: Whether to validate parameters with Pydantic
            state: Province two letters code (Example: AL) (required)

        Returns:
            Response from getFaxRateCentersUSA operation
        """
        ...

    async def getFaxStates(
        self,
        validate: bool = True,
        *,
        state: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve fax states information

        Args:
            validate: Whether to validate parameters with Pydantic
            state: CODE for a specific State (Example: AL)

        Returns:
            Response from getFaxStates operation
        """
        ...

    async def getForwardings(
        self,
        validate: bool = True,
        *,
        forwarding: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve forwardings information

        Args:
            validate: Whether to validate parameters with Pydantic
            forwarding: ID for a specific Forwarding (Example: 18635)

        Returns:
            Response from getForwardings operation
        """
        ...

    async def getIP(
        self,
        validate: bool = True,
    ) -> Dict[str, Any]:
        """Retrieve ip information

        Returns:
            Response from getIP operation
        """
        ...

    async def getIVRs(
        self,
        validate: bool = True,
        *,
        ivr: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve iv rs information

        Args:
            validate: Whether to validate parameters with Pydantic
            ivr: ID for a specific IVR (Example: 4636)

        Returns:
            Response from getIVRs operation
        """
        ...

    async def getInternationalTypes(
        self,
        validate: bool = True,
        *,
        type_: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve international types information

        Args:
            validate: Whether to validate parameters with Pydantic
            type_: Code for a specific International Type (Example: 'NATIONAL')

        Returns:
            Response from getInternationalTypes operation
        """
        ...

    async def getJoinWhenEmptyTypes(
        self,
        validate: bool = True,
        *,
        type_: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve join when empty types information

        Args:
            validate: Whether to validate parameters with Pydantic
            type_: Code for a specific 'JoinWhenEmpty' Type (Example: 'yes')

        Returns:
            Response from getJoinWhenEmptyTypes operation
        """
        ...

    async def getLNPAttach(
        self,
        validate: bool = True,
        *,
        attachid: int,
    ) -> Dict[str, Any]:
        """Retrieve lnp attach information

        Args:
            validate: Whether to validate parameters with Pydantic
            attachid: ID of the invoice (attachment) previously uploaded. (required)

        Returns:
            Response from getLNPAttach operation
        """
        ...

    async def getLNPAttachList(
        self,
        validate: bool = True,
        *,
        portid: int,
    ) -> Dict[str, Any]:
        """Retrieve lnp attach list information

        Args:
            validate: Whether to validate parameters with Pydantic
            portid: ID of the port previously created. (required)

        Returns:
            Response from getLNPAttachList operation
        """
        ...

    async def getLNPDetails(
        self,
        validate: bool = True,
        *,
        portid: int,
    ) -> Dict[str, Any]:
        """Retrieve lnp details information

        Args:
            validate: Whether to validate parameters with Pydantic
            portid: ID of the port previously created. (required)

        Returns:
            Response from getLNPDetails operation
        """
        ...

    async def getLNPList(
        self,
        validate: bool = True,
        *,
        portid: int,
        endDate: Optional[int] = None,
        portStatus: Optional[int] = None,
        startDate: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve lnp list information

        Args:
            validate: Whether to validate parameters with Pydantic
            endDate: End Date for filtering Ports. (Example: '2014-03-30')
            portStatus: Status code to filtering Ports. Example: precessing. (You can use the values returned by the method getLNPListStatus)
            portid: ID of the port previously created. (required)
            startDate: Start Date for filtering Ports. (Example: '2014-03-30')

        Returns:
            Response from getLNPList operation
        """
        ...

    async def getLNPListStatus(
        self,
        validate: bool = True,
    ) -> Dict[str, Any]:
        """Retrieve lnp list status information

        Returns:
            Response from getLNPListStatus operation
        """
        ...

    async def getLNPNotes(
        self,
        validate: bool = True,
        *,
        portid: int,
    ) -> Dict[str, Any]:
        """Retrieve lnp notes information

        Args:
            validate: Whether to validate parameters with Pydantic
            portid: ID of the port previously created. (required)

        Returns:
            Response from getLNPNotes operation
        """
        ...

    async def getLNPStatus(
        self,
        validate: bool = True,
        *,
        portid: int,
    ) -> Dict[str, Any]:
        """Retrieve lnp status information

        Args:
            validate: Whether to validate parameters with Pydantic
            portid: ID of the port previously created. (required)

        Returns:
            Response from getLNPStatus operation
        """
        ...

    async def getLanguages(
        self,
        validate: bool = True,
        *,
        language: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve languages information

        Args:
            validate: Whether to validate parameters with Pydantic
            language: Code for a specific Language (Example: 'en')

        Returns:
            Response from getLanguages operation
        """
        ...

    async def getLocales(
        self,
        validate: bool = True,
        *,
        locale: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve locales information

        Args:
            validate: Whether to validate parameters with Pydantic
            locale: Code for a specific Locale Code (Example: 'en-US')

        Returns:
            Response from getLocales operation
        """
        ...

    async def getLockInternational(
        self,
        validate: bool = True,
        *,
        lock_international: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve lock international information

        Args:
            validate: Whether to validate parameters with Pydantic
            lock_international: Code for a specific Lock International Mode (Example: 1)

        Returns:
            Response from getLockInternational operation
        """
        ...

    async def getMMS(
        self,
        validate: bool = True,
        *,
        all_messages: Optional[int] = None,
        contact: Optional[str] = None,
        did: Optional[int] = None,
        from_: Optional[str] = None,
        limit: Optional[int] = None,
        mms: Optional[int] = None,
        timezone: Optional[str] = None,
        to: Optional[str] = None,
        type_: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve mms information

        Args:
            validate: Whether to validate parameters with Pydantic
            all_messages: Filter to recive all MMSs and SMSs, 1 recive all SMS and MMS, 0 if only need MMS, important: the sms ID must be 0
            contact: Contact number for Filtering MMSs (Example: 5551234567)
            did: DID number for Filtering MMSs (Example: 5551234567)
            from_: Start Date for Filtering MMSs (Example: '2014-03-30') - Default value: Today
            limit: Number of records to be displayed (Example: 20) - Default value: 50
            mms: ID for a specific MMS (Example: 1918)
            timezone: Adjust time of MMSs according to Timezome (Numeric: -12 to 13)
            to: End Date for Filtering MMSs (Example: '2014-03-30') - Default value: Today
            type_: Filter MMSs by Type (Boolean: 1 = received / 0 = sent)

        Returns:
            Response from getMMS operation

        Note:
            Date parameters use 'from' and 'to' instead of 'date_from' and 'date_to'
        """
        ...

    async def getMediaMMS(
        self,
        validate: bool = True,
        *,
        id_: Optional[int] = None,
        media_as_array: Optional[Annotated[str, "Format: json"]] = None,
    ) -> Dict[str, Any]:
        """Retrieve media mms information

        Args:
            validate: Whether to validate parameters with Pydantic
            id_: ID for a specific MMS (Example: 1918)
            media_as_array: Return the list of media attachments as an Array if the value is 1 or as a JSON Object if the value is 0 (Default: 0)

        Returns:
            Response from getMediaMMS operation
        """
        ...

    async def getMusicOnHold(
        self,
        validate: bool = True,
        *,
        music_on_hold: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve music on hold information

        Args:
            validate: Whether to validate parameters with Pydantic
            music_on_hold: Code for a specific Music on Hold (Example: 'jazz')

        Returns:
            Response from getMusicOnHold operation
        """
        ...

    async def getNAT(
        self,
        validate: bool = True,
        *,
        nat: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve nat information

        Args:
            validate: Whether to validate parameters with Pydantic
            nat: Code for a specific NAT Option (Example: 'route')

        Returns:
            Response from getNAT operation
        """
        ...

    async def getPackages(
        self,
        validate: bool = True,
        *,
        package: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve packages information

        Args:
            validate: Whether to validate parameters with Pydantic
            package: Code for a specific Package (Example: 8378)

        Returns:
            Response from getPackages operation
        """
        ...

    async def getPhonebook(
        self,
        validate: bool = True,
        *,
        group: Optional[int] = None,
        group_name: Optional[str] = None,
        name: Optional[str] = None,
        phonebook: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve phonebook information

        Args:
            validate: Whether to validate parameters with Pydantic
            group: ID for a specific Phonebook group
            group_name: Group Name
            name: Name to be searched in database   (Example: 'jane')
            phonebook: ID for a specific Phonebook entry (Example: 32207)

        Returns:
            Response from getPhonebook operation
        """
        ...

    async def getPhonebookGroups(
        self,
        validate: bool = True,
        *,
        group: Optional[int] = None,
        name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve phonebook groups information

        Args:
            validate: Whether to validate parameters with Pydantic
            group: ID for a specific Phonebook group
            name: Group Name

        Returns:
            Response from getPhonebookGroups operation
        """
        ...

    async def getPlayInstructions(
        self,
        validate: bool = True,
        *,
        play_instructions: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve play instructions information

        Args:
            validate: Whether to validate parameters with Pydantic
            play_instructions: Code for a specific Play Instructions setting (Example: 'u')

        Returns:
            Response from getPlayInstructions operation
        """
        ...

    async def getPortability(
        self,
        validate: bool = True,
        *,
        did: int,
    ) -> Dict[str, Any]:
        """Retrieve portability information

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID Number to be ported into our network (Example: 5552341234) (required)

        Returns:
            Response from getPortability operation
        """
        ...

    async def getProtocols(
        self,
        validate: bool = True,
        *,
        protocol: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve protocols information

        Args:
            validate: Whether to validate parameters with Pydantic
            protocol: Code for a specific Protocol (Example: 3)

        Returns:
            Response from getProtocols operation
        """
        ...

    async def getProvinces(
        self,
        validate: bool = True,
    ) -> Dict[str, Any]:
        """Retrieve provinces information

        Returns:
            Response from getProvinces operation
        """
        ...

    async def getQueues(
        self,
        validate: bool = True,
        *,
        queue: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve queues information

        Args:
            validate: Whether to validate parameters with Pydantic
            queue: ID for a specific Queue (Example: 4764)

        Returns:
            Response from getQueues operation
        """
        ...

    async def getRateCentersCAN(
        self,
        validate: bool = True,
        *,
        province: str,
    ) -> Dict[str, Any]:
        """Retrieve rate centers can information

        Args:
            validate: Whether to validate parameters with Pydantic
            province: Canadian Province (Values from getProvinces) (required)

        Returns:
            Response from getRateCentersCAN operation
        """
        ...

    async def getRateCentersUSA(
        self,
        validate: bool = True,
        *,
        state: str,
    ) -> Dict[str, Any]:
        """Retrieve rate centers usa information

        Args:
            validate: Whether to validate parameters with Pydantic
            state: United States State (Values from getStates) (required)

        Returns:
            Response from getRateCentersUSA operation
        """
        ...

    async def getRates(
        self,
        validate: bool = True,
        *,
        package: int,
        query: str,
    ) -> Dict[str, Any]:
        """Retrieve rates information

        Args:
            validate: Whether to validate parameters with Pydantic
            package: ID for a specific Package (Example: 92364) (required)
            query: Query for searching rates (Example: 'Canada') (required)

        Returns:
            Response from getRates operation
        """
        ...

    async def getRecordingFile(
        self,
        validate: bool = True,
        *,
        recording: int,
    ) -> Dict[str, Any]:
        """Retrieve recording file information

        Args:
            validate: Whether to validate parameters with Pydantic
            recording: ID for a specific Recording (Example: 7567) (required)

        Returns:
            Response from getRecordingFile operation
        """
        ...

    async def getRecordings(
        self,
        validate: bool = True,
        *,
        recording: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve recordings information

        Args:
            validate: Whether to validate parameters with Pydantic
            recording: ID for a specific Recording (Example: 7567)

        Returns:
            Response from getRecordings operation
        """
        ...

    async def getRegistrationStatus(
        self,
        validate: bool = True,
        *,
        account: int,
    ) -> Dict[str, Any]:
        """Retrieve registration status information

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Specific Account (Example: '100001_VoIP') (required)

        Returns:
            Response from getRegistrationStatus operation
        """
        ...

    async def getReportEstimatedHoldTime(
        self,
        validate: bool = True,
        *,
        type_: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve report estimated hold time information

        Args:
            validate: Whether to validate parameters with Pydantic
            type_: Code for a specific 'ReportEstimatedHoldTime' Type (Example: 'yes')

        Returns:
            Response from getReportEstimatedHoldTime operation
        """
        ...

    async def getResellerBalance(
        self,
        validate: bool = True,
        *,
        client: int,
    ) -> Dict[str, Any]:
        """Retrieve reseller balance information

        Args:
            validate: Whether to validate parameters with Pydantic
            client: ID for a specific Reseller Client (Example: 561115) (required)

        Returns:
            Response from getResellerBalance operation
        """
        ...

    async def getResellerCDR(
        self,
        validate: bool = True,
        *,
        client: int,
        date_from: str,
        date_to: str,
        timezone: str,
        account: Optional[int] = None,
        answered: Optional[Literal["0", "1"]] = None,
        busy: Optional[Literal["0", "1"]] = None,
        callbilling: Optional[str] = None,
        calltype: Optional[str] = None,
        failed: Optional[Literal["0", "1"]] = None,
        noanswer: Optional[Literal["0", "1"]] = None,
    ) -> Dict[str, Any]:
        """Retrieve reseller cdr information

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Filter CDR by Account (Values from getCallAccounts)
            answered: Include Answered Calls to CDR (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            busy: Include Busy Calls to CDR (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            callbilling: Filter CDR by Call Billing (Values from getCallBilling)
            calltype: Filters CDR by Call Type (Values from getCallTypes)
            client: ID for a specific Reseller Client (Example: 561115) (required)
            date_from: Start Date for Filtering CDR (Example: '2010-11-30') (required)
            date_to: End Date for Filtering CDR (Example: '2010-11-30') (required)
            failed: Include Failed Calls to CDR (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            noanswer: Include NoAnswered calls to CDR (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            timezone: Adjust time of calls according to Timezome (Numeric: -12 to 13) (required)

        Returns:
            Response from getResellerCDR operation
        """
        ...

    async def getResellerMMS(
        self,
        validate: bool = True,
        *,
        client: int,
        mms: int,
        all_messages: Optional[int] = None,
        contact: Optional[str] = None,
        did: Optional[int] = None,
        from_: Optional[str] = None,
        limit: Optional[int] = None,
        timezone: Optional[str] = None,
        to: Optional[str] = None,
        type_: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve reseller mms information

        Args:
            validate: Whether to validate parameters with Pydantic
            all_messages: Filter to recive all SMSs and MMSs, 1 recive all SMS and MMS, 0 if only need SMS, important: the sms ID must be 0
            client:  (required)
            contact: Contact number for Filtering MMSs (Example: 5551234567)
            did: DID number for Filtering MMSs (Example: 5551234567)
            from_: Start Date for Filtering SMSs (Example: '2014-03-30') - Default value: Today
            limit: Number of records to be displayed (Example: 20) - Default value: 50
            mms:  (required)
            timezone: Adjust time of MMSs according to Timezome (Numeric: -12 to 13)
            to: End Date for Filtering MMSs (Example: '2014-03-30')
            type_: Filter SMSs by Type (Boolean: 1 = received / 0 = sent)

        Returns:
            Response from getResellerMMS operation
        """
        ...

    async def getResellerSMS(
        self,
        validate: bool = True,
        *,
        client: int,
        all_messages: Optional[int] = None,
        contact: Optional[str] = None,
        did: Optional[int] = None,
        from_: Optional[str] = None,
        limit: Optional[int] = None,
        sms: Optional[int] = None,
        timezone: Optional[str] = None,
        to: Optional[str] = None,
        type_: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve reseller sms information

        Args:
            validate: Whether to validate parameters with Pydantic
            all_messages: Filter to recive all SMSs and MMSs, 1 recive all SMS and MMS, 0 if only need SMS, important: the sms ID must be 0
            client:  (required)
            contact: Contact number for Filtering SMSs (Example: 5551234567)
            did: DID number for Filtering SMSs (Example: 5551234567)
            from_: Start Date for Filtering SMSs (Example: '2014-03-30') - Default value: Today
            limit: Number of records to be displayed (Example: 20) - Default value: 50
            sms: ID for a specific SMS (Example: 5853)
            timezone: Adjust time of SMSs according to Timezome (Numeric: -12 to 13)
            to: End Date for Filtering SMSs (Example: '2014-03-30')
            type_: Filter SMSs by Type (Boolean: 1 = received / 0 = sent)

        Returns:
            Response from getResellerSMS operation
        """
        ...

    async def getRingGroups(
        self,
        validate: bool = True,
        *,
        ring_group: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve ring groups information

        Args:
            validate: Whether to validate parameters with Pydantic
            ring_group: ID for a specific Ring Group (Example: 4768)

        Returns:
            Response from getRingGroups operation
        """
        ...

    async def getRingStrategies(
        self,
        validate: bool = True,
        *,
        strategy: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve ring strategies information

        Args:
            validate: Whether to validate parameters with Pydantic
            strategy: ID for a specific Ring Strategy (Example: 'rrmemory')

        Returns:
            Response from getRingStrategies operation
        """
        ...

    async def getRoutes(
        self,
        validate: bool = True,
        *,
        route: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve routes information

        Args:
            validate: Whether to validate parameters with Pydantic
            route: Code for a specific Route (Example: 2)

        Returns:
            Response from getRoutes operation
        """
        ...

    async def getSIPURIs(
        self,
        validate: bool = True,
        *,
        sipuri: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve sipur is information

        Args:
            validate: Whether to validate parameters with Pydantic
            sipuri: ID for a specific SIP URI (Example: 6199)

        Returns:
            Response from getSIPURIs operation
        """
        ...

    async def getSMS(
        self,
        validate: bool = True,
        *,
        all_messages: Optional[int] = None,
        contact: Optional[str] = None,
        did: Optional[int] = None,
        from_: Optional[str] = None,
        limit: Optional[int] = None,
        sms: Optional[int] = None,
        timezone: Optional[str] = None,
        to: Optional[str] = None,
        type_: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve sms information

        Args:
            validate: Whether to validate parameters with Pydantic
            all_messages: Filter to recive all SMSs and MMSs, 1 recive all SMS and MMS, 0 if only need SMS, important: the sms ID must be 0
            contact: Contact number for Filtering SMSs (Example: 5551234567)
            did: DID number for Filtering SMSs (Example: 5551234567)
            from_: Start Date for Filtering SMSs (Example: '2014-03-30') - Default value: Today
            limit: Number of records to be displayed (Example: 20) - Default value: 50
            sms: ID for a specific SMS (Example: 5853)
            timezone: Adjust time of SMSs according to Timezome (Numeric: -12 to 13)
            to: End Date for Filtering SMSs (Example: '2014-03-30') - Default value: Today
            type_: Filter SMSs by Type (Boolean: 1 = received / 0 = sent)

        Returns:
            Response from getSMS operation

        Note:
            Date parameters use 'from' and 'to' instead of 'date_from' and 'date_to'
        """
        ...

    async def getServersInfo(
        self,
        validate: bool = True,
        *,
        server_pop: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve servers info information

        Args:
            validate: Whether to validate parameters with Pydantic
            server_pop: POP for a specific Server (Example: 1)

        Returns:
            Response from getServersInfo operation
        """
        ...

    async def getStates(
        self,
        validate: bool = True,
    ) -> Dict[str, Any]:
        """Retrieve states information

        Returns:
            Response from getStates operation
        """
        ...

    async def getStaticMembers(
        self,
        validate: bool = True,
        *,
        queue: int,
        member: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve static members information

        Args:
            validate: Whether to validate parameters with Pydantic
            member: ID for a specific Static Member (Example: 163) - The Member must belong to the queue provided
            queue: ID for a specific Queue (Example: 4136) (required)

        Returns:
            Response from getStaticMembers operation
        """
        ...

    async def getSubAccounts(
        self,
        validate: bool = True,
        *,
        account: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve sub accounts information

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Parameter could have the following values: * Empty Value [Not Required] * Specific Sub Account (Example: '100000_VoIP') * Specific Reseller Client ID (Example: 561115)

        Returns:
            Response from getSubAccounts operation
        """
        ...

    async def getTerminationRates(
        self,
        validate: bool = True,
        *,
        query: str,
        route: int,
    ) -> Dict[str, Any]:
        """Retrieve termination rates information

        Args:
            validate: Whether to validate parameters with Pydantic
            query: Query for searching rates (Example: 'Canada') (required)
            route: Route Code (Values from getRoutes)(Example: '2') (required)

        Returns:
            Response from getTerminationRates operation
        """
        ...

    async def getTimeConditions(
        self,
        validate: bool = True,
        *,
        timecondition: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve time conditions information

        Args:
            validate: Whether to validate parameters with Pydantic
            timecondition: ID for a specific Time Condition (Example: 1830)

        Returns:
            Response from getTimeConditions operation
        """
        ...

    async def getTimezones(
        self,
        validate: bool = True,
        *,
        timezone: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve timezones information

        Args:
            validate: Whether to validate parameters with Pydantic
            timezone: Code for a specific Time Zone (Example: 'America/Buenos_Aires')

        Returns:
            Response from getTimezones operation
        """
        ...

    async def getTransactionHistory(
        self,
        validate: bool = True,
        *,
        date_from: str,
        date_to: str,
    ) -> Dict[str, Any]:
        """Retrieve transaction history information

        Args:
            validate: Whether to validate parameters with Pydantic
            date_from: Start Date for Filtering Transactions (Example: '2016-06-03') (required)
            date_to: End Date for Filtering Transactions (Example: '2016-06-04') (required)

        Returns:
            Response from getTransactionHistory operation
        """
        ...

    async def getVPRIs(
        self,
        validate: bool = True,
    ) -> Dict[str, Any]:
        """Retrieve vpr is information

        Returns:
            Response from getVPRIs operation
        """
        ...

    async def getVoicemailAttachmentFormats(
        self,
        validate: bool = True,
        *,
        email_attachment_format: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve voicemail attachment formats information

        Args:
            validate: Whether to validate parameters with Pydantic
            email_attachment_format: ID for a specific attachment format (Example: wav49)

        Returns:
            Response from getVoicemailAttachmentFormats operation
        """
        ...

    async def getVoicemailFolders(
        self,
        validate: bool = True,
        *,
        folder: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve voicemail folders information

        Args:
            validate: Whether to validate parameters with Pydantic
            folder: Folder Name (Example: 'INBOX')

        Returns:
            Response from getVoicemailFolders operation
        """
        ...

    async def getVoicemailMessageFile(
        self,
        validate: bool = True,
        *,
        folder: str,
        mailbox: int,
        message_num: int,
    ) -> Dict[str, Any]:
        """Retrieve voicemail message file information

        Args:
            validate: Whether to validate parameters with Pydantic
            folder: Name for specific Folder (Example: 'INBOX', values from: getVoicemailFolders) (required)
            mailbox: ID for specific Mailbox (Example: 1001) (required)
            message_num: ID for specific Voicemail Message (Example: 1) (required)

        Returns:
            Response from getVoicemailMessageFile operation
        """
        ...

    async def getVoicemailMessages(
        self,
        validate: bool = True,
        *,
        mailbox: int,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        folder: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve voicemail messages information

        Args:
            validate: Whether to validate parameters with Pydantic
            date_from: Start Date for Filtering Voicemail Messages (Example: '2016-01-30')
            date_to: End Date for Filtering Voicemail Messages (Example: '2016-01-30')
            folder: Name for specific Folder (Example: 'INBOX', values from: getVoicemailFolders)
            mailbox: ID for specific Mailbox (Example: 1001) (required)

        Returns:
            Response from getVoicemailMessages operation
        """
        ...

    async def getVoicemailSetups(
        self,
        validate: bool = True,
        *,
        voicemailsetup: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve voicemail setups information

        Args:
            validate: Whether to validate parameters with Pydantic
            voicemailsetup: ID for a specific Voicemail Setup (Example: 2)

        Returns:
            Response from getVoicemailSetups operation
        """
        ...

    async def getVoicemails(
        self,
        validate: bool = True,
        *,
        mailbox: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve voicemails information

        Args:
            validate: Whether to validate parameters with Pydantic
            mailbox: ID for specific Mailbox (Example: 1001)

        Returns:
            Response from getVoicemails operation
        """
        ...

    async def mailFaxMessagePDF(
        self,
        validate: bool = True,
        *,
        email: Annotated[str, "Format: email"],
        id_: int,
    ) -> Dict[str, Any]:
        """Mail fax message pdf

        Args:
            validate: Whether to validate parameters with Pydantic
            email: Destination email adreess (example: yourname@company.com) (required)
            id_: ID of the Fax Message requested (Values from getFaxMessages) (required)

        Returns:
            Response from mailFaxMessagePDF operation
        """
        ...

    async def markListenedVoicemailMessage(
        self,
        validate: bool = True,
        *,
        folder: str,
        listened: int,
        mailbox: int,
        message_num: int,
    ) -> Dict[str, Any]:
        """Mark listened voicemail message

        Args:
            validate: Whether to validate parameters with Pydantic
            folder: Name for specific Folder (Example: 'INBOX', values from: getVoicemailFolders) (required)
            listened: Code for mark voicemail as listened or not-listened (Values: 'yes'/'no') (required)
            mailbox: ID for specific Mailbox (Example: 1001) (required)
            message_num: ID for specific Voicemail Message (Example: 1) (required)

        Returns:
            Response from markListenedVoicemailMessage operation
        """
        ...

    async def markUrgentVoicemailMessage(
        self,
        validate: bool = True,
        *,
        folder: str,
        mailbox: int,
        message_num: int,
        urgent: int,
    ) -> Dict[str, Any]:
        """Mark urgent voicemail message

        Args:
            validate: Whether to validate parameters with Pydantic
            folder: Name for specific Folder (Example: 'INBOX', values from: getVoicemailFolders) (required)
            mailbox: ID for specific Mailbox (Example: 1001) (required)
            message_num: ID for specific Voicemail Message (Example: 1) (required)
            urgent: Code for mark voicemail as urgent or not-urgent (Values: 'yes'/'no') (required)

        Returns:
            Response from markUrgentVoicemailMessage operation
        """
        ...

    async def moveFaxMessage(
        self,
        validate: bool = True,
        *,
        fax_id: int,
        folder_id: int,
        test: Optional[Literal["true", "false"]] = None,
    ) -> Dict[str, Any]:
        """Move fax message

        Args:
            validate: Whether to validate parameters with Pydantic
            fax_id: ID of the Fax Message requested (Values from getFaxMessages) (required)
            folder_id: ID of the destination Fax Folder (Values from getFaxFolders) (required)
            test: Set to true if testing how to move a Fax Message (accepts: true/false, yes/no, on/off, 1/0, boolean)

        Returns:
            Response from moveFaxMessage operation
        """
        ...

    async def moveFolderVoicemailMessage(
        self,
        validate: bool = True,
        *,
        folder: str,
        mailbox: int,
        message_num: int,
        new_folder: str,
    ) -> Dict[str, Any]:
        """Move folder voicemail message

        Args:
            validate: Whether to validate parameters with Pydantic
            folder: Name for specific Folder (Example: 'INBOX', values from: getVoicemailFolders) (required)
            mailbox: ID for specific Mailbox (Example: 1001) (required)
            message_num: ID for specific Voicemail Message (Example: 1) (required)
            new_folder: Destination Folder (Example: 'Urgent', values from: getVoicemailFolders) (required)

        Returns:
            Response from moveFolderVoicemailMessage operation
        """
        ...

    async def orderDID(
        self,
        validate: bool = True,
        *,
        billing_type: Literal["1", "2"],
        cnam: Literal["0", "1"],
        dialtime: int,
        did: int,
        pop: int,
        routing: int,
        account: Optional[int] = None,
        callerid_prefix: Optional[int] = None,
        failover_busy: Optional[int] = None,
        failover_noanswer: Optional[int] = None,
        failover_unreachable: Optional[int] = None,
        minute: Optional[Annotated[str, "Units: minutes"]] = None,
        monthly: Optional[str] = None,
        note: Optional[int] = None,
        setup: Optional[str] = None,
        test: Optional[Literal["true", "false"]] = None,
        voicemail: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Order did

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Reseller Sub Account (Example: '100001_VoIP')
            billing_type: Billing type for the DID (1 = Per Minute, 2 = Flat) (required)
            callerid_prefix: Caller ID Prefix for the DID
            cnam: CNAM for the DID (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean) (required)
            dialtime: Dial Time Out for the DID (Example: 60 -> in seconds) (required)
            did: DID to be Ordered (Example: 5552223333) (required)
            failover_busy: Busy Routing for the DID
            failover_noanswer: NoAnswer Routing for the DID
            failover_unreachable: Unreachable Routing for the DID
            minute: Minute Rate for Reseller Client (Example: 0.03)
            monthly: Montly Fee for Reseller Client (Example: 3.50)
            note: Note for the DID
            pop: Point of Presence for the DID (Example: 5) (required)
            routing: Main Routing for the DID (required)
            setup: Setup Fee for Reseller Client (Example: 1.99)
            test: Set to true if testing how Orders work - Orders can not be undone - When testing, no Orders are made (accepts: true/false, yes/no, on/off, 1/0, boolean)
            voicemail: Voicemail for the DID (Example: 101)

        Returns:
            Response from orderDID operation

        Note:
            CNAM parameter is converted to '1'/'0' string
        """
        ...

    async def orderDIDInternationalGeographic(
        self,
        validate: bool = True,
        *,
        billing_type: Literal["1", "2"],
        cnam: Literal["0", "1"],
        dialtime: int,
        location_id: int,
        pop: int,
        quantity: int,
        routing: int,
        account: Optional[int] = None,
        callerid_prefix: Optional[int] = None,
        failover_busy: Optional[int] = None,
        failover_noanswer: Optional[int] = None,
        failover_unreachable: Optional[int] = None,
        minute: Optional[Annotated[str, "Units: minutes"]] = None,
        monthly: Optional[str] = None,
        note: Optional[int] = None,
        setup: Optional[str] = None,
        test: Optional[Literal["true", "false"]] = None,
        voicemail: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Order did international geographic

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Reseller Sub Account (Example: '100001_VoIP')
            billing_type: Billing type for the DID (1 = Per Minute, 2 = Flat) (required)
            callerid_prefix: Caller ID Prefix for the DID
            cnam: CNAM for the DID (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean) (required)
            dialtime: Dial Time Out for the DID (Example: 60 -> in seconds) (required)
            failover_busy: Busy Routing for the DID
            failover_noanswer: NoAnswer Routing for the DID
            failover_unreachable: Unreachable Routing for the DID
            location_id: ID for a specific International Location (Values from getDIDsInternationalGeographic) (required)
            minute: Minute Rate for Reseller Client (Example: 0.03)
            monthly: Montly Fee for Reseller Client (Example: 3.50)
            note: Note for the DID
            pop: Point of Presence for the DID (Example: 5) (required)
            quantity: Number of dids to be purchased (Example: 2) (required)
            routing: Main Routing for the DID (required)
            setup: Setup Fee for Reseller Client (Example: 1.99)
            test: Set to true if testing how Orders work - Orders can not be undone - When testing, no Orders are made (accepts: true/false, yes/no, on/off, 1/0, boolean)
            voicemail: Voicemail for the DID (Example: 101)

        Returns:
            Response from orderDIDInternationalGeographic operation
        """
        ...

    async def orderDIDInternationalNational(
        self,
        validate: bool = True,
        *,
        billing_type: Literal["1", "2"],
        cnam: Literal["0", "1"],
        dialtime: int,
        location_id: int,
        pop: int,
        quantity: int,
        routing: int,
        account: Optional[int] = None,
        callerid_prefix: Optional[int] = None,
        failover_busy: Optional[int] = None,
        failover_noanswer: Optional[int] = None,
        failover_unreachable: Optional[int] = None,
        minute: Optional[Annotated[str, "Units: minutes"]] = None,
        monthly: Optional[str] = None,
        note: Optional[int] = None,
        setup: Optional[str] = None,
        test: Optional[Literal["true", "false"]] = None,
        voicemail: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Order did international national

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Reseller Sub Account (Example: '100001_VoIP')
            billing_type: Billing type for the DID (1 = Per Minute, 2 = Flat) (required)
            callerid_prefix: Caller ID Prefix for the DID
            cnam: CNAM for the DID (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean) (required)
            dialtime: Dial Time Out for the DID (Example: 60 -> in seconds) (required)
            failover_busy: Busy Routing for the DID
            failover_noanswer: NoAnswer Routing for the DID
            failover_unreachable: Unreachable Routing for the DID
            location_id: ID for a specific International Location (Values from getDIDsInternationalNational) (required)
            minute: Minute Rate for Reseller Client (Example: 0.03)
            monthly: Montly Fee for Reseller Client (Example: 3.50)
            note: Note for the DID
            pop: Point of Presence for the DID (Example: 5) (required)
            quantity: Number of dids to be purchased (Example: 2) (required)
            routing: Main Routing for the DID (required)
            setup: Setup Fee for Reseller Client (Example: 1.99)
            test: Set to true if testing how Orders work - Orders can not be undone - When testing, no Orders are made (accepts: true/false, yes/no, on/off, 1/0, boolean)
            voicemail: Voicemail for the DID (Example: 101)

        Returns:
            Response from orderDIDInternationalNational operation
        """
        ...

    async def orderDIDInternationalTollFree(
        self,
        validate: bool = True,
        *,
        cnam: Literal["0", "1"],
        dialtime: int,
        location_id: int,
        pop: int,
        quantity: int,
        routing: int,
        account: Optional[int] = None,
        callerid_prefix: Optional[int] = None,
        failover_busy: Optional[int] = None,
        failover_noanswer: Optional[int] = None,
        failover_unreachable: Optional[int] = None,
        minute: Optional[Annotated[str, "Units: minutes"]] = None,
        monthly: Optional[str] = None,
        note: Optional[int] = None,
        setup: Optional[str] = None,
        test: Optional[Literal["true", "false"]] = None,
        voicemail: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Order did international toll free

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Reseller Sub Account (Example: '100001_VoIP')
            callerid_prefix: Caller ID Prefix for the DID
            cnam: CNAM for the DID (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean) (required)
            dialtime: Dial Time Out for the DID (Example: 60 -> in seconds) (required)
            failover_busy: Busy Routing for the DID
            failover_noanswer: NoAnswer Routing for the DID
            failover_unreachable: Unreachable Routing for the DID
            location_id: ID for a specific International Location (Values from getDIDsInternationalTollFree) (required)
            minute: Minute Rate for Reseller Client (Example: 0.03)
            monthly: Montly Fee for Reseller Client (Example: 3.50)
            note: Note for the DID
            pop: Point of Presence for the DID (Example: 5) (required)
            quantity: Number of dids to be purchased (Example: 2) (required)
            routing: Main Routing for the DID (required)
            setup: Setup Fee for Reseller Client (Example: 1.99)
            test: Set to true if testing how Orders work - Orders can not be undone - When testing, no Orders are made (accepts: true/false, yes/no, on/off, 1/0, boolean)
            voicemail: Voicemail for the DID (Example: 101)

        Returns:
            Response from orderDIDInternationalTollFree operation
        """
        ...

    async def orderDIDVirtual(
        self,
        validate: bool = True,
        *,
        cnam: Literal["0", "1"],
        dialtime: int,
        digits: int,
        pop: int,
        routing: int,
        account: Optional[int] = None,
        callerid_prefix: Optional[int] = None,
        failover_busy: Optional[int] = None,
        failover_noanswer: Optional[int] = None,
        failover_unreachable: Optional[int] = None,
        minute: Optional[Annotated[str, "Units: minutes"]] = None,
        monthly: Optional[str] = None,
        note: Optional[int] = None,
        setup: Optional[str] = None,
        test: Optional[Literal["true", "false"]] = None,
        voicemail: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Order did virtual

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Reseller Sub Account (Example: '100001_VoIP')
            callerid_prefix: Caller ID Prefix for the DID
            cnam: CNAM for the DID (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean) (required)
            dialtime: Dial Time Out for the DID (Example: 60 -> in seconds) (required)
            digits: Three Digits for the new Virtual DID (Example: 001) (required)
            failover_busy: Busy Routing for the DID
            failover_noanswer: NoAnswer Routing for the DID
            failover_unreachable: Unreachable Routing for the DID
            minute: Minute Rate for Reseller Client (Example: 0.03)
            monthly: Montly Fee for Reseller Client (Example: 3.50)
            note: Note for the DID
            pop: Point of Presence for the DID (Example: 5) (required)
            routing: Main Routing for the DID (required)
            setup: Setup Fee for Reseller Client (Example: 1.99)
            test: Set to true if testing how Orders work - Orders can not be undone - When testing, no Orders are made (accepts: true/false, yes/no, on/off, 1/0, boolean)
            voicemail: Voicemail for the DID (Example: 101)

        Returns:
            Response from orderDIDVirtual operation
        """
        ...

    async def orderFaxNumber(
        self,
        validate: bool = True,
        *,
        location: int,
        quantity: str,
        email: Optional[Annotated[str, "Format: email"]] = None,
        email_attach_file: Optional[Annotated[str, "Format: pdf"]] = None,
        email_enable: Optional[str] = None,
        test: Optional[Literal["true", "false"]] = None,
        url_callback: Optional[str] = None,
        url_callback_enable: Optional[str] = None,
        url_callback_retry: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Order fax number

        Args:
            validate: Whether to validate parameters with Pydantic
            email: Email address where send notifications when receive Fax Messages - (Example: yourname@company.com)
            email_attach_file: Flag to enable attach the Fax Message as a PDF file in the notifications. - (Values: 1 = true, 0 = false) - Default: 0
            email_enable: Flag to enable the email notifications. - (Values: 1 = true, 0 = false) - Default: 0
            location: Location ID of the Fax Number (Values from getFaxRateCentersCAN/getFaxRateCentersUSA) (required)
            quantity: Quantity of Fax Numbers to order (Example: 3) (required)
            test: Set to true if testing how Orders work - Orders can not be undone - When testing, no Orders are made (accepts: true/false, yes/no, on/off, 1/0, boolean)
            url_callback: URL where make a POST when you receive a Fax Message.
            url_callback_enable: Flag to enable the URL Callback functionality. - (Values: 1 = true, 0 = false) - Default: 0
            url_callback_retry: Flag to enable retry the POST action in case we don't receive "ok".

        Returns:
            Response from orderFaxNumber operation
        """
        ...

    async def orderTollFree(
        self,
        validate: bool = True,
        *,
        cnam: Literal["0", "1"],
        dialtime: int,
        did: int,
        pop: int,
        routing: int,
        account: Optional[int] = None,
        callerid_prefix: Optional[int] = None,
        failover_busy: Optional[int] = None,
        failover_noanswer: Optional[int] = None,
        failover_unreachable: Optional[int] = None,
        minute: Optional[Annotated[str, "Units: minutes"]] = None,
        monthly: Optional[str] = None,
        note: Optional[int] = None,
        setup: Optional[str] = None,
        test: Optional[Literal["true", "false"]] = None,
        voicemail: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Order toll free

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Reseller Sub Account (Example: '100001_VoIP')
            callerid_prefix: Caller ID Prefix for the DID
            cnam: CNAM for the DID (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean) (required)
            dialtime: Dial Time Out for the DID (Example: 60 -> in seconds) (required)
            did: DID to be Ordered (Example: 8772223333) (required)
            failover_busy: Busy Routing for the DID
            failover_noanswer: NoAnswer Routing for the DID
            failover_unreachable: Unreachable Routing for the DID
            minute: Minute Rate for Reseller Client (Example: 0.03)
            monthly: Montly Fee for Reseller Client (Example: 3.50)
            note: Note for the DID
            pop: Point of Presence for the DID (Example: 5) (required)
            routing: Main Routing for the DID (required)
            setup: Setup Fee for Reseller Client (Example: 1.99)
            test: Set to true if testing how Orders work - Orders can not be undone - When testing, no Orders are made (accepts: true/false, yes/no, on/off, 1/0, boolean)
            voicemail: Voicemail for the DID (Example: 101)

        Returns:
            Response from orderTollFree operation
        """
        ...

    async def orderVanity(
        self,
        validate: bool = True,
        *,
        carrier: int,
        cnam: Literal["0", "1"],
        dialtime: int,
        did: int,
        pop: int,
        routing: int,
        account: Optional[int] = None,
        callerid_prefix: Optional[int] = None,
        failover_busy: Optional[int] = None,
        failover_noanswer: Optional[int] = None,
        failover_unreachable: Optional[int] = None,
        minute: Optional[Annotated[str, "Units: minutes"]] = None,
        monthly: Optional[str] = None,
        note: Optional[int] = None,
        setup: Optional[str] = None,
        test: Optional[Literal["true", "false"]] = None,
        voicemail: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Order vanity

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Reseller Sub Account (Example: '100001_VoIP')
            callerid_prefix: Caller ID Prefix for the DID
            carrier: Carrier for the DID (Values from getCarriers) (required)
            cnam: CNAM for the DID (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean) (required)
            dialtime: Dial Time Out for the DID (Example: 60 -> in seconds) (required)
            did: DID to be Ordered (Example: 8772223333) (required)
            failover_busy: Busy Routing for the DID
            failover_noanswer: NoAnswer Routing for the DID
            failover_unreachable: Unreachable Routing for the DID
            minute: Minute Rate for Reseller Client (Example: 0.03)
            monthly: Montly Fee for Reseller Client (Example: 3.50)
            note: Note for the DID
            pop: Point of Presence for the DID (Example: 5) (required)
            routing: Main Routing for the DID (required)
            setup: Setup Fee for Reseller Client (Example: 1.99)
            test: Set to true if testing how Orders work - Orders can not be undone - When testing, no Orders are made (accepts: true/false, yes/no, on/off, 1/0, boolean)
            voicemail: Voicemail for the DID (Example: 101)

        Returns:
            Response from orderVanity operation
        """
        ...

    async def removeDIDvPRI(
        self,
        validate: bool = True,
        *,
        did: int,
        vpri: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Remove di dv pri

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID Number to be remove from our Vpri (Example: 561115) (required)
            vpri: Id for specific Vpri

        Returns:
            Response from removeDIDvPRI operation
        """
        ...

    async def searchDIDsCAN(
        self,
        validate: bool = True,
        *,
        query: str,
        type_: str,
        province: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Search for di ds can

        Args:
            validate: Whether to validate parameters with Pydantic
            province: Canadian Province (Values from getProvinces)
            query: Query for searching (Examples: 'JOHN', '555', '123ABC') (required)
            type_: Type of search (Values: 'starts', 'contains', 'ends') (required)

        Returns:
            Response from searchDIDsCAN operation
        """
        ...

    async def searchDIDsUSA(
        self,
        validate: bool = True,
        *,
        query: str,
        type_: str,
        state: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Search for di ds usa

        Args:
            validate: Whether to validate parameters with Pydantic
            query: Query for searching (Examples: 'JOHN', '555', '123ABC') (required)
            state: United States State (Values from getStates)
            type_: Type of search (Values: 'starts', 'contains', 'ends') (required)

        Returns:
            Response from searchDIDsUSA operation
        """
        ...

    async def searchFaxAreaCodeCAN(
        self,
        validate: bool = True,
        *,
        area_code: int,
    ) -> Dict[str, Any]:
        """Search for fax area code can

        Args:
            validate: Whether to validate parameters with Pydantic
            area_code: Area code number, as the initial of the Fax Number you looking for. (values from getFaxRateCentersCAN) (required)

        Returns:
            Response from searchFaxAreaCodeCAN operation
        """
        ...

    async def searchFaxAreaCodeUSA(
        self,
        validate: bool = True,
        *,
        area_code: int,
    ) -> Dict[str, Any]:
        """Search for fax area code usa

        Args:
            validate: Whether to validate parameters with Pydantic
            area_code: Area code number, as the initial of the Fax Number you looking for. (values from getFaxRateCentersUSA) (required)

        Returns:
            Response from searchFaxAreaCodeUSA operation
        """
        ...

    async def searchTollFreeCanUS(
        self,
        validate: bool = True,
        *,
        query: Optional[str] = None,
        type_: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Search for toll free can us

        Args:
            validate: Whether to validate parameters with Pydantic
            query: Query for searching (Examples: 'JOHN', '555', '123ABC')
            type_: Type of search (Values: 'starts', 'contains', 'ends')

        Returns:
            Response from searchTollFreeCanUS operation
        """
        ...

    async def searchTollFreeUSA(
        self,
        validate: bool = True,
        *,
        query: Optional[str] = None,
        type_: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Search for toll free usa

        Args:
            validate: Whether to validate parameters with Pydantic
            query: Query for searching (Examples: 'JOHN', '555', '123ABC')
            type_: Type of search (Values: 'starts', 'contains', 'ends')

        Returns:
            Response from searchTollFreeUSA operation
        """
        ...

    async def searchVanity(
        self,
        validate: bool = True,
        *,
        query: str,
        type_: str,
    ) -> Dict[str, Any]:
        """Search for vanity

        Args:
            validate: Whether to validate parameters with Pydantic
            query: Query for searching : 7 Chars Examples: '***JHON', '**555**', '**HELLO' (required)
            type_: Type of Vanity Number Values: '8**', '800', '833', '844', '855', '866', '877', '888' (required)

        Returns:
            Response from searchVanity operation
        """
        ...

    async def sendCallRecordingEmail(
        self,
        validate: bool = True,
        *,
        account: int,
        callrecording: str,
        email: str,
    ) -> Dict[str, Any]:
        """Send call recording email

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Filter Call Recordings by Account (Values from getCallAccounts) (required)
            callrecording: Call Recording (Values from getCallRecordings) (required)
            email: Email to send call recording (required)

        Returns:
            Response from sendCallRecordingEmail operation
        """
        ...

    async def sendFaxMessage(
        self,
        validate: bool = True,
        *,
        file: int,
        from_name: str,
        from_number: int,
        to_number: int,
        send_email: Optional[Annotated[str, "Format: email"]] = None,
        send_email_enabled: Optional[str] = None,
        station_id: Optional[int] = None,
        test: Optional[Literal["true", "false"]] = None,
    ) -> Dict[str, Any]:
        """Send fax message

        Args:
            validate: Whether to validate parameters with Pydantic
            file: The file must be encoded in Base64, and in one of the following formats: pdf, txt, jpg, gif, png, tif (required)
            from_name: Name of the sender (Example: 5552341234) (required)
            from_number: DID number of the Fax sender (required)
            send_email: Email address where you want send a copy of your Fax.
            send_email_enabled: Flag to enable the send of a copy of your Fax via email. - (Values: 1 = true, 0 = false) - Default: 0
            station_id: An word to identify a equipment or department sending the Fax.
            test: Set to true if testing how to send a Fax Message (accepts: true/false, yes/no, on/off, 1/0, boolean)
            to_number: Destination DID Number (Example: 5552341234) (required)

        Returns:
            Response from sendFaxMessage operation
        """
        ...

    async def sendMMS(
        self,
        validate: bool = True,
        *,
        did: int,
        dst: str,
        message: str,
        media1: Optional[Annotated[str, "Units: milliseconds"]] = None,
        media2: Optional[int] = None,
        media3: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Send mms

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID Numbers which is sending the message (Example: 5551234567) (required)
            dst: Destination Number (Example: 5551234568) (required)
            media1: [Optional]  Url to media file (Example: 'https://voip.ms/themes/voipms/assets/img/talent.jpg?v=2'
            media2: [Optional] Base 64 image encode (Example: data:image/png;base64,iVBORw0KGgoAAAANSUh...)
            media3: [Optional] Empty value (Example: '' )
            message: Message to be sent (Example: 'hello John Smith' max chars: 2048) (required)

        Returns:
            Response from sendMMS operation
        """
        ...

    async def sendSMS(
        self,
        validate: bool = True,
        *,
        did: int,
        dst: str,
        message: str,
    ) -> Dict[str, Any]:
        """Send sms

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID Numbers which is sending the message (Example: 5551234567) (required)
            dst: Destination Number (Example: 5551234568) (required)
            message: Message to be sent (Example: 'hello John Smith' max chars: 160) (required)

        Returns:
            Response from sendSMS operation
        """
        ...

    async def sendVoicemailEmail(
        self,
        validate: bool = True,
        *,
        email_address: Annotated[str, "Format: email"],
        folder: str,
        mailbox: int,
        message_num: int,
    ) -> Dict[str, Any]:
        """Send voicemail email

        Args:
            validate: Whether to validate parameters with Pydantic
            email_address: Destination Email address (Example: john.doe@my-domain.com) (required)
            folder: Name for specific Folder (Example: 'INBOX', values from: getVoicemailFolders) (required)
            mailbox: ID for specific Mailbox (Example: 1001) (required)
            message_num: ID for specific Voicemail Message (Example: 1) (required)

        Returns:
            Response from sendVoicemailEmail operation
        """
        ...

    async def setCallHunting(
        self,
        validate: bool = True,
        *,
        description: str,
        language: str,
        members: str,
        music: int,
        order: str,
        press: str,
        recording: str,
        ring_time: str,
        callhunting: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update call hunting settings

        Args:
            validate: Whether to validate parameters with Pydantic
            callhunting: ID for a specific Call Hunting (Example: 235 / Leave empty to create a new one)
            description: Description for the Call Hunting (required)
            language: Language for the Call Hunting (values from getLanguages) (required)
            members: The list of members assigned to the call hunting (required)
            music: Music on Hold Code (Values from getMusicOnHold) (required)
            order: The members will be called in follow or random order (values follow or random) (required)
            press: This option confirm if the member will take the call by pressing 1 * ring_time and press parameters need to have the same amount of items as the members parameter, one for each member. (required)
            recording: Recording for the Call Hunting (values from getRecordings) (required)
            ring_time: The Maximum amount of time the call will ring the member (required)

        Returns:
            Response from setCallHunting operation
        """
        ...

    async def setCallParking(
        self,
        validate: bool = True,
        *,
        delay: int,
        destination: int,
        failover: str,
        language: str,
        music: int,
        name: str,
        timeout: int,
        callparking: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update call parking settings

        Args:
            validate: Whether to validate parameters with Pydantic
            callparking: ID for a specific Call Parking (Example: 235 / Leave empty to create a new one)
            delay: The number of seconds before the Announce Destination receives an automatic call from the system to announce the extension of the parked call (required)
            destination: The system will make an automatic call to this destination to announce the extension of the parked call. (Values: parker, main account or sub-accounts) (required)
            failover: Final destination where the call will be forwarded if it isn’t answered. (Values: callback, system:hangup, vm:mailbox) (required)
            language: Language for the Call Parking (values from getLanguages) (required)
            music: Music on Hold Code (Values from getMusicOnHold) (required)
            name: Name for the Call Parking (required)
            timeout: The number of seconds a call will stay parked before it is forwarded to the Failover Destination (required)

        Returns:
            Response from setCallParking operation
        """
        ...

    async def setCallback(
        self,
        validate: bool = True,
        *,
        delay_before: str,
        description: str,
        digit_timeout: str,
        number: str,
        response_timeout: str,
        callback: Optional[int] = None,
        callerid_number: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update callback settings

        Args:
            validate: Whether to validate parameters with Pydantic
            callback: ID for a specific Callback (Example: 2359 / Leave empty to create a new one)
            callerid_number: Caller ID Override for the callback
            delay_before: Delay befor calling back (required)
            description: Description for the Callback (required)
            digit_timeout: Time between digits input (required)
            number: Number that will be called back (required)
            response_timeout: Time before hanging up for incomplete input (required)

        Returns:
            Response from setCallback operation
        """
        ...

    async def setCallerIDFiltering(
        self,
        validate: bool = True,
        *,
        callerid: int,
        did: int,
        routing: str,
        failover_busy: Optional[str] = None,
        failover_noanswer: Optional[str] = None,
        failover_unreachable: Optional[str] = None,
        filter: Optional[int] = None,
        note: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update caller id filtering settings

        Args:
            validate: Whether to validate parameters with Pydantic
            callerid: Caller ID that triggers the Filter (i = Not North American format, 0 = Anonymous, NPANXXXXXX, s or sb or sc = STIR/SHAKEN Attestation Level, p = All Phone Book, p:XXXX = Specific Phone Book Group) (required)
            did: DIDs affected by the filter (all, NPANXXXXXX) (required)
            failover_busy: Route the call follows when busy
            failover_noanswer: Route the call follows when noanswer
            failover_unreachable: Route the call follows when unreachable
            filter: ID for a specific Caller ID Filtering (Example: 18915 / Leave empty to create a new one)
            note: Note for the Caller ID Filtering
            routing: Route the call follows when filter is triggered (required)

        Returns:
            Response from setCallerIDFiltering operation
        """
        ...

    async def setClient(
        self,
        validate: bool = True,
        *,
        client: int,
        email: str,
        firstname: str,
        lastname: str,
        password: str,
        phone_number: Annotated[str, "Format: phone"],
        address: Optional[str] = None,
        balance_management: Optional[str] = None,
        city: Optional[str] = None,
        company: Optional[str] = None,
        country: Optional[int] = None,
        state: Optional[str] = None,
        zip: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update client settings

        Args:
            validate: Whether to validate parameters with Pydantic
            address: Client's Address
            balance_management: Balance Management for Client (Values from getBalanceManagement)
            city: Client's City
            client: ID for a specific Reseller Client (Example: 561115) (required)
            company: Client's Company
            country: Client's Country (Values from getCountries)
            email: Client's e-mail (required)
            firstname: Client's Firstname (required)
            lastname: Client's Lastname (required)
            password: Client's Password (required)
            phone_number: Client's Phone Number (required)
            state: Client's State
            zip: Client's Zip Code

        Returns:
            Response from setClient operation
        """
        ...

    async def setClientThreshold(
        self,
        validate: bool = True,
        *,
        client: int,
        threshold: Annotated[str, "Range: 1-250"],
        email: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update client threshold settings

        Args:
            validate: Whether to validate parameters with Pydantic
            client: ID for a specific Reseller Client (Example: 561115) (required)
            email: Client's e-mail for balance threshold notification
            threshold: Threshold amount between 1 and 250 (Example: 10) (required)

        Returns:
            Response from setClientThreshold operation
        """
        ...

    async def setConference(
        self,
        validate: bool = True,
        *,
        conference: int,
        description: str,
        max_members: str,
        name: str,
        language: Optional[str] = None,
        members: Optional[str] = None,
        sound_error_menu: Optional[str] = None,
        sound_get_pin: Optional[str] = None,
        sound_has_joined: Optional[str] = None,
        sound_has_left: Optional[str] = None,
        sound_invalid_pin: Optional[int] = None,
        sound_join: Optional[str] = None,
        sound_kicked: Optional[str] = None,
        sound_leave: Optional[str] = None,
        sound_locked: Optional[str] = None,
        sound_locked_now: Optional[str] = None,
        sound_muted: Optional[str] = None,
        sound_only_one: Optional[str] = None,
        sound_only_person: Optional[str] = None,
        sound_other_in_party: Optional[int] = None,
        sound_participants_muted: Optional[str] = None,
        sound_participants_unmuted: Optional[str] = None,
        sound_place_into_conference: Optional[str] = None,
        sound_there_are: Optional[str] = None,
        sound_unlocked_now: Optional[str] = None,
        sound_unmuted: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update conference settings

        Args:
            validate: Whether to validate parameters with Pydantic
            conference: ID for a specific Conference (Example: 5356) (required)
            description: Conference description (required)
            language: Conference Language (Values from getLanguages)
            max_members: Members Max Value (required)
            members: Conference Members
            name: Conference name (required)
            sound_error_menu: The recording played when there is an error on the menu. (Values from getRecordings)
            sound_get_pin: The recording played when prompting for a conference PIN (Values from getRecordings)
            sound_has_joined: The recording played as a user intro (Values from getRecordings)
            sound_has_left: The recording played as a user leaves the conference (Values from getRecordings)
            sound_invalid_pin: The recording played when an invalid PIN is entered too many (3) times (Values from getRecordings)
            sound_join: The recording played when a user joins, typically some kind of beep sound (Values from getRecordings)
            sound_kicked: The recording played to a user who has been kicked from the conference (Values from getRecordings)
            sound_leave: The recording played when a user leaves, typically some kind of beep sound (Values from getRecordings)
            sound_locked: The recording played to a user trying to join a locked conference (Values from getRecordings)
            sound_locked_now: The recording played to an Admin-level user after toggling the conference to locked mode (Values from getRecordings)
            sound_muted: The recording played to a user when the mute option is toggled on (Values from getRecordings)
            sound_only_one: The recording played to a user when there is only one other person in the conference. (Values from getRecordings)
            sound_only_person: The recording played when a user is the only person in the conference (Values from getRecordings)
            sound_other_in_party: The recording used in conjunction with the There are option, used like There are (number of participants) Other in party (Values from getRecordings)
            sound_participants_muted: The recording played when all non-admin participants are muted. (Values from getRecordings)
            sound_participants_unmuted: The recording played when all non-admin participants are unmuted. (Values from getRecordings)
            sound_place_into_conference: The recording played when a user is placed into a conference that cannot start until a marked user enters (Values from getRecordings)
            sound_there_are: The recording played when announcing how many users there are in a conference. (Values from getRecordings)
            sound_unlocked_now: The recording played to an Admin-level user after toggling the conference to unlocked mode (Values from getRecordings)
            sound_unmuted: The recording played to a user when the mute option is toggled off (Values from getRecordings)

        Returns:
            Response from setConference operation
        """
        ...

    async def setConferenceMember(
        self,
        validate: bool = True,
        *,
        conference: int,
        member: int,
        name: str,
        admin: Optional[Literal["yes", "no"]] = None,
        announce_join_leave: Optional[Literal["yes", "no"]] = None,
        announce_only_user: Optional[Literal["yes", "no"]] = None,
        announce_user_count: Optional[Literal["yes", "no"]] = None,
        announcement: Optional[str] = None,
        description: Optional[str] = None,
        drop_silence: Optional[Literal["yes", "no"]] = None,
        jitter_buffer: Optional[Literal["yes", "no"]] = None,
        moh_when_empty: Optional[str] = None,
        pin: Optional[str] = None,
        quiet: Optional[Literal["yes", "no"]] = None,
        silence_threshold: Optional[Literal["2000", "2100", "2200", "2300", "2400", "2500", "2600", "2700", "2800", "2900"]] = None,
        start_muted: Optional[Literal["yes", "no"]] = None,
        talk_detection: Optional[Literal["yes", "no"]] = None,
        talking_threshold: Optional[Literal["100", "120", "140", "160", "180", "200", "220", "240"]] = None,
    ) -> Dict[str, Any]:
        """Update conference member settings

        Args:
            validate: Whether to validate parameters with Pydantic
            admin: Sets if the member is an admin or not (yes/no). (accepts: yes/no, true/false, on/off, 1/0, boolean)
            announce_join_leave: Sets if the conference recording when a member joins or leaves will be played (yes/no). (accepts: yes/no, true/false, on/off, 1/0, boolean)
            announce_only_user: Sets if the "only user" announcement should be played when a caller enters an empty conference (yes/no). (accepts: yes/no, true/false, on/off, 1/0, boolean)
            announce_user_count: Sets if the number of members in the conference should be announced to the caller as he joins (yes/no). (accepts: yes/no, true/false, on/off, 1/0, boolean)
            announcement: If set, this recording will be heard only by the user as he joins the conference (Values from getRecordings).
            conference: ID for a specific Conference (Example: 5356) (required)
            description: Member description.
            drop_silence: The system will drop what is detected as silence from entering into the conference (yes/no). (accepts: yes/no, true/false, on/off, 1/0, boolean)
            jitter_buffer: When set to YES, the system will place a jitter buffer on the caller's audio stream before any audio mixing is performed (yes/no). (accepts: yes/no, true/false, on/off, 1/0, boolean)
            member: ID for a specific Member profile (Example: 5356) (required)
            moh_when_empty: Sets whether music on hold (MOH) should be played when only one person is in the conference (Values from getMusicOnHold).
            name: Member name. (required)
            pin: Assigned PIN.
            quiet: When set to "yes", enter/leave prompts and user introductions are not played (yes/no). (accepts: yes/no, true/false, on/off, 1/0, boolean)
            silence_threshold: The time, in milliseconds, that silence needs to be present in the user’s sound stream before the system can consider it to be in fact silent and close the audio (allowed values are 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900 or 3000).
            start_muted: Sets if the member should start out muted after entering the conference (yes/no). (accepts: yes/no, true/false, on/off, 1/0, boolean)
            talk_detection: If set to YES, the conference dashboard will display a notification when a participant starts and stops talking (yes/no). (accepts: yes/no, true/false, on/off, 1/0, boolean)
            talking_threshold: The time, in milliseconds, that a users needs to be sending sound or voice before the system can consider them to be talking (allowed values are 100, 120, 140, 160, 180, 200, 220, 240 or 250).

        Returns:
            Response from setConferenceMember operation
        """
        ...

    async def setDIDBillingType(
        self,
        validate: bool = True,
        *,
        billing_type: Literal["1", "2"],
        did: int,
    ) -> Dict[str, Any]:
        """Update did billing type settings

        Args:
            validate: Whether to validate parameters with Pydantic
            billing_type: Billing type for the DID (1 = Per Minute, 2 = Flat) (required)
            did: DID affected by the new billing plan (required)

        Returns:
            Response from setDIDBillingType operation
        """
        ...

    async def setDIDInfo(
        self,
        validate: bool = True,
        *,
        billing_type: Literal["1", "2"],
        cnam: Literal["0", "1"],
        dialtime: int,
        did: int,
        pop: int,
        routing: int,
        callerid_prefix: Optional[int] = None,
        failover_busy: Optional[int] = None,
        failover_noanswer: Optional[int] = None,
        failover_unreachable: Optional[int] = None,
        note: Optional[int] = None,
        port_out_pin: Optional[int] = None,
        record_calls: Optional[Literal["0", "1"]] = None,
        transcribe: Optional[Literal["0", "1"]] = None,
        transcription_email: Optional[str] = None,
        transcription_locale: Optional[str] = None,
        transcription_start_delay: Optional[Annotated[str, "Range: 0-60; Units: seconds"]] = None,
        voicemail: Optional[int] = None,
        voicemail_threshold: Optional[Annotated[str, "Range: 0-60; Units: seconds"]] = None,
    ) -> Dict[str, Any]:
        """Update did info settings

        Args:
            validate: Whether to validate parameters with Pydantic
            billing_type: Billing type for the DID (1 = Per Minute, 2 = Flat) (required)
            callerid_prefix: Caller ID Prefix for the DID
            cnam: CNAM for the DID (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean) (required)
            dialtime: Dial Time Out for the DID (Example: 60 -> in seconds) (required)
            did: DID to be Updated (Example: 5551234567) (required)
            failover_busy: Busy Routing for the DID
            failover_noanswer: NoAnswer Routing for the DID
            failover_unreachable: Unreachable Routing for the DID
            note: Note for the DID
            pop: Point of Presence for the DID ("server_pop" values from getServersInfo. Example: 3) (required)
            port_out_pin: Port Out PIN protection is used as a means of authorizing outgoing portability (only for selected US numbers with the lock icon)
            record_calls: Record Calls (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            routing: Main Routing for the DID (required)
            transcribe: Enable Call Transcription (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            transcription_email: Call Transcription Email
            transcription_locale: Call Transcription Locale (values from getLocales)
            transcription_start_delay: Call Transcription Delay Seconds between 0 and 60, Increments of 5 (Example: 10 -> seconds)
            voicemail: Voicemail for the DID
            voicemail_threshold: Voicemail Threshold Seconds between 0 and 60, Increments of 5 (Example: 10 -> seconds)

        Returns:
            Response from setDIDInfo operation
        """
        ...

    async def setDIDPOP(
        self,
        validate: bool = True,
        *,
        did: int,
        pop: int,
    ) -> Dict[str, Any]:
        """Update didpop settings

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID to be Updated (Example: 5551234567) (required)
            pop: Point of Presence for the DID ("server_pop" values from getServersInfo. Example: 3) (required)

        Returns:
            Response from setDIDPOP operation
        """
        ...

    async def setDIDRouting(
        self,
        validate: bool = True,
        *,
        did: int,
        routing: int,
    ) -> Dict[str, Any]:
        """Update did routing settings

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID to be Updated (Example: 5551234567) (required)
            routing: Main Routing for the DID (required)

        Returns:
            Response from setDIDRouting operation
        """
        ...

    async def setDIDVoicemail(
        self,
        validate: bool = True,
        *,
        did: int,
        voicemail: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update did voicemail settings

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID to be Updated (Example: 5551234567) (required)
            voicemail: Mailbox for the DID

        Returns:
            Response from setDIDVoicemail operation
        """
        ...

    async def setDISA(
        self,
        validate: bool = True,
        *,
        digit_timeout: str,
        name: str,
        pin: str,
        callerid_override: Optional[int] = None,
        disa: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update disa settings

        Args:
            validate: Whether to validate parameters with Pydantic
            callerid_override: Caller ID Override for the DISA
            digit_timeout: Time between digits (required)
            disa: ID for a specific DISA (Example: 2114 / Leave empty to create a new one)
            name: Name for the DISA (required)
            pin: Password for the DISA (required)

        Returns:
            Response from setDISA operation
        """
        ...

    async def setEmailToFax(
        self,
        validate: bool = True,
        *,
        auth_email: Annotated[str, "Format: email"],
        from_number_id: str,
        security_code: int,
        enabled: Optional[Literal["0", "1"]] = None,
        id_: Optional[int] = None,
        security_code_enabled: Optional[Literal["0", "1"]] = None,
        test: Optional[Literal["true", "false"]] = None,
    ) -> Dict[str, Any]:
        """Update email to fax settings

        Args:
            validate: Whether to validate parameters with Pydantic
            auth_email: Email address from you will sent Fax Messages (required)
            enabled: If Enable, we will send Fax Message when we receive an email from the provided address. (Values:1=Enable / 0=Disable) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            from_number_id: Fax number that will appear as fax sender. (values from getFaxNumbersInfo) (required)
            id_: [Only for updates] ID of the "Email to Fax" to edit (Values from getEmailToFax)
            security_code: An alphanumeric code to identify your emails before send as Fax. (required)
            security_code_enabled: If Enable, we will check the mail subject if this include a Security Code before send the Fax. (Values:1=Enable / 0=Disable) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            test: Set to true if testing. (accepts: true/false, yes/no, on/off, 1/0, boolean)

        Returns:
            Response from setEmailToFax operation
        """
        ...

    async def setFaxFolder(
        self,
        validate: bool = True,
        *,
        name: str,
        id_: Optional[int] = None,
        test: Optional[Literal["true", "false"]] = None,
    ) -> Dict[str, Any]:
        """Update fax folder settings

        Args:
            validate: Whether to validate parameters with Pydantic
            id_: [Only for updates] ID of the Fax Folder to edit (Values from getFaxFolders)
            name: Name of the Fax Folder to create or update (Example: FAMILY) (required)
            test: Set to true if testing how to create/update a Fax Folder (accepts: true/false, yes/no, on/off, 1/0, boolean)

        Returns:
            Response from setFaxFolder operation
        """
        ...

    async def setFaxNumberEmail(
        self,
        validate: bool = True,
        *,
        did: int,
        email: Optional[Annotated[str, "Format: email"]] = None,
        email_attach_file: Optional[Annotated[str, "Format: pdf"]] = None,
        email_enable: Optional[str] = None,
        test: Optional[Literal["true", "false"]] = None,
    ) -> Dict[str, Any]:
        """Update fax number email settings

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID Number to be ported into our network (Example: 5552341234) (required)
            email: Email address where send notifications when receive Fax Messages - (Example: yourname@company.com)
            email_attach_file: Flag to enable attach the Fax Message as a PDF file in the notifications. - (Values: 1 = true, 0 = false) - Default: 0
            email_enable: Flag to enable the email notifications. - (Values: 1 = true, 0 = false) - Default: 0
            test: Set to true if testing how to set the email of a Fax Number (accepts: true/false, yes/no, on/off, 1/0, boolean)

        Returns:
            Response from setFaxNumberEmail operation
        """
        ...

    async def setFaxNumberInfo(
        self,
        validate: bool = True,
        *,
        did: int,
        email: Optional[Annotated[str, "Format: email"]] = None,
        email_attach_file: Optional[Annotated[str, "Format: pdf"]] = None,
        email_enable: Optional[str] = None,
        test: Optional[Literal["true", "false"]] = None,
        url_callback: Optional[str] = None,
        url_callback_enable: Optional[str] = None,
        url_callback_retry: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update fax number info settings

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID Number to be ported into our network (Example: 5552341234) (required)
            email: Email address where send notifications when receive Fax Messages - (Example: yourname@company.com)
            email_attach_file: Flag to enable attach the Fax Message as a PDF file in the notifications. - (Values: 1 = true, 0 = false) - Default: 0
            email_enable: Flag to enable the email notifications. - (Values: 1 = true, 0 = false) - Default: 0
            test: Set to true if testing how to update the information of a Fax Number (accepts: true/false, yes/no, on/off, 1/0, boolean)
            url_callback: URL where make a POST when you receive a Fax Message.
            url_callback_enable: Flag to enable the URL Callback functionality. - (Values: 1 = true, 0 = false) - Default: 0
            url_callback_retry: Flag to enable retry the POST action in case we don't receive "ok".

        Returns:
            Response from setFaxNumberInfo operation
        """
        ...

    async def setFaxNumberURLCallback(
        self,
        validate: bool = True,
        *,
        did: int,
        test: Optional[Literal["true", "false"]] = None,
        url_callback: Optional[str] = None,
        url_callback_enable: Optional[str] = None,
        url_callback_retry: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update fax number url callback settings

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID Number to be ported into our network (Example: 5552341234) (required)
            test: Set to true if testing how to set the URL callback of a Fax Number (accepts: true/false, yes/no, on/off, 1/0, boolean)
            url_callback: URL where make a POST when you receive a Fax Message.
            url_callback_enable: Flag to enable the URL Callback functionality. - (Values: 1 = true, 0 = false) - Default: 0
            url_callback_retry: Flag to enable retry the POST action in case we don't receive "ok".

        Returns:
            Response from setFaxNumberURLCallback operation
        """
        ...

    async def setForwarding(
        self,
        validate: bool = True,
        *,
        phone_number: Annotated[str, "Format: phone"],
        callerid_override: Optional[int] = None,
        description: Optional[str] = None,
        diversion_header: Optional[str] = None,
        dtmf_digits: Optional[str] = None,
        forwarding: Optional[int] = None,
        pause: Optional[Annotated[str, "Units: seconds"]] = None,
    ) -> Dict[str, Any]:
        """Update forwarding settings

        Args:
            validate: Whether to validate parameters with Pydantic
            callerid_override: Caller ID Override for the Forwarding
            description: Description for the Forwarding
            diversion_header: If enabled, we will add a Diversion Header to your forwarded call
            dtmf_digits: Send DTMF digits when call is answered
            forwarding: ID for a specific Forwarding (Example: 19183 / Leave empty to create a new one)
            pause: Pause (seconds) when call is answered before sending digits (Example: 1.5 / Values: 0 to 10 in increments of 0.5)
            phone_number: Phone Number for the Forwarding (required)

        Returns:
            Response from setForwarding operation
        """
        ...

    async def setIVR(
        self,
        validate: bool = True,
        *,
        choices: str,
        language: str,
        name: str,
        recording: str,
        timeout: str,
        voicemailsetup: str,
        ivr: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update ivr settings

        Args:
            validate: Whether to validate parameters with Pydantic
            choices: Choices for the IVR (Example: '1=sip:5096 ; 2=fwd:20222') (required)
            ivr: ID for a specific IVR (Example: 4636 / Leave empty to create a new one)
            language: Language for the IVR (values from getLanguages) (required)
            name: Name for the IVR (required)
            recording: Recording for the IVR (values from getRecordings) (required)
            timeout: Maximum time for type in a choice after recording (required)
            voicemailsetup: Voicemail Setup for the IVR (values from getVoicemailSetups) (required)

        Returns:
            Response from setIVR operation
        """
        ...

    async def setMusicOnHold(
        self,
        validate: bool = True,
        *,
        description: str,
        recordings: Literal["1234", "1235", "1236"],
        name: Optional[str] = None,
        sort: Optional[str] = None,
        volume: Optional[Literal["0", "1"]] = None,
    ) -> Dict[str, Any]:
        """Update music on hold settings

        Args:
            validate: Whether to validate parameters with Pydantic
            description: Music on Hold Description (required)
            name: Music on Hold Name (Values from getMusicOnHold)
            recordings: Selected recordings separated by commas (Values from getRecordings, example: (1234,1235,1236) (required)
            sort: Selected recordings sort mode (Example: "alpha", "random")
            volume: Music on Hold Quiet Volume (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)

        Returns:
            Response from setMusicOnHold operation
        """
        ...

    async def setPhonebook(
        self,
        validate: bool = True,
        *,
        name: Annotated[str, "Format: phone"],
        number: str,
        callerid: Optional[int] = None,
        group: Optional[int] = None,
        note: Optional[Annotated[str, "Format: phone"]] = None,
        phonebook: Optional[int] = None,
        speed_dial: Optional[Annotated[str, "Format: phone"]] = None,
    ) -> Dict[str, Any]:
        """Update phonebook settings

        Args:
            validate: Whether to validate parameters with Pydantic
            callerid: Caller ID Override when dialing via Speed Dial
            group: ID for a specific Phonebook group
            name: Name for the Phonebook Entry (required)
            note: Note for the phonebook entry
            number: Number or SIP for the Phonebook entry (Example: 'sip:2563' or '5552223333') (required)
            phonebook: ID for a specific Phonebook entry (Example: 32207 / Leave empty to create a new one)
            speed_dial: Speed Dial for the Phonebook entry

        Returns:
            Response from setPhonebook operation
        """
        ...

    async def setPhonebookGroup(
        self,
        validate: bool = True,
        *,
        name: Annotated[str, "Format: phone"],
        phonebook: str,
        group: Optional[int] = None,
        members: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update phonebook group settings

        Args:
            validate: Whether to validate parameters with Pydantic
            group: ID for a specific Phonebook group (Example: 32207 / Leave empty to create a new one)
            members: Phonebook entry codes associated to this group separated by a semicolon
            name: Name for the Phonebook group (required)
            phonebook:  (required)

        Returns:
            Response from setPhonebookGroup operation
        """
        ...

    async def setQueue(
        self,
        validate: bool = True,
        *,
        join_when_empty: str,
        leave_when_empty: str,
        priority_weight: str,
        queue_language: int,
        queue_name: str,
        queue_number: str,
        report_hold_time_agent: int,
        ring_inuse: int,
        ring_strategy: str,
        agent_announcement: Optional[int] = None,
        agent_ring_timeout: Optional[int] = None,
        announce_position_frecuency: Optional[Annotated[str, "Units: seconds"]] = None,
        announce_round_seconds: Optional[Annotated[str, "Units: seconds"]] = None,
        callerid_prefix: Optional[int] = None,
        fail_over_routing_full: Optional[str] = None,
        fail_over_routing_join_empty: Optional[str] = None,
        fail_over_routing_join_unavail: Optional[str] = None,
        fail_over_routing_leave_empty: Optional[str] = None,
        fail_over_routing_leave_unavail: Optional[str] = None,
        fail_over_routing_timeout: Optional[str] = None,
        frequency_announcement: Optional[Annotated[str, "Units: seconds"]] = None,
        if_announce_position_enabled_report_estimated_hold_time: Optional[str] = None,
        join_announcement: Optional[int] = None,
        maximum_callers: Optional[str] = None,
        maximum_wait_time: Optional[Annotated[str, "Units: seconds"]] = None,
        member_delay: Optional[Annotated[str, "Units: seconds"]] = None,
        music_on_hold: Optional[int] = None,
        queue: Optional[int] = None,
        queue_password: Optional[str] = None,
        retry_timer: Optional[Annotated[str, "Units: seconds"]] = None,
        thankyou_for_your_patience: Optional[str] = None,
        voice_announcement: Optional[int] = None,
        wrapup_time: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update queue settings

        Args:
            validate: Whether to validate parameters with Pydantic
            agent_announcement: Recording Code (Values from getRecordings or 'none')
            agent_ring_timeout: Number of seconds to ring an agent (Values 5 to 60)
            announce_position_frecuency: How often to make any periodic announcement (Values in seconds: multiples of 15, max value: 1200 or 'none' = No announcement)
            announce_round_seconds: Announce seconds (Values in seconds: 1 to 60  or 'none' = Do not announce)
            callerid_prefix: Caller ID Prefix for queue
            fail_over_routing_full: Failover routing to Maximum callers reached
            fail_over_routing_join_empty: A call was sent to the queue but the queue had no members (Only works when Join when Empty is set to no)
            fail_over_routing_join_unavail: Same as routingjoinempty, except that there were still queue members, but all were status unavailable
            fail_over_routing_leave_empty: The last agent was removed form the queue before alls calls were handled (Only works when Leave when Empty is set to yes)
            fail_over_routing_leave_unavail: Same as routingleaveempty, except that there were still queue members, but all were status unavailable
            fail_over_routing_timeout: Failover routing to Maximum wait time reached
            frequency_announcement: Periodic interval to play voice announce recording (Values in seconds: multiples of 15, max value: 1200 or 'none' = No announcement)
            if_announce_position_enabled_report_estimated_hold_time:  Include estimated hold time in position announcements (Values 'yes'/'no'/'once')
            join_announcement: Recording Code (Values from getRecordings or 'none')
            join_when_empty: How caller join to the queue (Values from getJoinWhenEmptyTypes) Examples: yes     Callers can join a queue with no members or only unavailable members no      Callers cannot join a queue with no members strict  Callers cannot join a queue with no members or only unavailable members (required)
            leave_when_empty: How caller leave the queue (Values 'yes'/'no'/'strict') Examples: yes     Callers are sent to failover when there are no members no      Callers will remain in the queue even if there are no members strict  Callers are sent to failover if there are members but none of them is available. (required)
            maximum_callers: Maximum callers (Values: 1 to 60 or 'unlimited')
            maximum_wait_time: Ammount of time a caller can wait in queue (Values in seconds: multiples of 30, max value: 1200 or 'unlimited')
            member_delay: Member delay when the agent is connected to the caller (Values 1 to 15 in seconds or 'none')
            music_on_hold: Music on Hold Code (Values from getMusicOnHold)
            priority_weight: weight/priority of queue (Values 1 to 60) (required)
            queue: ID for a specific Queue entry (Example: 32208 / Leave empty to create a new one)
            queue_language: Language Code (Values from getLanguages) (required)
            queue_name: Queue entry name (required)
            queue_number: Queue entry number (required)
            queue_password: Queue Password
            report_hold_time_agent: Report hold time to agent (Values from getReportEstimatedHoldTime) (required)
            retry_timer: How long do we wait before trying all the members again (Values 5 to 60 seconds or 'none'= No Delay)
            ring_inuse: If you want the queue to avoid sending calls to members (Values 'yes'/'no') (required)
            ring_strategy: Ring strategy (Values from getRingStrategies) (required)
            thankyou_for_your_patience: Yes to say "Thank you for your patience" immediatly after announcing Queue Position and Estimated hold time left (Values 'yes'/'no')
            voice_announcement: Code for Recording (Values from getRecordings or 'none')
            wrapup_time: After a successful call, the number of seconds to wait before sending a free agent another call (Values 1 to 60 seconds or 'none'= No Delay)

        Returns:
            Response from setQueue operation

        Note:
            None values for certain parameters convert to 'none' or 'unlimited'
            Boolean parameters use 'yes'/'no' strings
        """
        ...

    async def setRecording(
        self,
        validate: bool = True,
        *,
        file: int,
        name: str,
        recording: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update recording settings

        Args:
            validate: Whether to validate parameters with Pydantic
            file: Base64 encoded file (Provide Recording ID and file if you want update the file only) (required)
            name: Name for the Recording Entry (Example: 'recording1') (Provide Recording ID and name if you want update the name only) (Provide Recording ID, file and name if you want update both parameters at the same time) (required)
            recording: ID for a specific Phonebook entry (Example: 33221 / Leave empty to create a new one)

        Returns:
            Response from setRecording operation
        """
        ...

    async def setRingGroup(
        self,
        validate: bool = True,
        *,
        members: int,
        name: str,
        voicemail: str,
        caller_announcement: Optional[int] = None,
        language: Optional[int] = None,
        music_on_hold: Optional[int] = None,
        ring_group: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update ring group settings

        Args:
            validate: Whether to validate parameters with Pydantic
            caller_announcement: Recording Code (Values from getRecordings)
            language: Code for Language (Values from getLanguages) "members" can receive the following routing headers: account     Used to route the call to an Account or a Sub Account fwd         Used to route the call to a Forwarding entry sip         Used to route the call to a SIP URI Each member can a specific ring time and press1 values, you can add those to the routing header as follow: Example: 'account:100001,25,0;fwd:16006,10,1' 25 = Default ring time value (Values from 1 to 60 sec) 0  = Default press1 value (Values allowed 0 and 1)
            members: Members for the Ring Group (Example: 'account:100001;fwd:16006') (required)
            music_on_hold: Music on Hold Code (Values from getMusicOnHold)
            name: Name for the Ring Group (required)
            ring_group: ID for a specific Ring Group (Example: 4768 / Leave empty to create a new one)
            voicemail: Voicemail for the Ring Group (Values from getVoicemails) (required)

        Returns:
            Response from setRingGroup operation
        """
        ...

    async def setSIPURI(
        self,
        validate: bool = True,
        *,
        uri: Annotated[str, "Format: email; Units: milliseconds"],
        callerid_e164: Optional[int] = None,
        callerid_override: Optional[int] = None,
        description: Optional[str] = None,
        sipuri: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update sipuri settings

        Args:
            validate: Whether to validate parameters with Pydantic
            callerid_e164: If this option is Enabled, then your CallerID will be E164 compliant.
            callerid_override: This setting is optional.  You can  configure a 'CallerID Number Override'. Your default CallerID number will be changed to the override you have configured here when using this SIP URI.
            description: Description for the SIP URI
            sipuri: ID for a specific SIP URI (Example: 6199 / Leave empty to create a new one)
            uri: SIP URI (Example: '5552223333@sip.voip.ms') (required)

        Returns:
            Response from setSIPURI operation
        """
        ...

    async def setSMS(
        self,
        validate: bool = True,
        *,
        did: int,
        enable: Literal["0", "1"],
        email_address: Optional[int] = None,
        email_enabled: Optional[int] = None,
        sms_forward: Optional[int] = None,
        sms_forward_enable: Optional[int] = None,
        sms_sipaccount: Optional[int] = None,
        sms_sipaccount_enabled: Optional[int] = None,
        url_callback: Optional[int] = None,
        url_callback_enable: Optional[int] = None,
        url_callback_retry: Optional[Annotated[str, "Units: minutes"]] = None,
    ) -> Dict[str, Any]:
        """Update sms settings

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID to be Updated (Example: 5551234567) (required)
            email_address: SMS Messages received by your DID will be sent to the email address provided
            email_enabled: If Enable, SMS Messages received by your DID will be sent to the email address provided (Values:1=Enable / 0=Disable)
            enable: Enable/Disable the DID to receive SMS Messages (Values:1=Enable / 0=Disable) (accepts: true/false, yes/no, on/off, 0/1, boolean) (required)
            sms_forward: SMS Messages received by your DID will be forwarded to the phone number provided (Example: 5551234567)
            sms_forward_enable: If Enable, SMS Messages received by your DID will be forwarded to the phone number provided (Values:1=Enable / 0=Disable)
            sms_sipaccount: SIP account or sub-account that will receive the SMS Messages
            sms_sipaccount_enabled: If Enable, SMS Messages received by your DID will be sent to the specified SIP account or sub-account (Values:1=Enable / 0=Disable)
            url_callback: SMS Messages received by your DID will be send a GET request to the URL callback provided Available Variables for your URL {FROM}    The phone number that sent you the message. {TO}      The DID number that received the message. {MESSAGE} The content of the message. Example: http://mysite.com/sms.php?to={TO}&from={FROM}&message={MESSAGE}
            url_callback_enable: If Enable, SMS Messages received by your DID will be send a GET request to the URL callback provided (Values:1=Enable / 0=Disable)
            url_callback_retry: Enable URL callback Retry (Values:1=Enable / 0=Disable) we will be expecting an 'ok' output (without quotes) from your URL callback page as an indicator that you have received the message correctly. If we don\'t receive the 'ok' letters (wihtout quotes) from your callback page, we will keep sending you the same message every 30 minutes.

        Returns:
            Response from setSMS operation
        """
        ...

    async def setStaticMember(
        self,
        validate: bool = True,
        *,
        member_name: str,
        priority: str,
        queue: int,
        account: Optional[str] = None,
        member: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update static member settings

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Static Member Routing to receive calls - You can get all sub accounts using the getSubAccounts function
            member: ID for a specific Member (Example: 619 / Leave empty to create a new one)
            member_name: Member Description (required)
            priority: Values for get calls first (Example: 0) (required)
            queue: ID for a specific Queue (required)

        Returns:
            Response from setStaticMember operation
        """
        ...

    async def setSubAccount(
        self,
        validate: bool = True,
        *,
        allowed_codecs: int,
        auth_type: int,
        device_type: int,
        dtmf_mode: int,
        id_: int,
        international_route: int,
        lock_international: int,
        music_on_hold: int,
        nat: int,
        transcribe: int,
        transcription_email: str,
        transcription_locale: str,
        callerid_number: Optional[int] = None,
        canada_routing: Optional[int] = None,
        default_e911: Optional[int] = None,
        description: Optional[int] = None,
        dialing_mode: Optional[Literal["0", "1", "2"]] = None,
        enable_ip_restriction: Optional[Literal["0", "1"]] = None,
        enable_pop_restriction: Optional[Literal["0", "1"]] = None,
        internal_dialtime: Optional[int] = None,
        internal_extension: Optional[int] = None,
        internal_voicemail: Optional[int] = None,
        ip: Optional[int] = None,
        ip_restriction: Optional[str] = None,
        language: Optional[int] = None,
        max_expiry: Optional[Annotated[str, "Range: 60-3600"]] = None,
        password: Optional[int] = None,
        pop_restriction: Optional[str] = None,
        record_calls: Optional[Literal["0", "1"]] = None,
        reseller_chargesetup: Optional[str] = None,
        reseller_client: Optional[int] = None,
        reseller_nextbilling: Optional[str] = None,
        reseller_package: Optional[str] = None,
        rtp_hold_timeout: Optional[Annotated[str, "Range: 1-3600"]] = None,
        rtp_timeout: Optional[Annotated[str, "Range: 1-3600"]] = None,
        send_bye: Optional[Literal["0", "1"]] = None,
        sip_traffic: Optional[Literal["0", "1"]] = None,
        tfcarrier: Optional[Literal["-1", "0", "1", "2"]] = None,
        transcription_start_delay: Optional[Annotated[str, "Range: 0-60; Units: seconds"]] = None,
    ) -> Dict[str, Any]:
        """Update sub account settings

        Args:
            validate: Whether to validate parameters with Pydantic
            allowed_codecs: List of Allowed Codecs (Values from getAllowedCodecs) Codecs separated by semicolon (Example: ulaw;g729;gsm) (required)
            auth_type: Authorization Type Code (Values from getAuthTypes) (required)
            callerid_number: Caller ID Override
            canada_routing: Route Code (Values from getRoutes)
            default_e911: e911 Default CallerID
            description: Sub Account Description (Example: 'VoIP Account')
            device_type: Device Type Code (Values from getDeviceTypes) (required)
            dialing_mode: Allows you to dial outgoing calls using either the NANPA configuration or the E164 configuration. (Values: 0 = Use Main Account Setting, 1 = E164, 2 = NANPA)
            dtmf_mode: DTMF Mode Code (Values from getDTMFModes) (required)
            enable_ip_restriction: Enable IP Restriction (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            enable_pop_restriction: Enable POP Restriction (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            id_: Sub Account ID (Example: 10236) (required)
            internal_dialtime: Sub Account Internal Dialtime (Example: 60 -> seconds)
            internal_extension: Sub Account Internal Extension (Example: 1 -> Creates 101)
            internal_voicemail: Sub Account Internal Voicemail (Example: 101)
            international_route: Route Code (Values from getRoutes) (required)
            ip: Sub Account IP (For IP Authentication)
            ip_restriction: List of IP/Netmask to allow outgoing calls separated by commas (Example: 123.45.3.21,10.255.12.0/22,device.mydomain.com)
            language: Language for system messages, such as "Invalid Option" (Values from getLanguages)
            lock_international: Lock International Code (Values from getLockInternational) (required)
            max_expiry: Max Expiry between 60 and 3600 (Example: 3000)
            music_on_hold: Music on Hold Code (Values from getMusicOnHold) (required)
            nat: NAT Mode Code (Values from getNAT) (required)
            password: Sub Account Password (For Password Authentication)
            pop_restriction: List of POP Servers to allow outgoing calls separated by commas (values from getServersInfo. Example: 10,23,45)
            record_calls: Record Calls (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            reseller_chargesetup: True if you want to charge Package Setup Fee after Save
            reseller_client: Reseller Account ID (Example: 561115)
            reseller_nextbilling: Reseller Next Billing Date (Example: '2012-12-31')
            reseller_package: Reseller Package (Example: 92364)
            rtp_hold_timeout: RTP Hold Time Out between 1 and 3600 (Example: 600)
            rtp_timeout: RTP Time Out between 1 and 3600 (Example: 60)
            send_bye: Send BYE on successful transfer (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            sip_traffic: Encrypted SIP Traffic (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            tfcarrier: This allows you to select the carrier to be used for outgoing calls to toll-free numbers. (Values: -1 = Use main account settings, 0 = Default server setting, 1 = US carrier, 2 = Canadian carrier)
            transcribe:  (required)
            transcription_email:  (required)
            transcription_locale:  (required)
            transcription_start_delay: Call Transcription Delay Seconds between 0 and 60, Increments of 5 (Example: 10 -> seconds)

        Returns:
            Response from setSubAccount operation
        """
        ...

    async def setTimeCondition(
        self,
        validate: bool = True,
        *,
        endhour: Annotated[str, "Units: hours"],
        endminute: Annotated[str, "Units: minutes"],
        name: str,
        routing_match: str,
        routing_nomatch: str,
        starthour: Annotated[str, "Units: hours"],
        startminute: Annotated[str, "Units: minutes"],
        weekdayend: Annotated[str, "Units: days"],
        weekdaystart: Annotated[str, "Units: days"],
        timecondition: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Update time condition settings

        Args:
            validate: Whether to validate parameters with Pydantic
            endhour: All the End Hour Conditions (Example: '16;12') (required)
            endminute: All the End Minute Conditions (Example: '0;0') (required)
            name: Name for the Time Condition (required)
            routing_match: Routing for the Call when condition matches (required)
            routing_nomatch: Routing for the Call when condition does not matche (required)
            starthour: All the Start Hour Conditions (Example: '8;8') (required)
            startminute: All the Start Minute Conditions (Example: '0;0') (required)
            timecondition: ID for a specific Time Condition (Example: 1830 / Leave empty to create a new one)
            weekdayend: All the Week Day End Conditions (Example: 'fri;sat') (required)
            weekdaystart: All the Week Day Start Conditions (Example: 'mon;sat') (required)

        Returns:
            Response from setTimeCondition operation
        """
        ...

    async def setVoicemail(
        self,
        validate: bool = True,
        *,
        attach_message: Annotated[str, "Format: wav"],
        delete_message: str,
        language: int,
        mailbox: int,
        name: str,
        password: str,
        play_instructions: int,
        say_callerid: int,
        say_time: str,
        skip_password: Literal["0", "1"],
        timezone: str,
        email: Optional[Annotated[str, "Format: email"]] = None,
        email_attachment_format: Optional[int] = None,
        transcription: Optional[str] = None,
        transcription_locale: Optional[int] = None,
        unavailable_message_recording: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update voicemail settings

        Args:
            validate: Whether to validate parameters with Pydantic
            attach_message: Yes for Attaching WAV files to Message (Values: 'yes'/'no') (required)
            delete_message: Yes for Deleting Messages (Values: 'yes'/'no') (required)
            email: Email address for receiving messages, multiple email addresses are allowed if separated by a comma
            email_attachment_format: Code for Email Attachment format (Values from getVoicemailAttachmentFormats)
            language: Code for Language (Values from getLanguages) (required)
            mailbox: ID for a specific Mailbox (Example: 1001) (required)
            name: Name for the Mailbox (required)
            password: Password for the Mailbox (required)
            play_instructions: Code for Play Instructions Setting (Values from getPlayInstructions) (required)
            say_callerid: Yes for Saying the Caller ID (Values: 'yes'/'no') (required)
            say_time: Yes for Saying Time Stamp (Values: 'yes'/'no') (required)
            skip_password: True if Skipping Password (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean) (required)
            timezone: Time Zone for Mailbox (Values from getTimeZones) (required)
            transcription: Voicemail Transcription
            transcription_locale: Transcription locale code (values from getLocales)
            unavailable_message_recording: Recording for the Unavailable Message (values from getRecordings)

        Returns:
            Response from setVoicemail operation

        Note:
            Boolean parameters like attach_message use 'yes'/'no' strings
            skip_password uses '1'/'0' string
        """
        ...

    async def signupClient(
        self,
        validate: bool = True,
        *,
        address: str,
        city: str,
        confirm_email: str,
        confirm_password: str,
        country: int,
        email: str,
        firstname: str,
        lastname: str,
        password: str,
        phone_number: Annotated[str, "Format: phone"],
        state: str,
        zip: int,
        activate: Optional[Literal["0", "1"]] = None,
        balance_management: Optional[str] = None,
        company: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Sign up client

        Args:
            validate: Whether to validate parameters with Pydantic
            activate: Activates Client (Boolean: 1/0) (accepts: true/false, yes/no, on/off, 0/1, boolean)
            address: Client's Address (required)
            balance_management: Balance Management for Client (Values from getBalanceManagement)
            city: Client's City (required)
            company: Client's Company
            confirm_email: Client's Confirmation e-mail (required)
            confirm_password: Client's Confirmation Password (required)
            country: Client's Country (Values from getCountries) (required)
            email: Client's e-mail (required)
            firstname: Client's Firstname (required)
            lastname: Client's Lastname (required)
            password: Client's Password (required)
            phone_number: Client's Phone Number (required)
            state: Client's State (required)
            zip: Client's Zip Code (required)

        Returns:
            Response from signupClient operation
        """
        ...

    async def unconnectDID(
        self,
        validate: bool = True,
        *,
        did: int,
    ) -> Dict[str, Any]:
        """Unconnect did

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID to be Unconnected from Reseller Sub Account(Example: 5551234567) (required)

        Returns:
            Response from unconnectDID operation
        """
        ...

    async def unconnectFAX(
        self,
        validate: bool = True,
        *,
        did: int,
    ) -> Dict[str, Any]:
        """Unconnect fax

        Args:
            validate: Whether to validate parameters with Pydantic
            did: FAX DID to be Unconnected from Reseller Sub Account (Example: 5551234567) (required)

        Returns:
            Response from unconnectFAX operation
        """
        ...
