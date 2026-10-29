"""Extended unit tests for date calculation with holidays."""
import pytest
from datetime import datetime, timedelta
from bot.services.date_calc import DateCalculator
from bot.services.calendar import CalendarService


@pytest.fixture
def calculator():
    return DateCalculator()


def test_add_days_crosses_weekend(calculator):
    """Test adding workdays that cross a weekend."""
    # Thursday (29 Oct) + 2 workdays = Monday (2 Nov)
    # 30 Oct (Fri) is workday #1, 2 Nov (Mon) is workday #2
    result = calculator.add_days(datetime(2026, 10, 29), 2, workdays=True)
    assert result.weekday() == 0  # Monday
    assert result.day == 2
    assert result.month == 11


def test_add_days_lands_on_weekend(calculator):
    """Test adding workdays that would land on a weekend."""
    # Wednesday (28 Oct) + 3 workdays = Tuesday (3 Nov)
    # 29 Oct (Thu) is workday #1, 30 Oct (Fri) is workday #2, 2 Nov (Mon) is workday #3
    result = calculator.add_days(datetime(2026, 10, 28), 3, workdays=True)
    assert result.weekday() == 0  # Monday
    assert result.day == 2
    assert result.month == 11


def test_add_days_zero(calculator):
    """Test adding zero days."""
    result = calculator.add_days(datetime(2026, 10, 29), 0)
    assert result.day == 29
    assert result.month == 10
    assert result.year == 2026


def test_get_reminder_dates_same_day(calculator):
    """Test reminder dates when deadline is today."""
    today = datetime(2026, 10, 29)
    dates = calculator.get_reminder_dates(today, [0, 1, 3])
    # Should have today, 1 day before, 3 days before
    assert len(dates) == 3
    # Sorted by date ascending
    assert dates[0].day == 26  # 3 days before
    assert dates[1].day == 28  # 1 day before
    assert dates[2].day == 29  # today


def test_format_deadline_past(calculator):
    """Test formatting past deadline."""
    past = datetime(2026, 10, 15)
    text = calculator.format_deadline(past)
    assert "15.10.2026" in text


def test_format_deadline_today(calculator):
    """Test formatting today's deadline."""
    today = datetime(2026, 10, 29)
    text = calculator.format_deadline(today)
    assert "29.10.2026" in text


def test_format_deadline_tomorrow(calculator):
    """Test formatting tomorrow's deadline."""
    tomorrow = datetime(2026, 10, 30)
    text = calculator.format_deadline(tomorrow)
    assert "30.10.2026" in text


def test_is_workday_holiday(calculator):
    """Test workday check on a holiday."""
    # New Year - holiday
    result = calculator.is_workday(datetime(2026, 1, 1))
    assert result is False


def test_is_workday_weekday(calculator):
    """Test workday check on a regular weekday."""
    # Monday
    result = calculator.is_workday(datetime(2026, 11, 2))
    assert result is True
