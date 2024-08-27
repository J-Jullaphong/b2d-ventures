from django.db import models


class Category(models.Model):
    """Category Model represents a category of a business"""
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.category_name)
