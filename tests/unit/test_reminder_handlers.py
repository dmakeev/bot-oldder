"""Unit tests for reminder handlers."""
import pytest
from unittest.mock import AsyncMock, MagicMock


@pytest.mark.asyncio
async def test_reminder_done_handler():
    """Test 'Done' button handler."""
    from bot.handlers.reminders import reminder_done_handler

    update = MagicMock()
    update.callback_query = MagicMock()
    update.callback_query.data = "done_42"
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    context = MagicMock()

    await reminder_done_handler(update, context)

    update.callback_query.answer.assert_called_once()
    update.callback_query.edit_message_text.assert_called_once_with("✅ Выполнено")


@pytest.mark.asyncio
async def test_reminder_cancel_handler():
    """Test 'Cancel' button handler."""
    from bot.handlers.reminders import reminder_cancel_handler

    update = MagicMock()
    update.callback_query = MagicMock()
    update.callback_query.data = "cancel_42"
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    context = MagicMock()

    await reminder_cancel_handler(update, context)

    update.callback_query.answer.assert_called_once()
    update.callback_query.edit_message_text.assert_called_once_with("❌ Отменено")


@pytest.mark.asyncio
async def test_reminder_mute_handler():
    """Test 'Mute' button handler."""
    from bot.handlers.reminders import reminder_mute_handler

    update = MagicMock()
    update.callback_query = MagicMock()
    update.callback_query.data = "mute_42"
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    context = MagicMock()

    await reminder_mute_handler(update, context)

    update.callback_query.answer.assert_called_once()
    update.callback_query.edit_message_text.assert_called_once_with("🔕 Больше не напоминать")
