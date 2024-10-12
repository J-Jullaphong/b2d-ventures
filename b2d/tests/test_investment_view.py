from django.urls import reverse
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from .basecase import BaseCase


class InvestmentViewTest(BaseCase):

    def test_investment_view_with_investor_user(self):
        """Test the investment view which login as investor user is rendered."""
        # login as investor
        login_successful = self.client.login(username=self.investor1.username, password="password123")
        self.assertTrue(login_successful)
        url = reverse('b2d:invest_fundraise', kwargs={'fundraise_id': self.fundraising1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'b2d/transaction.html')

    def test_investment_view_without_investor_user(self):
        """Test the investment view which not login as investor user is redirect."""
        url = reverse('b2d:invest_fundraise', kwargs={'fundraise_id': self.fundraising1.id})
        response = self.client.get(url)
        # Not authentication should redirect
        self.assertEqual(response.status_code, 302)
        # Business user should redirect
        login_successful = self.client.login(username=self.business1.username, password="password123")
        self.assertTrue(login_successful)
        self.assertEqual(response.status_code, 302)

    def test_investment_view_non_existent(self):
        """Test that requesting a non-existent fundraising returns a 404 error."""
        self.client.login(username=self.investor1.username, password="password123")
        url = reverse('b2d:invest_fundraise', kwargs={'fundraise_id': 9999999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_investment_view_with_valid_invest(self):
        """Test investor invest with valid submission should redirect"""
        self.client.login(username=self.investor1.username, password="password123")
        url = reverse('b2d:invest_fundraise', kwargs={'fundraise_id': self.fundraising1.id})

        investment_datetime = timezone.now().strftime('%Y-%m-%dT%H:%M')
        response = self.client.post(url, data={
            'amount': 500,
            'investment_datetime': investment_datetime,
            'transaction_slip': SimpleUploadedFile('slip.jpg', b'file_content')
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('b2d:business_detail', kwargs={'pk': self.fundraising1.business_id}))

    def test_investment_view_more_than_fundraising_goal(self):
        """Test that invalid form submission shows errors when investor invest more than fundraising goal."""
        self.client.login(username=self.investor1.username, password="password123")
        url = reverse('b2d:invest_fundraise', kwargs={'fundraise_id': self.fundraising1.id})

        investment_datetime = timezone.now().strftime('%Y-%m-%dT%H:%M')
        response = self.client.post(url, data={
            'amount': 10000000,
            'investment_datetime': investment_datetime,
            'transaction_slip': SimpleUploadedFile('slip.jpg', b'file_content')
        })

        current_investment = self.fundraising1.get_current_investment()
        remaining_amount = self.fundraising1.goal_amount - current_investment

        self.assertIn(f"The amount exceeds the remaining fundraising goal. "
                      f"You can only invest up to ${remaining_amount:.2f}.",
                      response.context['form'].errors.get('amount', []))

    def test_investment_view_less_than_minimum_invest(self):
        """Test that invalid form submission shows errors when investor invests less than minimum invest."""
        self.client.login(username=self.investor1.username, password="password123")
        url = reverse('b2d:invest_fundraise', kwargs={'fundraise_id': self.fundraising1.id})

        investment_datetime = timezone.now().strftime('%Y-%m-%dT%H:%M')
        response = self.client.post(url, data={
            'amount': 0,
            'investment_datetime': investment_datetime,
            'transaction_slip': SimpleUploadedFile('slip.jpg', b'file_content')
        })

        self.assertIn(f"The investment amount is too low. "
                      f"Minimum investment is ${self.fundraising1.minimum_investment:.2f}.",
                      response.context['form'].errors.get('amount', []))
