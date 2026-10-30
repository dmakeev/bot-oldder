"""Project management service for PROсрочка bot."""
import logging
import uuid

import aiosqlite

from ..config import DB_PATH

logger = logging.getLogger(__name__)


class ProjectService:
    """CRUD operations for projects."""

    def __init__(self):
        self.db_path = DB_PATH

    async def init_db(self):
        """Initialize database."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id TEXT PRIMARY KEY,
                    chat_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    case_number TEXT,
                    type TEXT NOT NULL,
                    procedures TEXT,
                    reminder_text TEXT,
                    reminder_date TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    active BOOLEAN DEFAULT TRUE
                )
            """)
            await db.commit()

    def _generate_id(self):
        """Generate a new UUID."""
        return str(uuid.uuid4())

    async def create_project(self, chat_id, name, case_number=None, project_type="bankruptcy", procedures=None, reminder_text=None, reminder_date=None):
        """Create a new project."""
        project_id = self._generate_id()
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    """INSERT INTO projects (id, chat_id, name, case_number, type, procedures, reminder_text, reminder_date)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (project_id, chat_id, name, case_number, project_type, procedures, reminder_text, reminder_date)
                )
                await db.commit()
                return project_id
        except aiosqlite.Error as e:
            logger.error(f"Failed to create project: {e}")
            raise RuntimeError(f"Database error: {e}") from e

    async def get_projects_by_chat(self, chat_id):
        """Get all projects for a chat."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute(
                    """SELECT id, name, case_number, type, created_at
                       FROM projects
                       WHERE chat_id = ? AND active = 1
                       ORDER BY created_at DESC""",
                    (chat_id,)
                )
                return await cursor.fetchall()
        except aiosqlite.Error as e:
            logger.error(f"Failed to get projects: {e}")
            raise RuntimeError(f"Database error: {e}") from e

    async def get_project(self, project_id):
        """Get a single project by ID."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute(
                    "SELECT * FROM projects WHERE id = ? AND active = 1",
                    (project_id,)
                )
                return await cursor.fetchone()
        except aiosqlite.Error as e:
            logger.error(f"Failed to get project: {e}")
            raise RuntimeError(f"Database error: {e}") from e

    async def delete_project(self, project_id):
        """Delete a project (set active to 0)."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "UPDATE projects SET active = 0 WHERE id = ?",
                    (project_id,)
                )
                await db.commit()
        except aiosqlite.Error as e:
            logger.error(f"Failed to delete project: {e}")
            raise RuntimeError(f"Database error: {e}") from e
