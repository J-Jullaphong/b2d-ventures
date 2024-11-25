from django.test import TestCase
from ..models import Category


class CategoryModelTest(TestCase):

    def setUp(self):
        """Set up data for the tests."""
        self.category = Category.objects.create(category_name="Technology")

    def test_category_creation(self):
        """Test that a category can be created successfully."""
        self.assertEqual(self.category.category_name, "Technology")

    def test_get_all_categories(self):
        """Test that the `get_all_category` method returns all categories."""
        self.category2 = Category.objects.create(category_name="Finance")
        self.category3 = Category.objects.create(category_name="Health")
        categories = self.category.get_all_category()
        self.assertEqual(categories.count(), 3)
        self.assertIn(self.category, categories)
        self.assertIn(self.category2, categories)
        self.assertIn(self.category3, categories)

    def test_category_string_representation(self):
        """Test the string representation of the Category model."""
        self.assertEqual(str(self.category), "Technology")
