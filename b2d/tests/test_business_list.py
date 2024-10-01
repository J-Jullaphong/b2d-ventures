from django.urls import reverse
from .basecase import BaseCase


class BusinessListViewTest(BaseCase):

    def test_business_list_view(self):
        """Test the business list view and ensure correct content is rendered."""
        response = self.client.get(reverse('b2d:search_page'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('b2d:search_page'))
        self.assertTemplateUsed(response, 'b2d/search_page.html')

    def test_business_list_view_no_filter(self):
        """Test search page without any filters applied."""
        response = self.client.get(reverse('b2d:search_page'))
        self.assertContains(response, "Tech Innovate")
        self.assertContains(response, "Foodies Unite")

    def test_business_list_view_filter_by_category(self):
        """Test filtering businesses by category."""
        response = self.client.get(reverse('b2d:search_page'), {'category': self.category_tech.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tech Innovate")
        self.assertNotContains(response, "Foodies Unite")

    def test_business_list_view_sort_by_recent(self):
        """Test sorting businesses by most recent."""
        response = self.client.get(reverse('b2d:search_page'), {'sort': 'recent'})
        self.assertEqual(response.status_code, 200)
        businesses = response.context['businesses']
        self.assertEqual(businesses[0].name, "Foodies Unite")

    def test_business_list_view_sort_by_investors(self):
        """Test sorting businesses by most investors."""
        response = self.client.get(reverse('b2d:search_page'), {'sort': 'investors'})
        self.assertEqual(response.status_code, 200)
        businesses = response.context['businesses']
        self.assertEqual(businesses[0].name, "Tech Innovate")

    def test_business_list_view_sort_by_alphabetical(self):
        """Test sorting businesses alphabetically."""
        response = self.client.get(reverse('b2d:search_page'), {'sort': 'alphabetical'})
        self.assertEqual(response.status_code, 200)
        businesses = response.context['businesses']
        self.assertEqual(businesses[0].name, "Foodies Unite")

    def test_business_list_view_query(self):
        """Test search functionality with query term."""
        response = self.client.get(reverse('b2d:search_page'), {'q': 'Tech'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tech Innovate")
        self.assertNotContains(response, "Foodies Unite")
