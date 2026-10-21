from datetime import datetime
from ingabotool import generate_id, slugify, truncate, mask_email

class User:
    """Represents a person joining the project waitlist."""

    def __init__(self, username, email, user_id=None, referral_code=None, referred_by=None, created_at=None):
        self.user_id = user_id or generate_id("usr")
        self.username = slugify(username.strip())
        self.email = email.strip().lower()
        self.referral_code = referral_code or generate_id("ref")
        self.referred_by = referred_by
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def masked_email(self):
        """Returns privacy-safe masked email using ingabotool."""
        return mask_email(self.email)

    def display_name(self, max_length=15):
        """Returns truncated username for clean table formatting using ingabotool."""
        return truncate(self.username, max_length)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "referral_code": self.referral_code,
            "referred_by": self.referred_by,
            "created_at": self.created_at,
        }

    def __repr__(self):
        return f"<User {self.username} ({self.masked_email})>"
