"""Simple in-memory rate limiter."""
import time
from collections import defaultdict


class RateLimiter:
    """Rate limiter that tracks request counts per key."""

    def __init__(self, max_requests=10, window_seconds=60):
        """Initialize rate limiter.

        Args:
            max_requests: Maximum number of requests allowed in the window.
            window_seconds: Time window in seconds.
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)

    def is_allowed(self, key):
        """Check if a request is allowed for the given key.

        Args:
            key: Identifier for the client (e.g., user_id or chat_id).

        Returns:
            True if allowed, False if rate limit exceeded.
        """
        now = time.time()
        window_start = now - self.window_seconds

        # Clean up old requests
        self.requests[key] = [t for t in self.requests[key] if t > window_start]

        # Check if limit exceeded
        if len(self.requests[key]) >= self.max_requests:
            return False

        # Record this request
        self.requests[key].append(now)
        return True

    def get_remaining(self, key):
        """Get remaining requests for the given key.

        Args:
            key: Identifier for the client.

        Returns:
            Number of remaining requests in the current window.
        """
        now = time.time()
        window_start = now - self.window_seconds

        # Clean up old requests
        self.requests[key] = [t for t in self.requests[key] if t > window_start]

        return max(0, self.max_requests - len(self.requests[key]))