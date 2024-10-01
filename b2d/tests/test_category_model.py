from django.test import TestCase
from ..models import Category


class CategoryModelTest(TestCase):

    def setUp(self):
        """
        Set up data for the tests.
        """
        self.category1 = Category.objects.create(category_name='Technology')
        self.category2 = Category.objects.create(category_name='Healthcare')
        self.category3 = Category.objects.create(category_name='Finance')

    def test_category_creation(self):
        """
        Test that a category can be created successfully.
        """
        category = Category.objects.create(category_name='Retail')
        self.assertEqual(Category.objects.count(), 4)
        self.assertEqual(category.category_name, 'Retail')

    def test_get_all_category(self):
        """
        Test the get_all_category method returns all categories.
        """
        categories = self.category1.get_all_category()
        self.assertEqual(categories.count(), 3)
        self.assertIn(self.category1, categories)
        self.assertIn(self.category2, categories)
        self.assertIn(self.category3, categories)

    def test_category_string_representation(self):
        """
        Test the string representation of the Category model.
        """
        self.assertEqual(str(self.category1), 'Technology')
        self.assertEqual(str(self.category2), 'Healthcare')
        self.assertEqual(str(self.category3), 'Finance')
