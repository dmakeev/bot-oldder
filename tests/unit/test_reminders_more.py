"""Additional unit tests for reminder service."""
import os
import tempfile
from datetime import datetime

import pytest


@pytest.fixture
def temp_db():
    """Create a temporary database file."""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)


@pytest.mark.asyncio
async def test_get_today_reminders(temp_db):
    """Test getting today's reminders."""
    from bot.services.reminders import ReminderService

    service = ReminderService()
    service.db_path = temp_db
    await service.init_db()

    # Create event and reminder for today
    today = datetime(2026, 10, 29)
    event_id = await service.create_event(
        project_id=1,
        event_type="hearing",
        scheduled_at=today
    )
    await service.create_reminder(
        event_id=event_id,
        scheduled_at=today
    )

    reminders = await service.get_today_reminders(today)
    assert len(reminders) == 1
    assert reminders[0][4] == "hearing"  # event type


@pytest.mark.asyncio
async def test_get_today_reminders_empty(temp_db):
    """Test getting today's reminders when none exist."""
    from bot.services.reminders import ReminderService

    service = ReminderService()
    service.db_path = temp_db
    await service.init_db()

    reminders = await service.get_today_reminders(datetime(2026, 10, 29))
    assert len(reminders) == 0
