from django.contrib.auth.models import User
from django.db import models


def investor_document_path(instance, filename):
    """
    Custom path to store investor documents in S3.
    The path will include the investor id and the document type (field name).
    """
    ext = filename.split('.')[-1]
    return f'investor_docs/{instance.id}.{ext}'


class Investor(User):
    """Investor Model represents an investor, containing basic information."""
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    financial_statements = models.FileField(upload_to=investor_document_path)

    class Meta:
        verbose_name = "Investor"
        verbose_name_plural = "Investors"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
