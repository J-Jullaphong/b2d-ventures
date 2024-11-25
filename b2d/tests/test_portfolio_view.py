from django.urls import reverse
from decimal import Decimal

from .basecase import BaseCase


class PortfolioViewTest(BaseCase):
    def test_portfolio_view_accessible_for_investor(self):
        """Test that the portfolio view is accessible for logged-in investors."""
        self.client.login(username=self.investor1.username, password="#Password1234")
        url = reverse('b2d:portfolio')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'b2d/portfolio.html')

    def test_portfolio_view_forbidden_for_non_investor(self):
        """Test that the portfolio view is forbidden for non-investor users."""
        self.client.logout()
        url = reverse('b2d:portfolio')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    def test_portfolio_view_with_investments(self):
        """Test that the portfolio view displays investments for the logged-in investor."""
        self.client.login(username=self.investor1.username, password="#Password1234")
        response = self.client.get(reverse('b2d:portfolio'))
        self.assertEqual(response.status_code, 200)

        self.assertIn('investments', response.context)
        self.assertIn('total_investment', response.context)
        self.assertIn('investment_data', response.context)

        # Assert investments data
        investments = response.context['investments']
        self.assertEqual(len(investments), 2)  # investor1 has 2 investments
