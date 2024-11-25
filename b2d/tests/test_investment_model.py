from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import Investment, FundRaising, Investor, Business, Category


class InvestmentModelTest(TestCase):

    def setUp(self):
        """Set up data for the tests."""
        self.category = Category.objects.create(category_name="Finance")
        self.business = Business.objects.create_user(
            username="business_tester",
            email="business_tester@example.com",
            name="Tech Innovators",
            phone_number="1234567890"
        )
        self.business.category.add(self.category)

        self.investor = Investor.objects.create_user(
            username="investor_tester",
            email="investor_tester@example.com",
            first_name="Investor",
            last_name="Tester",
            phone_number="1234567890"
        )

        self.fundraising = FundRaising.objects.create(
            business=self.business,
            goal_amount=Decimal('100000.00'),
            publish_date=timezone.now().date(),
            deadline_date=timezone.now().date() + timezone.timedelta(days=45),
            share_type="common",
            shares=1000,
            minimum_shares=10,
            fundraising_status="approve"
        )

        self.investment = Investment.objects.create(
            investor=self.investor,
            fundraise=self.fundraising,
            amount=Decimal("5000.00"),
            shares=50,
            transaction_slip=SimpleUploadedFile(name="slip.jpg", content=b"This is a test transaction slip.")
        )

    def test_investment_creation(self):
        """Test that an Investment instance is created with correct attributes."""
        self.assertEqual(self.investment.investor, self.investor)
        self.assertEqual(self.investment.fundraise, self.fundraising)
        self.assertEqual(self.investment.amount, Decimal("5000.00"))
        self.assertEqual(self.investment.shares, 50)
        self.assertEqual(self.investment.investment_status, "wait")

    def test_investment_string_representation(self):
        """Test the string representation of the Investment model."""
        self.assertEqual(str(self.investment), "Investor Tester - investor_tester@example.com: Investment of 5000.00 in Tech Innovators (50 shares)")
