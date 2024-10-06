from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from ..models import FundRaising, Business, Investment, Investor


class FundRaisingModelTest(TestCase):

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
            email="testinvestor@example.com",
            phone_number="0987654321"
        )

        self.fundraise = FundRaising.objects.create(
            business=self.business,
            goal_amount=Decimal('10000.00'),
            publish_date=timezone.now().date(),
            deadline_date=timezone.now().date() + timezone.timedelta(days=30),
            minimum_investment=Decimal('100.00'),
            shares_percentage=Decimal('10.00'),
            fundraising_status='wait'
        )

    def test_fundraising_creation(self):
        """
        Test that a FundRaising instance can be created successfully.
        """
        self.assertEqual(FundRaising.objects.count(), 1)
        self.assertEqual(self.fundraise.business, self.business)
        self.assertEqual(self.fundraise.goal_amount, Decimal('10000.00'))
        self.assertEqual(self.fundraise.fundraising_status, 'wait')

    def test_get_current_investment_with_no_investment(self):
        """
        Test get_current_investment method returns 0.00 when no investments exist.
        """
        self.assertEqual(self.fundraise.get_current_investment(), Decimal('0.00'))

    def test_get_current_investment_with_investments(self):
        """
        Test get_current_investment method returns the correct investment total.
        """
        Investment.objects.create(
            fundraise=self.fundraise,
            investor=self.investor,
            amount=Decimal('1000.00'),
            shares_percentage=Decimal('5.00'),
            investment_status = 'approve'
        )
        Investment.objects.create(
            fundraise=self.fundraise,
            investor=self.investor,
            amount=Decimal('500.00'),
            shares_percentage=Decimal('2.50'),
            investment_status = 'approve'
        )
        self.assertEqual(self.fundraise.get_current_investment(), Decimal('1500.00'))

    def test_get_percentage_investment_with_no_investment(self):
        """
        Test get_percentage_investment returns 0.00 when no investments exist.
        """
        self.assertEqual(self.fundraise.get_percentage_investment(), Decimal('0.00'))

    def test_get_percentage_investment_with_investments(self):
        """
        Test get_percentage_investment method returns the correct percentage of the goal reached.
        """
        Investment.objects.create(
            fundraise=self.fundraise,
            investor=self.investor,
            amount=Decimal('2500.00'),
            shares_percentage=Decimal('5.00'),
            investment_status = 'approve'
        )
        self.assertEqual(self.fundraise.get_percentage_investment(), Decimal('25.00'))

    def test_fundraising_string_representation(self):
        """
        Test the string representation of the FundRaising model.
        """
        Investment.objects.create(
            fundraise=self.fundraise,
            investor=self.investor,
            amount=Decimal('1000.25'),
            shares_percentage=Decimal('2.50'),
            investment_status='approve'
        )
        expected_str = f"Test Business - 1000.25/10000.00"
        self.assertEqual(str(self.fundraise), expected_str)
