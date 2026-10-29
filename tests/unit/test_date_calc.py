"""Unit tests for date calculation service."""
import pytest
from datetime import datetime
from bot.services.date_calc import DateCalculator
from bot.services.calendar import CalendarService


@pytest.fixture
def date_calc():
    """Create DateCalculator instance."""
    return DateCalculator()


def test_add_calendar_days(date_calc):
    """Test adding calendar days."""
    start = datetime(2026, 10, 30)
    result = date_calc.add_days(start, 10)
    assert result.day == 9
    assert result.month == 11


def test_is_workday_weekday(date_calc):
    """Test workday check for weekday."""
    # Friday
    assert date_calc.is_workday(datetime(2026, 10, 30)) is True
    # Monday
    assert date_calc.is_workday(datetime(2026, 11, 2)) is True


def test_is_workday_weekend(date_calc):
    """Test workday check for weekend."""
    # Saturday
    assert date_calc.is_workday(datetime(2026, 10, 31)) is False
    # Sunday
    assert date_calc.is_workday(datetime(2026, 11, 1)) is False


def test_get_reminder_dates(date_calc):
    """Test reminder date calculation."""
    deadline = datetime(2026, 11, 15)
    dates = date_calc.get_reminder_dates(deadline, [7, 3, 1])
    assert len(dates) == 3
    assert dates[0].day == 8
    assert dates[1].day == 12
    assert dates[2].day == 14


def test_format_deadline_date(date_calc):
    """Test deadline formatting for date only."""
    deadline = datetime(2026, 11, 15)
    assert date_calc.format_deadline(deadline) == "15.11.2026"


def test_format_deadline_datetime(date_calc):
    """Test deadline formatting for date and time."""
    deadline = datetime(2026, 11, 15, 14, 30)
    assert date_calc.format_deadline(deadline) == "15.11.2026 14:30"
