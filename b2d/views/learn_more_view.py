from django.views.generic import TemplateView


class LearnMoreView(TemplateView):
    """View for displaying the learn more page."""
    template_name = 'b2d/learn_more.html'
