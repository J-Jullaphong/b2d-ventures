from django import forms
from django.forms import ModelForm
from django_recaptcha.fields import ReCaptchaField
from ..models import FundRaising

class FundRaisingForm(ModelForm):
    """Form for creating fundraising campaigns."""
    captcha = ReCaptchaField()

    class Meta:
        model = FundRaising
        fields = [
            'goal_amount', 'publish_date', 'deadline_date',
            'minimum_investment', 'share_type', 'shares'
        ]
        labels = {
            'goal_amount': 'Goal Amount',
            'publish_date': 'Publish Date',
            'deadline_date': 'Deadline Date',
            'minimum_investment': 'Minimum Investment',
            'share_type': 'Share Type',
            'shares': 'Number of Shares'
        }
        widgets = {
            'publish_date': forms.DateInput(format='%d-%m-%Y', attrs={'type': 'date'}),
            'deadline_date': forms.DateInput(format='%d-%m-%Y', attrs={'type': 'date'}),
            'share_type': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name != 'captcha':
                field.widget.attrs['class'] = 'form-control'

    def save(self, business, commit=True):
        """Saves the fundraising instance, linking it to the specified business."""
        fundraising = super().save(commit=False)
        fundraising.business = business

        if commit:
            fundraising.save()
        return fundraising
