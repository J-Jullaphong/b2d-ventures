from django.urls import reverse
from .basecase import BaseCase


class FundRaisingDashboardViewTest(BaseCase):

    def test_fundraising_dashboard_view_with_business_user(self):
        """Test the fundraising dashboard view which login as business user is rendered."""
        # login as business 1
        login_successful = self.client.login(username=self.business1.username, password="password123")
        self.assertTrue(login_successful)
        url = reverse('b2d:fundraising')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'b2d/fundraising_dashboard.html')

    def test_fundraising_dashboard_view_without_business_user(self):
        """Test the fundraising dashboard view which not login as business user is redirect."""
        url = reverse('b2d:fundraising')
        response = self.client.get(url)
        # Not authentication should redirect
        self.assertEqual(response.status_code, 302)
        # Investor user should redirect
        login_successful = self.client.login(username=self.investor1.username, password="password123")
        self.assertTrue(login_successful)
        self.assertEqual(response.status_code, 302)

    def test_fundraising_dashboard_view_context_with_active_fundraising(self):
        """Test fundraising dashboard view with active fundraising context."""
        self.client.login(username=self.business1.username, password="password123")
        url = reverse('b2d:fundraising')
        response = self.client.get(url)

        self.assertTrue(response.context['active_fundraising'])
        self.assertFalse(response.context['pending_fundraising'])
        self.assertFalse(response.context['finished_fundraising'])
        self.assertTrue(response.context['show_chart'])
        self.assertIsNotNone(response.context['investments'])
        self.assertIn('chart_labels', response.context)
        expected_dates = [
            self.investment1.investment_datetime.strftime('%Y-%m-%d'),
            self.investment3.investment_datetime.strftime('%Y-%m-%d')
        ]
        self.assertEqual(response.context['chart_labels'], expected_dates)
        self.assertIn('chart_data', response.context)
        expected_amount = [
            float(self.investment1.amount),
            float(self.investment1.amount)+float(self.investment3.amount)
        ]
        self.assertEqual(response.context['chart_data'], expected_amount)
        self.assertIn('form', response.context)

    def test_fundraising_dashboard_view_context_with_pending_fundraising(self):
        """Test fundraising dashboard view with pending fundraising context."""
        self.client.login(username=self.business5.username, password="password123")
        url = reverse('b2d:fundraising')
        response = self.client.get(url)

        self.assertFalse(response.context['active_fundraising'])
        self.assertIsNone(response.context['pending_fundraising'])
        self.assertFalse(response.context['finished_fundraising'])
        self.assertFalse(response.context['show_chart'])
        self.assertIsNone(response.context['investments'])
        self.assertIn('chart_labels', response.context)
        self.assertEqual(response.context['chart_labels'], [])
        self.assertIn('chart_data', response.context)
        self.assertEqual(response.context['chart_data'], [])
        self.assertIn('form', response.context)

    def test_fundraising_dashboard_view_context_with_finished_fundraising(self):
        """Test fundraising dashboard view with finished fundraising context."""
        self.client.login(username=self.business3.username, password="password123")
        url = reverse('b2d:fundraising')
        response = self.client.get(url)

        self.assertFalse(response.context['active_fundraising'])
        self.assertFalse(response.context['pending_fundraising'])
        self.assertTrue(response.context['finished_fundraising'])
        self.assertTrue(response.context['show_chart'])
        self.assertIsNotNone(response.context['investments'])
        self.assertIn('chart_labels', response.context)
        self.assertEqual(response.context['chart_labels'], [])
        self.assertIn('chart_data', response.context)
        self.assertEqual(response.context['chart_data'], [])
        self.assertIn('form', response.context)
