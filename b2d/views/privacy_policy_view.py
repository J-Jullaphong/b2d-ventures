# views.py
from django.views.generic import TemplateView


class PrivacyPolicyView(TemplateView):
    template_name = 'b2d/privacy_policy.html'
