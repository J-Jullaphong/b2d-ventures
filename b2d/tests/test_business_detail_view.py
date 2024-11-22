from django.conf import settings
from django.urls import reverse
from .basecase import BaseCase


class BusinessDetailViewTest(BaseCase):

    def test_business_detail_view(self):
        """Test the business detail view and ensure correct content is rendered."""
        url = reverse('b2d:business_detail', kwargs={'pk': self.business1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'b2d/business_detail.html')

    def test_business_detail_information(self):
        """Test the business detail view show correct information about business."""
        url = reverse('b2d:business_detail', kwargs={'pk': self.business1.id})
        response = self.client.get(url)
        self.assertContains(response, self.business1.name)
        self.assertContains(response, self.business1.description)
        self.assertContains(response, self.fundraising1.goal_amount)
        self.assertContains(response, self.fundraising1.minimum_shares)
        percentage_investment = self.fundraising1.get_percentage_investment()
        self.assertContains(response, f"{percentage_investment}%")
