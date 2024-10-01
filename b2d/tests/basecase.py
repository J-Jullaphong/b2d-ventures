import uuid

from django.test import TestCase
from django.utils import timezone
from b2d.models import Business, Category, FundRaising, Investment, Investor


def generate_file_path(suffix):
    """Helper method to generate file paths dynamically"""
    return f'path/to/{suffix}.pdf'


class BaseCase(TestCase):

    def setUp(self):
        # Create categories
        self.category_tech = Category.objects.create(category_name="Tech")
        self.category_food = Category.objects.create(category_name="Food")
        self.category_retail = Category.objects.create(category_name="Retail")

        # Generate unique identifiers for business entries
        self.business1_uid = uuid.uuid4().hex
        self.business2_uid = uuid.uuid4().hex
        self.business3_uid = uuid.uuid4().hex
        self.business4_uid = uuid.uuid4().hex
        self.business5_uid = uuid.uuid4().hex
        self.business6_uid = uuid.uuid4().hex
        self.user1_uid = uuid.uuid4().hex
        self.user2_uid = uuid.uuid4().hex

        # Create businesses with dynamic file paths and unique identifiers
        self.business1 = Business.objects.create(
            username=f"username_{self.business1_uid}",
            email=f"user{self.business1_uid}@example.com",
            name="Tech Innovate",
            phone_number="1234567890",
            description="Innovative tech solutions.",
            category=self.category_tech,
            business_registration_certificate=generate_file_path('certificate1'),
            tax_identification_number=generate_file_path('tin1'),
            proof_of_address=generate_file_path('address1'),
            financial_statements=generate_file_path('statements1'),
            ownership_documents=generate_file_path('ownership1'),
            director_identification=generate_file_path('director1'),
            licenses_and_permits=generate_file_path('licenses1'),
            bank_account_details=generate_file_path('bank1')
        )

        self.business2 = Business.objects.create(
            username=f"username_{self.business2_uid}",
            email=f"user{self.business2_uid}@example.com",
            name="Foodies Unite",
            phone_number="0987654321",
            description="A delightful culinary journey.",
            category=self.category_food,
            business_registration_certificate=generate_file_path('certificate2'),
            tax_identification_number=generate_file_path('tin2'),
            proof_of_address=generate_file_path('address2'),
            financial_statements=generate_file_path('statements2'),
            ownership_documents=generate_file_path('ownership2'),
            director_identification=generate_file_path('director2'),
            licenses_and_permits=generate_file_path('licenses2'),
            bank_account_details=generate_file_path('bank2')
        )

        self.business3 = Business.objects.create(
            username=f"username_{self.business3_uid}",
            email=f"user{self.business3_uid}@example.com",
            name="Retail Giants",
            phone_number="1928374650",
            description="Revolutionizing retail shopping.",
            category=self.category_retail,
            business_registration_certificate=generate_file_path('certificate3'),
            tax_identification_number=generate_file_path('tin3'),
            proof_of_address=generate_file_path('address3'),
            financial_statements=generate_file_path('statements3'),
            ownership_documents=generate_file_path('ownership3'),
            director_identification=generate_file_path('director3'),
            licenses_and_permits=generate_file_path('licenses3'),
            bank_account_details=generate_file_path('bank3')
        )

        self.business4 = Business.objects.create(
            username=f"username_{self.business4_uid}",
            email=f"user{self.business4_uid}@example.com",
            name="Retail Giants",
            phone_number="1928374650",
            description="Revolutionizing retail shopping.",
            category=self.category_retail,
            business_registration_certificate=generate_file_path('certificate4'),
            tax_identification_number=generate_file_path('tin4'),
            proof_of_address=generate_file_path('address4'),
            financial_statements=generate_file_path('statements4'),
            ownership_documents=generate_file_path('ownership4'),
            director_identification=generate_file_path('director4'),
            licenses_and_permits=generate_file_path('licenses4'),
            bank_account_details=generate_file_path('bank4')
        )

        self.business5 = Business.objects.create(
            username=f"username_{self.business5_uid}",
            email=f"user{self.business5_uid}@example.com",
            name="Retail Giants",
            phone_number="1928374650",
            description="Revolutionizing retail shopping.",
            category=self.category_retail,
            business_registration_certificate=generate_file_path('certificate5'),
            tax_identification_number=generate_file_path('tin5'),
            proof_of_address=generate_file_path('address5'),
            financial_statements=generate_file_path('statements5'),
            ownership_documents=generate_file_path('ownership5'),
            director_identification=generate_file_path('director5'),
            licenses_and_permits=generate_file_path('licenses5'),
            bank_account_details=generate_file_path('bank5')
        )

        self.business6 = Business.objects.create(
            username=f"username_{self.business6_uid}",
            email=f"user{self.business6_uid}@example.com",
            name="Retail Giants",
            phone_number="1928374650",
            description="Revolutionizing retail shopping.",
            category=self.category_retail,
            business_registration_certificate=generate_file_path('certificate6'),
            tax_identification_number=generate_file_path('tin6'),
            proof_of_address=generate_file_path('address6'),
            financial_statements=generate_file_path('statements6'),
            ownership_documents=generate_file_path('ownership6'),
            director_identification=generate_file_path('director6'),
            licenses_and_permits=generate_file_path('licenses6'),
            bank_account_details=generate_file_path('bank6')
        )

        self.fundraising1 = FundRaising.objects.create(
            business=self.business1,
            goal_amount=10000.00,
            publish_date=timezone.now().date(),
            deadline_date=timezone.now().date() + timezone.timedelta(days=10),
            minimum_investment=500.00,
            shares_percentage=10.00,
            fundraising_status='approve'
        )

        self.fundraising2 = FundRaising.objects.create(
            business=self.business2,
            goal_amount='20000.00',
            publish_date=timezone.now().date(),
            deadline_date=timezone.now().date() + timezone.timedelta(days=15),
            minimum_investment='1000.00',
            shares_percentage='15.00',
            fundraising_status='approve'
        )

        self.fundraising3 = FundRaising.objects.create(
            business=self.business3,
            goal_amount='15000.00',
            publish_date=timezone.now().date(),
            deadline_date=timezone.now().date() + timezone.timedelta(days=-15),
            minimum_investment='750.00',
            shares_percentage='12.50',
            fundraising_status='approve'
        )

        self.fundraising4 = FundRaising.objects.create(
            business=self.business4,
            goal_amount='15000.00',
            publish_date=timezone.now().date(),
            deadline_date=timezone.now().date() + timezone.timedelta(days=15),
            minimum_investment='750.00',
            shares_percentage='12.50',
            fundraising_status='rejects'
        )

        self.fundraising5 = FundRaising.objects.create(
            business=self.business4,
            goal_amount='15000.00',
            publish_date=timezone.now().date(),
            deadline_date=timezone.now().date() + timezone.timedelta(days=15),
            minimum_investment='750.00',
            shares_percentage='12.50',
            fundraising_status='wait'
        )

        # Create investors
        self.investor1 = Investor.objects.create_user(
            username=f"investor_{self.user1_uid}",
            email=f"investor1@example.com",
            password="password123",
            first_name="Investor",
            last_name="One",
            financial_statements=generate_file_path('investor1')
        )

        self.investor2 = Investor.objects.create_user(
            username=f"investor_{self.user2_uid}",
            email=f"investor2@example.com",
            password="password123",
            first_name="Investor",
            last_name="Two",
            financial_statements=generate_file_path('investor2')
        )

        # Create investments
        self.investment1 = Investment.objects.create(
            investor=self.investor1,
            fundraise=self.fundraising1,
            amount=5000.00,
            shares_percentage=self.fundraising1.shares_percentage,
            investment_status='approve'
        )

        self.investment2 = Investment.objects.create(
            investor=self.investor1,
            fundraise=self.fundraising2,
            amount=2500.00,
            shares_percentage=self.fundraising2.shares_percentage,
            investment_status='approve'
        )

        self.investment3 = Investment.objects.create(
            investor=self.investor2,
            fundraise=self.fundraising1,
            amount=2500.00,
            shares_percentage=self.fundraising1.shares_percentage,
            investment_status='approve'
        )

    def tearDown(self):
        """Clean up data after each test case."""
        super().tearDown()
