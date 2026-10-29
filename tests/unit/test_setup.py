"""Unit tests for bot setup."""
import pytest
from unittest.mock import MagicMock
from bot.services.date_calc import DateCalculator
from bot.services.calendar import CalendarService


def test_setup_handlers():
    """Test that all handlers are set up."""
    from bot.handlers import setup_handlers

    app = MagicMock()
    date_calc = DateCalculator()
    calendar = CalendarService()

    setup_handlers(app, date_calc, calendar)

    # Check that add_handler was called multiple times
    assert app.add_handler.call_count > 0


def test_setup_command_handlers():
    """Test command handler setup."""
    from bot.handlers.commands import setup_commands

    app = MagicMock()
    setup_commands(app)

    # Should register start, projects, and table commands
    assert app.add_handler.call_count == 3


def test_setup_project_handlers():
    """Test project handler setup."""
    from bot.handlers.projects import setup_project_handlers

    app = MagicMock()
    date_calc = DateCalculator()
    calendar = CalendarService()
    setup_project_handlers(app, date_calc, calendar)

    assert app.add_handler.call_count == 1


def test_setup_reminder_handlers():
    """Test reminder handler setup."""
    from bot.handlers.reminders import setup_reminder_handlers

    app = MagicMock()
    date_calc = DateCalculator()
    calendar = CalendarService()
    setup_reminder_handlers(app, date_calc, calendar)

    # Should register 3 callback handlers
    assert app.add_handler.call_count == 3
