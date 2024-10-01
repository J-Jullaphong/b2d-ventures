from django.views.generic import ListView
from django.conf import settings
from django.utils import timezone
from django.db.models import Count, Q, Min
from ..models import Business, Category


class BusinessListView(ListView):
    model = Business
    template_name = 'b2d/search_page.html'
    context_object_name = 'businesses'
    paginate_by = 10

    def get_queryset(self):
        queryset = Business.objects.all()
        category_id = self.request.GET.get('category')
        sort_by = self.request.GET.get('sort', 'recent')
        query = self.request.GET.get('q', '')

        queryset = queryset.filter(fundraising__fundraising_status='approve')
        queryset = queryset.filter(
            fundraising__publish_date__lte=timezone.now(),
            fundraising__deadline_date__gt=timezone.now()
        )

        if category_id and category_id.isdigit():
            queryset = queryset.filter(category__id=int(category_id))

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )

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
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category', None)
        context['query'] = self.request.GET.get('q', '')
        context['settings'] = settings
        return context
