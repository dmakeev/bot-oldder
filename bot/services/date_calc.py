"""Date calculation service for PROсрочка bot."""
from datetime import datetime, timedelta

import pytz

from .calendar import CalendarService


class DateCalculator:
    """Calculate dates for deadlines and reminders."""

    def __init__(self, calendar: CalendarService = None):
        self.calendar = calendar or CalendarService()
        self.msk = pytz.timezone("Europe/Moscow")

    def add_days(self, date, days, workdays=False):
        """Add calendar or working days to a date."""
        if not workdays:
            return date + timedelta(days=days)

        result = date
        added = 0
        while added < days:
            result += timedelta(days=1)
            if self.calendar.is_workday(result):
                added += 1
        return result

    def is_workday(self, date):
        """Check if a date is a working day."""
        return self.calendar.is_workday(date)

    def get_reminder_dates(self, deadline, days_before):
        """Calculate reminder dates for a deadline."""
        dates = []
        for days in days_before:
            reminder_date = deadline - timedelta(days=days)
            dates.append(reminder_date)
        return sorted(dates)

    def format_deadline(self, deadline, workday_info=None):
        """Format deadline for display."""
        if isinstance(deadline, datetime):
            if deadline.hour != 0 or deadline.minute != 0:
                return deadline.strftime("%d.%m.%Y %H:%M")
            return deadline.strftime("%d.%m.%Y")
        return str(deadline)

    def get_now(self):
        """Get current time in Moscow timezone."""
        return datetime.now(self.msk)
