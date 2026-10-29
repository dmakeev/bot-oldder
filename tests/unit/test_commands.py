"""Unit tests for command handlers."""
import pytest
import tempfile
import os
from unittest.mock import MagicMock, AsyncMock, patch
from bot.handlers.commands import (
    start_command,
    projects_command,
    table_command,
)
from bot.services.projects import ProjectService


@pytest.mark.asyncio
async def test_start_command():
    """Test /start command."""
    update = MagicMock()
    update.message = MagicMock()
    update.message.reply_text = AsyncMock()

    context = MagicMock()

    await start_command(update, context)

    update.message.reply_text.assert_called_once()
    text = update.message.reply_text.call_args[0][0]
    assert "Добро пожаловать" in text


@pytest.mark.asyncio
async def test_projects_command_empty():
    """Test /projects command with no projects."""
    update = MagicMock()
    update.message = MagicMock()
    update.message.chat_id = 123
    update.message.reply_text = AsyncMock()

    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    try:
        service = ProjectService()
        service.db_path = db_path
        await service.init_db()

        with patch("bot.handlers.commands.project_service", service):
            await projects_command(update, None)

        update.message.reply_text.assert_called_once()
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


@pytest.mark.asyncio
async def test_table_command_empty():
    """Test /table command with no projects."""
    update = MagicMock()
    update.message = MagicMock()
    update.message.chat_id = 123
    update.message.reply_text = AsyncMock()

    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    try:
        service = ProjectService()
        service.db_path = db_path
        await service.init_db()

        with patch("bot.handlers.commands.project_service", service):
            await table_command(update, None)

        update.message.reply_text.assert_called_once_with("Нет проектов.")
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)