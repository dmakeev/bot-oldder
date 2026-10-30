"""Unit tests for access control service."""
import os
import tempfile

import pytest

from bot.services.access import AccessService


def _make_service():
    """Create service with temp db."""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    service = AccessService()
    service.db_path = path
    return service, path


@pytest.mark.asyncio
async def test_request_access():
    """Test requesting access."""
    service, path = _make_service()
    await service.init_db()
    status = await service.request_access(123, 456)
    assert status == 'pending'
    if os.path.exists(path):
        os.remove(path)


@pytest.mark.asyncio
async def test_approve_access():
    """Test approving access."""
    service, path = _make_service()
    await service.init_db()
    await service.request_access(123, 456)
    await service.approve_access(123, 789)
    has = await service.has_access(123)
    assert has is True
    if os.path.exists(path):
        os.remove(path)


@pytest.mark.asyncio
async def test_deny_access():
    """Test denying access."""
    service, path = _make_service()
    await service.init_db()
    await service.request_access(123, 456)
    await service.deny_access(123)
    has = await service.has_access(123)
    assert has is False
    if os.path.exists(path):
        os.remove(path)


@pytest.mark.asyncio
async def test_get_pending_requests():
    """Test getting pending requests."""
    service, path = _make_service()
    await service.init_db()
    await service.request_access(123, 456)
    await service.request_access(789, 101)
    requests = await service.get_pending_requests()
    assert len(requests) == 2
    if os.path.exists(path):
        os.remove(path)