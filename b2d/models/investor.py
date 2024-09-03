from django.contrib.auth.models import User
from django.db import models


class Investor(User):
    """Investor Model represents an investor, containing basic information."""
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    financial_statements = models.FileField(upload_to='investor_docs/financial_statements')

    class Meta:
        verbose_name = "Investor"
        verbose_name_plural = "Investors"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
