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
        fields = ['amount', 'investment_datetime', 'transaction_slip']
        labels = {
            'amount': 'Investment Amount',
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

    def clean_amount(self):
        """Validates the investment amount against the fundraising limits."""
        amount = self.cleaned_data.get('amount')
        current_investment = self.fundraise.get_current_investment()
        remaining_amount = self.fundraise.goal_amount - current_investment

        if amount < self.fundraise.minimum_investment:
            raise ValidationError(
                f"The investment amount is too low. Minimum investment is ${self.fundraise.minimum_investment:.2f}."
            )

        if amount > remaining_amount:
            raise ValidationError(
                f"The amount exceeds the remaining fundraising goal. You can only invest up to ${remaining_amount:.2f}."
            )

        return amount

    def save(self, investor, fundraise, commit=True):
        """Saves the investment instance linked to the investor and fundraising campaign."""
        investment = super().save(commit=False)
        investment.investor = investor
        investment.fundraise = fundraise

        price_per_share = fundraise.get_price_per_share()
        investment.shares = int(investment.amount / price_per_share)

        if commit:
            investment.save()
        return investment
