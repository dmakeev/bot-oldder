"""Unit tests for reminder handlers."""
import os
import tempfile
from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.mark.asyncio
async def test_reminder_done_handler():
    """Test 'Done' button handler."""
    from bot.handlers.reminders import reminder_done_handler, reminder_service

    # Use temp database
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    reminder_service.db_path = path
    await reminder_service.init_db()

    # Create a project and reminder chain for ownership verification
    from bot.services.projects import ProjectService
    project_service = ProjectService()
    project_service.db_path = path
    await project_service.init_db()
    project_id = await project_service.create_project(100, "Test Project")

    event_id = await reminder_service.create_event(project_id, "test", "2026-10-30")
    reminder_id = await reminder_service.create_reminder(event_id, "2026-10-30")

    update = MagicMock()
    update.callback_query = MagicMock()
    update.callback_query.data = f"done_{reminder_id}"
    update.callback_query.message = MagicMock()
    update.callback_query.message.chat_id = 100
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    context = MagicMock()

    await reminder_done_handler(update, context)

    update.callback_query.answer.assert_called_once()
    update.callback_query.edit_message_text.assert_called_once_with("✅ Выполнено")

    # Cleanup
    if os.path.exists(path):
        os.remove(path)


@pytest.mark.asyncio
async def test_reminder_cancel_handler():
    """Test 'Cancel' button handler."""
    from bot.handlers.reminders import reminder_cancel_handler, reminder_service

    # Use temp database
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    reminder_service.db_path = path
    await reminder_service.init_db()

    # Create a project and reminder chain for ownership verification
    from bot.services.projects import ProjectService
    project_service = ProjectService()
    project_service.db_path = path
    await project_service.init_db()
    project_id = await project_service.create_project(100, "Test Project")

    event_id = await reminder_service.create_event(project_id, "test", "2026-10-30")
    reminder_id = await reminder_service.create_reminder(event_id, "2026-10-30")

    update = MagicMock()
    update.callback_query = MagicMock()
    update.callback_query.data = f"cancel_{reminder_id}"
    update.callback_query.message = MagicMock()
    update.callback_query.message.chat_id = 100
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    context = MagicMock()

    await reminder_cancel_handler(update, context)

    update.callback_query.answer.assert_called_once()
    update.callback_query.edit_message_text.assert_called_once_with("❌ Отменено")

    # Cleanup
    if os.path.exists(path):
        os.remove(path)


@pytest.mark.asyncio
async def test_reminder_mute_handler():
    """Test 'Mute' button handler."""
    from bot.handlers.reminders import reminder_mute_handler, reminder_service

    # Use temp database
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    reminder_service.db_path = path
    await reminder_service.init_db()

    # Create a project and reminder chain for ownership verification
    from bot.services.projects import ProjectService
    project_service = ProjectService()
    project_service.db_path = path
    await project_service.init_db()
    project_id = await project_service.create_project(100, "Test Project")

    event_id = await reminder_service.create_event(project_id, "test", "2026-10-30")
    reminder_id = await reminder_service.create_reminder(event_id, "2026-10-30")

    update = MagicMock()
    update.callback_query = MagicMock()
    update.callback_query.data = f"mute_{reminder_id}"
    update.callback_query.message = MagicMock()
    update.callback_query.message.chat_id = 100
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    context = MagicMock()

    await reminder_mute_handler(update, context)

    update.callback_query.answer.assert_called_once()
    update.callback_query.edit_message_text.assert_called_once_with("🔕 Больше не напоминать")

    # Cleanup
    if os.path.exists(path):
        os.remove(path)