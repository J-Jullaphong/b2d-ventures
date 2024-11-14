from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_recaptcha.fields import ReCaptchaField
from django_otp.plugins.otp_email.models import EmailDevice

from ..models import Investor, UserConsent


class InvestorRegistrationForm(UserCreationForm):
    """Form for registering new investors."""
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
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Last name'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Phone number'
            })
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
        """Saves the investor instance with inactive status until approved."""
        user = super().save(commit=False)
        if commit:
            user.is_active = False
            user.username = user.email
            user.save()
            EmailDevice.objects.create(user=user, email=user.email,
                                       name="Email")
            UserConsent.objects.create(user=user, consent=True)
        return user
