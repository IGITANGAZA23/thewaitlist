import os
import sqlite3
from user import User

class StorageManager:
    """Handles permanent SQLite data storage for waitlist registrations."""

    def __init__(self, db_path="data/waitlist.db"):
        self.db_path = db_path
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS waitlist_users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT UNIQUE NOT NULL,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        referral_code TEXT UNIQUE NOT NULL,
                        referred_by TEXT,
                        created_at TEXT NOT NULL
                    )
                """)
                conn.commit()
        except sqlite3.Error as e:
            raise RuntimeError(f"Database initialization failed: {e}")

    def save_user(self, user: User) -> bool:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO waitlist_users (user_id, username, email, referral_code, referred_by, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (user.user_id, user.username, user.email, user.referral_code, user.referred_by, user.created_at))
                conn.commit()
                return True
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Registration conflict: {e}")
        except sqlite3.Error as e:
            raise RuntimeError(f"Database error while saving user: {e}")

    def get_user_by_email(self, email: str):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT user_id, username, email, referral_code, referred_by, created_at FROM waitlist_users WHERE email = ?", (email.strip().lower(),))
                row = cursor.fetchone()
                if row:
                    return User(username=row[1], email=row[2], user_id=row[0], referral_code=row[3], referred_by=row[4], created_at=row[5])
                return None
        except sqlite3.Error as e:
            raise RuntimeError(f"Database query error: {e}")

    def get_user_by_username(self, username: str):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT user_id, username, email, referral_code, referred_by, created_at FROM waitlist_users WHERE username = ?", (username.strip().lower(),))
                row = cursor.fetchone()
                if row:
                    return User(username=row[1], email=row[2], user_id=row[0], referral_code=row[3], referred_by=row[4], created_at=row[5])
                return None
        except sqlite3.Error as e:
            raise RuntimeError(f"Database query error: {e}")

    def get_position(self, email: str) -> int:
        """Calculates queue position based on registration sequence."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT COUNT(*) FROM waitlist_users 
                    WHERE id <= (SELECT id FROM waitlist_users WHERE email = ?)
                """, (email.strip().lower(),))
                result = cursor.fetchone()
                if result and result[0] > 0:
                    return result[0]
                return -1
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to fetch position: {e}")

    def get_all_users(self):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT user_id, username, email, referral_code, referred_by, created_at FROM waitlist_users ORDER BY id ASC")
                rows = cursor.fetchall()
                return [User(username=r[1], email=r[2], user_id=r[0], referral_code=r[3], referred_by=r[4], created_at=r[5]) for r in rows]
        except sqlite3.Error as e:
            raise RuntimeError(f"Database error while listing users: {e}")

    def delete_user(self, email: str) -> bool:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM waitlist_users WHERE email = ?", (email.strip().lower(),))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            raise RuntimeError(f"Database deletion error: {e}")

    def get_total_count(self) -> int:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM waitlist_users")
                return cursor.fetchone()[0]
        except sqlite3.Error as e:
            raise RuntimeError(f"Count query failed: {e}")
