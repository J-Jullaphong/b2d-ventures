from django.contrib.auth.models import User
from django.db import models


class Business(User):
    """Business Model represents a business, containing detailed information."""
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)
    business_registration_certificate = models.FileField(upload_to='business_docs/registration_certificates/')
    tax_identification_number = models.FileField(upload_to='business_docs/tax_ids/')
    proof_of_address = models.FileField(upload_to='business_docs/proof_of_address/')
    financial_statements = models.FileField(upload_to='business_docs/financial_statements/', null=True, blank=True)
    ownership_documents = models.FileField(upload_to='business_docs/ownership_documents/')
    director_identification = models.FileField(upload_to='business_docs/director_identification/')
    licenses_and_permits = models.FileField(upload_to='business_docs/licenses_and_permits/', null=True, blank=True)
    bank_account_details = models.FileField(upload_to='business_docs/bank_account_details/')

    class Meta:
        verbose_name = "Business"
        verbose_name_plural = "Businesses"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
