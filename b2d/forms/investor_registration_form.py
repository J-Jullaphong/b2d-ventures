from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django_recaptcha.fields import ReCaptchaField
from django_otp.plugins.otp_email.models import EmailDevice
from django.core.exceptions import ValidationError
from django.utils.html import escape

from ..models import Investor, UserConsent


class InvestorRegistrationForm(UserCreationForm):
    """Form for registering new investors with enhanced validation."""
    usable_password = None
    captcha = ReCaptchaField()

    class Meta:
        model = Investor
        fields = ['first_name', 'last_name', 'email', 'phone_number',
                  'password1', 'password2']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'phone_number': 'Phone Number',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].required = True
            self.fields[field_name].help_text = None
            if self.fields[field_name] != self.fields['captcha']:
                self.fields[field_name].widget.attrs["class"] = "form-control"

        self.fields['password1'].widget.attrs["placeholder"] = "Password"
        self.fields['password2'].widget.attrs["placeholder"] = "Confirm Password"
        self.fields['password2'].label = "Confirm Password"

    def clean_first_name(self):
        """Validate and escape first name."""
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise ValidationError("First name must contain only letters.")
        return escape(first_name)

    def clean_last_name(self):
        """Validate and escape last name."""
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise ValidationError("Last name must contain only letters.")
        return escape(last_name)

    def clean_email(self):
        """Validate email format, uniqueness, and escape."""
        email = self.cleaned_data.get('email')
        if Investor.objects.filter(email=email).exists():
            raise ValidationError("An investor with this email already exists.")
        return escape(email)

    def clean_phone_number(self):
        """Validate and escape phone number."""
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        if len(phone_number) < 10 or len(phone_number) > 15:
            raise ValidationError("Phone number must be between 10 and 15 digits.")
        return escape(phone_number)

    def clean(self):
        """Clean all fields and apply escaping."""
        cleaned_data = super().clean()
        for field_name, value in cleaned_data.items():
            if value:
                cleaned_data[field_name] = escape(value)
        return cleaned_data

    def save(self, commit=True):
        """Saves the investor instance with inactive status until approved."""
        user = super().save(commit=False)
        if commit:
            user.is_active = False
            user.username = user.email
            user.save()

            # Add the user to the Investor group
            try:
                investor_group = Group.objects.get(name="Investor")
                investor_group.user_set.add(user)
            except Group.DoesNotExist:
                raise ValidationError("The 'Investor' group does not exist. Please configure it.")

            # Create related objects
            EmailDevice.objects.create(user=user, email=user.email, name="Email")
            UserConsent.objects.create(user=user, consent=True)

        return user
