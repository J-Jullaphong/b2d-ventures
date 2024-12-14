from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django_recaptcha.fields import ReCaptchaField
from django.utils.html import escape
from django.utils.timezone import now

from ..models import Investment


class InvestmentForm(ModelForm):
    """Form for creating investments with enhanced validation and input escaping."""
    captcha = ReCaptchaField()

    class Meta:
        model = Investment
        fields = ['shares', 'investment_datetime', 'transaction_slip']
        labels = {
            'shares': 'Number of Shares',
            'investment_datetime': 'Investment Date/Time',
            'transaction_slip': 'Transaction Slip'
        }
        widgets = {
            'investment_datetime': forms.DateTimeInput(
                format=('%Y-%m-%dT%H:%M'),
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                }),
            'transaction_slip': forms.ClearableFileInput(attrs={
                'accept': 'image/*,application/pdf',
                'class': 'form-control-file',
            }),
        }

    def __init__(self, *args, **kwargs):
        self.fundraise = kwargs.pop('fundraise', None)
        super().__init__(*args, **kwargs)

        # Add Bootstrap styling
        for field_name, field in self.fields.items():
            if field_name != 'captcha':
                field.widget.attrs["class"] = "form-control"

        # Ensure that fundraise context is provided
        if not self.fundraise:
            raise ValueError(
                "The 'fundraise' argument is required for InvestmentForm."
            )

    def clean_shares(self):
        """Validate the number of shares and escape the input."""
        shares = self.cleaned_data.get('shares')

        if shares is None:
            raise ValidationError("The number of shares is required.")

        if shares < self.fundraise.minimum_shares:
            raise ValidationError(
                f"The number of shares must be at least {self.fundraise.minimum_shares}."
            )

        current_investment = self.fundraise.get_current_investment()
        remaining_amount = self.fundraise.goal_amount - current_investment
        price_per_share = self.fundraise.get_price_per_share()
        max_shares = int(remaining_amount / price_per_share)

        if shares > max_shares:
            raise ValidationError(
                f"The number of shares exceeds the maximum available. You can invest up to {max_shares} shares."
            )

        # Calculate and store the investment amount
        self.cleaned_data['amount'] = shares * price_per_share
        return escape(shares)

    def clean_investment_datetime(self):
        """Ensure the investment date/time is valid and escape the input."""
        investment_datetime = self.cleaned_data.get('investment_datetime')

        if investment_datetime is None:
            raise ValidationError("The investment date/time is required.")

        if investment_datetime < now():
            raise ValidationError("The investment date/time cannot be in the past.")

        return escape(investment_datetime)

    def clean(self):
        """Escape all inputs and validate cross-field dependencies."""
        cleaned_data = super().clean()

        for field_name, value in cleaned_data.items():
            if value and isinstance(value, str):  # Escape only string inputs
                cleaned_data[field_name] = escape(value)

        return cleaned_data

    def save(self, investor, commit=True):
        """Save the investment instance linked to the investor and fundraising campaign."""
        investment = super().save(commit=False)
        investment.investor = investor
        investment.fundraise = self.fundraise

        # Ensure the calculated amount is saved
        investment.amount = self.cleaned_data.get('amount', 0)

        if commit:
            investment.save()
        return investment
