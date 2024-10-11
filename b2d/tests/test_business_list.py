from django.urls import reverse
from .basecase import BaseCase


class BusinessListViewTest(BaseCase):

    def test_business_list_view(self):
        """Test the business list view and ensure correct content is rendered."""
        url = reverse('b2d:search_page')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'b2d/search_page.html')

    def test_business_list_view_no_filter(self):
        """Test search page without any filters applied."""
        response = self.client.get(reverse('b2d:search_page'))
        # approve and correctly fundraising
        self.assertContains(response, "business_tech_1")
        self.assertContains(response, "business_tech_2")
        # fundraising with incorrect deadline
        self.assertNotContains(response, "business_food_1")
        # fundraising was rejected
        self.assertNotContains(response, "business_food_2")
        # fundraising that wait for approve
        self.assertNotContains(response, "business_retail_1")
        # No fundraising
        self.assertNotContains(response, "business_retail_2")

    def test_business_list_view_filter_by_category(self):
        """Test filtering businesses by category."""
        response = self.client.get(reverse('b2d:search_page'), {'category': self.category_tech.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "business_tech_1")
        self.assertContains(response, "business_tech_2")
        self.assertNotContains(response, "business_food_1")
        self.assertNotContains(response, "business_retail_1")

    def test_business_list_view_sort_by_most_recent(self):
        """Test sorting businesses by most recent."""
        response = self.client.get(reverse('b2d:search_page'), {'sort': 'recent'})
        self.assertEqual(response.status_code, 200)
        businesses = response.context['businesses']
        self.assertEqual(businesses[0].name, "business_tech_2")

    def test_business_list_view_sort_by_most_investors(self):
        """Test sorting businesses by most investors."""
        response = self.client.get(reverse('b2d:search_page'), {'sort': 'investors'})
        self.assertEqual(response.status_code, 200)
        businesses = response.context['businesses']
        self.assertEqual(businesses[0].name, "business_tech_1")

    def test_business_list_view_sort_by_alphabetical(self):
        """Test sorting businesses alphabetically."""
        response = self.client.get(reverse('b2d:search_page'), {'sort': 'alphabetical'})
        self.assertEqual(response.status_code, 200)
        businesses = response.context['businesses']
        self.assertEqual(businesses[0].name, "business_tech_1")

    def test_business_list_view_sort_by_minimum_invest(self):
        """Test sorting businesses by minimum invest."""
        response = self.client.get(reverse('b2d:search_page'), {'sort': 'alphabetical'})
        self.assertEqual(response.status_code, 200)
        businesses = response.context['businesses']
        self.assertEqual(businesses[0].name, "business_tech_1")

    def test_business_list_view_query(self):
        """Test search functionality with query term."""
        response = self.client.get(reverse('b2d:search_page'), {'q': 'Tech'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "business_tech_1")
        self.assertNotContains(response, "business_food_1")
        self.assertNotContains(response, "business_retail_1")
