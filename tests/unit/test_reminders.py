"""Unit tests for reminder logic."""
import pytest
import os
import tempfile
from datetime import datetime


@pytest.fixture
def temp_db():
    """Create a temporary database file."""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)


@pytest.mark.asyncio
async def test_create_reminder(temp_db):
    """Test creating a reminder."""
    from bot.services.reminders import ReminderService

    service = ReminderService()
    service.db_path = temp_db
    await service.init_db()

    # Create event
    event_id = await service.create_event(
        project_id=1,
        event_type="meeting",
        scheduled_at=datetime(2026, 11, 15)
    )

    # Create reminder
    reminder_id = await service.create_reminder(
        event_id=event_id,
        scheduled_at=datetime(2026, 11, 8)
    )

    assert reminder_id > 0


@pytest.mark.asyncio
async def test_mark_reminder_done(temp_db):
    """Test marking a reminder as done."""
    from bot.services.reminders import ReminderService

    service = ReminderService()
    service.db_path = temp_db
    await service.init_db()

    event_id = await service.create_event(
        project_id=1,
        event_type="meeting",
        scheduled_at=datetime(2026, 11, 15)
    )

    reminder_id = await service.create_reminder(
        event_id=event_id,
        scheduled_at=datetime(2026, 11, 8)
    )

    await service.mark_reminder_done(reminder_id)


@pytest.mark.asyncio
async def test_mark_reminder_cancelled(temp_db):
    """Test marking a reminder as cancelled."""
    from bot.services.reminders import ReminderService

    service = ReminderService()
    service.db_path = temp_db
    await service.init_db()

    event_id = await service.create_event(
        project_id=1,
        event_type="meeting",
        scheduled_at=datetime(2026, 11, 15)
    )

    reminder_id = await service.create_reminder(
        event_id=event_id,
        scheduled_at=datetime(2026, 11, 8)
    )

    await service.mark_reminder_cancelled(reminder_id)
