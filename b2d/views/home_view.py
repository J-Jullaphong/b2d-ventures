from django.conf import settings
from django.db.models import Count, Q
from django.utils import timezone
from django.views.generic import ListView

from ..models import Business, TopDeal, Category


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

        # Fetch top 3 trending businesses for the carousel.
        two_weeks_ago = timezone.now() - timezone.timedelta(weeks=5)
        trending_fundraising = Business.objects.filter(
            fundraising__fundraising_status='approve',
            fundraising__publish_date__lte=timezone.now(),
            fundraising__deadline_date__gt=timezone.now()
        ).annotate(
            num_recent_investors=Count(
                'fundraising__investment',
                filter=Q(fundraising__investment__investment_datetime__gte=two_weeks_ago) &
                       Q(fundraising__investment__investment_status='approve')
            )
        ).order_by('-num_recent_investors')[:3]

        top_deal_fundraising_ids = TopDeal.objects.values_list('fundraising_id', flat=True)
        top_deal_fundraising = Business.objects.filter(
            fundraising__in=top_deal_fundraising_ids
        ).distinct()
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category', None)
        context['query'] = self.request.GET.get('q', '')
        context['carousel_businesses'] = trending_fundraising
        context['card_businesses'] = top_deal_fundraising
        context['settings'] = settings

        return context
