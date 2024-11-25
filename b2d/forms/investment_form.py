from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django_recaptcha.fields import ReCaptchaField

from ..models import Investment


class InvestmentForm(ModelForm):
    """Form for creating investments."""
    captcha = ReCaptchaField()

    class Meta:
        model = Investment
        fields = ['shares', 'investment_datetime', 'transaction_slip']
        labels = {
            'shares': 'Number Of Shares',
            'investment_datetime': 'Investment Date/Time',
            'transaction_slip': 'Transaction Slip'
        }

        widgets = {
            'investment_datetime': forms.DateTimeInput(
                format=('%d-%m-%Y %H:%M'),
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                }),
        }

    def __init__(self, *args, **kwargs):
        self.fundraise = kwargs.pop('fundraise', None)
        super().__init__(*args, **kwargs)

        # Add Bootstrap styling
        for field_name, field in self.fields.items():
            if field != self.fields['captcha']:
                field.widget.attrs["class"] = "form-control"

        # Validate that fundraise context is provided
        if not self.fundraise:
            raise ValueError(
                "The 'fundraise' argument is required for InvestmentForm.")

    def clean_shares(self):
        """Validates the number of shares against the fundraising limits."""
        shares = self.cleaned_data.get('shares')

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
                f"The number of shares exceeds the maximum available. You can only invest up to {max_shares} shares."
            )

        self.cleaned_data['amount'] = shares * price_per_share
        return shares

    def save(self, investor, fundraise, commit=True):
        """Saves the investment instance linked to the investor and fundraising campaign."""
        investment = super().save(commit=False)
        investment.investor = investor
        investment.fundraise = fundraise

        # Ensure the calculated amount is saved
        investment.amount = self.cleaned_data['amount']

        if commit:
            investment.save()
        return investment


