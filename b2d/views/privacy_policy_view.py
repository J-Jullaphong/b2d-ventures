from django.views.generic import TemplateView


class PrivacyPolicyView(TemplateView):
    """View for rendering the privacy policy page."""
    template_name = 'b2d/privacy_policy.html'
