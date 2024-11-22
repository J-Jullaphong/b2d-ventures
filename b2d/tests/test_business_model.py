from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import Business, Category


class BusinessModelTest(TestCase):

    def setUp(self):
        self.category1 = Category.objects.create(category_name="Technology")
        self.category2 = Category.objects.create(category_name="Finance")

        self.business = Business.objects.create_user(
            username="business_tester",
            email="business_tester@example.com",
            name="Tech Innovators",
            phone_number="1234567890"
        )
        self.business.category.add(self.category1, self.category2)

    def test_business_creation(self):
        """Test that a Business instance is created with correct attributes."""
        self.assertEqual(self.business.username, "business_tester")
        self.assertEqual(self.business.email, "business_tester@example.com")
        self.assertEqual(self.business.name, 'Tech Innovators')
        self.assertEqual(self.business.phone_number, '1234567890')

    def test_investor_documents_upload(self):
        """Test that Business can upload documents successfully."""
        self.business_registration_certificate = SimpleUploadedFile('business_registration_certificate.pdf', b'certificate content')
        self.tax_identification_number = SimpleUploadedFile('tax_identification_number.pdf', b'tax content')
        self.proof_of_address = SimpleUploadedFile('proof_of_address.pdf', b'address content')
        self.financial_statements = SimpleUploadedFile('financial_statements.pdf', b'statements content')
        self.ownership_documents = SimpleUploadedFile('ownership_documents.pdf', b'ownership content')
        self.director_identification = SimpleUploadedFile('director_identification.pdf', b'identification content')
        self.licenses_and_permits = SimpleUploadedFile('licenses_and_permits.pdf', b'licenses content')
        self.bank_account_details = SimpleUploadedFile('bank_account_details.pdf', b'bank content')

        self.business.business_registration_certificate = self.business_registration_certificate
        self.business.tax_identification_number = self.tax_identification_number
        self.business.proof_of_address = self.proof_of_address
        self.business.financial_statements = self.financial_statements
        self.business.ownership_documents = self.ownership_documents
        self.business.director_identification = self.director_identification
        self.business.licenses_and_permits = self.licenses_and_permits
        self.business.bank_account_details = self.bank_account_details

        self.business.save()

        self.assertEqual(self.business.business_registration_certificate.name, f"business_docs/{self.business.id}/business_registration_certificate.pdf")
        self.assertEqual(self.business.tax_identification_number.name, f"business_docs/{self.business.id}/tax_identification_number.pdf")
        self.assertEqual(self.business.proof_of_address.name, f"business_docs/{self.business.id}/proof_of_address.pdf")
        self.assertEqual(self.business.financial_statements.name, f"business_docs/{self.business.id}/financial_statements.pdf")
        self.assertEqual(self.business.ownership_documents.name, f"business_docs/{self.business.id}/ownership_documents.pdf")
        self.assertEqual(self.business.director_identification.name, f"business_docs/{self.business.id}/director_identification.pdf")
        self.assertEqual(self.business.licenses_and_permits.name, f"business_docs/{self.business.id}/licenses_and_permits.pdf")
        self.assertEqual(self.business.bank_account_details.name, f"business_docs/{self.business.id}/bank_account_details.pdf")

    def test_business_string_representation(self):
        """Test the string representation of the Business model."""
        self.assertEqual(str(self.business), "Tech Innovators - business_tester@example.com")
