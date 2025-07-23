"""
Simple retry configuration using Tenacity for VoIP.ms API client.
"""

import logging

import httpx
from tenacity import (
    before_sleep_log,
    retry,
    stop_after_attempt,
    wait_random_exponential,
)

from .exceptions import VoIPMSError

logger = logging.getLogger(__name__)


# VoIP.ms error codes that should trigger retries
RETRYABLE_ERROR_CODES = {
    "server_unavailable",
    "timeout",
    "rate_limit_exceeded",
    "server_error",
    "temporary_unavailable",
    "service_unavailable",
}

# HTTP status codes that should trigger retries
RETRYABLE_HTTP_STATUS = {429, 500, 502, 503, 504}


def should_retry_error(exception: Exception) -> bool:
    """Determine if an error should be retried"""

    # HTTP errors
    if isinstance(exception, httpx.HTTPStatusError):
        return exception.response.status_code in RETRYABLE_HTTP_STATUS

    # Network errors - generally retryable
    if isinstance(exception, (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError)):
        return True

    # VoIP.ms API errors
    if isinstance(exception, VoIPMSError):
        return exception.code in RETRYABLE_ERROR_CODES

    # Other exceptions - don't retry
    return False


def create_api_retry_decorator(
    max_attempts: int = 3, base_delay: float = 1.0, max_delay: float = 60.0
):
    """Create a simple retry decorator for API calls"""

    def retry_condition(retry_state):
        exception = retry_state.outcome.exception()
        should_retry = should_retry_error(exception)
        if should_retry:
            logger.warning(f"Retrying after error: {exception}")
        return should_retry

    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_random_exponential(multiplier=base_delay, max=max_delay),
        retry=retry_condition,
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )


# Default retry decorator
api_retry = create_api_retry_decorator()
