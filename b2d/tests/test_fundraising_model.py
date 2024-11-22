from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from ..models import FundRaising, Business, Investment, Investor, Category


class FundRaisingModelTest(TestCase):

    def setUp(self):
        """Set up data for the tests."""
        self.category1 = Category.objects.create(category_name="Technology")
        self.category2 = Category.objects.create(category_name="Finance")
        self.business = Business.objects.create_user(
            username="business_tester",
            email="business_tester@example.com",
            name="Tech Innovators",
            phone_number="1234567890"
        )
        self.business.category.add(self.category1, self.category2)

        self.investor1 = Investor.objects.create_user(
            username="investor_tester",
            email="investor_tester@example.com",
            first_name="Investor",
            last_name="Tester",
            phone_number="1234567890"
        )

        self.investor2 = Investor.objects.create_user(
            username="investor_tester2",
            email="investor_teste2r@example.com",
            first_name="Investor2",
            last_name="Tester2",
            phone_number="1234567890"
        )

        self.fundraising = FundRaising.objects.create(
            business=self.business,
            goal_amount=Decimal('100000.00'),
            publish_date=timezone.now().date(),
            deadline_date=timezone.now().date() + timezone.timedelta(days=30),
            share_type="common",
            shares=1000,
            minimum_shares=10,
            fundraising_status="approve"
        )

        self.investment1 = Investment.objects.create(
            investor=self.investor1,
            fundraise=self.fundraising,
            amount=Decimal("5000.00"),
            shares=50,
            investment_status="approve"
        )

        self.investment2 = Investment.objects.create(
            investor=self.investor2,
            fundraise=self.fundraising,
            amount=Decimal("10000.00"),
            shares=100,
            investment_status="approve"
        )

    def test_fundraising_creation(self):
        """Test that a FundRaising instance is created correctly."""
        self.assertEqual(self.fundraising.business.name, "Tech Innovators")
        self.assertEqual(self.fundraising.goal_amount, Decimal("100000.00"))
        self.assertEqual(self.fundraising.share_type, "common")
        self.assertEqual(self.fundraising.minimum_shares, 10)
        self.assertEqual(self.fundraising.shares, 1000)
        self.assertEqual(self.fundraising.fundraising_status, 'approve')

    def test_get_current_investors(self):
        """Test the number of current investors in the fundraising."""
        current_investors = self.fundraising.get_current_investors()
        self.assertEqual(current_investors, 2)

    def test_get_current_investment(self):
        """Test the total current investment amount."""
        total_investment = self.fundraising.get_current_investment()
        self.assertEqual(total_investment, Decimal("15000.00"))  # 5000 + 1000

    def test_get_price_per_share(self):
        """Test the calculated price per share."""
        price_per_share = self.fundraising.get_price_per_share()
        self.assertEqual(price_per_share, Decimal("100.00"))  # goal_amount / shares

    def test_get_percentage_investment(self):
        """Test the percentage of the goal amount that has been invested."""
        percentage_investment = self.fundraising.get_percentage_investment()
        self.assertEqual(percentage_investment, Decimal("15.00"))  # (15000 / 100000) * 100

    def test_fundraising_string_representation(self):
        """Test the string representation of the FundRaising model."""
        self.assertEqual(str(self.fundraising), "Tech Innovators - 15000/100000.00 (Common Stock)")









