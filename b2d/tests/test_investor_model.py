from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import Investor


class InvestorModelTest(TestCase):

    def setUp(self):
        """
        Set up data for the tests.
        """
        self.investor = Investor.objects.create_user(
            username='testinvestor',
            email='testinvestor@example.com',
            password='testpassword',
            first_name='Test',
            last_name='Investor',
            phone_number='1234567890'
        )

        self.financial_statement_file = SimpleUploadedFile(
            name="financial_statement.pdf",
            content=b"This is a test financial statement.",
            content_type="application/pdf"
        )

    def test_investor_creation(self):
        """
        Test that an Investor instance can be created successfully.
        """
        self.assertEqual(Investor.objects.count(), 1)
        self.assertEqual(self.investor.username, 'testinvestor')
        self.assertEqual(self.investor.email, 'testinvestor@example.com')
        self.assertEqual(self.investor.first_name, 'Test')
        self.assertEqual(self.investor.last_name, 'Investor')
        self.assertEqual(self.investor.phone_number, '1234567890')

    def test_investor_financial_statements_upload(self):
        """
        Test that an Investor can upload financial statements successfully.
        """
        self.investor.financial_statements = self.financial_statement_file
        self.investor.save()

        expected_path = f'investor_docs/{self.investor.id}.pdf'
        self.assertEqual(self.investor.financial_statements.name, expected_path)

    def test_investor_string_representation(self):
        """
        Test the string representation of the Investor model.
        """
        expected_str = f"{self.investor.first_name} {self.investor.last_name} - {self.investor.email}"
        self.assertEqual(str(self.investor), expected_str)
