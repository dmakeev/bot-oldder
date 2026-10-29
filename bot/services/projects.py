"""Project management service for PROсрочка bot."""
import aiosqlite
from ..config import DB_PATH


class ProjectService:
    """CRUD operations for projects."""

    def __init__(self):
        self.db_path = DB_PATH

    async def init_db(self):
        """Initialize database."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    case_number TEXT NOT NULL,
                    type TEXT NOT NULL,
                    procedures TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    active BOOLEAN DEFAULT TRUE
                )
            """)
            await db.commit()

    async def create_project(self, chat_id, name, case_number, project_type, procedures=None):
        """Create a new project."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """INSERT INTO projects (chat_id, name, case_number, type, procedures)
                   VALUES (?, ?, ?, ?, ?)""",
                (chat_id, name, case_number, project_type, procedures)
            )
            await db.commit()
            return cursor.lastrowid

    async def get_projects_by_chat(self, chat_id):
        """Get all projects for a chat."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """SELECT id, name, case_number, type, created_at
                   FROM projects
                   WHERE chat_id = ? AND active = 1
                   ORDER BY created_at DESC""",
                (chat_id,)
            )
            return await cursor.fetchall()

    async def get_project(self, project_id):
        """Get a single project by ID."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT * FROM projects WHERE id = ? AND active = 1",
                (project_id,)
            )
            return await cursor.fetchone()

    async def delete_project(self, project_id):
        """Delete a project (set active to 0)."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE projects SET active = 0 WHERE id = ?",
                (project_id,)
            )
            await db.commit()
