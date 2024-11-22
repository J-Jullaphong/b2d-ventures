from django.urls import reverse


from .basecase import BaseCase
from ..models import TopDeal


class HomeViewTest(BaseCase):
    def test_home_view(self):
        """Test the home view and ensure correct content is rendered."""
        url = reverse('b2d:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'b2d/home.html')

    def test_carousel_businesses(self):
        """
        Test that the HomeView context contains the correct businesses for the carousel.
        Carousel businesses should be the top 3 trending businesses based on recent investments.
        """
        url = reverse('b2d:home')
        response = self.client.get(url)
        carousel_businesses = response.context['carousel_businesses']

        self.assertEqual(len(carousel_businesses), 2)  # Only fundraising1 and fundraising2 are active
        self.assertIn(self.business1, carousel_businesses)  # Has the most investments
        self.assertIn(self.business2, carousel_businesses)

    def test_card_businesses(self):
        """
        Test that the HomeView context contains the correct businesses for the card section.
        Card businesses should be the ones in the TopDeal model.
        """
        # Add a TopDeal for business1 and business2
        TopDeal.objects.create(fundraising=self.fundraising1, display_order=1)
        TopDeal.objects.create(fundraising=self.fundraising2, display_order=2)

        url = reverse('b2d:home')
        response = self.client.get(url)
        card_businesses = response.context['card_businesses']

        self.assertEqual(len(card_businesses), 2)
        self.assertIn(self.business1, card_businesses)
        self.assertIn(self.business2, card_businesses)

    def test_context_settings(self):
        """Test that the settings are included in the context."""
        url = reverse('b2d:home')
        response = self.client.get(url)
        self.assertIn('settings', response.context)
