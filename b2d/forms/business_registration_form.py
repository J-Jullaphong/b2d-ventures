from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_recaptcha.fields import ReCaptchaField
from django.contrib.auth.models import Group
from django_otp.plugins.otp_email.models import EmailDevice

from ..models import Business, UserConsent


class BusinessRegistrationForm(UserCreationForm):
    """Form for registering a new business."""
    usable_password = None
    captcha = ReCaptchaField()

    class Meta:
        model = Business
        fields = [
            'name', 'email', 'phone_number', 'password1', 'password2',
            'business_registration_certificate', 'tax_identification_number',
            'proof_of_address', 'financial_statements', 'ownership_documents',
            'director_identification', 'licenses_and_permits',
            'bank_account_details'
        ]
        labels = {
            'email': 'Email',
            'phone_number': 'Phone Number',
            'business_registration_certificate':
                'Business Registration Certificate',
            'tax_identification_number': 'Tax Identification Number',
            'proof_of_address': 'Proof Of Address',
            'financial_statements': 'Financial Statements',
            'ownership_documents': 'Ownership Documents',
            'director_identification': 'Director Identification',
            'licenses_and_permits': 'Licenses And Permits',
            'bank_account_details': 'Bank Account Details',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Company Name'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Phone Number'
            }),
            'business_registration_certificate': forms.ClearableFileInput(
                attrs={
                    'accept': 'application/pdf',
                }),
            'tax_identification_number': forms.ClearableFileInput(attrs={
                'accept': 'application/pdf',
            }),
            'proof_of_address': forms.ClearableFileInput(attrs={
                'accept': 'application/pdf',
            }),
            'financial_statements': forms.ClearableFileInput(attrs={
                'accept': 'application/pdf',
            }),
            'ownership_documents': forms.ClearableFileInput(attrs={
                'accept': 'application/pdf',
            }),
            'director_identification': forms.ClearableFileInput(attrs={
                'accept': 'application/pdf',
            }),
            'licenses_and_permits': forms.ClearableFileInput(attrs={
                'accept': 'application/pdf',
            }),
            'bank_account_details': forms.ClearableFileInput(attrs={
                'accept': 'application/pdf',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].required = True
            self.fields[field_name].help_text = None
            if self.fields[field_name] != self.fields['captcha']:
                self.fields[field_name].widget.attrs["class"] = "form-control"

        self.fields['password1'].widget.attrs["placeholder"] = "Password"
        self.fields['password2'].widget.attrs[
            "placeholder"] = "Confirm Password"
        self.fields['password2'].label = "Confirm Password"

    def save(self, commit=True):
        """Saves the business with inactive status until approval and sets username to email."""
        user = super().save(commit=False)
        if commit:
            user.is_active = False
            user.username = user.email
            user.save()
            EmailDevice.objects.create(user=user, email=user.email,
                                       name="Email")
            UserConsent.objects.create(user=user, consent=True)

            business_group = Group.objects.get(name="Business")
            business_group.user_set.add(user)

        return user
