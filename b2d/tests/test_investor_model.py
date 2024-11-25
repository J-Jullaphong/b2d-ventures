from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import Investor


class InvestorModelTest(TestCase):

    def setUp(self):
        """
        Set up data for the tests.
        """
        self.investor = Investor.objects.create_user(
            username="investor_tester",
            email="investor_tester@example.com",
            first_name="Investor",
            last_name="Tester",
            phone_number="1234567890"
        )

    def test_investor_creation(self):
        """Test that an Investor instance is created with correct attributes."""
        self.assertEqual(self.investor.username, "investor_tester")
        self.assertEqual(self.investor.email, "investor_tester@example.com")
        self.assertEqual(self.investor.first_name, "Investor")
        self.assertEqual(self.investor.last_name, "Tester")
        self.assertEqual(self.investor.phone_number, "1234567890")

    def test_business_financial_statements_upload(self):
        """Test that an Investor can upload financial statements successfully."""
        self.financial_statement_file = SimpleUploadedFile(
            "financial_statement.pdf",
            b"This is a test financial statement."
        )
        self.investor.financial_statements = self.financial_statement_file
        self.investor.save()
        expected_path = f"investor_docs/{self.investor.id}.pdf"
        self.assertEqual(self.investor.financial_statements.name, expected_path)

    def test_investor_string_representation(self):
        """Test the string representation of the Investor model."""
        self.assertEqual(str(self.investor), "Investor Tester - investor_tester@example.com")
