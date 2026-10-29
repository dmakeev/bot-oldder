"""Unit tests for project handlers."""
import pytest
import tempfile
import os
from unittest.mock import MagicMock, AsyncMock, patch
from datetime import datetime
from bot.handlers.projects import (
    project_type_handler,
    project_name_handler,
    case_number_handler,
    custom_name_handler,
    custom_text_handler,
    custom_date_handler,
)
from bot.services.projects import ProjectService


@pytest.mark.asyncio
async def test_project_type_handler_bankruptcy():
    """Test project type handler for bankruptcy."""
    query = MagicMock()
    query.data = "project_bankruptcy"
    query.answer = AsyncMock()
    query.edit_message_text = AsyncMock()
    update = MagicMock()
    update.callback_query = query

    context = MagicMock()
    context.user_data = {}

    with patch("bot.handlers.projects.project_service"):
        result = await project_type_handler(update, context)

    assert context.user_data['project_type'] == 'bankruptcy'
    query.answer.assert_called_once()
    query.edit_message_text.assert_called_once()


@pytest.mark.asyncio
async def test_project_type_handler_custom():
    """Test project type handler for custom reminder."""
    query = MagicMock()
    query.data = "project_custom"
    query.answer = AsyncMock()
    query.edit_message_text = AsyncMock()
    update = MagicMock()
    update.callback_query = query

    context = MagicMock()
    context.user_data = {}

    with patch("bot.handlers.projects.project_service"):
        result = await project_type_handler(update, context)

    assert context.user_data['project_type'] == 'custom'
    query.edit_message_text.assert_called_once_with("Введите название напоминания:")


@pytest.mark.asyncio
async def test_project_name_handler():
    """Test project name handler."""
    update = MagicMock()
    update.message = MagicMock()
    update.message.text = "Дело Иванов"
    update.message.reply_text = AsyncMock()

    context = MagicMock()
    context.user_data = {}

    with patch("bot.handlers.projects.project_service"):
        result = await project_name_handler(update, context)

    assert context.user_data['project_name'] == "Дело Иванов"
    update.message.reply_text.assert_called_once_with(
        "Введите номер дела (например, А123-456/2026):"
    )


@pytest.mark.asyncio
async def test_case_number_handler():
    """Test case number handler."""
    update = MagicMock()
    update.message = MagicMock()
    update.message.text = "А123-456/2026"
    update.message.chat_id = 123
    update.message.reply_text = AsyncMock()

    context = MagicMock()
    context.user_data = {'project_name': 'Дело Иванов', 'project_type': 'bankruptcy'}

    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    try:
        service = ProjectService()
        service.db_path = db_path
        await service.init_db()

        with patch("bot.handlers.projects.project_service", service):
            result = await case_number_handler(update, context)

        # Check project was created
        projects = await service.get_projects_by_chat(123)
        assert len(projects) == 1
        # Projects are returned as tuples: (id, name, case_number, type, created_at)
        assert projects[0][2] == 'А123-456/2026'
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


@pytest.mark.asyncio
async def test_custom_name_handler():
    """Test custom name handler."""
    update = MagicMock()
    update.message = MagicMock()
    update.message.text = "Мой срок"
    update.message.reply_text = AsyncMock()

    context = MagicMock()
    context.user_data = {}

    with patch("bot.handlers.projects.project_service"):
        result = await custom_name_handler(update, context)

    assert context.user_data['project_name'] == "Мой срок"
    update.message.reply_text.assert_called_once_with("Введите текст напоминания:")


@pytest.mark.asyncio
async def test_custom_text_handler():
    """Test custom text handler."""
    update = MagicMock()
    update.message = MagicMock()
    update.message.text = "Предоставить документы"
    update.message.reply_text = AsyncMock()

    context = MagicMock()
    context.user_data = {}

    with patch("bot.handlers.projects.project_service"):
        result = await custom_text_handler(update, context)

    assert context.user_data['reminder_text'] == "Предоставить документы"
    update.message.reply_text.assert_called_once()


@pytest.mark.asyncio
async def test_custom_date_handler_success():
    """Test custom date handler with valid date."""
    update = MagicMock()
    update.message = MagicMock()
    update.message.text = "15.12.2026"
    update.message.chat_id = 123
    update.message.reply_text = AsyncMock()

    context = MagicMock()
    context.user_data = {
        'project_name': 'Мой срок',
        'reminder_text': 'Предоставить документы'
    }

    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    try:
        service = ProjectService()
        service.db_path = db_path
        await service.init_db()

        with patch("bot.handlers.projects.project_service", service):
            result = await custom_date_handler(update, context)

        projects = await service.get_projects_by_chat(123)
        assert len(projects) == 1
        # Projects are returned as tuples: (id, name, case_number, type, created_at)
        assert projects[0][3] == 'custom'
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


@pytest.mark.asyncio
async def test_custom_date_handler_invalid_date():
    """Test custom date handler with invalid date."""
    update = MagicMock()
    update.message = MagicMock()
    update.message.text = "неверная дата"
    update.message.reply_text = AsyncMock()

    context = MagicMock()
    context.user_data = {
        'project_name': 'Мой срок',
        'reminder_text': 'Предоставить документы'
    }

    with patch("bot.handlers.projects.project_service"):
        result = await custom_date_handler(update, context)

    update.message.reply_text.assert_called_once_with(
        "Неверный формат даты. Используйте ДД.ММ.ГГГГ"
    )