#!/usr/bin/env python3
"""
Example demonstrating improved async client lifecycle management.

This example shows the enhanced error handling, cleanup, and health checking
capabilities of the VoIP.ms async client.
"""

import asyncio
import os

from voipms import VoIPMSAsyncClient

# Set up your credentials (or use environment variables)
os.environ["VOIPMS_USERNAME"] = "your_username@example.com"
os.environ["VOIPMS_API_PASSWORD"] = "your_api_password"


async def basic_usage_example():
    """Basic async client usage with proper lifecycle management"""
    print("🔄 Example 1: Basic Async Usage")

    async with VoIPMSAsyncClient() as client:
        try:
            # Client is automatically initialized and will be cleaned up
            balance = await client.getBalance()
            print(
                f"✅ Account balance: ${balance.get('balance', {}).get('current_balance', 'N/A')}"
            )
        except Exception as e:
            print(f"❌ API call failed: {e}")

    # Client is automatically cleaned up here, even if exceptions occurred
    print("✅ Client properly cleaned up")


async def health_check_example():
    """Example of using the health check functionality"""
    print("\n🏥 Example 2: Health Check")

    async with VoIPMSAsyncClient() as client:
        # Check if client is healthy and can make API calls
        is_healthy = await client.test_connectivity()

        if is_healthy:
            print("✅ Client is healthy - API connectivity confirmed")

            # Make actual API calls
            try:
                _ = await client.getBalance()
                print("✅ Successfully retrieved balance")
            except Exception as e:
                print(f"❌ API call failed despite connectivity test: {e}")
        else:
            print("❌ Client is not healthy - check credentials and connectivity")


async def error_resilience_example():
    """Example showing error resilience and proper cleanup"""
    print("\n🛡️  Example 3: Error Resilience")

    try:
        async with VoIPMSAsyncClient() as client:
            # Even if we have an error in our code, cleanup still happens
            print("✅ Client initialized successfully")

            # Simulate some work that might fail
            await client.getBalance()
            print("✅ API call succeeded")

            # Simulate an error in user code
            if True:  # Change to False to test normal flow
                raise ValueError("Simulated user error")

    except ValueError as e:
        print(f"❌ User error occurred: {e}")
        print("✅ But client was still cleaned up properly!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


async def health_monitoring_example():
    """Example of health monitoring capabilities"""
    print("\n🏥 Example 4: Health Monitoring")

    async with VoIPMSAsyncClient() as client:
        try:
            # Lightweight health check (no API call)
            healthy = client.is_healthy()
            print(f"✅ Lightweight health check: {'Healthy' if healthy else 'Unhealthy'}")

            # Full connectivity test (makes API call)
            if healthy:
                connectivity = await client.test_connectivity()
                print(f"✅ Connectivity test: {'Connected' if connectivity else 'Disconnected'}")

                if connectivity:
                    _ = await client.getBalance()
                    print("✅ API call succeeded")

        except Exception as e:
            print(f"❌ Error during health monitoring: {e}")

    # Automatic cleanup via context manager
    print("✅ Client automatically cleaned up")


async def connection_monitoring_example():
    """Example of monitoring connection health over time"""
    print("\n📊 Example 5: Connection Monitoring")

    async with VoIPMSAsyncClient() as client:
        print("🔍 Starting connection monitoring...")

        # Monitor health over several checks
        for i in range(3):
            healthy = await client.health_check()
            status = "✅ Healthy" if healthy else "❌ Unhealthy"
            print(f"   Check {i+1}: {status}")

            if healthy:
                try:
                    # Make a test call
                    await client.getBalance()
                    print(f"   ✅ API call {i+1} successful")
                except Exception as e:
                    print(f"   ❌ API call {i+1} failed: {e}")

            # Wait a bit between checks (in real usage, this might be longer)
            await asyncio.sleep(0.1)


async def demonstrate_improvements():
    """Show what improvements were made"""
    print("\n💡 Async Client Improvements:")
    print("  ✅ Automatic cleanup on initialization failure")
    print("  ✅ Comprehensive error handling in cleanup process")
    print("  ✅ Health check method for connectivity testing")
    print("  ✅ Proper state management (_initialized flag)")
    print("  ✅ Context manager exception safety")
    print("  ✅ Prevention of double initialization")
    print("  ✅ Resource leak prevention")


async def main():
    print("🚀 VoIP.ms Async Client Lifecycle Examples\n")

    # Note: These examples will only work with valid credentials
    # For demonstration purposes, they'll fail with authentication errors

    await basic_usage_example()
    await health_check_example()
    await error_resilience_example()
    await health_monitoring_example()
    await connection_monitoring_example()
    await demonstrate_improvements()

    print("\n💡 Best Practices:")
    print("  - Always use 'async with' context manager")
    print("  - Use health_check() to verify connectivity")
    print("  - Let automatic cleanup handle resource management")
    print("  - Manual lifecycle management is rarely needed")
    print("  - Health checks use lightweight getBalance() calls")


if __name__ == "__main__":
    asyncio.run(main())
