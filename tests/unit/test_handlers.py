"""Unit tests for bot handlers."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.mark.asyncio
async def test_start_command():
    """Test /start command handler."""
    from bot.handlers.commands import start_command

    update = MagicMock()
    update.message = MagicMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()

    await start_command(update, context)

    update.message.reply_text.assert_called_once()
    call_args = update.message.reply_text.call_args
    assert "PROсрочка" in call_args[0][0]


@pytest.mark.asyncio
async def test_projects_command_empty():
    """Test /projects command when no projects."""
    from bot.handlers.commands import projects_command

    update = MagicMock()
    update.message = MagicMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()

    await projects_command(update, context)

    update.message.reply_text.assert_called_once()
    call_args = update.message.reply_text.call_args
    assert "Нет" in call_args[0][0] or "Пока" in call_args[0][0]


@pytest.mark.asyncio
async def test_project_type_handler():
    """Test project type selection handler."""
    from bot.handlers.projects import project_type_handler

    update = MagicMock()
    update.callback_query = MagicMock()
    update.callback_query.data = "project_bankruptcy"
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    context = MagicMock()

    await project_type_handler(update, context)

    update.callback_query.answer.assert_called_once()
    update.callback_query.edit_message_text.assert_called_once()
    call_args = update.callback_query.edit_message_text.call_args
    assert "bankruptcy" in call_args[0][0].lower() or "банкротстве" in call_args[0][0].lower()
