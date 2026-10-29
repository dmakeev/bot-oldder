"""Handler setup for PROсрочка bot."""
from .commands import setup_commands
from .projects import setup_project_handlers
from .reminders import setup_reminder_handlers


def setup_handlers(app, date_calc, calendar):
    """Set up all handlers."""
    setup_commands(app)
    setup_project_handlers(app, date_calc, calendar)
    setup_reminder_handlers(app, date_calc, calendar)
