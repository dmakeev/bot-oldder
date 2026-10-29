"""Extended unit tests for calendar service."""
import pytest
from datetime import datetime
from bot.services.calendar import CalendarService


@pytest.fixture
def calendar():
    return CalendarService()


def test_is_holiday_year_not_in_calendar(calendar):
    """Test holiday check for year not in calendar."""
    # Year 2050 is not in our calendar file
    result = calendar.is_holiday(datetime(2050, 1, 1))
    assert result is False


def test_is_transfer_day_year_not_in_calendar(calendar):
    """Test transfer day check for year not in calendar."""
    result = calendar.is_transfer_day(datetime(2050, 1, 1))
    assert result is False


def test_is_transfer_day(calendar):
    """Test transfer day check."""
    # May 9, 2026 is a transfer day (Day of Victory moved to Saturday)
    # Check that it's a holiday
    result = calendar.is_workday(datetime(2026, 5, 9))
    assert result is False  # Holiday


def test_is_workday_regular_day(calendar):
    """Test workday check for a regular working day."""
    # Tuesday, not a holiday
    result = calendar.is_workday(datetime(2026, 10, 20))
    assert result is True
