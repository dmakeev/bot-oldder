"""Unit tests for access control handlers."""
import os
import tempfile
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from bot.handlers.access import (
    approve_user_handler,
    deny_user_handler,
    handle_start_with_access,
    list_users_handler,
)
from bot.services.access import AccessService


@pytest.mark.asyncio
async def test_approve_user_handler():
    """Test approve user callback handler."""
    query = MagicMock()
    query.data = "approve_123"
    query.from_user = MagicMock()
    query.from_user.id = 123456  # Admin user ID from conftest
    query.answer = AsyncMock()
    query.edit_message_text = AsyncMock()
    update = MagicMock()
    update.callback_query = query

    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    try:
        service = AccessService()
        service.db_path = db_path
        await service.init_db()
        await service.request_access(123, 456)

        with patch("bot.handlers.access.access_service", service):
            await approve_user_handler(update, None)

        has = await service.has_access(123)
        assert has is True
        query.answer.assert_called_once()
        query.edit_message_text.assert_called_once()
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


@pytest.mark.asyncio
async def test_deny_user_handler():
    """Test deny user callback handler."""
    query = MagicMock()
    query.data = "deny_123"
    query.from_user = MagicMock()
    query.from_user.id = 123456  # Admin user ID from conftest
    query.answer = AsyncMock()
    query.edit_message_text = AsyncMock()
    update = MagicMock()
    update.callback_query = query

    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    try:
        service = AccessService()
        service.db_path = db_path
        await service.init_db()
        await service.request_access(123, 456)

        with patch("bot.handlers.access.access_service", service):
            await deny_user_handler(update, None)

        has = await service.has_access(123)
        assert has is False
        query.answer.assert_called_once()
        query.edit_message_text.assert_called_once()
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


@pytest.mark.asyncio
async def test_list_users_handler_empty():
    """Test listing users when no users exist."""
    update = MagicMock()
    update.message = MagicMock()
    update.message.from_user = MagicMock()
    update.message.from_user.id = 123456  # Admin user ID from conftest
    update.message.reply_text = AsyncMock()

    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    try:
        service = AccessService()
        service.db_path = db_path
        await service.init_db()

        with patch("bot.handlers.access.access_service", service):
            await list_users_handler(update, None)

        update.message.reply_text.assert_called_once_with("Нет пользователей.")
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


@pytest.mark.asyncio
async def test_list_users_handler_with_users():
    """Test listing users with existing users."""
    update = MagicMock()
    update.message = MagicMock()
    update.message.from_user = MagicMock()
    update.message.from_user.id = 123456  # Admin user ID from conftest
    update.message.reply_text = AsyncMock()

    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    try:
        service = AccessService()
        service.db_path = db_path
        await service.init_db()
        await service.request_access(123, 456)
        await service.request_access(789, 100)
        await service.approve_access(789, 100)

        with patch("bot.handlers.access.access_service", service):
            await list_users_handler(update, None)

        call_args = update.message.reply_text.call_args[0][0]
        assert "123" in call_args
        assert "789" in call_args
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


@pytest.mark.asyncio
async def test_start_with_access_approved():
    """Test /start when user has access."""
    update = MagicMock()
    update.message = MagicMock()
    update.message.from_user = MagicMock()
    update.message.from_user.id = 123
    update.message.chat_id = 456
    update.message.reply_text = AsyncMock()

    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    try:
        service = AccessService()
        service.db_path = db_path
        await service.init_db()
        await service.approve_access(123, 100)

        with patch("bot.handlers.access.access_service", service):
            await handle_start_with_access(update, None)
            update.message.reply_text.assert_called_once()
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


@pytest.mark.asyncio
async def test_start_with_access_denied():
    """Test /start when user access is denied."""
    update = MagicMock()
    update.message = MagicMock()
    update.message.from_user = MagicMock()
    update.message.from_user.id = 123
    update.message.chat_id = 456
    update.message.reply_text = AsyncMock()

    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    try:
        service = AccessService()
        service.db_path = db_path
        await service.init_db()
        await service.request_access(123, 456)
        await service.deny_access(123)

        with patch("bot.handlers.access.access_service", service):
            await handle_start_with_access(update, None)

        update.message.reply_text.assert_called_once_with("❌ Нет доступа к боту.")
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


@pytest.mark.asyncio
async def test_start_with_access_pending():
    """Test /start when user access is pending."""
    update = MagicMock()
    update.message = MagicMock()
    update.message.from_user = MagicMock()
    update.message.from_user.id = 123
    update.message.from_user.first_name = "TestUser"
    update.message.chat_id = 456
    update.message.reply_text = AsyncMock()

    context = MagicMock()
    context.bot = MagicMock()

    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    try:
        service = AccessService()
        service.db_path = db_path
        await service.init_db()

        with patch("bot.handlers.access.access_service", service):
            await handle_start_with_access(update, context)

        update.message.reply_text.assert_called_once_with(
            "⏳ Запрос на доступ отправлен администратору."
        )
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)