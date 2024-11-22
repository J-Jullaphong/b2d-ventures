import uuid
import shutil
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile

from django.test import TestCase, Client
from django.utils import timezone
from b2d.models import Business, Category, FundRaising, Investment, Investor


def generate_file(suffix):
    """Helper method to generate file dynamically"""
    return SimpleUploadedFile(f"{suffix}.pdf", b'content')


class BaseCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.category_tech = Category.objects.create(category_name="Tech")
        self.category_food = Category.objects.create(category_name="Food")
        self.category_retail = Category.objects.create(category_name="Retail")

        self.business1_uid = uuid.uuid4().hex
        self.business2_uid = uuid.uuid4().hex
        self.business3_uid = uuid.uuid4().hex
        self.business4_uid = uuid.uuid4().hex
        self.business5_uid = uuid.uuid4().hex
        self.business6_uid = uuid.uuid4().hex

        self.user1_uid = uuid.uuid4().hex
        self.user2_uid = uuid.uuid4().hex

        self.business1 = Business.objects.create_user(
            username="business_tester1",
            email="business_teste1@example.com",
            password="#Password1234",
            is_active=True,
            name="business1",
            phone_number="0987654321",
            business_registration_certificate=generate_file("certificate1"),
            tax_identification_number=generate_file("tin1"),
            proof_of_address=generate_file("address1"),
            financial_statements=generate_file("statements1"),
            ownership_documents=generate_file("ownership1"),
            director_identification=generate_file("director1"),
            licenses_and_permits=generate_file("licenses1"),
            bank_account_details=generate_file("bank1")
        )

        self.business2 = Business.objects.create_user(
            username="business_tester2",
            email="business_teste2@example.com",
            password="#Password1234",
            is_active=True,
            name="business2",
            phone_number="0987654321",
            business_registration_certificate=generate_file("certificate2"),
            tax_identification_number=generate_file("tin2"),
            proof_of_address=generate_file("address2"),
            financial_statements=generate_file("statements2"),
            ownership_documents=generate_file("ownership2"),
            director_identification=generate_file("director2"),
            licenses_and_permits=generate_file("licenses2"),
            bank_account_details=generate_file("bank2")
        )

        self.business3 = Business.objects.create_user(
            username="business_tester3",
            email="business_teste3@example.com",
            password="#Password1234",
            is_active=True,
            name="business3",
            phone_number="0987654321",
            business_registration_certificate=generate_file("certificate3"),
            tax_identification_number=generate_file("tin3"),
            proof_of_address=generate_file("address3"),
            financial_statements=generate_file("statements3"),
            ownership_documents=generate_file("ownership3"),
            director_identification=generate_file("director3"),
            licenses_and_permits=generate_file("licenses3"),
            bank_account_details=generate_file("bank3")
        )

        self.business4 = Business.objects.create_user(
            username="business_tester4",
            email="business_teste4@example.com",
            password="#Password1234",
            is_active=True,
            name="business4",
            phone_number="0987654321",
            business_registration_certificate=generate_file("certificate4"),
            tax_identification_number=generate_file("tin4"),
            proof_of_address=generate_file("address4"),
            financial_statements=generate_file("statements4"),
            ownership_documents=generate_file("ownership4"),
            director_identification=generate_file("director4"),
            licenses_and_permits=generate_file("licenses4"),
            bank_account_details=generate_file("bank4")
        )

        self.business5 = Business.objects.create_user(
            username="business_tester5",
            email="business_teste5@example.com",
            password="#Password1234",
            is_active=True,
            name="business5",
            phone_number="0987654321",
            business_registration_certificate=generate_file("certificate5"),
            tax_identification_number=generate_file("tin5"),
            proof_of_address=generate_file("address5"),
            financial_statements=generate_file("statements5"),
            ownership_documents=generate_file("ownership5"),
            director_identification=generate_file("director5"),
            licenses_and_permits=generate_file("licenses5"),
            bank_account_details=generate_file("bank5")
        )

        self.business6 = Business.objects.create_user(
            username="business_tester6",
            email="business_teste6@example.com",
            password="#Password1234",
            is_active=True,
            name="business6",
            phone_number="0987654321",
            business_registration_certificate=generate_file("certificate6"),
            tax_identification_number=generate_file("tin6"),
            proof_of_address=generate_file("address6"),
            financial_statements=generate_file("statements6"),
            ownership_documents=generate_file("ownership6"),
            director_identification=generate_file("director6"),
            licenses_and_permits=generate_file("licenses6"),
            bank_account_details=generate_file("bank6")
        )

        self.business1.category.add(self.category_tech)
        self.business2.category.add(self.category_food)
        self.business3.category.add(self.category_retail)
        self.business4.category.add(self.category_tech)
        self.business5.category.add(self.category_food)
        self.business6.category.add(self.category_retail)

        self.fundraising1 = FundRaising.objects.create(
            business=self.business1,
            goal_amount=Decimal("10000.00"),
            publish_date=timezone.now().date() + timezone.timedelta(days=-5),
            deadline_date=timezone.now().date() + timezone.timedelta(days=10),
            share_type="common",
            shares=1000,
            minimum_shares=10,
            fundraising_status="approve"
        )

        self.fundraising2 = FundRaising.objects.create(
            business=self.business2,
            goal_amount=Decimal("20000.00"),
            publish_date=timezone.now().date(),
            deadline_date=timezone.now().date() + timezone.timedelta(days=15),
            share_type="common",
            shares=1000,
            minimum_shares=100,
            fundraising_status="approve"
        )

        self.fundraising3 = FundRaising.objects.create(
            business=self.business3,
            goal_amount=Decimal("15000.00"),
            publish_date=timezone.now().date(),
            deadline_date=timezone.now().date() + timezone.timedelta(days=-15),
            share_type="common",
            shares=1000,
            minimum_shares=10,
            fundraising_status="approve"
        )

        self.fundraising4 = FundRaising.objects.create(
            business=self.business4,
            goal_amount=Decimal("5000.00"),
            publish_date=timezone.now().date(),
            deadline_date=timezone.now().date() + timezone.timedelta(days=15),
            share_type="common",
            shares=1000,
            minimum_shares=10,
            fundraising_status="rejects"
        )

        self.fundraising5 = FundRaising.objects.create(
            business=self.business4,
            goal_amount=Decimal("15000.00"),
            publish_date=timezone.now().date(),
            deadline_date=timezone.now().date() + timezone.timedelta(days=15),
            share_type="common",
            shares=1000,
            minimum_shares=10,
            fundraising_status="wait"
        )

        self.investor1 = Investor.objects.create_user(
            username="investor_tester1",
            email="investor_tester1@example.com",
            password="#Password1234",
            is_active=True,
            first_name="Investor1",
            last_name="Tester1",
            phone_number="0987654321",
            financial_statements=generate_file("investor1")

        )

        self.investor2 = Investor.objects.create_user(
            username="investor_tester2",
            email="investor_tester2@example.com",
            password="#Password1234",
            is_active=True,
            first_name="Investor2",
            last_name="Tester2",
            phone_number="0987654321",
            financial_statements=generate_file("investor2")
        )

        self.investor3 = Investor.objects.create_user(
            username="investor_tester3",
            email="investor_tester3@example.com",
            password="#Password1234",
            is_active=True,
            first_name="Investor3",
            last_name="Tester3",
            phone_number="0987654321",
            financial_statements=generate_file("investor3")
        )

        self.investment1 = Investment.objects.create(
            investor=self.investor1,
            fundraise=self.fundraising1,
            amount=Decimal("5000.00"),
            shares=50,
            transaction_slip=generate_file("slip1"),
            investment_status="approve"
        )

        self.investment2 = Investment.objects.create(
            investor=self.investor1,
            fundraise=self.fundraising2,
            amount=Decimal("2500.00"),
            shares=50,
            transaction_slip=generate_file("slip2"),
            investment_status="approve"
        )

        self.investment3 = Investment.objects.create(
            investor=self.investor2,
            fundraise=self.fundraising1,
            amount=Decimal("2500.00"),
            shares=50,
            transaction_slip=generate_file("slip3"),
            investment_status="approve"
        )

    def tearDown(self):
        """Clean up data after each test case."""
        super().tearDown()

