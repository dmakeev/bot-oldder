"""Additional tests for access service."""
import pytest
import tempfile
import os
from bot.services.access import AccessService


def _make_service():
    """Create service with temp db."""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    service = AccessService()
    service.db_path = path
    return service, path


@pytest.mark.asyncio
async def test_revoke_access():
    """Test revoking user access."""
    service, path = _make_service()
    await service.init_db()
    await service.request_access(123, 456)
    await service.approve_access(123, 100)
    
    has_before = await service.has_access(123)
    assert has_before is True
    
    await service.revoke_access(123)
    
    has_after = await service.has_access(123)
    assert has_after is False
    
    if os.path.exists(path):
        os.remove(path)


@pytest.mark.asyncio
async def test_get_all_users():
    """Test getting all users."""
    service, path = _make_service()
    await service.init_db()
    await service.request_access(123, 456)
    await service.request_access(789, 100)
    
    users = await service.get_all_users()
    assert len(users) == 2
    
    if os.path.exists(path):
        os.remove(path)