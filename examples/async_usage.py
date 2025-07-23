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

from voipms import VoIPMSAsyncClient


async def main():
    # Create async client
    async with VoIPMSAsyncClient() as client:
        # Run multiple requests concurrently
        print("Fetching data concurrently...")

        # Create tasks for concurrent execution
        tasks = [client.getBalance(), client.getServersInfo(), client.getIP()]

        # Wait for all tasks to complete
        balance, servers, ip_info = await asyncio.gather(*tasks)

        # Display results
        print(f"\nBalance: ${balance['balance']['current_balance']}")
        print(f"Available servers: {len(servers.get('servers', []))}")
        print(f"Your IP: {ip_info.get('ip', 'N/A')}")


if __name__ == "__main__":
    asyncio.run(main())
