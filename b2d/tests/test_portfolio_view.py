import json
from decimal import Decimal

from django.urls import reverse
from .basecase import BaseCase


class PortfolioViewTest(BaseCase):

    def test_portfolio_view_with_investor_user(self):
        """Test the portfolio view which login as investor user is rendered."""
        # login as investor
        login_successful = self.client.login(username=self.investor1.username, password="password123")
        self.assertTrue(login_successful)
        url = reverse('b2d:portfolio')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'b2d/portfolio.html')

    def test_profile_view_without_investor_user(self):
        """Test the portfolio view which not login as investor user is redirect."""
        url = reverse('b2d:portfolio')
        response = self.client.get(url)
        # Not authentication should redirect
        self.assertEqual(response.status_code, 302)
        # Business user should redirect
        login_successful = self.client.login(username=self.business1.username, password="password123")
        self.assertTrue(login_successful)
        self.assertEqual(response.status_code, 302)

    def test_portfolio_view_context(self):
        """Test portfolio view return correct investment information context"""
        self.client.login(username=self.investor1.username, password="password123")
        url = reverse('b2d:portfolio')
        response = self.client.get(url)
        self.assertIn(self.business1.name,
                      [investment['business_name'] for investment in response.context['investments']])
        self.assertIn(self.business2.name,
                      [investment['business_name'] for investment in response.context['investments']])
        self.assertEqual(response.context['total_investment'], Decimal('7500'))
        expected_investment_data = {
            "labels": ["business_tech_1", "business_tech_2"],
            "data": [66.66666666666666, 33.33333333333333]
        }
        self.assertEqual(json.loads(response.context['investment_data']), expected_investment_data)
