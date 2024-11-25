from django.db import models

from .custom_user import CustomUser


def investor_document_path(instance, filename):
    """
    Custom path to store investor documents in S3.
    The path will include the investor id and the document type (field name).
    """
    ext = filename.split('.')[-1]
    return f'investor_docs/{instance.id}.{ext}'


class Investor(CustomUser):
    """Investor Model represents an investor, containing basic information."""
    financial_statements = models.FileField(upload_to=investor_document_path,
                                            null=True, blank=True)

    class Meta:
        verbose_name = "Investor Registration"
        verbose_name_plural = "Investor Registrations"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
