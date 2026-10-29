"""Unit tests for calendar service."""
import pytest
from datetime import datetime
from bot.services.calendar import CalendarService


@pytest.fixture
def calendar():
    """Create CalendarService instance."""
    return CalendarService()


def test_is_workday_weekday(calendar):
    """Test workday check for weekday."""
    # Friday
    assert calendar.is_workday(datetime(2026, 10, 30)) is True
    # Monday
    assert calendar.is_workday(datetime(2026, 11, 2)) is True


def test_is_workday_weekend(calendar):
    """Test workday check for weekend."""
    # Saturday
    assert calendar.is_workday(datetime(2026, 10, 31)) is False
    # Sunday
    assert calendar.is_workday(datetime(2026, 11, 1)) is False
