from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import Business, Category


class BusinessModelTest(TestCase):

    def setUp(self):
        """
        Set up initial data for the tests. This includes creating a category and a business.
        """
        self.category = Category.objects.create(category_name='Technology')
        self.business_data = {
            'username': 'testbusiness',
            'password': 'password123',
            'name': 'Test Business',
            'phone_number': '1234567890',
            'category': self.category,
            'business_registration_certificate': SimpleUploadedFile(
                'business_registration_certificate.pdf', b'certificate content'),
            'tax_identification_number': SimpleUploadedFile(
                'tax_identification_number.pdf', b'tax content'),
            'proof_of_address': SimpleUploadedFile(
                'proof_of_address.pdf', b'address content'),
            'financial_statements': SimpleUploadedFile(
                'financial_statements.pdf', b'statements content'),
            'ownership_documents': SimpleUploadedFile(
                'ownership_documents.pdf', b'ownership content'),
            'director_identification': SimpleUploadedFile(
                'director_identification.pdf', b'identification content'),
            'licenses_and_permits': SimpleUploadedFile(
                'licenses_and_permits.pdf', b'licenses content'),
            'bank_account_details': SimpleUploadedFile(
                'bank_account_details.pdf', b'bank content')
        }

    def test_business_creation(self):
        """
        Test business model creation with all fields.
        """
        business = Business.objects.create(
            username=self.business_data['username'],
            password=self.business_data['password'],
            name=self.business_data['name'],
            phone_number=self.business_data['phone_number'],
            category=self.category,
            business_registration_certificate=self.business_data['business_registration_certificate'],
            tax_identification_number=self.business_data['tax_identification_number'],
            proof_of_address=self.business_data['proof_of_address'],
            financial_statements=self.business_data['financial_statements'],
            ownership_documents=self.business_data['ownership_documents'],
            director_identification=self.business_data['director_identification'],
            licenses_and_permits=self.business_data['licenses_and_permits'],
            bank_account_details=self.business_data['bank_account_details']
        )

        self.assertEqual(Business.objects.count(), 1)
        self.assertEqual(business.name, 'Test Business')

    def test_business_file_upload_urls(self):
        """
        Test that the file fields have correct custom upload URLs.
        """
        business = Business.objects.create(
            username=self.business_data['username'],
            password=self.business_data['password'],
            name=self.business_data['name'],
            phone_number=self.business_data['phone_number'],
            category=self.category,
            business_registration_certificate=self.business_data['business_registration_certificate'],
            tax_identification_number=self.business_data['tax_identification_number'],
            proof_of_address=self.business_data['proof_of_address'],
            financial_statements=self.business_data['financial_statements'],
            ownership_documents=self.business_data['ownership_documents'],
            director_identification=self.business_data['director_identification'],
            licenses_and_permits=self.business_data['licenses_and_permits'],
            bank_account_details=self.business_data['bank_account_details']
        )

        self.assertIn(f'business_docs/{business.id}/business_registration_certificate.pdf', business.business_registration_certificate.url)
        self.assertIn(f'business_docs/{business.id}/tax_identification_number.pdf', business.tax_identification_number.url)
        self.assertIn(f'business_docs/{business.id}/proof_of_address.pdf', business.proof_of_address.url)
        self.assertIn(f'business_docs/{business.id}/financial_statements.pdf', business.financial_statements.url)
        self.assertIn(f'business_docs/{business.id}/ownership_documents.pdf', business.ownership_documents.url)
        self.assertIn(f'business_docs/{business.id}/director_identification.pdf', business.director_identification.url)
        self.assertIn(f'business_docs/{business.id}/licenses_and_permits.pdf', business.licenses_and_permits.url)
        self.assertIn(f'business_docs/{business.id}/bank_account_details.pdf', business.bank_account_details.url)

    def test_business_string_representation(self):
        """
        Test the string representation of the business model.
        """
        business = Business.objects.create(
            username=self.business_data['username'],
            password=self.business_data['password'],
            name=self.business_data['name'],
            phone_number=self.business_data['phone_number'],
            category=self.category,
        )

        self.assertEqual(str(business), f'{business.name} - {business.email}')
