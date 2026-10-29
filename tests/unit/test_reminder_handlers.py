"""Unit tests for reminder handlers."""
import pytest
import tempfile
import os
from unittest.mock import AsyncMock, MagicMock


@pytest.mark.asyncio
async def test_reminder_done_handler():
    """Test 'Done' button handler."""
    from bot.handlers.reminders import reminder_done_handler, reminder_service

    # Use temp database
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    reminder_service.db_path = path
    await reminder_service.init_db()

    update = MagicMock()
    update.callback_query = MagicMock()
    update.callback_query.data = "done_1"
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

    update = MagicMock()
    update.callback_query = MagicMock()
    update.callback_query.data = "cancel_1"
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

    update = MagicMock()
    update.callback_query = MagicMock()
    update.callback_query.data = "mute_1"
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    context = MagicMock()

    await reminder_mute_handler(update, context)

    update.callback_query.answer.assert_called_once()
    update.callback_query.edit_message_text.assert_called_once_with("🔕 Больше не напоминать")

    # Cleanup
    if os.path.exists(path):
        os.remove(path)