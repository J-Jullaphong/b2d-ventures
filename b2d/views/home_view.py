from django.conf import settings
from django.db.models import Count
from django.utils import timezone
from django.views.generic import ListView

from ..models import Business


class HomeView(ListView):
    """View for displaying the home page with a list of businesses."""
    model = Business
    template_name = 'b2d/home.html'

    def get_context_data(self, **kwargs):
        """
        Provides context data to the home page template, including businesses for the carousel
        and card sections. The businesses are filtered by their fundraising campaign status
        and date to ensure only active campaigns are shown.
        """
        context = super().get_context_data(**kwargs)

        # Fetch top 3 recent businesses for the carousel.
        carousel_businesses = Business.objects.filter(
            fundraising__fundraising_status='approve',
            fundraising__publish_date__lte=timezone.now(),
            fundraising__deadline_date__gt=timezone.now()
        ).order_by('fundraising__publish_date')[:3]

        # Fetch top 6 most investor businesses for cards.
        card_businesses = Business.objects.filter(
            fundraising__fundraising_status='approve',
            fundraising__publish_date__lte=timezone.now(),
            fundraising__deadline_date__gt=timezone.now()
        ).annotate(
            num_investors=Count('fundraising__investment')
        ).order_by('-num_investors')[:6]

        context['carousel_businesses'] = carousel_businesses
        context['card_businesses'] = card_businesses
        context['settings'] = settings

        return context
