from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django_otp.plugins.otp_email.models import EmailDevice
from django.utils.html import escape

from ..models import Investor


class InvestorProfileForm(forms.ModelForm):
    """Form for updating investor profile information with enhanced validation and input escaping."""

    current_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Current Password',
            'class': 'form-control'
        }),
        required=False
    )

    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'New Password',
            'class': 'form-control'
        }),
        required=False,
        validators=[validate_password]
    )

    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm New Password',
            'class': 'form-control'
        }),
        required=False,
        validators=[validate_password]
    )

    class Meta:
        model = Investor
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'financial_statements']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'phone_number': 'Phone Number',
            'financial_statements': 'Financial Statements',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'financial_statements': forms.ClearableFileInput(attrs={'accept': 'application/pdf'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].help_text = None
            self.fields[field_name].widget.attrs["class"] = "form-control"

        # Required fields
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['phone_number'].required = True

    def clean_email(self):
        """Validate and escape the email address."""
        email = self.cleaned_data.get('email')
        if Investor.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This email is already in use.")
        return escape(email)

    def clean_phone_number(self):
        """Validate and escape the phone number."""
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        if len(phone_number) < 10 or len(phone_number) > 15:
            raise ValidationError("Phone number must be between 10 and 15 digits.")
        return escape(phone_number)

    def clean(self):
        """Perform cross-field validation and escape all string inputs."""
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if current_password:
            user = authenticate(username=self.instance.email, password=current_password)
            if not user:
                raise ValidationError("The current password is incorrect.")

        if new_password1 or new_password2:
            if new_password1 != new_password2:
                raise ValidationError("The new passwords do not match.")

        # Escape all string inputs
        for field_name, value in cleaned_data.items():
            if isinstance(value, str):
                cleaned_data[field_name] = escape(value)

        return cleaned_data

    def save(self, commit=True):
        """Save the investor profile with updated password and email device."""
        investor = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password1')
        new_email = self.cleaned_data.get('email')

        investor.username = new_email

        # Update email device if it exists
        try:
            email_device = EmailDevice.objects.get(user=self.instance)
            email_device.email = new_email
            email_device.save()
        except EmailDevice.DoesNotExist:
            pass

        # Set new password if provided
        if new_password:
            investor.set_password(new_password)

        if commit:
            investor.save()

        return investor
