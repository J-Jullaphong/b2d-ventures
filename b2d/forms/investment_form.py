from django import forms
from django.forms import ModelForm

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
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs["class"] = "form-control"

    def save(self, investor, fundraise, commit=True):
        investment = super().save(commit=False)
        investment.investor = investor
        investment.fundraise = fundraise
        investment.shares_percentage = (investment.amount / fundraise.goal_amount) * fundraise.shares_percentage
        if commit:
            investment.save()
        return investment
