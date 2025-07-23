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
Basic usage of the VoIP.ms Python client

Shows the simplest way to:
- Get account balance
- Check registration status
- List available servers
"""

from voipms import VoIPMSClient

# Set credentials via environment variables
# export VOIPMS_USERNAME='your-email@example.com'
# export VOIPMS_API_PASSWORD='your-api-password'


def main():
    # Create client (uses environment variables for credentials)
    with VoIPMSClient() as client:
        try:
            # Get account balance
            print("Getting account balance...")
            balance = client.getBalance()
            print(f"Current balance: ${balance['balance']['current_balance']}")
            print(f"Spent today: ${balance['balance']['spent_today']}")

            # Get registration status
            print("\nGetting registration status...")
            status = client.getRegistrationStatus()
            registered = status.get("registered", [])
            print(f"Registered accounts: {len(registered)}")

            # Get server information
            print("\nGetting server information...")
            servers = client.getServersInfo()
            server_list = servers.get("servers", [])
            print(f"Available servers: {len(server_list)}")
            for server in server_list[:3]:  # Show first 3
                print(f"  - {server['server_name']} ({server['server_hostname']})")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
