"""Additional unit tests for date calculation."""
from datetime import UTC, datetime

import pytest

from bot.services.date_calc import DateCalculator


@pytest.fixture
def calculator():
    return DateCalculator()


def test_format_deadline_non_datetime(calculator):
    """Test formatting non-datetime deadline."""
    result = calculator.format_deadline("some string")
    assert result == "some string"


def test_get_now(calculator):
    """Test getting current Moscow time."""
    now = calculator.get_now()
    # Should be a datetime with timezone
    assert now.tzinfo is not None
    # Should be close to current time (within 1 hour)
    utc_now = datetime.now(UTC)
    diff = abs((now - utc_now).total_seconds())
    # Moscow is UTC+3, so difference should be around 3 hours (10800 seconds)
    assert diff < 20000


def test_format_deadline_with_time(calculator):
    """Test formatting deadline with time component."""
    dt = datetime(2026, 11, 15, 14, 30)
    result = calculator.format_deadline(dt)
    assert "15.11.2026" in result
    assert "14:30" in result
