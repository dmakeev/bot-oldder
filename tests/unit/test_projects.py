"""Unit tests for project management."""
import pytest
import os
import tempfile
from datetime import datetime


@pytest.fixture
def temp_db():
    """Create a temporary database file."""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)


@pytest.mark.asyncio
async def test_create_project(temp_db):
    """Test creating a project."""
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

    assert project_id > 0


@pytest.mark.asyncio
async def test_get_projects_by_chat(temp_db):
    """Test getting projects for a chat."""
    from bot.services.projects import ProjectService

    service = ProjectService()
    service.db_path = temp_db
    await service.init_db()

    # Create project
    project_id = await service.create_project(
        chat_id=123,
        name="Тестовое дело",
        case_number="А123-456/2026",
        project_type="bankruptcy"
    )

    # Get projects
    projects = await service.get_projects_by_chat(123)
    assert len(projects) == 1
    assert projects[0][1] == "Тестовое дело"


@pytest.mark.asyncio
async def test_delete_project(temp_db):
    """Test deleting a project."""
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

    await service.delete_project(project_id)

    projects = await service.get_projects_by_chat(123)
    assert len(projects) == 0
