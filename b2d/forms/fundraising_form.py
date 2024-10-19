from django import forms
from django.forms import ModelForm
from django_recaptcha.fields import ReCaptchaField

from ..models import FundRaising


class FundRaisingForm(ModelForm):
    """Form for creating fundraising campaigns."""
    captcha = ReCaptchaField()

    class Meta:
        model = FundRaising
        fields = ['goal_amount', 'publish_date', 'deadline_date',
                  'minimum_investment', 'shares_percentage']
        labels = {
            'goal_amount': 'Goal Amount',
            'publish_date': 'Publish Date',
            'deadline_date': 'Deadline Date',
            'minimum_investment': 'Minimum Investment',
            'shares_percentage': 'Shares Percentage'
        }
        widgets = {
            'publish_date': forms.DateInput(format=('%d-%m-%Y'),
                                            attrs={'type': 'date'}),
            'deadline_date': forms.DateInput(format=('%d-%m-%Y'),
                                             attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            if self.fields[field_name] != self.fields['captcha']:
                self.fields[field_name].widget.attrs["class"] = "form-control"

    def save(self, business, commit=True):
        """Saves the fundraising instance, linking it to the specified business."""
        fundraising = super().save(commit=False)
        fundraising.business = business
        if commit:
            fundraising.save()
        return fundraising
