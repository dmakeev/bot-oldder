"""Additional unit tests for project service."""
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
async def test_get_project_by_id(temp_db):
    """Test getting a single project by ID."""
    from bot.services.projects import ProjectService

    service = ProjectService()
    service.db_path = temp_db
    await service.init_db()

    project_id = await service.create_project(
        chat_id=123,
        name="Тестовое дело",
        case_number="А123-456/2026",
        project_type="bankruptcy"
    )

    project = await service.get_project(project_id)
    assert project is not None
    assert project[1] == 123  # chat_id
    assert project[2] == "Тестовое дело"  # name


@pytest.mark.asyncio
async def test_get_project_not_found(temp_db):
    """Test getting a non-existent project."""
    from bot.services.projects import ProjectService

    service = ProjectService()
    service.db_path = temp_db
    await service.init_db()

    project = await service.get_project(999)
    assert project is None
