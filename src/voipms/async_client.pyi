"""
Type stubs for VoIP.ms Async Client

Generated on 2025-07-23
DO NOT EDIT MANUALLY - This file is auto-generated
"""

from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Union, Literal, Annotated
from .config import VoIPMSConfig


class VoIPMSAsyncService:
    """Pure async service for VoIP.ms API calls."""
    
    api_definition: dict[str, Any]
    config: VoIPMSConfig
    username: str
    password: str
    base_url: str
    timeout: float
    max_retries: int
    verify_ssl: bool
    debug: bool
    enable_retries: bool
    
    def is_healthy(self) -> bool: ...
    async def test_connectivity(self) -> bool: ...
    def get_available_methods(self) -> list[str]: ...
    def get_method_info(self, method_name: str) -> dict[str, Any] | None: ...
    def debug_method_params(self, op_name: str, **kwargs: Any) -> None: ...
    
    # API Methods (async versions)

    async def addCharge(
        self,
        validate: bool = True,
        *,
        charge: float,
        client: int,
        description: str | None = None,
        test: bool | None = None,
    ) -> dict[str, Any]:
        """- Adds a Charge to a specific Reseller Client

        Args:
            validate: Whether to validate parameters with Pydantic
            charge: Amount of money that will be Debited from the customer (Example: 4.99) (required)
            client: ID for a specific Reseller Client (Example: 561115) (required)
            description: Charge Description
            test: Set to true if testing how adding charges works

        Returns:
            Response from addCharge operation
        """
        ...

    async def addLNPFile(
        self,
        validate: bool = True,
        *,
        file: str,
        portid: int,
    ) -> dict[str, Any]:
        """- Add an invoice file to a portability process.

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
        country: str,
        firstName: str,
        lastName: str,
        numbers: str,
        portType: int,
        providerAccount: str,
        providerName: str,
        state: str,
        statementName: str,
        zip: str,
        address2: str | None = None,
        btn: str | None = None,
        isMobile: int | None = None,
        isPartial: int | None = None,
        locationType: int | None = None,
        notes: str | None = None,
        pin: str | None = None,
        services: str | None = None,
        tfType: int | None = None,
    ) -> dict[str, Any]:
        """- Add one or more numbers to start a portability process.

        Args:
            validate: Whether to validate parameters with Pydantic
            address1: This is the "Customer Address" as it appears on the CSR (Customer Service Record) of the losing carrier. (required)
            address2: Optional Address information (e.g: Suite 343)
            btn: [Required If isMobile = 1] BTN: It is the phone number to which all the other numbers of the customer are
            city: This is the "City" as it appears on the CSR (Customer Service Record) of the losing carrier. (required)
            country: This is the "Country" as it appears on the CSR (Customer Service Record) of the losing carrier. (required)
            firstName: This is the "Customer First Name" as it appears on  the CSR (Customer Service Record) of the (required)
            isMobile: - (Values: 1 = All the numbers are mobile numbers, 0 = false) - Default: 0
            isPartial: If you have more then 1 number with your current carrier and not porting them all, choose yes.
            lastName: This is the "Customer Last Name" as it appears on  the CSR (Customer Service Record) of the (required)
            locationType: - (Values: 1 = Business, 0 = Residential) - Default: 0
            notes: - If you would like to include additional information regarding this port, you can use this parameter.
            numbers: DID(s) to port into VoIP.ms network (Example: 5552341234,5552341233). If you (required)
            pin: PIN Number
            portType: Digits from 1 to 4: (required)
            providerAccount: Your Account with your current service provider. (required)
            providerName: The name of your current service provider. (required)
            services: [Required If isMobile = 1] Please be specific and describe ALL remaining services with the current carrier. This includes DSL/Data
            state: This is the "State or Province" as it appears on the CSR (Customer Service Record) of the losing carrier. (required)
            statementName: This is for Business numbers only. Please type your Company Name if applicable, otherwise leave it blank. (required)
            tfType: [Required If portType = 3] Values: 1 - American Carrier, American Callers Only, 2 - American Carrier, American
            zip: This is the "ZIP or Postal Code" as it appears on the CSR (Customer Service Record) of the (required)

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
    ) -> dict[str, Any]:
        """- Add Member to a Conference

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
        payment: float,
        description: str | None = None,
        test: bool | None = None,
    ) -> dict[str, Any]:
        """- Adds a Payment to a specific Reseller Client

        Args:
            validate: Whether to validate parameters with Pydantic
            client: ID for a specific Reseller Client (Example: 561115) (required)
            description: Payment Description
            payment: Amount of money that will be Credited to the customer (Example: 4.99) (required)
            test: Set to true if testing how adding payments works

        Returns:
            Response from addPayment operation
        """
        ...

    async def assignDIDvPRI(
        self,
        validate: bool = True,
        *,
        did: str,
        vpri: int,
    ) -> dict[str, Any]:
        """- Assigns a Per Minute DID to a VPRI (Flat Rate DIDs can’t be assigned)

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
        billing_type: int,
        cnam: int,
        dialtime: int,
        pop: int,
        province: str,
        quantity: int,
        ratecenter: str,
        routing: str,
        callerid_prefix: str | None = None,
        failover_busy: str | None = None,
        failover_noanswer: str | None = None,
        failover_unreachable: str | None = None,
        note: str | None = None,
        test: bool | None = None,
        voicemail: str | None = None,
    ) -> dict[str, Any]:
        """- Backorder DID (CANADA) from a specific ratecenter and province.

        Args:
            validate: Whether to validate parameters with Pydantic
            billing_type: Billing type for the DID (1 = Per Minute, 2 = Flat) (required)
            callerid_prefix: Caller ID Prefix for the DID
            cnam: CNAM for the DID (Boolean: 1/0) (required)
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
            test: Set to true if testing how Orders work
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
        billing_type: int,
        cnam: int,
        dialtime: int,
        pop: int,
        quantity: int,
        ratecenter: str,
        routing: str,
        state: str,
        callerid_prefix: str | None = None,
        failover_busy: str | None = None,
        failover_noanswer: str | None = None,
        failover_unreachable: str | None = None,
        note: str | None = None,
        test: bool | None = None,
        voicemail: str | None = None,
    ) -> dict[str, Any]:
        """- Backorder DID (USA) from a specific ratecenter and state.

        Args:
            validate: Whether to validate parameters with Pydantic
            billing_type: Billing type for the DID (1 = Per Minute, 2 = Flat) (required)
            callerid_prefix: Caller ID Prefix for the DID
            cnam: CNAM for the DID (Boolean: 1/0) (required)
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
            test: Set to true if testing how Orders work
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
        did: str,
        cancelcomment: str | None = None,
        portout: bool | None = None,
        test: bool | None = None,
    ) -> dict[str, Any]:
        """- Deletes a specific DID from your Account.

        Args:
            validate: Whether to validate parameters with Pydantic
            cancelcomment: Comment for DID cancellation
            did: DID to be canceled and deleted (Example: 5551234567) (required)
            portout: Set to true if the DID is being ported out
            test: Set to true if testing how cancellation works

        Returns:
            Response from cancelDID operation
        """
        ...

    async def cancelFaxNumber(
        self,
        validate: bool = True,
        *,
        id_: int,
        test: int | None = None,
    ) -> dict[str, Any]:
        """- Deletes a specific Fax Number from your Account.

        Args:
            validate: Whether to validate parameters with Pydantic
            id_: ID for a specific Fax Number (Example: 923) (required)
            test: Set to true if testing how cancel a Fax Number

        Returns:
            Response from cancelFaxNumber operation
        """
        ...

    async def connectDID(
        self,
        validate: bool = True,
        *,
        account: str,
        did: str,
        minute: float,
        monthly: float,
        setup: float,
        dont_charge_monthly: float | None = None,
        dont_charge_setup: float | None = None,
        next_billing: str | None = None,
    ) -> dict[str, Any]:
        """- Connects a specific DID to a specific Reseller Client Sub Account

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
        account: str,
        did: str,
        minute: float,
        monthly: float,
        setup: float,
        dont_charge_monthly: float | None = None,
        dont_charge_setup: float | None = None,
        next_billing: str | None = None,
    ) -> dict[str, Any]:
        """- Connects a specific FAX DID to a specific Reseller Client Sub Account

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
        allowed_codecs: str,
        auth_type: int,
        device_type: int,
        dtmf_mode: str,
        international_route: int,
        lock_international: int,
        music_on_hold: str,
        nat: str,
        protocol: int,
        username: str,
        callerid_number: str | None = None,
        canada_routing: str | None = None,
        description: str | None = None,
        dialing_mode: int | None = None,
        enable_internal_cnam: int | None = None,
        enable_ip_restriction: int | None = None,
        enable_pop_restriction: int | None = None,
        internal_cnam: str | None = None,
        internal_dialtime: str | None = None,
        internal_extension: str | None = None,
        internal_voicemail: str | None = None,
        ip: str | None = None,
        ip_restriction: str | None = None,
        language: str | None = None,
        max_expiry: int | None = None,
        password: str | None = None,
        pop_restriction: str | None = None,
        record_calls: int | None = None,
        reseller_chargesetup: str | None = None,
        reseller_client: str | None = None,
        reseller_nextbilling: str | None = None,
        reseller_package: str | None = None,
        rtp_hold_timeout: int | None = None,
        rtp_timeout: int | None = None,
        send_bye: int | None = None,
        sip_traffic: int | None = None,
        tfcarrier: int | None = None,
        transcribe: int | None = None,
        transcription_email: str | None = None,
        transcription_locale: str | None = None,
        transcription_start_delay: int | None = None,
    ) -> dict[str, Any]:
        """- Adds a new Sub Account entry to your Account

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
            enable_ip_restriction: Enable IP Restriction (Boolean: 1/0)
            enable_pop_restriction: Enable POP Restriction (Boolean: 1/0)
            internal_cnam: Internal CallerID Name
            internal_dialtime: Sub Account Internal Dialtime (Example: 60 -> seconds)
            internal_extension: Sub Account Internal Extension (Example: 1 -> Creates 101)
            internal_voicemail: Sub Account Internal Voicemail (Example: 101)
            international_route: Route Code (Values from getRoutes) (required)
            ip: Sub Account IP (For IP Authentication)
            ip_restriction: List of IP Addresses, IP Addresses/Netmask, or Fully Qualified Domain Names to allow outgoing calls separated by commas
            language: Language for system messages, such as "Invalid Option" (Values from getLanguages)
            lock_international: Lock International Code (Values from getLockInternational) (required)
            max_expiry: Max Expiry between 60 and 3600 (Example: 3000)
            music_on_hold: Music on Hold Code (Values from getMusicOnHold) (required)
            nat: NAT Mode Code (Values from getNAT) (required)
            password: Sub Account Password (For Password Authentication)
            pop_restriction: List of POP Servers to allow outgoing calls separated by commas
            protocol: Protocol used for the Sub Account (Values from getProtocols) (required)
            record_calls: Record Calls (Boolean: 1/0)
            reseller_chargesetup: True if you want to charge Package Setup Fee after Save
            reseller_client: Reseller Account ID (Example: 561115)
            reseller_nextbilling: Reseller Next Billing Date (Example: '2012-12-31')
            reseller_package: Reseller Package (Example: 92364)
            rtp_hold_timeout: RTP Hold Time Out between 1 and 3600 (Example: 600)
            rtp_timeout: RTP Time Out between 1 and 3600 (Example: 60)
            send_bye: Send BYE on successful transfer (Boolean: 1/0)
            sip_traffic: Encrypted SIP Traffic (Boolean: 1/0)
            tfcarrier: This allows you to select the carrier to be used for outgoing calls to toll-free numbers. (Values: -1 = Use main account settings, 0 = Default server setting, 1 = US carrier, 2 = Canadian carrier)
            transcribe: Enable Call Transcription (Boolean: 1/0)
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
        attach_message: str,
        delete_message: str,
        digits: int,
        language: str,
        name: str,
        password: str,
        play_instructions: str,
        say_callerid: str,
        say_time: str,
        skip_password: str,
        timezone: str,
        email: str | None = None,
        email_attachment_format: str | None = None,
        transcription: str | None = None,
        transcription_locale: str | None = None,
        unavailable_message_recording: str | None = None,
    ) -> dict[str, Any]:
        """- Adds a new Voicemail entry to your Account

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
            skip_password: True if Skipping Password (Boolean: 1/0) (required)
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
    ) -> dict[str, Any]:
        """- Deletes a specific Call Hunting from your Account.

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
    ) -> dict[str, Any]:
        """- Deletes a specific Call Parking entry from your Account.

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
        account: str,
        callrecording: str,
    ) -> dict[str, Any]:
        """- Delete specific call recording, audio file and information related.

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
    ) -> dict[str, Any]:
        """- Deletes a specific Callback from your Account.

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
    ) -> dict[str, Any]:
        """- Deletes a specific CallerID Filtering from your Account.

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
    ) -> dict[str, Any]:
        """- Deletes a specific reseller client from your Account.

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
    ) -> dict[str, Any]:
        """- Deletes a specific Conference from your Account.

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
    ) -> dict[str, Any]:
        """- Deletes a specific Member profile from your Account.

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
    ) -> dict[str, Any]:
        """- Deletes a specific DISA from your Account.

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
        test: int | None = None,
    ) -> dict[str, Any]:
        """- Deletes a specific "Email to Fax configuration" from your Account.

        Args:
            validate: Whether to validate parameters with Pydantic
            id_: ID for a specific "Email To Fax Configuration" (Example: 923) (required)
            test: Set to true if testing how cancel a "Email To Fax Configuration"

        Returns:
            Response from delEmailToFax operation
        """
        ...

    async def delFaxFolder(
        self,
        validate: bool = True,
        *,
        id_: int,
        test: int | None = None,
    ) -> dict[str, Any]:
        """- Deletes a specific Fax Folder from your Account.

        Args:
            validate: Whether to validate parameters with Pydantic
            id_: ID for a specific Fax Folder (Example: 923) (required)
            test: Set to true if testing how to delete a Fax Folder

        Returns:
            Response from delFaxFolder operation
        """
        ...

    async def delForwarding(
        self,
        validate: bool = True,
        *,
        forwarding: int | None = None,
    ) -> dict[str, Any]:
        """- Deletes a specific Forwarding from your Account.

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
    ) -> dict[str, Any]:
        """- Deletes a specific IVR from your Account.

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
        conference: int | None = None,
    ) -> dict[str, Any]:
        """- Removes a member profile from a specific Conference from your Account

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
        folder: str | None = None,
        message_num: int | None = None,
    ) -> dict[str, Any]:
        """- Deletes all messages in all servers from a specific Voicemail from your Account

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
    ) -> dict[str, Any]:
        """- Deletes a specific custom Music on Hold.

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
    ) -> dict[str, Any]:
        """- Deletes a specific Phonebook from your Account.

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
        group: str,
    ) -> dict[str, Any]:
        """- Deletes a specific Phonebook group from your Account.

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
    ) -> dict[str, Any]:
        """- Deletes a specific Queue from your Account.

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
    ) -> dict[str, Any]:
        """- Deletes a specific Recording from your Account.

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
    ) -> dict[str, Any]:
        """- Deletes a specific Ring Group from your Account.

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
    ) -> dict[str, Any]:
        """- Deletes a specific SIP URI from your Account.

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
    ) -> dict[str, Any]:
        """- Deletes a specific Static Member from Queue.

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
        id_: int | None = None,
    ) -> dict[str, Any]:
        """- Deletes a specific Sub Account from your Account

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
    ) -> dict[str, Any]:
        """- Deletes a specific Time Condition from your Account.

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
    ) -> dict[str, Any]:
        """- Deletes a specific Voicemail from your Account

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
        test: int | None = None,
    ) -> dict[str, Any]:
        """- Deletes a specific Fax Message from your Account.

        Args:
            validate: Whether to validate parameters with Pydantic
            id_: ID for a specific Fax Message (Example: 923) (required)
            test: Set to true if testing how cancel a Fax Message

        Returns:
            Response from deleteFaxMessage operation
        """
        ...

    async def deleteMMS(
        self,
        validate: bool = True,
        *,
        id_: int,
    ) -> dict[str, Any]:
        """- Deletes a specific MMS from your Account.

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
    ) -> dict[str, Any]:
        """- Deletes a specific SMS from your Account.

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
        type_: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of e911 Address Types if no additional parameter is provided. - Retrieves a specific e911 Address Type if an Address code is provided.

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
        did: str,
    ) -> dict[str, Any]:
        """- Cancel the e911 Service from a specific DID.

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
        did: str,
    ) -> dict[str, Any]:
        """- Retrieves the e911 information from a specific DID.

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
        country: str,
        did: str,
        full_name: str,
        language: str,
        state: str,
        street_name: str,
        street_number: int,
        zip: str,
        address_number: int | None = None,
        address_type: str | None = None,
        other_info: str | None = None,
    ) -> dict[str, Any]:
        """- Subscribes your DID to the e911 Emergency Services.

        Args:
            validate: Whether to validate parameters with Pydantic
            address_number: Address Number that will be sent to the e911 service.
            address_type: Address Type that will be sent to the e911 service (Values from e911AddressTypes).
            city: City that will be sent to the e911 service. (required)
            country: Country that will be sent to the e911 service. (required)
            did: DID that will be sent to the e911 service. (required)
            full_name: Full Name that will be sent to the e911 service. (required)
            language: Language that will be sent to the e911 service. (required)
            other_info: Additional Address Information that will be sent to the e911 service.
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
        country: str,
        did: str,
        full_name: str,
        language: str,
        state: str,
        street_name: str,
        street_number: int,
        zip: str,
        address_number: int | None = None,
        address_type: str | None = None,
        other_info: str | None = None,
    ) -> dict[str, Any]:
        """- Subscribes your DID to the e911 Emergency Services. - All e911 information will be validated by the VoIP.ms staff.

        Args:
            validate: Whether to validate parameters with Pydantic
            address_number: Address Number that will be sent to the e911 service.
            address_type: Address Type that will be sent to the e911 service (Values from e911AddressTypes).
            city: City that will be sent to the e911 service. (required)
            country: Country that will be sent to the e911 service. (required)
            did: DID that will be sent to the e911 service. (required)
            full_name: Full Name that will be sent to the e911 service. (required)
            language: Language that will be sent to the e911 service. (required)
            other_info: Additional Address Information that will be sent to the e911 service.
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
        country: str,
        did: str,
        full_name: str,
        language: str,
        state: str,
        street_name: str,
        street_number: int,
        zip: str,
        address_number: int | None = None,
        address_type: str | None = None,
        other_info: str | None = None,
    ) -> dict[str, Any]:
        """- Updates the Information from your e911 Emergency Services Subscription.

        Args:
            validate: Whether to validate parameters with Pydantic
            address_number: Address Number that will be updated to the e911 service.
            address_type: Address Type that will be updated to the e911 service (Values from e911AddressTypes).
            city: City that will be updated to the e911 service. (required)
            country: Country that will be updated to the e911 service. (required)
            did: DID with e911 enabled / in process. (required)
            full_name: Full Name that will be updated to the e911 service. (required)
            language: Language that will be updated to the e911 service. (required)
            other_info: Additional Address Information that will be updated to the e911 service.
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
        city: str,
        country: str,
        did: str,
        full_name: str,
        state: str,
        street_name: str,
        street_number: int,
        zip: str,
        address_number: int | None = None,
        address_type: str | None = None,
        language: str | None = None,
        other_info: str | None = None,
    ) -> dict[str, Any]:
        """- Validates your e911 information in order to start your e911 Emergency Services Subscription.

        Args:
            validate: Whether to validate parameters with Pydantic
            address_number: Address Number that will be validated.
            address_type: Address Type that will be validated (Values from e911AddressTypes).
            city: City that will be validated. (required)
            country: Country that will be validated. (required)
            did: DID with e911 enabled / in process. (required)
            full_name: Full Name that will be validated. (required)
            language: Language that will be validated.
            other_info: Additional Address Information that will be validated.
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
        codec: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Allowed Codecs if no additional parameter is provided. - Retrieves a specific Allowed Codec if a codec code is provided.

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
        type_: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Authentication Types if no additional parameter is provided. - Retrieves a specific Authentication Type if an auth type code is provided.

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
        id_: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of backorder DIDs if no additional parameter is provided. - Retrieves a specific backorder DID if a backorder DID code is provided.

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
        account: str | None = None,
        advanced: Literal["0", "1"] | None = None,
    ) -> dict[str, Any]:
        """- Retrieves Balance for your Account if no additional parameter is provided. - Retrieves Balance and Calls Statistics for your Account if "advanced" parameter is true.

        Args:
            validate: Whether to validate parameters with Pydantic
            account: No description
            advanced: True for Calls Statistics (accepts: true/false, yes/no, on/off, 0/1, boolean)

        Returns:
            Response from getBalance operation
        """
        ...

    async def getBalanceManagement(
        self,
        validate: bool = True,
        *,
        balance_management: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Balance Management Options if no additional parameter is provided. - Retrieves a specific Balance Management Option if a code is provided.

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
        timezone: float,
        account: str | None = None,
        answered: bool | None = None,
        busy: bool | None = None,
        callbilling: str | None = None,
        calltype: str | None = None,
        failed: bool | None = None,
        noanswer: bool | None = None,
    ) -> dict[str, Any]:
        """- Retrieves the Call Detail Records of all your calls.

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Filter CDR by Account (Values from getCallAccounts)
            answered: Include Answered Calls to CDR (Boolean: 1/0)
            busy: Include Busy Calls to CDR (Boolean: 1/0)
            callbilling: Filter CDR by Call Billing (Values from getCallBilling)
            calltype: Filters CDR by Call Type (Values from getCallTypes)
            date_from: Start Date for Filtering CDR (Example: '2010-11-30') (required)
            date_to: End Date for Filtering CDR (Example: '2010-11-30') (required)
            failed: Include Failed Calls to CDR (Boolean: 1/0)
            noanswer: Include NoAnswered calls to CDR (Boolean: 1/0)
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
    ) -> dict[str, Any]:
        """- Retrieves all Sub Accounts if no additional parameter is provided. - Retrieves Reseller Client Accounts if Reseller Client ID is provided.

        Returns:
            Response from getCallAccounts operation
        """
        ...

    async def getCallBilling(
        self,
        validate: bool = True,
    ) -> dict[str, Any]:
        """- Retrieves a list of Call Billing Options.

        Returns:
            Response from getCallBilling operation
        """
        ...

    async def getCallHuntings(
        self,
        validate: bool = True,
        *,
        callhunting: int | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Call Huntings if no additional parameter is provided. - Retrieves a specific Call Huntings if a Call Hunting code is provided.

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
        callparking: int | None = None,
    ) -> dict[str, Any]:
        """- Retrieves all Call Parking entries if no additional parameter is provided. - Retrieves a specific Parking entry if a Call Parking ID is provided.

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
        account: str,
        callrecording: str,
    ) -> dict[str, Any]:
        """- Retrieves one especific call recording information, including the recording file on mp3 format.

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
        account: str,
        date_from: str,
        date_to: str,
        length: int | None = None,
        start: int | None = None,
    ) -> dict[str, Any]:
        """- Retrieves all call recordings related to account.

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
        client: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Call Types and All DIDs if no additional parameter is provided. - Retrieves a list of Call Types and Reseller Client DIDs if a Reseller Client ID is provided.

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
        callback: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Callbacks if no additional parameter is provided. - Retrieves a specific Callback if a Callback code is provided.

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
        did: str,
        filtering: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of CallerID Filterings if no additional parameter is provided. - Retrieves a specific CallerID Filtering if a CallerID Filtering code is provided.

        Args:
            validate: Whether to validate parameters with Pydantic
            did:  (required)
            filtering: ID for a specific CallerID Filtering (Example: 18915)

        Returns:
            Response from getCallerIDFiltering operation
        """
        ...

    async def getCarriers(
        self,
        validate: bool = True,
        *,
        carrier: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Carriers for Vanity Numbers if no additional parameter is provided. - Retrieves a specific Carrier for Vanity Numbers if a carrier code is provided.

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
        client: str,
    ) -> dict[str, Any]:
        """- Retrieves Charges made to a specific Reseller Client.

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
        client: str,
    ) -> dict[str, Any]:
        """- Retrieves a list of Packages for a specific Reseller Client.

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
        client: str,
    ) -> dict[str, Any]:
        """- Retrieves the Threshold Information for a specific Reseller Client.

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
        client: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of all Clients if no additional parameter is provided. - Retrieves a specific Reseller Client if a Reseller Client ID is provided. - Retrieves a specific Reseller Client if a Reseller Client e-mail is provided.

        Args:
            validate: Whether to validate parameters with Pydantic
            client: Parameter could have the following values:

        Returns:
            Response from getClients operation
        """
        ...

    async def getConference(
        self,
        validate: bool = True,
        *,
        conference: int | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Conferences if no additional parameter is provided. - Retrieves a specific Conference if a conference code is provided.

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
        member: int | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Member profiles if no additional parameter is provided. - Retrieves a specific member if a member code is provided.

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
    ) -> dict[str, Any]:
        """- Retrieves a specific Recording File data in Base64 format.

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
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of recordings of a specific conference.

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
        country: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Countries if no additional parameter is provided. - Retrieves a specific Country if a country code is provided.

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
        type_: str,
        country_id: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Countries for International DIDs if no country code is provided. - Retrieves a specific Country for International DIDs if a country code is provided.

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
        ratecenter: str | None = None,
    ) -> dict[str, Any]:
        """- Retrives a list of Canadian DIDs by Province and Ratecenter.

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
        client: str | None = None,
        did: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves information from all your DIDs if no additional parameter is provided. - Retrieves information from Reseller Client's DIDs if a Reseller Client ID is provided. - Retrieves information from Sub Account's DIDs if a Sub Accunt is provided. - Retrieves information from a specific DID if a DID Number is provided. - Retrieves SMS information from a specific DID if the SMS is available.

        Args:
            validate: Whether to validate parameters with Pydantic
            client: Parameter could have the following values:
            did: DID from Client or Sub Account (Example: 5551234567)

        Returns:
            Response from getDIDsInfo operation
        """
        ...

    async def getDIDsInternationalGeographic(
        self,
        validate: bool = True,
        *,
        country_id: str,
    ) -> dict[str, Any]:
        """- Retrieves a list of International Geographic DIDs by Country.

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
        country_id: str,
    ) -> dict[str, Any]:
        """- Retrieves a list of International National DIDs by Country.

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
        country_id: str,
    ) -> dict[str, Any]:
        """- Retrieves a list of International TollFree DIDs by Country.

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
        ratecenter: str | None = None,
    ) -> dict[str, Any]:
        """- Retrives a list of USA DIDs by State and Ratecenter.

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
        vpri: str,
    ) -> dict[str, Any]:
        """- Retrives the list of DIDs assigned to the VPRI.

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
        disa: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of DISAs if no additional parameter is provided. - Retrieves a specific DISA if a DISA code is provided.

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
        dtmf_mode: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of DTMF Modes if no additional parameter is provided. - Retrieves a specific DTMF Mode if a DTMF mode code is provided.

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
        client: str,
    ) -> dict[str, Any]:
        """- Retrieves Deposits made for a specific Reseller Client.

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
        device_type: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Device Types if no additional parameter is provided. - Retrieves a specific Device Type if a device type code is provided.

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
    ) -> dict[str, Any]:
        """- Retrieves a list of "Email to Fax configurations" from your account if no additional parameter is provided. - Retrieves a specific "Email to Fax configuration" from your account if a ID is provided.

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
    ) -> dict[str, Any]:
        """- Retrieves a list of Fax Folders from your account.

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
    ) -> dict[str, Any]:
        """- Retrieves a Base64 code of the Fax Message to create a PDF file.

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
        folder: str | None = None,
        from_: str | None = None,
        id_: int | None = None,
        to: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Fax Messages. - Retrieves a specific Fax Message if a Fax Message ID is provided.

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
        did: int | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Fax Numbers.

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
    ) -> dict[str, Any]:
        """- Shows if a Fax Number can be ported into our network

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
        province: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Canadian Fax Provinces if no additional parameter is provided. - Retrieves a specific Canadian Fax Province if a province code is provided.

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
        province: str,
    ) -> dict[str, Any]:
        """- Retrieves a list of Canadian Ratecenters by Province.

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
        state: str,
    ) -> dict[str, Any]:
        """- Retrieves a list of USA Ratecenters by State.

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
        state: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of American Fax States if no additional parameter is provided. - Retrieves a specific American Fax State if a state code is provided.

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
        forwarding: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Forwardings if no additional parameter is provided. - Retrieves a specific Forwarding if a fwd code is provided.

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
    ) -> dict[str, Any]:
        """- Shows the IP used by the client application requesting information from the API* this is the only function not using the IP for authentication.* the IP returned should be the one used in the API Configuration.

        Returns:
            Response from getIP operation
        """
        ...

    async def getIVRs(
        self,
        validate: bool = True,
        *,
        ivr: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of IVRs if no additional parameter is provided. - Retrieves a specific IVR if a IVR code is provided.

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
        type_: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Types for International DIDs if no additional parameter is provided. - Retrieves a specific Types for International DIDs if a type code is provided.

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
        type_: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of 'JoinWhenEmpty' Types if no additional parameter is provided. - Retrieves a specific 'JoinWhenEmpty' Types if a type code is provided.

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
    ) -> dict[str, Any]:
        """- Retrieve the details of an attached invoice.

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
    ) -> dict[str, Any]:
        """- Retrieve the list of invoice (attached) files from a given portability process.

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
    ) -> dict[str, Any]:
        """- Retrieve the details of a given portability process.

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
        endDate: str | None = None,
        portStatus: str | None = None,
        startDate: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieve the full list of all your portability processes.

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
    ) -> dict[str, Any]:
        """- Retrieve the list of possible status of a portability process.

        Returns:
            Response from getLNPListStatus operation
        """
        ...

    async def getLNPNotes(
        self,
        validate: bool = True,
        *,
        portid: int,
    ) -> dict[str, Any]:
        """- Retrieve the list of notes from the given portability process.

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
    ) -> dict[str, Any]:
        """- Retrieve the current status of a given portability process.

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
        language: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Languages if no additional parameter is provided. - Retrieves a specific Language if a language code is provided.

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
        locale: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of locale codes if no additional parameter is provided. - Retrieves a specific locale code if a language code is provided.

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
        lock_international: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Lock Modes if no additional parameter is provided. - Retrieves a specific Lock Mode if a lock code is provided.

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
        all_messages: int | None = None,
        contact: str | None = None,
        did: str | None = None,
        from_: str | None = None,
        limit: str | None = None,
        mms: int | None = None,
        timezone: str | None = None,
        to: str | None = None,
        type_: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of MMS messages by: date range, mms type, DID number, and contact.

        Args:
            validate: Whether to validate parameters with Pydantic
            all_messages: Filter to recive all MMSs and SMSs, 1 recive all SMS and MMS, 0 if only need MMS, important: the sms ID must be 0
            contact: Contact number for Filtering MMSs (Example: 5551234567)
            did: DID number for Filtering MMSs (Example: 5551234567)
            from_: Start Date for Filtering MMSs (Example: '2014-03-30')
            limit: Number of records to be displayed (Example: 20)
            mms: ID for a specific MMS (Example: 1918)
            timezone: Adjust time of MMSs according to Timezome (Numeric: -12 to 13)
            to: End Date for Filtering MMSs (Example: '2014-03-30')
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
        id_: int | None = None,
        media_as_array: int | None = None,
    ) -> dict[str, Any]:
        """- Retrieves media files from the message.

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
        music_on_hold: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Music on Hold Options if no additional parameter is provided. - Retrieves a specific Music on Hold Option if a MOH code is provided.

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
        nat: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of NAT Options if no additional parameter is provided. - Retrieves a specific NAT Option if a NAT code is provided.

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
        package: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Packages if no additional parameter is provided. - Retrieves a specific Package if a package code is provided.

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
        group: str | None = None,
        group_name: str | None = None,
        name: str | None = None,
        phonebook: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Phonebook entries if no additional parameter is provided. - Retrieves a list of Phonebook entries if a name is provided. - Retrieves a specific Phonebook entry if a Phonebook code is provided. - Retrieves a list of Phonebook entries if a phonebook group name is provided. - Retrieves a list of Phonebook entries if a phonebook group code is provided.

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
        group: str | None = None,
        name: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Phonebook groups if no additional parameter is provided. - Retrieves a list of Phonebook groups if a name is provided. - Retrieves a specific Phonebook group if a group ID is provided.

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
        play_instructions: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Play Instructions modes if no additional parameter is provided. - Retrieves a specific Play Instructions mode if a play code is provided.

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
        did: str,
    ) -> dict[str, Any]:
        """- Shows if a DID Number can be ported into our network. - Display plans and rates available if the DID Number can be ported into our network.

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
        protocol: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Protocols if no additional parameter is provided. - Retrieves a specific Protocol if a protocol code is provided.

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
    ) -> dict[str, Any]:
        """- Retrieves a list of Canadian Provinces.

        Returns:
            Response from getProvinces operation
        """
        ...

    async def getQueues(
        self,
        validate: bool = True,
        *,
        queue: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Queue entries if no additional parameter is provided. - Retrieves a specific Queue entry if a Queue code is provided.

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
    ) -> dict[str, Any]:
        """- Retrieves a list of Canadian Ratecenters by Province.

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
    ) -> dict[str, Any]:
        """- Retrieves a list of USA Ratecenters by State.

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
        package: str,
        query: str,
    ) -> dict[str, Any]:
        """- Retrieves the Rates for a specific Package and a Search term.

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
        recording: str,
    ) -> dict[str, Any]:
        """- Retrieves a specific Recording File data in Base64 format.

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
        recording: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Recordings if no additional parameter is provided. - Retrieves a specific Recording if a Recording code is provided.

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
        account: str,
    ) -> dict[str, Any]:
        """- Retrieves the Registration Status of all accounts if no account is provided.

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
        type_: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of 'ReportEstimateHoldTime' Types if no additional parameter is provided. - Retrieves a specific 'ReportEstimateHoldTime' Type if a type code is provided.

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
        client: str,
    ) -> dict[str, Any]:
        """- Retrieves Balance and Calls Statistics for a specific Reseller Client for the last 30 days and current day.

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
        timezone: float,
        account: str | None = None,
        answered: bool | None = None,
        busy: bool | None = None,
        callbilling: str | None = None,
        calltype: str | None = None,
        failed: bool | None = None,
        noanswer: bool | None = None,
    ) -> dict[str, Any]:
        """- Retrieves the Call Detail Records for a specific Reseller Client.

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Filter CDR by Account (Values from getCallAccounts)
            answered: Include Answered Calls to CDR (Boolean: 1/0)
            busy: Include Busy Calls to CDR (Boolean: 1/0)
            callbilling: Filter CDR by Call Billing (Values from getCallBilling)
            calltype: Filters CDR by Call Type (Values from getCallTypes)
            client: ID for a specific Reseller Client (Example: 561115) (required)
            date_from: Start Date for Filtering CDR (Example: '2010-11-30') (required)
            date_to: End Date for Filtering CDR (Example: '2010-11-30') (required)
            failed: Include Failed Calls to CDR (Boolean: 1/0)
            noanswer: Include NoAnswered calls to CDR (Boolean: 1/0)
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
        all_messages: int | None = None,
        contact: str | None = None,
        did: str | None = None,
        from_: str | None = None,
        limit: str | None = None,
        timezone: str | None = None,
        to: str | None = None,
        type_: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of MMS messages for a specific Reseller Client. by: date range, mms type, DID number, and contact

        Args:
            validate: Whether to validate parameters with Pydantic
            all_messages: Filter to recive all SMSs and MMSs, 1 recive all SMS and MMS, 0 if only need SMS, important: the sms ID must be 0
            client:  (required)
            contact: Contact number for Filtering MMSs (Example: 5551234567)
            did: DID number for Filtering MMSs (Example: 5551234567)
            from_: Start Date for Filtering SMSs (Example: '2014-03-30')
            limit: Number of records to be displayed (Example: 20)
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
        all_messages: int | None = None,
        contact: str | None = None,
        did: str | None = None,
        from_: str | None = None,
        limit: str | None = None,
        sms: int | None = None,
        timezone: str | None = None,
        to: str | None = None,
        type_: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of SMS messages for a specific Reseller Client. by: date range, sms type, DID number, and contact

        Args:
            validate: Whether to validate parameters with Pydantic
            all_messages: Filter to recive all SMSs and MMSs, 1 recive all SMS and MMS, 0 if only need SMS, important: the sms ID must be 0
            client:  (required)
            contact: Contact number for Filtering SMSs (Example: 5551234567)
            did: DID number for Filtering SMSs (Example: 5551234567)
            from_: Start Date for Filtering SMSs (Example: '2014-03-30')
            limit: Number of records to be displayed (Example: 20)
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
        ring_group: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Ring Groups if no additional parameter is provided. - Retrieves a specific Ring Group if a ring group code is provided.

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
        strategy: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Ring Strategies if no additional parameter is provided. - Retrieves a specific Ring Strategy if a ring strategy code is provided.

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
        route: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Route Options if no additional parameter is provided. - Retrieves a specific Route Option if a route code is provided.

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
        sipuri: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of SIP URIs if no additional parameter is provided. - Retrieves a specific SIP URI if a SIP URI code is provided.

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
        all_messages: int | None = None,
        contact: str | None = None,
        did: str | None = None,
        from_: str | None = None,
        limit: str | None = None,
        sms: int | None = None,
        timezone: str | None = None,
        to: str | None = None,
        type_: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of SMS messages by: date range, sms type, DID number, and contact.

        Args:
            validate: Whether to validate parameters with Pydantic
            all_messages: Filter to recive all SMSs and MMSs, 1 recive all SMS and MMS, 0 if only need SMS, important: the sms ID must be 0
            contact: Contact number for Filtering SMSs (Example: 5551234567)
            did: DID number for Filtering SMSs (Example: 5551234567)
            from_: Start Date for Filtering SMSs (Example: '2014-03-30')
            limit: Number of records to be displayed (Example: 20)
            sms: ID for a specific SMS (Example: 5853)
            timezone: Adjust time of SMSs according to Timezome (Numeric: -12 to 13)
            to: End Date for Filtering SMSs (Example: '2014-03-30')
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
        server_pop: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Servers with their info if no additional parameter is provided. - Retrieves a specific Server with its info if a Server POP is provided.

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
    ) -> dict[str, Any]:
        """- Retrieves a list of USA States.

        Returns:
            Response from getStates operation
        """
        ...

    async def getStaticMembers(
        self,
        validate: bool = True,
        *,
        queue: str,
        member: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Static Members from a queue if no additional parameter is provided. - Retrieves a specific Static Member from a queue if Queue ID and Member ID are provided

        Args:
            validate: Whether to validate parameters with Pydantic
            member: ID for a specific Static Member (Example: 163)
            queue: ID for a specific Queue (Example: 4136) (required)

        Returns:
            Response from getStaticMembers operation
        """
        ...

    async def getSubAccounts(
        self,
        validate: bool = True,
        *,
        account: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves all Sub Accounts if no additional parameter is provided. - Retrieves Reseller Client Accounts if Reseller Client ID is provided. - Retrieves a specific Sub Account if a Sub Account is provided.

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Parameter could have the following values:

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
    ) -> dict[str, Any]:
        """- Retrieves the Rates for a specific Route (Premium, Value) and a Search term.

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
        timecondition: int | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Time Conditions if no additional parameter is provided. - Retrieves a specific Time Condition if a time condition code is provided.

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
        timezone: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Timezones if no additional parameter is provided. - Retrieves a specific Timezone if a timezone code is provided.

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
    ) -> dict[str, Any]:
        """- Retrieves the Transaction History records between two dates.

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
    ) -> dict[str, Any]:
        """- Retrieves a list of vpri.

        Returns:
            Response from getVPRIs operation
        """
        ...

    async def getVoicemailAttachmentFormats(
        self,
        validate: bool = True,
        *,
        email_attachment_format: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Email Attachment Format Options if no additional parameter is provided. - Retrieves a specific Email Attachment Format Option if a format value is provided.

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
        folder: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of default Voicemail Folders if no additional parameter is provided. - Retrieves a list of Voicemail Folders within a mailbox if mailbox parameter is provided. - Retrieves a specific Folder if a folder name is provided.

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
        mailbox: str,
        message_num: int,
    ) -> dict[str, Any]:
        """- Retrieves a specific Voicemail Message File in Base64 format.

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
        mailbox: str,
        date_from: str | None = None,
        date_to: str | None = None,
        folder: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Voicemail Messages if mailbox parameter is provided. - Retrieves a list of Voicemail Messages in a Folder if a folder is provided. - Retrieves a list of Voicemail Messages in a date range if a from and to are provided.

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
        voicemailsetup: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Voicemail Setup Options if no additional parameter is provided. - Retrieves a specific Voicemail Setup Option if a voicemail setup code is provided.

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
        mailbox: str | None = None,
    ) -> dict[str, Any]:
        """- Retrieves a list of Voicemails if no additional parameter is provided. - Retrieves a specific Voicemail if a voicemail code is provided.

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
        email: str,
        id_: int,
    ) -> dict[str, Any]:
        """- Send a Fax Message attached as a PDF file to an email destination.

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
        listened: str,
        mailbox: str,
        message_num: int,
    ) -> dict[str, Any]:
        """- Mark a Voicemail Message as Listened or Unlistened. - If value is 'yes', the voicemail message will be marked as listened and will be moved to the Old Folder. - If value is 'no', the voicemail message will be marked as not-listened and will be moved to the INBOX Folder.

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
        mailbox: str,
        message_num: int,
        urgent: str,
    ) -> dict[str, Any]:
        """- Mark Voicemail Message as Urgent or not Urgent. - If value is 'yes', the voicemail message will be marked as urgent and will be moved to the Urgent Folder. - If value is 'no', the voicemail message will be unmarked as urgent and will be moved to the INBOX Folder.

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
        test: int | None = None,
    ) -> dict[str, Any]:
        """- Moves a Fax Message to a different folder.

        Args:
            validate: Whether to validate parameters with Pydantic
            fax_id: ID of the Fax Message requested (Values from getFaxMessages) (required)
            folder_id: ID of the destination Fax Folder (Values from getFaxFolders) (required)
            test: Set to true if testing how to move a Fax Message

        Returns:
            Response from moveFaxMessage operation
        """
        ...

    async def moveFolderVoicemailMessage(
        self,
        validate: bool = True,
        *,
        folder: str,
        mailbox: str,
        message_num: int,
        new_folder: str,
    ) -> dict[str, Any]:
        """- Move Voicemail Message to a Destination Folder.

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
        billing_type: int,
        cnam: int,
        dialtime: int,
        did: str,
        pop: int,
        routing: str,
        account: str | None = None,
        callerid_prefix: str | None = None,
        failover_busy: str | None = None,
        failover_noanswer: str | None = None,
        failover_unreachable: str | None = None,
        minute: str | None = None,
        monthly: str | None = None,
        note: str | None = None,
        setup: str | None = None,
        test: bool | None = None,
        voicemail: str | None = None,
    ) -> dict[str, Any]:
        """- Orders and Adds a new DID Number to the Account.

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Reseller Sub Account (Example: '100001_VoIP')
            billing_type: Billing type for the DID (1 = Per Minute, 2 = Flat) (required)
            callerid_prefix: Caller ID Prefix for the DID
            cnam: CNAM for the DID (Boolean: 1/0) (required)
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
            test: Set to true if testing how Orders work
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
        billing_type: int,
        cnam: str,
        dialtime: int,
        location_id: str,
        pop: int,
        quantity: int,
        routing: str,
        account: str | None = None,
        callerid_prefix: str | None = None,
        failover_busy: str | None = None,
        failover_noanswer: str | None = None,
        failover_unreachable: str | None = None,
        minute: str | None = None,
        monthly: str | None = None,
        note: str | None = None,
        setup: str | None = None,
        test: int | None = None,
        voicemail: str | None = None,
    ) -> dict[str, Any]:
        """- Orders and Adds new International Geographic DID Numbers to the Account.

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Reseller Sub Account (Example: '100001_VoIP')
            billing_type: Billing type for the DID (1 = Per Minute, 2 = Flat) (required)
            callerid_prefix: Caller ID Prefix for the DID
            cnam: CNAM for the DID (Boolean: 1/0) (required)
            dialtime: Dial Time Out for the DID (Example: 60 -> in seconds) (required)
            failover_busy: Busy Routing for the DID
            failover_noanswer: NoAnswer Routing for the DID
            failover_unreachable: Unreachable Routing for the DID
            location_id: ID for a specific International Location (required)
            minute: Minute Rate for Reseller Client (Example: 0.03)
            monthly: Montly Fee for Reseller Client (Example: 3.50)
            note: Note for the DID
            pop: Point of Presence for the DID (Example: 5) (required)
            quantity: Number of dids to be purchased (Example: 2) (required)
            routing: Main Routing for the DID (required)
            setup: Setup Fee for Reseller Client (Example: 1.99)
            test: Set to true if testing how Orders work
            voicemail: Voicemail for the DID (Example: 101)

        Returns:
            Response from orderDIDInternationalGeographic operation
        """
        ...

    async def orderDIDInternationalNational(
        self,
        validate: bool = True,
        *,
        billing_type: int,
        cnam: str,
        dialtime: int,
        location_id: str,
        pop: int,
        quantity: int,
        routing: str,
        account: str | None = None,
        callerid_prefix: str | None = None,
        failover_busy: str | None = None,
        failover_noanswer: str | None = None,
        failover_unreachable: str | None = None,
        minute: str | None = None,
        monthly: str | None = None,
        note: str | None = None,
        setup: str | None = None,
        test: int | None = None,
        voicemail: str | None = None,
    ) -> dict[str, Any]:
        """- Orders and Adds new International National DID Numbers to the Account.

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Reseller Sub Account (Example: '100001_VoIP')
            billing_type: Billing type for the DID (1 = Per Minute, 2 = Flat) (required)
            callerid_prefix: Caller ID Prefix for the DID
            cnam: CNAM for the DID (Boolean: 1/0) (required)
            dialtime: Dial Time Out for the DID (Example: 60 -> in seconds) (required)
            failover_busy: Busy Routing for the DID
            failover_noanswer: NoAnswer Routing for the DID
            failover_unreachable: Unreachable Routing for the DID
            location_id: ID for a specific International Location (required)
            minute: Minute Rate for Reseller Client (Example: 0.03)
            monthly: Montly Fee for Reseller Client (Example: 3.50)
            note: Note for the DID
            pop: Point of Presence for the DID (Example: 5) (required)
            quantity: Number of dids to be purchased (Example: 2) (required)
            routing: Main Routing for the DID (required)
            setup: Setup Fee for Reseller Client (Example: 1.99)
            test: Set to true if testing how Orders work
            voicemail: Voicemail for the DID (Example: 101)

        Returns:
            Response from orderDIDInternationalNational operation
        """
        ...

    async def orderDIDInternationalTollFree(
        self,
        validate: bool = True,
        *,
        cnam: str,
        dialtime: int,
        location_id: str,
        pop: int,
        quantity: int,
        routing: str,
        account: str | None = None,
        callerid_prefix: str | None = None,
        failover_busy: str | None = None,
        failover_noanswer: str | None = None,
        failover_unreachable: str | None = None,
        minute: str | None = None,
        monthly: str | None = None,
        note: str | None = None,
        setup: str | None = None,
        test: int | None = None,
        voicemail: str | None = None,
    ) -> dict[str, Any]:
        """- Orders and Adds new International TollFree DID Numbers to the Account.

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Reseller Sub Account (Example: '100001_VoIP')
            callerid_prefix: Caller ID Prefix for the DID
            cnam: CNAM for the DID (Boolean: 1/0) (required)
            dialtime: Dial Time Out for the DID (Example: 60 -> in seconds) (required)
            failover_busy: Busy Routing for the DID
            failover_noanswer: NoAnswer Routing for the DID
            failover_unreachable: Unreachable Routing for the DID
            location_id: ID for a specific International Location (required)
            minute: Minute Rate for Reseller Client (Example: 0.03)
            monthly: Montly Fee for Reseller Client (Example: 3.50)
            note: Note for the DID
            pop: Point of Presence for the DID (Example: 5) (required)
            quantity: Number of dids to be purchased (Example: 2) (required)
            routing: Main Routing for the DID (required)
            setup: Setup Fee for Reseller Client (Example: 1.99)
            test: Set to true if testing how Orders work
            voicemail: Voicemail for the DID (Example: 101)

        Returns:
            Response from orderDIDInternationalTollFree operation
        """
        ...

    async def orderDIDVirtual(
        self,
        validate: bool = True,
        *,
        cnam: str,
        dialtime: int,
        digits: int,
        pop: int,
        routing: str,
        account: str | None = None,
        callerid_prefix: str | None = None,
        failover_busy: str | None = None,
        failover_noanswer: str | None = None,
        failover_unreachable: str | None = None,
        minute: str | None = None,
        monthly: str | None = None,
        note: str | None = None,
        setup: str | None = None,
        test: int | None = None,
        voicemail: str | None = None,
    ) -> dict[str, Any]:
        """- Orders and Adds a new Virtual DID Number to the Account.

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Reseller Sub Account (Example: '100001_VoIP')
            callerid_prefix: Caller ID Prefix for the DID
            cnam: CNAM for the DID (Boolean: 1/0) (required)
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
            test: Set to true if testing how Orders work
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
        quantity: int,
        email: str | None = None,
        email_attach_file: str | None = None,
        email_enable: str | None = None,
        test: int | None = None,
        url_callback: str | None = None,
        url_callback_enable: str | None = None,
        url_callback_retry: str | None = None,
    ) -> dict[str, Any]:
        """- Orders and Adds a new Fax Number to the Account.

        Args:
            validate: Whether to validate parameters with Pydantic
            email: Email address where send notifications when receive Fax Messages
            email_attach_file: Flag to enable attach the Fax Message as a PDF file in the notifications.
            email_enable: Flag to enable the email notifications.
            location: Location ID of the Fax Number (Values from getFaxRateCentersCAN/getFaxRateCentersUSA) (required)
            quantity: Quantity of Fax Numbers to order (Example: 3) (required)
            test: Set to true if testing how Orders work
            url_callback: URL where make a POST when you receive a Fax Message.
            url_callback_enable: Flag to enable the URL Callback functionality.
            url_callback_retry: Flag to enable retry the POST action in case we don't receive "ok".

        Returns:
            Response from orderFaxNumber operation
        """
        ...

    async def orderTollFree(
        self,
        validate: bool = True,
        *,
        cnam: int,
        dialtime: int,
        did: str,
        pop: int,
        routing: str,
        account: str | None = None,
        callerid_prefix: str | None = None,
        failover_busy: str | None = None,
        failover_noanswer: str | None = None,
        failover_unreachable: str | None = None,
        minute: str | None = None,
        monthly: str | None = None,
        note: str | None = None,
        setup: str | None = None,
        test: bool | None = None,
        voicemail: str | None = None,
    ) -> dict[str, Any]:
        """- Orders and Adds a new Toll Free Number to the Account.

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Reseller Sub Account (Example: '100001_VoIP')
            callerid_prefix: Caller ID Prefix for the DID
            cnam: CNAM for the DID (Boolean: 1/0) (required)
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
            test: Set to true if testing how Orders work
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
        cnam: int,
        dialtime: int,
        did: str,
        pop: int,
        routing: str,
        account: str | None = None,
        callerid_prefix: str | None = None,
        failover_busy: str | None = None,
        failover_noanswer: str | None = None,
        failover_unreachable: str | None = None,
        minute: str | None = None,
        monthly: str | None = None,
        note: str | None = None,
        setup: str | None = None,
        test: bool | None = None,
        voicemail: str | None = None,
    ) -> dict[str, Any]:
        """- Orders and Adds a new Vanity Toll Free Number to the Account.

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Reseller Sub Account (Example: '100001_VoIP')
            callerid_prefix: Caller ID Prefix for the DID
            carrier: Carrier for the DID (Values from getCarriers) (required)
            cnam: CNAM for the DID (Boolean: 1/0) (required)
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
            test: Set to true if testing how Orders work
            voicemail: Voicemail for the DID (Example: 101)

        Returns:
            Response from orderVanity operation
        """
        ...

    async def removeDIDvPRI(
        self,
        validate: bool = True,
        *,
        did: str,
        vpri: int | None = None,
    ) -> dict[str, Any]:
        """- Removes a DID from a VPRI

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
        province: str | None = None,
    ) -> dict[str, Any]:
        """- Searches for Canadian DIDs by Province using a Search Criteria.

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
        state: str | None = None,
    ) -> dict[str, Any]:
        """- Searches for USA DIDs by State using a Search Criteria.

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
    ) -> dict[str, Any]:
        """- Retrieves a list of Canadian Ratecenters searched by Area Code.

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
    ) -> dict[str, Any]:
        """- Retrieves a list of USA Ratecenters searched by Area Code.

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
        query: str | None = None,
        type_: str | None = None,
    ) -> dict[str, Any]:
        """- Searches for USA/Canada Toll Free Numbers using a Search Criteria. - Shows all USA/Canada Toll Free Numbers available if no criteria is provided.

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
        query: str | None = None,
        type_: str | None = None,
    ) -> dict[str, Any]:
        """- Searches for USA Toll Free Numbers using a Search Criteria. - Shows all USA Toll Free Numbers available if no criteria is provided.

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
    ) -> dict[str, Any]:
        """- Searches for Vanity Toll Free Numbers using a Search Criteria.

        Args:
            validate: Whether to validate parameters with Pydantic
            query: Query for searching : 7 Chars (required)
            type_: Type of Vanity Number (required)

        Returns:
            Response from searchVanity operation
        """
        ...

    async def sendCallRecordingEmail(
        self,
        validate: bool = True,
        *,
        account: str,
        callrecording: str,
        email: str,
    ) -> dict[str, Any]:
        """- Send information and audio file to email account.

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
        file: str,
        from_name: str,
        from_number: str,
        to_number: str,
        send_email: str | None = None,
        send_email_enabled: int | None = None,
        station_id: str | None = None,
        test: int | None = None,
    ) -> dict[str, Any]:
        """- Send a Fax message to a Destination Number.

        Args:
            validate: Whether to validate parameters with Pydantic
            file: The file must be encoded in Base64, and in one of the following formats: pdf, txt, jpg, gif, png, tif (required)
            from_name: Name of the sender (Example: 5552341234) (required)
            from_number: DID number of the Fax sender (required)
            send_email: Email address where you want send a copy of your Fax.
            send_email_enabled: Flag to enable the send of a copy of your Fax via email.
            station_id: An word to identify a equipment or department sending the Fax.
            test: Set to true if testing how to send a Fax Message
            to_number: Destination DID Number (Example: 5552341234) (required)

        Returns:
            Response from sendFaxMessage operation
        """
        ...

    async def sendMMS(
        self,
        validate: bool = True,
        *,
        did: str,
        dst: str,
        message: str,
        media1: str | None = None,
        media2: str | None = None,
        media3: str | None = None,
    ) -> dict[str, Any]:
        """- Send a MMS message to a Destination Number.

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
        did: str,
        dst: str,
        message: str,
    ) -> dict[str, Any]:
        """- Send a SMS message to a Destination Number.

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
        email_address: str,
        folder: str,
        mailbox: str,
        message_num: int,
    ) -> dict[str, Any]:
        """- Send a Voicemail Message File to an Email Address.

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
        music: str,
        order: str,
        press: str,
        recording: str,
        ring_time: str,
        callhunting: int | None = None,
    ) -> dict[str, Any]:
        """- Updates a specific Call Hunting if a Call Hunting code is provided. - Adds a new Call Hunting if no Call Hunting code is provided.

        Args:
            validate: Whether to validate parameters with Pydantic
            callhunting: ID for a specific Call Hunting (Example: 235 / Leave empty to create a new one)
            description: Description for the Call Hunting (required)
            language: Language for the Call Hunting (values from getLanguages) (required)
            members: The list of members assigned to the call hunting (required)
            music: Music on Hold Code (Values from getMusicOnHold) (required)
            order: The members will be called in follow or random order (values follow or random) (required)
            press: This option confirm if the member will take the call by pressing 1 (required)
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
        destination: str,
        failover: str,
        language: str,
        music: str,
        name: str,
        timeout: int,
        callparking: int | None = None,
    ) -> dict[str, Any]:
        """- Updates a specific Call Parking entry if a Call Parking ID is provided. - Adds a new Call Parking entry if no Call Parking ID is provided.

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
        delay_before: int,
        description: str,
        digit_timeout: int,
        number: int,
        response_timeout: int,
        callback: str | None = None,
        callerid_number: str | None = None,
    ) -> dict[str, Any]:
        """- Updates a specific Callback if a callback code is provided. - Adds a new Callback entry if no callback code is provided.

        Args:
            validate: Whether to validate parameters with Pydantic
            callback: ID for a specific Callback
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
        callerid: str,
        did: str,
        routing: str,
        failover_busy: str | None = None,
        failover_noanswer: str | None = None,
        failover_unreachable: str | None = None,
        filter: str | None = None,
        note: str | None = None,
    ) -> dict[str, Any]:
        """- Updates a specific Caller ID Filtering if a filtering code is provided. - Adds a new Caller ID Filtering if no filtering code is provided.

        Args:
            validate: Whether to validate parameters with Pydantic
            callerid: Caller ID that triggers the Filter (required)
            did: DIDs affected by the filter (all, NPANXXXXXX) (required)
            failover_busy: Route the call follows when busy
            failover_noanswer: Route the call follows when noanswer
            failover_unreachable: Route the call follows when unreachable
            filter: ID for a specific Caller ID Filtering
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
        phone_number: str,
        address: str | None = None,
        balance_management: int | None = None,
        city: str | None = None,
        company: str | None = None,
        country: str | None = None,
        state: str | None = None,
        zip: str | None = None,
    ) -> dict[str, Any]:
        """- Updates Reseller Client information.

        Args:
            validate: Whether to validate parameters with Pydantic
            address: Client's Address
            balance_management: Balance Management for Client
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
        threshold: int,
        email: str | None = None,
    ) -> dict[str, Any]:
        """- Update the Threshold Amount for a specific Reseller Client. - Update the Threshold notification e-mail for a specific Reseller Client if the e-mail address is provided.

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
        language: str | None = None,
        members: str | None = None,
        sound_error_menu: str | None = None,
        sound_get_pin: str | None = None,
        sound_has_joined: str | None = None,
        sound_has_left: str | None = None,
        sound_invalid_pin: str | None = None,
        sound_join: str | None = None,
        sound_kicked: str | None = None,
        sound_leave: str | None = None,
        sound_locked: str | None = None,
        sound_locked_now: str | None = None,
        sound_muted: str | None = None,
        sound_only_one: str | None = None,
        sound_only_person: str | None = None,
        sound_other_in_party: str | None = None,
        sound_participants_muted: str | None = None,
        sound_participants_unmuted: str | None = None,
        sound_place_into_conference: str | None = None,
        sound_there_are: str | None = None,
        sound_unlocked_now: str | None = None,
        sound_unmuted: str | None = None,
    ) -> dict[str, Any]:
        """- Updates a specific Conference if a conference code is provided. - Adds a new Conference entry if no conference code is provided.

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
        admin: str | None = None,
        announce_join_leave: str | None = None,
        announce_only_user: str | None = None,
        announce_user_count: str | None = None,
        announcement: int | None = None,
        description: str | None = None,
        drop_silence: str | None = None,
        jitter_buffer: str | None = None,
        moh_when_empty: str | None = None,
        pin: int | None = None,
        quiet: str | None = None,
        silence_threshold: int | None = None,
        start_muted: str | None = None,
        talk_detection: str | None = None,
        talking_threshold: int | None = None,
    ) -> dict[str, Any]:
        """- Updates a specific Member profile if a member code is provided. - Adds a new Member profile entry if no member code is provided.

        Args:
            validate: Whether to validate parameters with Pydantic
            admin: Sets if the member is an admin or not (yes/no).
            announce_join_leave: Sets if the conference recording when a member joins or leaves will be played (yes/no).
            announce_only_user: Sets if the "only user" announcement should be played when a caller enters an empty conference (yes/no).
            announce_user_count: Sets if the number of members in the conference should be announced to the caller as he joins (yes/no).
            announcement: If set, this recording will be heard only by the user as he joins the conference (Values from getRecordings).
            conference: ID for a specific Conference (Example: 5356) (required)
            description: Member description.
            drop_silence: The system will drop what is detected as silence from entering into the conference (yes/no).
            jitter_buffer: When set to YES, the system will place a jitter buffer on the caller's audio stream before any audio mixing is performed (yes/no).
            member: ID for a specific Member profile (Example: 5356) (required)
            moh_when_empty: Sets whether music on hold (MOH) should be played when only one person is in the conference (Values from getMusicOnHold).
            name: Member name. (required)
            pin: Assigned PIN.
            quiet: When set to "yes", enter/leave prompts and user introductions are not played (yes/no).
            silence_threshold: The time, in milliseconds, that silence needs to be present in the user’s sound stream before the system can consider it to be in fact silent and close the audio (allowed values are 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900 or 3000).
            start_muted: Sets if the member should start out muted after entering the conference (yes/no).
            talk_detection: If set to YES, the conference dashboard will display a notification when a participant starts and stops talking (yes/no).
            talking_threshold: The time, in milliseconds, that a users needs to be sending sound or voice before the system can consider them to be talking (allowed values are 100, 120, 140, 160, 180, 200, 220, 240 or 250).

        Returns:
            Response from setConferenceMember operation
        """
        ...

    async def setDIDBillingType(
        self,
        validate: bool = True,
        *,
        billing_type: int,
        did: str,
    ) -> dict[str, Any]:
        """- Updates the Billing Plan from a specific DID.

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
        billing_type: int,
        cnam: int,
        dialtime: int,
        did: str,
        pop: int,
        routing: str,
        callerid_prefix: str | None = None,
        failover_busy: str | None = None,
        failover_noanswer: str | None = None,
        failover_unreachable: str | None = None,
        note: str | None = None,
        port_out_pin: int | None = None,
        record_calls: int | None = None,
        transcribe: int | None = None,
        transcription_email: str | None = None,
        transcription_locale: str | None = None,
        transcription_start_delay: int | None = None,
        voicemail: str | None = None,
        voicemail_threshold: int | None = None,
    ) -> dict[str, Any]:
        """- Updates the information from a specific DID.

        Args:
            validate: Whether to validate parameters with Pydantic
            billing_type: Billing type for the DID (1 = Per Minute, 2 = Flat) (required)
            callerid_prefix: Caller ID Prefix for the DID
            cnam: CNAM for the DID (Boolean: 1/0) (required)
            dialtime: Dial Time Out for the DID (Example: 60 -> in seconds) (required)
            did: DID to be Updated (Example: 5551234567) (required)
            failover_busy: Busy Routing for the DID
            failover_noanswer: NoAnswer Routing for the DID
            failover_unreachable: Unreachable Routing for the DID
            note: Note for the DID
            pop: Point of Presence for the DID (required)
            port_out_pin: Port Out PIN protection is used as a means of authorizing outgoing portability (only for selected US numbers with the lock icon)
            record_calls: Record Calls (Boolean: 1/0)
            routing: Main Routing for the DID (required)
            transcribe: Enable Call Transcription (Boolean: 1/0)
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
        did: str,
        pop: int,
    ) -> dict[str, Any]:
        """- Updates the POP from a specific DID.

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
        did: str,
        routing: str,
    ) -> dict[str, Any]:
        """- Updates the Routing from a specific DID.

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
        did: str,
        voicemail: str | None = None,
    ) -> dict[str, Any]:
        """- Updates the Voicemail from a specific DID.

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
        digit_timeout: int,
        name: str,
        pin: int,
        callerid_override: str | None = None,
        disa: str | None = None,
    ) -> dict[str, Any]:
        """- Updates a specific DISA if a disa code is provided. - Adds a new DISA entry if no disa code is provided.

        Args:
            validate: Whether to validate parameters with Pydantic
            callerid_override: Caller ID Override for the DISA
            digit_timeout: Time between digits (required)
            disa: ID for a specific DISA
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
        auth_email: str,
        from_number_id: str,
        security_code: str,
        enabled: int | None = None,
        id_: int | None = None,
        security_code_enabled: int | None = None,
        test: int | None = None,
    ) -> dict[str, Any]:
        """- Create or update the information of a specific "Email to Fax configuration".

        Args:
            validate: Whether to validate parameters with Pydantic
            auth_email: Email address from you will sent Fax Messages (required)
            enabled: If Enable, we will send Fax Message when we receive an email from the provided address. (Values:1=Enable / 0=Disable)
            from_number_id: Fax number that will appear as fax sender. (values from getFaxNumbersInfo) (required)
            id_: [Only for updates] ID of the "Email to Fax" to edit (Values from getEmailToFax)
            security_code: An alphanumeric code to identify your emails before send as Fax. (required)
            security_code_enabled: If Enable, we will check the mail subject if this include a Security Code before send the Fax. (Values:1=Enable / 0=Disable)
            test: Set to true if testing.

        Returns:
            Response from setEmailToFax operation
        """
        ...

    async def setFaxFolder(
        self,
        validate: bool = True,
        *,
        name: str,
        id_: int | None = None,
        test: int | None = None,
    ) -> dict[str, Any]:
        """- Create or update the information of a specific Fax Folder.

        Args:
            validate: Whether to validate parameters with Pydantic
            id_: [Only for updates] ID of the Fax Folder to edit (Values from getFaxFolders)
            name: Name of the Fax Folder to create or update (Example: FAMILY) (required)
            test: Set to true if testing how to create/update a Fax Folder

        Returns:
            Response from setFaxFolder operation
        """
        ...

    async def setFaxNumberEmail(
        self,
        validate: bool = True,
        *,
        did: int,
        email: str | None = None,
        email_attach_file: str | None = None,
        email_enable: str | None = None,
        test: int | None = None,
    ) -> dict[str, Any]:
        """- Updates the email configuration from a specific Fax Number.

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID Number to be ported into our network (Example: 5552341234) (required)
            email: Email address where send notifications when receive Fax Messages
            email_attach_file: Flag to enable attach the Fax Message as a PDF file in the notifications.
            email_enable: Flag to enable the email notifications.
            test: Set to true if testing how to set the email of a Fax Number

        Returns:
            Response from setFaxNumberEmail operation
        """
        ...

    async def setFaxNumberInfo(
        self,
        validate: bool = True,
        *,
        did: int,
        email: str | None = None,
        email_attach_file: str | None = None,
        email_enable: str | None = None,
        test: int | None = None,
        url_callback: str | None = None,
        url_callback_enable: str | None = None,
        url_callback_retry: str | None = None,
    ) -> dict[str, Any]:
        """- Updates the information from a specific Fax Number.

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID Number to be ported into our network (Example: 5552341234) (required)
            email: Email address where send notifications when receive Fax Messages
            email_attach_file: Flag to enable attach the Fax Message as a PDF file in the notifications.
            email_enable: Flag to enable the email notifications.
            test: Set to true if testing how to update the information of a Fax Number
            url_callback: URL where make a POST when you receive a Fax Message.
            url_callback_enable: Flag to enable the URL Callback functionality.
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
        test: int | None = None,
        url_callback: str | None = None,
        url_callback_enable: str | None = None,
        url_callback_retry: str | None = None,
    ) -> dict[str, Any]:
        """- Updates the url callback configuration from a specific Fax Number.

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID Number to be ported into our network (Example: 5552341234) (required)
            test: Set to true if testing how to set the URL callback of a Fax Number
            url_callback: URL where make a POST when you receive a Fax Message.
            url_callback_enable: Flag to enable the URL Callback functionality.
            url_callback_retry: Flag to enable retry the POST action in case we don't receive "ok".

        Returns:
            Response from setFaxNumberURLCallback operation
        """
        ...

    async def setForwarding(
        self,
        validate: bool = True,
        *,
        phone_number: str,
        callerid_override: str | None = None,
        description: str | None = None,
        diversion_header: int | None = None,
        dtmf_digits: str | None = None,
        forwarding: str | None = None,
        pause: str | None = None,
    ) -> dict[str, Any]:
        """- Updates a specific Forwarding if a fwd code is provided. - Adds a new Forwarding entry if no fwd code is provided.

        Args:
            validate: Whether to validate parameters with Pydantic
            callerid_override: Caller ID Override for the Forwarding
            description: Description for the Forwarding
            diversion_header: If enabled, we will add a Diversion Header to your forwarded call
            dtmf_digits: Send DTMF digits when call is answered
            forwarding: ID for a specific Forwarding
            pause: Pause (seconds) when call is answered before sending digits
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
        recording: int,
        timeout: int,
        voicemailsetup: int,
        ivr: str | None = None,
    ) -> dict[str, Any]:
        """- Updates a specific IVR if an IVR code is provided. - Adds a new IVR entry if no IVR code is provided.

        Args:
            validate: Whether to validate parameters with Pydantic
            choices: Choices for the IVR (Example: '1=sip:5096 ; 2=fwd:20222') (required)
            ivr: ID for a specific IVR
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
        name: str,
        recordings: str,
        sort: str,
        volume: str,
    ) -> dict[str, Any]:
        """- Update music on hold settings

        Args:
            validate: Whether to validate parameters with Pydantic
            description:  (required)
            name:  (required)
            recordings:  (required)
            sort:  (required)
            volume:  (required)

        Returns:
            Response from setMusicOnHold operation
        """
        ...

    async def setPhonebook(
        self,
        validate: bool = True,
        *,
        name: str,
        number: int,
        callerid: str | None = None,
        group: int | None = None,
        note: str | None = None,
        phonebook: str | None = None,
        speed_dial: str | None = None,
    ) -> dict[str, Any]:
        """- Updates a specific Phonebook entry if a phonebook code is provided. - Adds a new Phonebook entry if no phonebook code is provided.

        Args:
            validate: Whether to validate parameters with Pydantic
            callerid: Caller ID Override when dialing via Speed Dial
            group: ID for a specific Phonebook group
            name: Name for the Phonebook Entry (required)
            note: Note for the phonebook entry
            number: Number or SIP for the Phonebook entry (Example: 'sip:2563' or '5552223333') (required)
            phonebook: ID for a specific Phonebook entry
            speed_dial: Speed Dial for the Phonebook entry

        Returns:
            Response from setPhonebook operation
        """
        ...

    async def setPhonebookGroup(
        self,
        validate: bool = True,
        *,
        name: str,
        phonebook: str,
        group: str | None = None,
        members: str | None = None,
    ) -> dict[str, Any]:
        """- Updates a specific Phonebook group if a phonebook code is provided. - Adds a new Phonebook group if no phonebook group code is provided. - Assigns or modifies group members if a member list is provided

        Args:
            validate: Whether to validate parameters with Pydantic
            group: ID for a specific Phonebook group
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
        if_announce_position_enabled_report_estimated_hold_time: str,
        join_when_empty: str,
        leave_when_empty: str,
        priority_weight: str,
        queue_language: str,
        queue_name: str,
        queue_number: int,
        report_hold_time_agent: str,
        ring_inuse: str,
        ring_strategy: str,
        agent_announcement: str | None = None,
        agent_ring_timeout: int | None = None,
        announce_position_frecuency: str | None = None,
        announce_round_seconds: str | None = None,
        callerid_prefix: int | None = None,
        fail_over_routing_full: str | None = None,
        fail_over_routing_join_empty: str | None = None,
        fail_over_routing_join_unavail: str | None = None,
        fail_over_routing_leave_empty: str | None = None,
        fail_over_routing_leave_unavail: str | None = None,
        fail_over_routing_timeout: str | None = None,
        frequency_announcement: str | None = None,
        join_announcement: str | None = None,
        maximum_callers: str | None = None,
        maximum_wait_time: str | None = None,
        member_delay: str | None = None,
        music_on_hold: str | None = None,
        queue: str | None = None,
        queue_password: str | None = None,
        retry_timer: str | None = None,
        thankyou_for_your_patience: str | None = None,
        voice_announcement: str | None = None,
        wrapup_time: str | None = None,
    ) -> dict[str, Any]:
        """- Updates a specific Queue entry if a queue code is provided. - Adds a new Queue entry if no queue code is provided.

        Args:
            validate: Whether to validate parameters with Pydantic
            agent_announcement: Recording Code (Values from getRecordings or 'none')
            agent_ring_timeout: Number of seconds to ring an agent (Values 5 to 60)
            announce_position_frecuency: How often to make any periodic announcement
            announce_round_seconds: Announce seconds (Values in seconds: 1 to 60  or 'none' = Do not announce)
            callerid_prefix: Caller ID Prefix for queue
            fail_over_routing_full: Failover routing to Maximum callers reached
            fail_over_routing_join_empty: A call was sent to the queue but the queue had no members (Only works when Join when Empty is set to no)
            fail_over_routing_join_unavail: Same as routingjoinempty, except that there were still queue members, but all were status unavailable
            fail_over_routing_leave_empty: The last agent was removed form the queue before alls calls were handled
            fail_over_routing_leave_unavail: Same as routingleaveempty, except that there were still queue members, but all were status unavailable
            fail_over_routing_timeout: Failover routing to Maximum wait time reached
            frequency_announcement: Periodic interval to play voice announce recording
            if_announce_position_enabled_report_estimated_hold_time:  (required)
            join_announcement: Recording Code (Values from getRecordings or 'none')
            join_when_empty: How caller join to the queue (Values from getJoinWhenEmptyTypes) (required)
            leave_when_empty: How caller leave the queue (Values 'yes'/'no'/'strict') (required)
            maximum_callers: Maximum callers (Values: 1 to 60 or 'unlimited')
            maximum_wait_time: Ammount of time a caller can wait in queue
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
            thankyou_for_your_patience: Yes to say "Thank you for your patience" immediatly after announcing Queue Position and Estimated hold time left
            voice_announcement: Code for Recording (Values from getRecordings or 'none')
            wrapup_time: After a successful call, the number of seconds to wait before sending a free agent another call

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
        file: str,
        name: str,
        recording: str | None = None,
    ) -> dict[str, Any]:
        """- Updates a specific Recording File if a Recording ID is provided. - Adds a new Recording file entry if no Recording ID is provided.

        Args:
            validate: Whether to validate parameters with Pydantic
            file: Base64 encoded file (required)
            name: Name for the Recording Entry (Example: 'recording1') (required)
            recording: ID for a specific Phonebook entry

        Returns:
            Response from setRecording operation
        """
        ...

    async def setRingGroup(
        self,
        validate: bool = True,
        *,
        members: str,
        name: str,
        voicemail: str,
        caller_announcement: str | None = None,
        language: str | None = None,
        music_on_hold: str | None = None,
        ring_group: str | None = None,
    ) -> dict[str, Any]:
        """- Updates a specific Ring Group if a ring group code is provided. - Adds a new Ring Group entry if no ring group code is provided.

        Args:
            validate: Whether to validate parameters with Pydantic
            caller_announcement: Recording Code (Values from getRecordings)
            language: Code for Language (Values from getLanguages)
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
        uri: str,
        callerid_e164: int | None = None,
        callerid_override: str | None = None,
        description: str | None = None,
        sipuri: str | None = None,
    ) -> dict[str, Any]:
        """- Updates a specific SIP URI if a SIP URI code is provided. - Adds a new SIP URI entry if no SIP URI code is provided.

        Args:
            validate: Whether to validate parameters with Pydantic
            callerid_e164: If this option is Enabled, then your CallerID will be E164 compliant.
            callerid_override: This setting is optional.  You can  configure a 'CallerID Number Override'.
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
        did: str,
        enable: str,
        email_address: str | None = None,
        email_enabled: str | None = None,
        sms_forward: str | None = None,
        sms_forward_enable: str | None = None,
        sms_sipaccount: str | None = None,
        sms_sipaccount_enabled: str | None = None,
        url_callback: str | None = None,
        url_callback_enable: str | None = None,
        url_callback_retry: str | None = None,
    ) -> dict[str, Any]:
        """- Enable/Disable the SMS Service for a DID- Change the SMS settings for a DID

        Args:
            validate: Whether to validate parameters with Pydantic
            did: DID to be Updated (Example: 5551234567) (required)
            email_address: SMS Messages received by your DID will be sent to the email address provided
            email_enabled: If Enable, SMS Messages received by your DID will be sent to the email address provided
            enable: Enable/Disable the DID to receive SMS Messages (Values:1=Enable / 0=Disable) (required)
            sms_forward: SMS Messages received by your DID will be forwarded to the phone number provided (Example: 5551234567)
            sms_forward_enable: If Enable, SMS Messages received by your DID will be forwarded to the phone number provided
            sms_sipaccount: SIP account or sub-account that will receive the SMS Messages
            sms_sipaccount_enabled: If Enable, SMS Messages received by your DID will be sent to the specified SIP account or sub-account
            url_callback: SMS Messages received by your DID will be send a GET request to the URL callback provided Available
            url_callback_enable: If Enable, SMS Messages received by your DID will be send a GET request to the URL callback provided
            url_callback_retry: Enable URL callback Retry

        Returns:
            Response from setSMS operation
        """
        ...

    async def setStaticMember(
        self,
        validate: bool = True,
        *,
        member_name: str,
        priority: int,
        queue: int,
        account: str | None = None,
        member: str | None = None,
    ) -> dict[str, Any]:
        """- Updates a specific Member from queue if a Member code is provided. - Adds a new Member to Queue if no Member code is provided.

        Args:
            validate: Whether to validate parameters with Pydantic
            account: Static Member Routing to receive calls
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
        allowed_codecs: str,
        auth_type: int,
        device_type: int,
        dtmf_mode: str,
        id_: int,
        international_route: int,
        lock_international: int,
        music_on_hold: str,
        nat: str,
        transcribe: int,
        transcription_email: str,
        transcription_locale: str,
        callerid_number: str | None = None,
        canada_routing: str | None = None,
        default_e911: str | None = None,
        description: str | None = None,
        dialing_mode: int | None = None,
        enable_ip_restriction: int | None = None,
        enable_pop_restriction: int | None = None,
        internal_dialtime: str | None = None,
        internal_extension: str | None = None,
        internal_voicemail: str | None = None,
        ip: str | None = None,
        ip_restriction: str | None = None,
        language: str | None = None,
        max_expiry: int | None = None,
        password: str | None = None,
        pop_restriction: str | None = None,
        record_calls: int | None = None,
        reseller_chargesetup: str | None = None,
        reseller_client: str | None = None,
        reseller_nextbilling: str | None = None,
        reseller_package: str | None = None,
        rtp_hold_timeout: int | None = None,
        rtp_timeout: int | None = None,
        send_bye: int | None = None,
        sip_traffic: int | None = None,
        tfcarrier: int | None = None,
        transcription_start_delay: int | None = None,
    ) -> dict[str, Any]:
        """- Updates Sub Account information.

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
            enable_ip_restriction: Enable IP Restriction (Boolean: 1/0)
            enable_pop_restriction: Enable POP Restriction (Boolean: 1/0)
            id_: Sub Account ID (Example: 10236) (required)
            internal_dialtime: Sub Account Internal Dialtime (Example: 60 -> seconds)
            internal_extension: Sub Account Internal Extension (Example: 1 -> Creates 101)
            internal_voicemail: Sub Account Internal Voicemail (Example: 101)
            international_route: Route Code (Values from getRoutes) (required)
            ip: Sub Account IP (For IP Authentication)
            ip_restriction: List of IP/Netmask to allow outgoing calls separated by commas
            language: Language for system messages, such as "Invalid Option" (Values from getLanguages)
            lock_international: Lock International Code (Values from getLockInternational) (required)
            max_expiry: Max Expiry between 60 and 3600 (Example: 3000)
            music_on_hold: Music on Hold Code (Values from getMusicOnHold) (required)
            nat: NAT Mode Code (Values from getNAT) (required)
            password: Sub Account Password (For Password Authentication)
            pop_restriction: List of POP Servers to allow outgoing calls separated by commas
            record_calls: Record Calls (Boolean: 1/0)
            reseller_chargesetup: True if you want to charge Package Setup Fee after Save
            reseller_client: Reseller Account ID (Example: 561115)
            reseller_nextbilling: Reseller Next Billing Date (Example: '2012-12-31')
            reseller_package: Reseller Package (Example: 92364)
            rtp_hold_timeout: RTP Hold Time Out between 1 and 3600 (Example: 600)
            rtp_timeout: RTP Time Out between 1 and 3600 (Example: 60)
            send_bye: Send BYE on successful transfer (Boolean: 1/0)
            sip_traffic: Encrypted SIP Traffic (Boolean: 1/0)
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
        endhour: str,
        endminute: str,
        name: str,
        routing_match: str,
        routing_nomatch: str,
        starthour: str,
        startminute: str,
        weekdayend: str,
        weekdaystart: str,
        timecondition: str | None = None,
    ) -> dict[str, Any]:
        """- Updates a specific Time Condition if a time condition code is provided. - Adds a new Time Condition entry if no time condition code is provided.

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
        attach_message: str,
        delete_message: str,
        language: str,
        mailbox: int,
        name: str,
        password: str,
        play_instructions: str,
        say_callerid: str,
        say_time: str,
        skip_password: str,
        timezone: str,
        email: str | None = None,
        email_attachment_format: str | None = None,
        transcription: str | None = None,
        transcription_locale: str | None = None,
        unavailable_message_recording: str | None = None,
    ) -> dict[str, Any]:
        """- Updates the information from a specific Voicemail.

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
            skip_password: True if Skipping Password (Boolean: 1/0) (required)
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
        country: str,
        email: str,
        firstname: str,
        lastname: str,
        password: str,
        phone_number: str,
        state: str,
        zip: str,
        activate: bool | None = None,
        balance_management: int | None = None,
        company: str | None = None,
    ) -> dict[str, Any]:
        """- Signs a new Reseller Client to your Reseller Account.

        Args:
            validate: Whether to validate parameters with Pydantic
            activate: Activates Client (Boolean: 1/0)
            address: Client's Address (required)
            balance_management: Balance Management for Client
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
        did: str,
    ) -> dict[str, Any]:
        """- Unconnects specific DID from Reseller Client Sub Account.

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
        did: str,
    ) -> dict[str, Any]:
        """- Unconnects specific FAX DID from Reseller Client Sub Account.

        Args:
            validate: Whether to validate parameters with Pydantic
            did: FAX DID to be Unconnected from Reseller Sub Account (Example: 5551234567) (required)

        Returns:
            Response from unconnectFAX operation
        """
        ...


@asynccontextmanager
async def VoIPMSAsyncClient(
    config: VoIPMSConfig | None = None,
    **kwargs: Any
) -> AsyncGenerator[VoIPMSAsyncService, None]: ...
