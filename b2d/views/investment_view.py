from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic.edit import FormView

from ..models import FundRaising, Investor
from ..forms import InvestmentForm


class InvestmentView(FormView):
    """View to handle the investment process for a fundraising campaign."""
    template_name = 'b2d/transaction.html'
    form_class = InvestmentForm

    def get(self, request, *args, **kwargs):
        """Provides context data to the investment template including the current fundraising campaign."""
        try:
            investor = Investor.objects.get(id=request.user.id)
        except Investor.DoesNotExist:
            return redirect("b2d:home")

        context = {
            'fundraise': get_object_or_404(FundRaising, id=self.kwargs['fundraise_id'])
        }
        return render(request, self.template_name, context)

    def get_form_kwargs(self):
        """Passes additional keyword arguments to the form including the current fundraising campaign."""
        kwargs = super().get_form_kwargs()
        fundraise = get_object_or_404(FundRaising, id=self.kwargs['fundraise_id'])
        kwargs['fundraise'] = fundraise
        return kwargs

    def form_invalid(self, form):
        """Handles form validation failure by displaying an error message and re-rendering the form."""
        messages.error(self.request, "There was an error with your submission.")
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        """Handles form validation success by saving the investment and redirecting to the business detail page."""
        investor = Investor.objects.get(id=self.request.user.id)
        fundraise = get_object_or_404(FundRaising, id=self.kwargs['fundraise_id'])
        form.save(investor=investor, fundraise=fundraise)
        messages.success(self.request, "Your investment has been submitted and is pending admin approval.")
        return redirect(reverse('b2d:business_detail', kwargs={'pk': fundraise.business_id}))
