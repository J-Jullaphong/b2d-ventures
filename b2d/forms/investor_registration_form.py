from django import forms
from django.contrib.auth.forms import UserCreationForm
from ..models import Investor


class InvestorRegistrationForm(UserCreationForm):
    usable_password = None

    class Meta:
        model = Investor
        fields = ['first_name', 'last_name', 'email', 'phone_number',
                  'password1', 'password2',  'financial_statements']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'financial_statements': 'Financial Statements',
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
            }),
            'financial_statements': forms.ClearableFileInput(attrs={
                'accept': 'application/pdf',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].help_text = None
            self.fields[field_name].widget.attrs["class"] = "form-control"

        self.fields['password1'].widget.attrs["placeholder"] = "Password"
        self.fields['password2'].widget.attrs["placeholder"] = "Confirm Password"
        self.fields['password2'].label = "Confirm Password"

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.is_active = False
            user.username = user.email
            user.save()
        return user
