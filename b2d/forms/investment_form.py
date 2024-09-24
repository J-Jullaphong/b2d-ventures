from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from ..models import Investment


class InvestmentForm(ModelForm):
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
                    'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        self.fundraise = kwargs.pop('fundraise', None)
        print(self.fundraise)
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs["class"] = "form-control"

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        current_investment = self.fundraise.get_current_investment()
        remaining_amount = self.fundraise.goal_amount - current_investment

        if amount > remaining_amount:
            raise ValidationError(
                f"The amount exceeds the remaining fundraising goal. You can only invest up to ${remaining_amount:.2f}.")
        return amount

    def save(self, investor, fundraise, commit=True):
        investment = super().save(commit=False)
        investment.investor = investor
        investment.fundraise = fundraise
        investment.shares_percentage = (investment.amount / fundraise.goal_amount) * fundraise.shares_percentage
        if commit:
            investment.save()
        return investment