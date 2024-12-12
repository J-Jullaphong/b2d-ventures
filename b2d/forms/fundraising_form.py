from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.html import escape
from django_recaptcha.fields import ReCaptchaField
from ..models import FundRaising


class FundRaisingForm(ModelForm):
    """Form for creating fundraising campaigns with enhanced validation."""
    captcha = ReCaptchaField()

    class Meta:
        model = FundRaising
        fields = [
            'goal_amount', 'publish_date', 'deadline_date',
            'minimum_shares', 'share_type', 'shares'
        ]
        labels = {
            'goal_amount': 'Goal Amount ($)',
            'publish_date': 'Publish Date',
            'deadline_date': 'Deadline Date',
            'minimum_shares': 'Minimum Shares',
            'share_type': 'Share Type',
            'shares': 'Number of Shares'
        }
        widgets = {
            'goal_amount': forms.NumberInput(attrs={'min': 0, 'placeholder': 'Goal Amount ($)'}),
            'minimum_shares': forms.NumberInput(attrs={'min': 1, 'placeholder': 'Minimum Shares'}),
            'shares': forms.NumberInput(attrs={'min': 0, 'placeholder': 'Shares'}),
            'publish_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'deadline_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'share_type': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name != 'captcha':
                field.widget.attrs['class'] = 'form-control'

    def clean_goal_amount(self):
        """Validate and sanitize goal amount."""
        goal_amount = self.cleaned_data.get('goal_amount')
        if goal_amount < 0:
            raise ValidationError("Goal amount cannot be negative.")
        return escape(goal_amount)

    def clean_minimum_shares(self):
        """Validate and sanitize minimum shares."""
        minimum_shares = self.cleaned_data.get('minimum_shares')
        if minimum_shares < 1:
            raise ValidationError("Minimum shares must be at least 1.")
        return escape(minimum_shares)

    def clean_shares(self):
        """Validate and sanitize number of shares."""
        shares = self.cleaned_data.get('shares')
        if shares < 0:
            raise ValidationError("Number of shares cannot be negative.")
        return escape(shares)

    def clean(self):
        """Cross-field validation for dates."""
        cleaned_data = super().clean()
        publish_date = cleaned_data.get('publish_date')
        deadline_date = cleaned_data.get('deadline_date')

        if publish_date and deadline_date and publish_date > deadline_date:
            raise ValidationError("Publish date cannot be after the deadline date.")

        # Escape all inputs to ensure safety
        for field_name, value in cleaned_data.items():
            if value and isinstance(value, str):
                cleaned_data[field_name] = escape(value)

        return cleaned_data

    def save(self, business, commit=True):
        """Saves the fundraising instance, linking it to the specified business."""
        fundraising = super().save(commit=False)
        fundraising.business = business

        if commit:
            fundraising.save()
        return fundraising
