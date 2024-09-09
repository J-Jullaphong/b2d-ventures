from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from ..models import Business, FundRaising

class BusinessDetailView(DetailView):
    model = Business
    template_name = 'b2d/business_detail.html'
    context_object_name = 'business'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get related fundraising details
        fundraisings = FundRaising.objects.filter(business=self.object)
        context['fundraisings'] = fundraisings
        return context
