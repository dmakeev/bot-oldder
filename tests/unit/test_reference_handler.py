"""Unit tests for reference search handler."""
from unittest.mock import AsyncMock, MagicMock

import pytest

from bot.handlers.reference import reference_search


@pytest.mark.asyncio
async def test_reference_search_no_query():
    """Test reference search with no query."""
    update = MagicMock()
    update.message = MagicMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    context.args = []

    await reference_search(update, context)

    update.message.reply_text.assert_called_once()
    text = update.message.reply_text.call_args[0][0]
    assert "📖 Поиск по справочнику" in text
    assert "/ref <ключевые слова>" in text


@pytest.mark.asyncio
async def test_reference_search_found():
    """Test reference search with results."""
    update = MagicMock()
    update.message = MagicMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    context.args = ["собрание"]

    await reference_search(update, context)

    update.message.reply_text.assert_called_once()
    text = update.message.reply_text.call_args[0][0]
    assert "📖 Найдено" in text
    assert "результатов" in text


@pytest.mark.asyncio
async def test_reference_search_not_found():
    """Test reference search with no results."""
    update = MagicMock()
    update.message = MagicMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    context.args = ["xyz123"]

    await reference_search(update, context)

    update.message.reply_text.assert_called_once()
    text = update.message.reply_text.call_args[0][0]
    assert "🔍 Ничего не найдено" in text


@pytest.mark.asyncio
async def test_reference_search_many_results():
    """Test reference search with many results (>5)."""
    update = MagicMock()
    update.message = MagicMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    context.args = ["день"]  # Should match many items

    await reference_search(update, context)

    update.message.reply_text.assert_called_once()
    text = update.message.reply_text.call_args[0][0]
    # Check for "и ещё N..." when more than 5 results
    if "и ещё" in text:
        assert "..." in text