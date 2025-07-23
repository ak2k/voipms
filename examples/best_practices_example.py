#!/usr/bin/env python3
"""
Example demonstrating the refactored async client using Python best practices.

This shows different ways to use the clean async client:
1. Environment variables approach (simplest)
2. API method usage (camelCase naming)
3. Custom configuration approach (most flexible)
4. Testing and health monitoring examples
"""

import asyncio
import os

from voipms import VoIPMSAsyncClient, VoIPMSConfig

# Set up your credentials (or use environment variables)
os.environ["VOIPMS_USERNAME"] = "your_username@example.com"
os.environ["VOIPMS_API_PASSWORD"] = "your_api_password"


async def environment_variables_approach():
    """
    Example 1: Using environment variables (simplest approach)

    The factory function automatically reads credentials from environment variables.
    """
    print("🌍 Example 1: Environment Variables Approach (Simplest)")

    async with VoIPMSAsyncClient() as client:
        try:
            balance = await client.getBalance()
            print(f"✅ Balance: ${balance.get('balance', {}).get('current_balance', 'N/A')}")

            # API methods use camelCase
            print(f"✅ Health check: {client.is_healthy()}")
            print(f"✅ Username from config: {client.config.username}")

        except Exception as e:
            print(f"❌ Error: {e}")


async def api_method_usage():
    """
    Example 2: API method usage

    All API methods use camelCase naming.
    """
    print("\n📋 Example 2: API Method Usage")

    async with VoIPMSAsyncClient() as client:
        try:
            # API methods use camelCase
            balance = await client.getBalance()
            print(f"✅ getBalance(): ${balance.get('balance', {}).get('current_balance', 'N/A')}")

        except Exception as e:
            print(f"❌ Error: {e}")


async def custom_configuration_approach():
    """
    Example 3: Custom configuration approach (most flexible)

    This shows how to use custom configuration with dataclasses.
    """
    print("\n⚙️  Example 3: Custom Configuration Approach")

    # Create custom configuration
    config = VoIPMSConfig(
        username="your_username@example.com",
        password="your_api_password",
        timeout=60.0,  # Longer timeout
        max_retries=5,  # More retries
        debug=True,  # Enable debug logging
        enable_retries=True,
    )

    async with VoIPMSAsyncClient(config) as client:
        try:
            balance = await client.getBalance()
            print(f"✅ Balance: ${balance.get('balance', {}).get('current_balance', 'N/A')}")

        except Exception as e:
            print(f"❌ Error: {e}")


async def testing_approach():
    """
    Example 4: Testing approach using configuration helpers

    This shows how to create test-friendly configurations.
    """
    print("\n🧪 Example 4: Testing Configuration")

    # Use the testing helper
    test_config = VoIPMSConfig.for_testing(username="test_user", password="test_pass")

    print(f"✅ Test config created with retries disabled: {not test_config.enable_retries}")
    print(f"✅ Debug enabled: {test_config.debug}")


async def health_monitoring_example():
    """
    Example 5: Health monitoring with the new client

    Shows the improved health checking capabilities.
    """
    print("\n🏥 Example 5: Health Monitoring")

    async with VoIPMSAsyncClient() as client:
        # Quick health check (no API call)
        health = client.is_healthy()
        print(f"✅ Service health: {'Healthy' if health else 'Unhealthy'}")

        # Full connectivity test (makes API call)
        if health:
            connectivity = await client.test_connectivity()
            print(f"✅ API connectivity: {'Connected' if connectivity else 'Disconnected'}")


async def error_handling_example():
    """
    Example 6: Robust error handling

    Shows how the new client handles various error scenarios.
    """
    print("\n🛡️  Example 6: Error Handling")

    # Test with invalid credentials
    bad_config = VoIPMSConfig(
        username="invalid", password="invalid", enable_retries=False  # Fail fast for this example
    )

    try:
        async with VoIPMSAsyncClient(bad_config) as client:
            await client.getBalance()
    except Exception as e:
        print(f"✅ Error handled gracefully: {type(e).__name__}")


def demonstrate_improvements():
    """Show what improvements were made"""
    print("\n💡 Key Improvements in the Clean Implementation:")
    print("  ✅ Uses @asynccontextmanager for automatic resource management")
    print("  ✅ Uses dataclasses for clean configuration")
    print("  ✅ Factory function pattern for the cleanest API")
    print("  ✅ Separates service logic from lifecycle management")
    print("  ✅ Leverages httpx's built-in connection management")
    print("  ✅ Uses camelCase method naming")
    print("  ✅ Eliminates all custom lifecycle complexity")
    print("  ✅ Uses Python async best practices throughout")


async def main():
    print("🚀 VoIP.ms Async Client - Clean Implementation Examples\n")

    # Note: These examples will only work with valid credentials
    # For demonstration purposes, they'll fail with authentication errors

    await environment_variables_approach()
    await api_method_usage()
    await custom_configuration_approach()
    await testing_approach()
    await health_monitoring_example()
    await error_handling_example()
    demonstrate_improvements()

    print("\n💡 Usage Guide:")
    print("  - Use VoIPMSAsyncClient() for all async code")
    print("  - Set VOIPMS_USERNAME and VOIPMS_API_PASSWORD environment variables")
    print("  - Use VoIPMSConfig for custom configuration")
    print("  - API methods use camelCase naming")
    print("  - Use is_healthy() for quick checks, test_connectivity() for full tests")
    print("  - All resource cleanup is automatic - no manual close() needed")


if __name__ == "__main__":
    asyncio.run(main())
