from django.db import models
from ingabotool import slugify, generate_id, mask_email

class WaitlistEntry(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    referral_code = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'waitlist_entries'
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        if self.username:
            self.username = slugify(self.username)
        if not self.referral_code:
            self.referral_code = generate_id("ref")
        super().save(*args, **kwargs)

    @property
    def masked_email(self):
        return mask_email(self.email)

    def __str__(self):
        return f"{self.username} ({self.email})"
