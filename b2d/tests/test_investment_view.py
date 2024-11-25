from unittest.mock import patch
from django.urls import reverse
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from .basecase import BaseCase, Investment


class InvestmentViewTest(BaseCase):

    def test_investment_view_accessible_for_investor(self):
        """Test that the investment view is accessible for logged-in investors."""
        self.client.login(username=self.investor1.username, password="#Password1234")
        url = reverse("b2d:invest_fundraise", kwargs={"fundraise_id": self.fundraising1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'b2d/transaction.html')

    def test_investment_view_forbidden_for_non_investor(self):
        """Test that the investment view is forbidden for non-investor users."""
        self.client.logout()
        url = reverse("b2d:invest_fundraise", kwargs={"fundraise_id": self.fundraising1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    @patch('django_recaptcha.fields.ReCaptchaField.clean', return_value=True)
    def test_post_investment_valid_data(self, mock_captcha_clean):
        """Test the investment submission with valid data."""
        self.client.login(username=self.investor1.username, password="#Password1234")
        form_data = {
            'shares': 50,
            'investment_datetime': timezone.now().strftime('%Y-%m-%dT%H:%M'),
            'transaction_slip': SimpleUploadedFile('slip.jpg', b'file_content'),
            'captcha': 'PASSED'
        }

        url = reverse("b2d:invest_fundraise", kwargs={"fundraise_id": self.fundraising1.id})
        response = self.client.post(url, form_data)

        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertRedirects(response, reverse('b2d:business_detail', kwargs={'pk': self.fundraising1.business.id}))

    def test_post_investment_exceeds_max_shares(self):
        """Test that the form rejects submissions exceeding maximum shares."""
        self.client.login(username=self.investor1.username, password="#Password1234")
        form_data = {
            'shares': 2000,  # Exceeds maximum
            'investment_datetime': timezone.now().strftime('%Y-%m-%dT%H:%M'),
            'transaction_slip': SimpleUploadedFile('slip.jpg', b'file_content'),
        }
        url = reverse("b2d:invest_fundraise", kwargs={"fundraise_id": self.fundraising1.id})
        response = self.client.post(url, form_data)

        self.assertEqual(response.status_code, 200)  # Re-renders form with errors
        form = response.context['form']
        self.assertIn("The number of shares exceeds the maximum available. You can only invest up to 250 shares.", form.errors.get('shares', []))

    def test_post_investment_below_min_shares(self):
        """Test that the form rejects submissions below minimum shares."""
        self.client.login(username=self.investor1.username, password="#Password1234")
        form_data = {
            'shares': 1,
            'investment_datetime': timezone.now().strftime('%Y-%m-%dT%H:%M'),
            'transaction_slip': SimpleUploadedFile('slip.jpg', b'file_content'),
        }
        url = reverse("b2d:invest_fundraise", kwargs={"fundraise_id": self.fundraising1.id})
        response = self.client.post(url, form_data)

        self.assertEqual(response.status_code, 200)  # Re-renders form with errors
        form = response.context['form']
        self.assertIn("The number of shares must be at least 10.", form.errors.get('shares', []))

    def test_missing_transaction_slip(self):
        """Test that the form rejects submissions without a transaction slip."""
        self.client.login(username=self.investor1.username, password="#Password1234")
        form_data = {
            'shares': 50,
            'investment_datetime': timezone.now().strftime('%Y-%m-%dT%H:%M'),
        }
        url = reverse("b2d:invest_fundraise", kwargs={"fundraise_id": self.fundraising1.id})
        response = self.client.post(url, form_data)

        self.assertEqual(response.status_code, 200)  # Re-renders form with errors
        form = response.context['form']
        self.assertIn("This field is required.", form.errors.get('transaction_slip', []))
