from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django_otp.plugins.otp_email.models import EmailDevice
from ..models import Investor


class InvestorProfileForm(forms.ModelForm):
    """Form for updating investor profile information, including password change and email OTP device update."""

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
        fields = ['first_name', 'last_name', 'email', 'phone_number',
                  'financial_statements']
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

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['phone_number'].required = True

    def clean(self):
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

        return cleaned_data

    def save(self, commit=True):
        investor = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password1')
        new_email = self.cleaned_data.get('email')

        investor.username = new_email

        try:
            email_device = EmailDevice.objects.get(user=self.instance)
            email_device.email = new_email
            email_device.save()
        except EmailDevice.DoesNotExist:
            pass

        if new_password:
            investor.set_password(new_password)

        if commit:
            investor.save()

        return investor
