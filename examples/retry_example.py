#!/usr/bin/env python3
"""
Example demonstrating the Tenacity retry functionality in VoIP.ms client.

This example shows how to configure retry behavior and demonstrates
what happens with different types of errors.
"""

import os

from voipms import VoIPMSClient, VoIPMSConfig

# Set up your credentials (or use environment variables)
os.environ["VOIPMS_USERNAME"] = "your_username@example.com"
os.environ["VOIPMS_API_PASSWORD"] = "your_api_password"


def retry_enabled_example():
    """Example with retries enabled (default behavior)"""
    print("🔄 Example 1: Retries Enabled (Default)")

    # Create config with default retry settings
    config = VoIPMSConfig.from_env(
        enable_retries=True,  # Default: True
        max_retries=3,  # Default: 3
        debug=True,  # To see retry logs
    )

    with VoIPMSClient(config) as client:
        try:
            # This will retry on network errors, 5xx HTTP status codes,
            # and certain VoIP.ms error codes like "rate_limit_exceeded"
            balance = client.getBalance()
            print(f"✅ Success: {balance}")
        except Exception as e:
            print(f"❌ Final failure after retries: {e}")


def retry_disabled_example():
    """Example with retries disabled"""
    print("\n🚫 Example 2: Retries Disabled")

    # Create config with retries disabled
    config = VoIPMSConfig.from_env(enable_retries=False, debug=True)

    with VoIPMSClient(config) as client:
        try:
            # This will fail immediately on any error
            balance = client.getBalance()
            print(f"✅ Success: {balance}")
        except Exception as e:
            print(f"❌ Immediate failure (no retries): {e}")


def custom_retry_example():
    """Example with custom retry configuration"""
    print("\n⚙️  Example 3: Custom Retry Configuration")

    # Create config with custom retry settings
    config = VoIPMSConfig.from_env(enable_retries=True, max_retries=5, debug=True)

    with VoIPMSClient(config) as client:
        try:
            balance = client.getBalance()
            print(f"✅ Success: {balance}")
        except Exception as e:
            print(f"❌ Final failure after 5 retries: {e}")


def demonstrate_retry_behavior():
    """Demonstrate which errors trigger retries and which don't"""
    print("\n📚 Retry Behavior Information:")
    print("  ✅ Retryable errors:")
    print("    - Network errors (connection timeout, DNS failure)")
    print("    - HTTP 429 (Too Many Requests)")
    print("    - HTTP 5xx (Server errors: 500, 502, 503, 504)")
    print("    - VoIP.ms errors: rate_limit_exceeded, server_unavailable, timeout")
    print("  ")
    print("  ❌ Non-retryable errors:")
    print("    - HTTP 4xx (Client errors: 400, 401, 403, 404)")
    print("    - VoIP.ms errors: invalid_credentials, invalid_method, missing_parameter")
    print("  ")
    print("  🔧 Retry Strategy:")
    print("    - Exponential backoff with jitter")
    print("    - Base delay: 1 second")
    print("    - Maximum delay: 60 seconds")
    print("    - Automatic retry on transient failures")


if __name__ == "__main__":
    print("🚀 VoIP.ms Client Retry Examples\n")

    # Note: These examples will only work with valid credentials
    # For demonstration purposes, they'll fail with authentication errors

    retry_enabled_example()
    retry_disabled_example()
    custom_retry_example()
    demonstrate_retry_behavior()

    print("\n💡 Pro Tips:")
    print("  - Enable retries (default) for production use")
    print("  - Disable retries for testing or when you want immediate failures")
    print("  - Use debug=True to see retry attempts in logs")
    print("  - Network errors and server issues are automatically retried")
    print("  - Authentication errors are never retried (fail fast)")
