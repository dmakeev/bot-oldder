"""Edge case tests for calendar service."""
import pytest
import os
import tempfile
from datetime import datetime
from bot.services.calendar import CalendarService


def test_calendar_file_not_found():
    """Test calendar service when file doesn't exist."""
    # Create calendar service in temp directory
    class TempCalendar(CalendarService):
        def __init__(self):
            self.holidays = {}
            self.transfers = {}
            # Override CALENDAR_FILE temporarily
            self._original_file = CalendarService.__init__.__globals__['CALENDAR_FILE']
            CalendarService.__init__.__globals__['CALENDAR_FILE'] = "/tmp/nonexistent_calendar.json"
            self._load_calendar()
            CalendarService.__init__.__globals__['CALENDAR_FILE'] = self._original_file

    cal = TempCalendar()
    # Should not crash
    assert cal.holidays == {}
    assert cal.transfers == {}


def test_transfer_day_is_not_workday():
    """Test that transfer day is not a workday."""
    cal = CalendarService()
    # May 9, 2026 is a transfer day (Day of Victory on Saturday)
    # Check that it's not a workday
    result = cal.is_workday(datetime(2026, 5, 9))
    assert result is False
