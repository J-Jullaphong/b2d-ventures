from django.views.generic import ListView
from django.conf import settings
from django.utils import timezone
from django.db.models import Count
from ..models import Business


class HomeView(ListView):
    model = Business
    template_name = 'b2d/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        carousel_businesses = Business.objects.filter(
            fundraising__fundraising_status='approve',
            fundraising__publish_date__lte=timezone.now(),
            fundraising__deadline_date__gt=timezone.now()
        ).order_by('fundraising__publish_date')[:3]

        card_businesses = Business.objects.annotate(
            num_investors=Count('fundraising__investment')
        ).order_by('-num_investors')[:3]

        context['carousel_businesses'] = carousel_businesses
        context['card_businesses'] = card_businesses
        context['settings'] = settings
        return context
