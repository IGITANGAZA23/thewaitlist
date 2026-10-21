from ingabotool import is_valid_email, mask_email, truncate, slugify
from storage import StorageManager
from user import User

class Waitlist:
    """Core business logic for waitlist registrations, validations, and administrative actions."""

    def __init__(self, storage: StorageManager = None):
        self.storage = storage or StorageManager()

    def join(self, username: str, email: str, referred_by: str = None) -> dict:
        """
        Registers a new user to the waitlist after validations.
        Uses ingabotool for validation and formatting.
        """
        # 1. Basic empty validation
        if not username or not username.strip():
            return {"success": False, "message": "Username cannot be empty."}

        if not email or not email.strip():
            return {"success": False, "message": "Email address cannot be empty."}

        clean_email = email.strip().lower()
        clean_username = slugify(username.strip())

        # 2. Email format validation using ingabotool
        if not is_valid_email(clean_email):
            return {"success": False, "message": f"'{email}' is not a valid email address."}

        # 3. Duplicate checks
        if self.storage.get_user_by_email(clean_email):
            existing_pos = self.storage.get_position(clean_email)
            return {
                "success": False,
                "already_registered": True,
                "message": f"Email {mask_email(clean_email)} is already on the waitlist at position #{existing_pos}!",
                "position": existing_pos
            }

        if self.storage.get_user_by_username(clean_username):
            return {
                "success": False,
                "message": f"Username '{clean_username}' is already taken. Please choose another."
            }

        # 4. Create and persist user
        new_user = User(username=clean_username, email=clean_email, referred_by=referred_by)
        try:
            self.storage.save_user(new_user)
        except Exception as e:
            return {"success": False, "message": f"Error registering user: {e}"}

        position = self.storage.get_position(clean_email)

        return {
            "success": True,
            "message": f"Welcome aboard, @{new_user.username}! You are #{position} in line.",
            "user_id": new_user.user_id,
            "username": new_user.username,
            "masked_email": new_user.masked_email,
            "position": position,
            "referral_code": new_user.referral_code
        }

    def get_position(self, email: str) -> int:
        return self.storage.get_position(email)

    def get_user(self, email: str):
        return self.storage.get_user_by_email(email)

    def remove_entry(self, email: str) -> bool:
        """Admin functionality to remove a registration."""
        return self.storage.delete_user(email)

    def get_statistics(self) -> dict:
        """Calculates total users and overview stats."""
        total = self.storage.get_total_count()
        return {
            "total_users": total,
            "status": "Registration Open"
        }

    def display_waitlist(self, as_admin: bool = False):
        """Displays formatted waitlist entries."""
        users = self.storage.get_all_users()
        if not users:
            print("The waitlist is currently empty.")
            return

        print("\n" + "=" * 65)
        title = "ADMIN WAITLIST VIEW (CONFIDENTIAL)" if as_admin else "PUBLIC WAITLIST QUEUE"
        print(f"{title:^65}")
        print("=" * 65)
        print(f"{'Pos':<5} {'Username':<18} {'Email':<25} {'Joined At':<16}")
        print("-" * 65)

        for idx, u in enumerate(users, start=1):
            email_display = u.email if as_admin else u.masked_email
            username_display = u.display_name(16)
            print(f"#{idx:<4} {username_display:<18} {email_display:<25} {u.created_at[:16]}")
        print("=" * 65 + "\n")
