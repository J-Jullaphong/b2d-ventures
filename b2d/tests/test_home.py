from django.urls import reverse
from .basecase import BaseCase


class HomePageTest(BaseCase):
    def test_home_view(self):
        """Test the home view and ensure correct content is rendered."""
        url = reverse('b2d:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('b2d:home'))
        self.assertTemplateUsed(response, 'b2d/home.html')

    def test_home_view_carousel_businesses_count(self):
        """Test if the correct businesses appear in the carousel (based on publish date and approval)."""
        response = self.client.get(reverse('b2d:home'))
        carousel_businesses = response.context['carousel_businesses']
        self.assertEqual(len(carousel_businesses),2)

    def test_home_view_card_businesses_count(self):
        """Test if the correct businesses appear in the top deals section."""
        response = self.client.get(reverse('b2d:home'))
        card_businesses = response.context['card_businesses']
        self.assertEqual(len(card_businesses), 2)

    def test_home_view_carousel_business_data(self):
        """Test if carousel businesses data is correct and in the right order."""
        response = self.client.get(reverse('b2d:home'))
        carousel_businesses = response.context['carousel_businesses']

        # Ensure businesses appear in the correct order by publish_date
        self.assertEqual(carousel_businesses[0].name, self.business1.name)
        self.assertEqual(carousel_businesses[1].name, self.business2.name)

    def test_home_view_card_business_data(self):
        """Test if the card businesses data is correct and ordered by investors."""
        response = self.client.get(reverse('b2d:home'))
        card_businesses = response.context['card_businesses']

        # Ensure businesses appear in the correct oder by most investors
        self.assertEqual(card_businesses[0].name, self.business1.name)
        self.assertEqual(card_businesses[1].name, self.business2.name)
