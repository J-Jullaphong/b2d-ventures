from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.edit import FormView
from ..models import FundRaising, Investor
from ..forms import InvestmentForm


class InvestmentView(FormView):
    template_name = 'b2d/transaction.html'
    form_class = InvestmentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fundraise'] = get_object_or_404(FundRaising, id=self.kwargs['fundraise_id'])
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        fundraise = get_object_or_404(FundRaising, id=self.kwargs['fundraise_id'])
        kwargs['fundraise'] = fundraise
        return kwargs

    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your submission.")
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        investor = Investor.objects.get(id=self.request.user.id)
        fundraise = get_object_or_404(FundRaising, id=self.kwargs['fundraise_id'])
        form.save(investor=investor, fundraise=fundraise)
        return redirect(reverse('b2d:business_detail', kwargs={'pk': fundraise.business_id}))
