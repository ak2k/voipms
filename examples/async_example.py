#!/usr/bin/env python3
"""
Async example of using the VoIP.ms Python client
"""

import asyncio
import os
from voipms import VoIPMSClientAsync

async def main():
    # Create async client
    async with VoIPMSClientAsync() as client:
        # Run multiple requests concurrently
        print("Fetching data concurrently...")
        
        # Create tasks for concurrent execution
        tasks = [
            client.getBalance(),
            client.getRegistrationStatus(),
            client.getServersInfo()
        ]
        
        # Wait for all tasks to complete
        balance, status, servers = await asyncio.gather(*tasks)
        
        # Display results
        print(f"\nBalance: ${balance['balance']['current_balance']}")
        print(f"Registered accounts: {len(status.get('registered', []))}")
        print(f"Available servers: {len(servers.get('servers', []))}")
        

if __name__ == "__main__":
    asyncio.run(main())