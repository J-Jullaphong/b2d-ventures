from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class Business(AbstractUser):
    """Business Model represents a business, containing details information."""
    description = models.TextField()
    phone_number = models.CharField(max_length=10)
    chairman = models.CharField(max_length=100)
    founded_year = models.IntegerField()
    valuation = models.DecimalField(max_digits=10, decimal_places=2)
    revenue = models.DecimalField(max_digits=10, decimal_places=2)
    employees_count = models.IntegerField()
    groups = models.ManyToManyField(Group, related_name='business_groups')
    user_permissions = models.ManyToManyField(Permission,
                                              related_name='business_user_permissions')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
