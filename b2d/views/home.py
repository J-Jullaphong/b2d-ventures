from django.views.generic import ListView
from django.conf import settings
from django.db.models import Count
from ..models import Business


class HomeView(ListView):
    model = Business
    template_name = 'b2d/home.html'
    context_object_name = 'businesses'
    paginate_by = 3

    def get_queryset(self):
        queryset = Business.objects.annotate(num_investors=Count('fundraising__investment')).order_by('-num_investors')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = settings
        return context
