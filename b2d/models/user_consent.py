from django.db import models
from django.utils import timezone

from .custom_user import CustomUser


class UserConsent(models.Model):
    """UserConsent Model represents a consent of a user regarding the terms of service and the privacy policy."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    consent = models.BooleanField(default=False)
    consent_date = models.DateTimeField(default=timezone.now,
                                        help_text="Date and time when consent was given")
    last_updated = models.DateTimeField(auto_now=True,
                                        help_text="Date and time when the record was last updated")

    class Meta:
        verbose_name = 'User Consent'
        verbose_name_plural = 'User Consents'

    def __str__(self):
        return f"{self.user.username} - {'Agreed' if self.consent else 'Revoked'}"
