from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import Investment, FundRaising, Investor, Business


class InvestmentModelTest(TestCase):

    def setUp(self):
        """
        Set up data for the tests.
        """
        self.business = Business.objects.create(
            username="testbusiness",
            email="testbusiness@example.com",
            name="Test Business",
            phone_number="1234567890"
        )

        self.investor = Investor.objects.create(
            username="testinvestor",
            first_name="test",
            last_name="investor",
            email="testinvestor@example.com",
            phone_number="0987654321"
        )

        self.fundraise = FundRaising.objects.create(
            business=self.business,
            goal_amount=Decimal('5000.00'),
            publish_date=timezone.now().date(),
            deadline_date=timezone.now().date() + timezone.timedelta(days=30),
            minimum_investment=Decimal('100.00'),
            shares_percentage=Decimal('10.00')
        )

        self.transaction_slip = SimpleUploadedFile(
            name="slip.jpg",
            content=b"This is a test transaction slip.",
            content_type="image/jpeg"
        )

    def test_investment_creation(self):
        """
        Test that an Investment instance can be created successfully.
        """
        investment = Investment.objects.create(
            investor=self.investor,
            fundraise=self.fundraise,
            amount=Decimal('1000.00'),
            shares_percentage=Decimal('5.00'),
            transaction_slip=self.transaction_slip
        )
        self.assertEqual(Investment.objects.count(), 1)
        self.assertEqual(investment.amount, Decimal('1000.00'))
        self.assertEqual(investment.shares_percentage, Decimal('5.00'))
        self.assertEqual(investment.investment_status, 'wait')

    def test_default_investment_values(self):
        """
        Test the default values for investment_datetime and investment_status.
        """
        investment = Investment.objects.create(
            investor=self.investor,
            fundraise=self.fundraise,
            amount=Decimal('500.00'),
            shares_percentage=Decimal('2.50')
        )
        self.assertEqual(investment.investment_status, 'wait')
        self.assertAlmostEqual(investment.investment_datetime.date(), timezone.now().date())

    def test_transaction_slip_upload_path(self):
        """
        Test that the transaction_slip file path is generated correctly.
        """
        investment = Investment.objects.create(
            investor=self.investor,
            fundraise=self.fundraise,
            amount=Decimal('1000.00'),
            shares_percentage=Decimal('5.00'),
            transaction_slip=self.transaction_slip
        )
        expected_path = f"investment_slips/{self.fundraise.id}/{self.investor.id}/slip.jpg"
        self.assertEqual(investment.transaction_slip.name, expected_path)

    def test_investment_string_representation(self):
        """
        Test the string representation of the Investment model.
        """
        investment = Investment.objects.create(
            investor=self.investor,
            fundraise=self.fundraise,
            amount=Decimal('1000.00'),
            shares_percentage=Decimal('5.00')
        )
        expected_str = f"test investor - testinvestor@example.com: Investment of 1000.00 in Test Business"
        self.assertEqual(str(investment), expected_str)
