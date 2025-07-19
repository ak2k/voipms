#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx>=0.24.0",
#     "pydantic>=2.0.0",
#     "python-dotenv>=1.0.0",
# ]
# ///
"""
Async example of using the VoIP.ms Python client
"""

import asyncio

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
