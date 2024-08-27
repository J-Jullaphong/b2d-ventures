from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class Investor(AbstractUser):
    """Investor Model represents an investor, containing basic information."""
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name='investor_groups')
    user_permissions = models.ManyToManyField(Permission,
                                              related_name='investor_user_permissions')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
