from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
from unittest.mock import patch

from .basecase import BaseCase
from b2d.models import Investment


class FundRaisingDashboardViewTest(BaseCase):
    def test_dashboard_accessible_for_business_owner(self):
        """Test that the fundraising dashboard is accessible for logged-in business owners."""
        self.client.login(username=self.business1.username, password="#Password1234")
        url = reverse('b2d:fundraising')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'b2d/fundraising_dashboard.html')

    def test_dashboard_restricted_for_non_business_owner(self):
        """Test that the fundraising dashboard is restricted for non-business users."""
        self.client.logout()
        url = reverse('b2d:fundraising')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirected to home

    def test_active_fundraising_displayed(self):
        """Test that the active fundraising campaign is displayed."""
        self.client.login(username=self.business1.username, password="#Password1234")
        url = reverse('b2d:fundraising')
        response = self.client.get(url)
        active_fundraising = response.context['active_fundraising']

        self.assertIsNotNone(active_fundraising)
        self.assertEqual(active_fundraising.business, self.business1)

    def test_finished_fundraising_displayed(self):
        """Test that finished fundraising campaigns are displayed."""
        self.fundraising1.deadline_date = timezone.now() - timezone.timedelta(days=1)
        self.fundraising1.save()

        self.client.login(username=self.business1.username, password="#Password1234")
        url = reverse('b2d:fundraising')
        response = self.client.get(url)
        finished_fundraising = response.context['finished_fundraising']

        self.assertIsNotNone(finished_fundraising)
        self.assertIn(self.fundraising1, finished_fundraising)

    def test_investments_chart_data(self):
        """Test that chart data is correctly generated for active fundraising."""
        self.client.login(username=self.business1.username, password="#Password1234")
        response = self.client.get(reverse('b2d:fundraising'))

        chart_labels = response.context['chart_labels']
        chart_data = response.context['chart_data']

        self.assertTrue(chart_labels)  # Ensure chart labels are populated
        self.assertTrue(chart_data)  # Ensure chart data is populated

        # Verify chart data matches cumulative investments
        approved_investments = Investment.objects.filter(
            fundraise=self.fundraising1, investment_status='approve'
        ).order_by('investment_datetime')

        cumulative_sum = 0
        expected_data = []
        for investment in approved_investments:
            cumulative_sum += float(investment.amount)
            expected_data.append(cumulative_sum)

        self.assertEqual(chart_data, expected_data)

    @patch('django_recaptcha.fields.ReCaptchaField.clean', return_value=True)
    def test_create_new_fundraising_campaign(self, mock_captcha_clean):
        """Test that a new fundraising campaign can be created."""
        self.client.login(username=self.business1.username, password="#Password1234")
        form_data = {
            'goal_amount': Decimal('10000.00'),
            'publish_date': timezone.now().date(),
            'deadline_date': timezone.now().date() + timezone.timedelta(days=30),
            'minimum_shares': 100,
            'share_type': 'common',
            'shares': 1000,
            'captcha': 'PASSED'
        }
        url = reverse('b2d:fundraising')
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 302)  # Redirect on success

    def test_update_investment_status(self):
        """Test that investment status can be updated."""
        self.client.login(username=self.business1.username, password="#Password1234")

        form_data = {
            'investment_id': self.investment1.id,
            'investment_status': 'approve',
        }
        url = reverse('b2d:fundraising')
        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 302)  # Redirect on success
        updated_investment = Investment.objects.get(id=self.investment1.id)
        self.assertEqual(updated_investment.investment_status, 'approve')
