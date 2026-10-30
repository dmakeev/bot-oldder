"""Reminder service for PROсрочка bot."""
import logging
import uuid

import aiosqlite

from ..config import DB_PATH

logger = logging.getLogger(__name__)


class ReminderService:
    """Create and manage reminders."""

    def __init__(self):
        self.db_path = DB_PATH

    async def init_db(self):
        """Initialize database."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id TEXT PRIMARY KEY,
                    project_id TEXT NOT NULL,
                    type TEXT NOT NULL,
                    scheduled_at TIMESTAMP NOT NULL,
                    status TEXT NOT NULL DEFAULT 'upcoming',
                    data TEXT
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS reminders (
                    id TEXT PRIMARY KEY,
                    event_id TEXT NOT NULL,
                    scheduled_at TIMESTAMP NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending'
                )
            """)
            await db.commit()

    def _generate_id(self):
        """Generate a new UUID."""
        return str(uuid.uuid4())

    async def create_event(self, project_id, event_type, scheduled_at, data=None):
        """Create a new event."""
        event_id = self._generate_id()
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    """INSERT INTO events (id, project_id, type, scheduled_at, data)
                       VALUES (?, ?, ?, ?, ?)""",
                    (event_id, project_id, event_type, scheduled_at, data)
                )
                await db.commit()
                return event_id
        except aiosqlite.Error as e:
            logger.error(f"Failed to create event: {e}")
            raise RuntimeError(f"Database error: {e}") from e

    async def create_reminder(self, event_id, scheduled_at):
        """Create a reminder for an event."""
        reminder_id = self._generate_id()
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    """INSERT INTO reminders (id, event_id, scheduled_at)
                       VALUES (?, ?, ?)""",
                    (reminder_id, event_id, scheduled_at)
                )
                await db.commit()
                return reminder_id
        except aiosqlite.Error as e:
            logger.error(f"Failed to create reminder: {e}")
            raise RuntimeError(f"Database error: {e}") from e

    async def get_today_reminders(self, now):
        """Get all reminders for today."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute(
                    """SELECT r.id, r.event_id, r.scheduled_at, r.status,
                              e.type, e.data
                       FROM reminders r
                       JOIN events e ON r.event_id = e.id
                       WHERE date(r.scheduled_at) = date(?)
                       AND r.status = 'pending'""",
                    (now,)
                )
                return await cursor.fetchall()
        except aiosqlite.Error as e:
            logger.error(f"Failed to get reminders: {e}")
            raise RuntimeError(f"Database error: {e}") from e

    async def mark_reminder_done(self, reminder_id):
        """Mark a reminder as done."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "UPDATE reminders SET status = 'done' WHERE id = ?",
                    (reminder_id,)
                )
                await db.commit()
        except aiosqlite.Error as e:
            logger.error(f"Failed to mark reminder done: {e}")
            raise RuntimeError(f"Database error: {e}") from e

    async def mark_reminder_cancelled(self, reminder_id):
        """Mark a reminder as cancelled."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "UPDATE reminders SET status = 'cancelled' WHERE id = ?",
                    (reminder_id,)
                )
                await db.commit()
        except aiosqlite.Error as e:
            logger.error(f"Failed to mark reminder cancelled: {e}")
            raise RuntimeError(f"Database error: {e}") from e

    async def mark_reminder_muted(self, reminder_id):
        """Mark a reminder as muted (don't remind again)."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "UPDATE reminders SET status = 'muted' WHERE id = ?",
                    (reminder_id,)
                )
                await db.commit()
        except aiosqlite.Error as e:
            logger.error(f"Failed to mark reminder muted: {e}")
            raise RuntimeError(f"Database error: {e}") from e

    async def reminder_belongs_to_chat(self, reminder_id, chat_id):
        """Verify that a reminder belongs to a given chat via project."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute(
                    """SELECT e.project_id FROM reminders r
                       JOIN events e ON r.event_id = e.id
                       WHERE r.id = ?""",
                    (reminder_id,)
                )
                row = await cursor.fetchone()
                if not row:
                    return False

                project_id = row[0]
                cursor = await db.execute(
                    "SELECT chat_id FROM projects WHERE id = ?",
                    (project_id,)
                )
                project = await cursor.fetchone()
                if not project:
                    return False

                return project[0] == chat_id
        except aiosqlite.Error as e:
            logger.error(f"Failed to check reminder ownership: {e}")
            return False
