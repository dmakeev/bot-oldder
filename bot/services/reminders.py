"""Reminder service for PROсрочка bot."""
import aiosqlite
from ..config import DB_PATH


class ReminderService:
    """Create and manage reminders."""

    def __init__(self):
        self.db_path = DB_PATH

    async def init_db(self):
        """Initialize database."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER NOT NULL,
                    type TEXT NOT NULL,
                    scheduled_at TIMESTAMP NOT NULL,
                    status TEXT NOT NULL DEFAULT 'upcoming',
                    data TEXT
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id INTEGER NOT NULL,
                    scheduled_at TIMESTAMP NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending'
                )
            """)
            await db.commit()

    async def create_event(self, project_id, event_type, scheduled_at, data=None):
        """Create a new event."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """INSERT INTO events (project_id, type, scheduled_at, data)
                   VALUES (?, ?, ?, ?)""",
                (project_id, event_type, scheduled_at, data)
            )
            await db.commit()
            return cursor.lastrowid

    async def create_reminder(self, event_id, scheduled_at):
        """Create a reminder for an event."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """INSERT INTO reminders (event_id, scheduled_at)
                   VALUES (?, ?)""",
                (event_id, scheduled_at)
            )
            await db.commit()
            return cursor.lastrowid

    async def get_today_reminders(self, now):
        """Get all reminders for today."""
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

    async def mark_reminder_done(self, reminder_id):
        """Mark a reminder as done."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE reminders SET status = 'done' WHERE id = ?",
                (reminder_id,)
            )
            await db.commit()

    async def mark_reminder_cancelled(self, reminder_id):
        """Mark a reminder as cancelled."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE reminders SET status = 'cancelled' WHERE id = ?",
                (reminder_id,)
            )
            await db.commit()
