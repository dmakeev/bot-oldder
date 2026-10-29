"""Integration tests for bot startup."""
import pytest
import os
import tempfile


@pytest.fixture
def temp_db():
    """Create a temporary database file."""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)


@pytest.mark.asyncio
async def test_bot_application_created(temp_db, monkeypatch):
    """Test that bot application is created successfully."""
    # Set up environment
    monkeypatch.setenv("BOT_TOKEN", "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
    monkeypatch.setenv("ADMIN_USER_ID", "12345")
    monkeypatch.setenv("DB_PATH", temp_db)
    monkeypatch.setenv("TZ", "Europe/Moscow")

    # Import and create application
    from bot.main import create_application

    app = await create_application()
    assert app is not None
    assert app.bot is not None
    assert app.job_queue is not None


@pytest.mark.asyncio
async def test_bot_handlers_registered(temp_db, monkeypatch):
    """Test that handlers are registered on the application."""
    monkeypatch.setenv("BOT_TOKEN", "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
    monkeypatch.setenv("ADMIN_USER_ID", "12345")
    monkeypatch.setenv("DB_PATH", temp_db)
    monkeypatch.setenv("TZ", "Europe/Moscow")

    from bot.main import create_application

    app = await create_application()
    assert len(app.handlers) > 0