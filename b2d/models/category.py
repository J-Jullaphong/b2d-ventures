from django.db import models


class Category(models.Model):
    """Category Model represents a category of a business"""
    category_name = models.CharField(max_length=50)

    def get_all_category(self):
        return Category.objects.all()

    def __str__(self):
        return str(self.category_name)
