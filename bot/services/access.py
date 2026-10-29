"""User access control service."""
import aiosqlite
from ..config import ADMIN_USER_ID, DB_PATH


class AccessService:
    """Manage user access approvals."""

    def __init__(self):
        self.db_path = DB_PATH

    async def init_db(self):
        """Initialize access control tables."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS user_access (
                    user_id INTEGER PRIMARY KEY,
                    chat_id INTEGER,
                    status TEXT NOT NULL DEFAULT 'pending',
                    approved_by INTEGER,
                    approved_at TEXT
                )
            """)
            await db.commit()

    async def request_access(self, user_id, chat_id=None):
        """Create a pending access request."""
        async with aiosqlite.connect(self.db_path) as db:
            # Check if already exists
            cursor = await db.execute(
                "SELECT status FROM user_access WHERE user_id = ?", (user_id,)
            )
            row = await cursor.fetchone()
            if row:
                return row[0]  # Already has a status

            await db.execute(
                "INSERT INTO user_access (user_id, chat_id, status) VALUES (?, ?, 'pending')",
                (user_id, chat_id)
            )
            await db.commit()
            return 'pending'

    async def approve_access(self, user_id, approved_by):
        """Approve user access."""
        from datetime import datetime
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """UPDATE user_access SET status = 'approved', approved_by = ?,
                   approved_at = ? WHERE user_id = ?""",
                (approved_by, datetime.now().isoformat(), user_id)
            )
            await db.commit()

    async def deny_access(self, user_id):
        """Deny user access."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE user_access SET status = 'denied' WHERE user_id = ?", (user_id,)
            )
            await db.commit()

    async def revoke_access(self, user_id):
        """Revoke user access."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE user_access SET status = 'revoked' WHERE user_id = ?", (user_id,)
            )
            await db.commit()

    async def has_access(self, user_id):
        """Check if user has access."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT status FROM user_access WHERE user_id = ?", (user_id,)
            )
            row = await cursor.fetchone()
            if not row:
                return False
            return row[0] in ('approved',)

    async def get_pending_requests(self):
        """Get all pending access requests."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT user_id, chat_id FROM user_access WHERE status = 'pending'"
            )
            return await cursor.fetchall()

    async def get_all_users(self):
        """Get all users."""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT user_id, chat_id, status, approved_by, approved_at FROM user_access"
            )
            return await cursor.fetchall()