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

        # Assert businesses with approved fundraising and valid deadlines are displayed
        self.assertContains(response, self.business1.name)
        self.assertContains(response, self.business2.name)

        # Assert businesses with invalid deadlines are not displayed
        self.assertNotContains(response, self.business3.name)

        # Assert businesses with rejected fundraising are not displayed
        self.assertNotContains(response, self.business4.name)

        # Assert businesses waiting for approval are not displayed
        self.assertNotContains(response, self.business5.name)

        # Assert businesses with no fundraising are not displayed
        self.assertNotContains(response, self.business6.name)

    def test_business_list_view_filter_by_category(self):
        """Test filtering businesses by category."""
        response = self.client.get(reverse('b2d:search_page'), {'category': self.category_tech.id})
        self.assertEqual(response.status_code, 200)

        # Assert businesses in the Tech category are displayed
        self.assertContains(response, self.business1.name)

        # Assert businesses in other categories are not displayed
        self.assertNotContains(response, self.business2.name)

    def test_business_list_view_sort_by_most_recent(self):
        """Test sorting businesses by most recent."""
        response = self.client.get(reverse('b2d:search_page'), {'sort': 'most_recent'})
        self.assertEqual(response.status_code, 200)
        businesses = response.context['businesses']

        # Assert the most recently added business is first
        self.assertEqual(businesses[0].name, self.business2.name)
        self.assertEqual(businesses[1].name, self.business1.name)

    def test_business_list_view_sort_by_most_investors(self):
        """Test sorting businesses by most investors."""
        response = self.client.get(reverse('b2d:search_page'), {'sort': 'most_investors'})
        self.assertEqual(response.status_code, 200)
        businesses = response.context['businesses']

        # Assert the business with the most investors is first
        self.assertEqual(businesses[0].name, self.business1.name)
        self.assertEqual(businesses[1].name, self.business2.name)

    def test_business_list_view_sort_by_minimum_share(self):
        """Test sorting businesses by minimum investment."""
        response = self.client.get(reverse('b2d:search_page'), {'sort': 'min_shares'})
        self.assertEqual(response.status_code, 200)
        businesses = response.context['businesses']

        # Assert the business with the lowest minimum investment is first
        self.assertEqual(businesses[0].name, self.business1.name)
        self.assertEqual(businesses[1].name, self.business2.name)

    def test_business_list_view_full_query(self):
        """Test search functionality with full query term."""
        response = self.client.get(reverse('b2d:search_page'), {'q': 'business1'})
        self.assertEqual(response.status_code, 200)

        # Assert businesses matching the query are displayed
        self.assertContains(response, self.business1.name)

        # Assert businesses not matching the query are not displayed
        self.assertNotContains(response, self.business2.name)

    def test_business_list_view_partial_query(self):
        """Test search functionality with partial query term."""
        response = self.client.get(reverse('b2d:search_page'), {'q': 'business'})
        self.assertEqual(response.status_code, 200)

        # Assert businesses matching the query are displayed
        self.assertContains(response, self.business1.name)
        self.assertContains(response, self.business2.name)
