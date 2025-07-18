#!/usr/bin/env python3
"""
Example of how to handle VoIP.ms API quirks systematically
"""

# 1. Method-specific quirks in API definition
API_QUIRKS = {
    "getCDR": {
        "parameter_transforms": {
            # Convert boolean True/False to string "1"/"0"
            "answered": lambda x: "1" if x else "0",
            "noanswer": lambda x: "1" if x else "0", 
            "busy": lambda x: "1" if x else "0",
            "failed": lambda x: "1" if x else "0"
        },
        "required_defaults": {
            "timezone": "1"  # API requires timezone even though docs say optional
        }
    },
    "getCallRecordings": {
        "parameter_aliases": {
            "from_date": "date_from",  # Handle parameter name variations
            "to_date": "date_to"
        }
    }
}

# 2. Field name standardization
FIELD_MAPPINGS = {
    "getCallRecordings": {
        "response_key": "recordings",
        "id_field": "callrecording"  # Not "recording" or "id"
    },
    "getCDR": {
        "response_key": "cdr", 
        "id_field": "uniqueid"
    }
}

# Usage examples:
async def example_usage():
    from voipms import VoIPMSClientAsync
    
    async with VoIPMSClientAsync() as client:
        # Method 1: Use validate=False for known problematic methods
        cdr = await client.getCDR(
            validate=False,
            date_from="2025-07-17",
            date_to="2025-07-17", 
            answered="1",  # String, not boolean
            timezone="1"
        )
        
        # Method 2: Use normal validation for well-behaved methods
        accounts = await client.getCallAccounts()  # This works fine
        
        # Method 3: Use helper functions (if we implement them)
        # cdr = await client.getCDR_fixed(
        #     date_from="2025-07-17",
        #     date_to="2025-07-17",
        #     answered=True,  # Boolean gets converted automatically
        # )

if __name__ == "__main__":
    import asyncio
    asyncio.run(example_usage())