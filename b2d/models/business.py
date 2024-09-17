from django.contrib.auth.models import User
from django.db import models

from .category import Category


def business_registration_certificate_path(instance, filename):
    """
    Path for storing business registration certificates.
    """
    ext = filename.split('.')[-1]
    return f'business_docs/{instance.id}/business_registration_certificate.{ext}'


def tax_identification_number_path(instance, filename):
    """
    Path for storing tax identification numbers.
    """
    ext = filename.split('.')[-1]
    return f'business_docs/{instance.id}/tax_identification_number.{ext}'


def proof_of_address_path(instance, filename):
    """
    Path for storing proof of address.
    """
    ext = filename.split('.')[-1]
    return f'business_docs/{instance.id}/proof_of_address.{ext}'


def financial_statements_path(instance, filename):
    """
    Path for storing financial statements.
    """
    ext = filename.split('.')[-1]
    return f'business_docs/{instance.id}/financial_statements.{ext}'


def ownership_documents_path(instance, filename):
    """
    Path for storing ownership documents.
    """
    ext = filename.split('.')[-1]
    return f'business_docs/{instance.id}/ownership_documents.{ext}'


def director_identification_path(instance, filename):
    """
    Path for storing director identification.
    """
    ext = filename.split('.')[-1]
    return f'business_docs/{instance.id}/director_identification.{ext}'


def licenses_and_permits_path(instance, filename):
    """
    Path for storing licenses and permits.
    """
    ext = filename.split('.')[-1]
    return f'business_docs/{instance.id}/licenses_and_permits.{ext}'


def bank_account_details_path(instance, filename):
    """
    Path for storing bank account details.
    """
    ext = filename.split('.')[-1]
    return f'business_docs/{instance.id}/bank_account_details.{ext}'


class Business(User):
    """Business Model represents a business, containing detailed information."""
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, null=True,
                                 on_delete=models.SET_NULL)
    phone_number = models.CharField(max_length=10)
    business_registration_certificate = models.FileField(
        upload_to=business_registration_certificate_path)
    tax_identification_number = models.FileField(
        upload_to=tax_identification_number_path)
    proof_of_address = models.FileField(
        upload_to=proof_of_address_path)
    financial_statements = models.FileField(
        upload_to=financial_statements_path, null=True, blank=True)
    ownership_documents = models.FileField(
        upload_to=ownership_documents_path)
    director_identification = models.FileField(
        upload_to=director_identification_path)
    licenses_and_permits = models.FileField(
        upload_to=licenses_and_permits_path, null=True, blank=True)
    bank_account_details = models.FileField(
        upload_to=bank_account_details_path)

    class Meta:
        verbose_name = "Business"
        verbose_name_plural = "Businesses"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
