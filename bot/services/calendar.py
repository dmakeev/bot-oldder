"""Calendar service for PROсрочка bot."""
import json
import os
from datetime import datetime

CALENDAR_FILE = "bot/data/calendar.json"


class CalendarService:
    """Manage production calendar (holidays and transfers)."""

    def __init__(self):
        self.holidays = {}
        self.transfers = {}
        self._load_calendar()

    def _load_calendar(self):
        """Load calendar data from JSON file."""
        if os.path.exists(CALENDAR_FILE):
            with open(CALENDAR_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            for year_str, year_data in data["years"].items():
                year = int(year_str)
                self.holidays[year] = set()
                for h in year_data.get("holidays", []):
                    self.holidays[year].add(h["date"])
                self.transfers[year] = {}
                for t in year_data.get("transfers", []):
                    self.transfers[year][t["from"]] = t["to"]
        else:
            # Default: no holidays, no transfers
            pass

    def is_holiday(self, date):
        """Check if a date is a holiday."""
        year = date.year
        date_str = date.strftime("%Y-%m-%d")
        if year not in self.holidays:
            return False
        return date_str in self.holidays[year]

    def is_transfer_day(self, date):
        """Check if a date is a transfer day (extra holiday due to transfer)."""
        year = date.year
        date_str = date.strftime("%Y-%m-%d")
        if year not in self.transfers:
            return False
        return any(to == date_str for to in self.transfers[year].values())

    def is_workday(self, date):
        """Check if a date is a working day."""
        # Weekend
        if date.weekday() >= 5:
            return False
        # Holiday
        if self.is_holiday(date):
            return False
        # Transfer day
        if self.is_transfer_day(date):
            return False
        return True
