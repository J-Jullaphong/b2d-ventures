from django.conf import settings
from django.db.models import Count, Q, Min
from django.utils import timezone
from django.views.generic import ListView

from ..models import Business, Category


class BusinessListView(ListView):
    """View for displaying a list of businesses with various filtering, searching, and sorting options."""
    model = Business
    template_name = 'b2d/search_page.html'
    context_object_name = 'businesses'
    paginate_by = 10

    def get_queryset(self):
        """Returns the filtered and sorted queryset of businesses."""
        queryset = Business.objects.all()
        category_id = self.request.GET.get('category')
        sort_by = self.request.GET.get('sort', 'alphabetical')
        query = self.request.GET.get('q', '')

        # Filter by approved and active fundraising campaigns
        queryset = queryset.filter(
            fundraising__fundraising_status='approve',
            fundraising__publish_date__lte=timezone.now(),
            fundraising__deadline_date__gt=timezone.now()
        )

        # Filter by category if provided
        if category_id and category_id.isdigit():
            queryset = queryset.filter(category__id=int(category_id))

        # Filter by search query business name or description
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))

        # Apply sorting based on the selected option
        if sort_by == 'recent':
            queryset = queryset.order_by('-id')
        elif sort_by == 'investors':
            queryset = queryset.annotate(num_investors=Count('fundraising__investment')).order_by('-num_investors')
        elif sort_by == 'alphabetical':
            queryset = queryset.order_by('name')
        elif sort_by == 'min_invest':
            queryset = queryset.annotate(min_invest=Min('fundraising__minimum_investment')).order_by('min_invest')
        return queryset

    def get_context_data(self, **kwargs):
        """
        Provides context data to the search template including the available categories,
        the current category selected by the user, and the search query entered.
        """
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category', None)
        context['query'] = self.request.GET.get('q', '')
        context['settings'] = settings
        return context
