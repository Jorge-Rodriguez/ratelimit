"""
Function decorator for rate limiting.

This module provides a function decorator that can be used to wrap a function
such that it will raise an exception if the number of calls to that function
exceeds a maximum within a specified time window.

For examples and full documentation see the README at
https://github.com/tomasbasham/ratelimit
"""
from ratelimit.decorators import (
    RateLimitDecorator,
    SleepAndRetryDecorator,
    sleep_and_retry,
)
from ratelimit.exception import RateLimitException

limits = RateLimitDecorator
rate_limited = RateLimitDecorator  # For backwards compatibility

__all__ = [
    "RateLimitException",
    "limits",
    "rate_limited",
    "sleep_and_retry",
    "SleepAndRetryDecorator",
]

__version__ = "2.2.2"
