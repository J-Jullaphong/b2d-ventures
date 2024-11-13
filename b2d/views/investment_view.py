import logging
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic.edit import FormView

from ..models import FundRaising, Investor
from ..forms import InvestmentForm

db_logger = logging.getLogger('db')


class InvestmentView(FormView):
    """View to handle the investment process for a fundraising campaign."""
    template_name = 'b2d/transaction.html'
    form_class = InvestmentForm

    def get_form_kwargs(self):
        """Passes additional keyword arguments to the form, including the current fundraising campaign."""
        kwargs = super().get_form_kwargs()
        fundraise = get_object_or_404(FundRaising, id=self.kwargs['fundraise_id'])
        kwargs['fundraise'] = fundraise
        return kwargs

    def get(self, request, *args, **kwargs):
        """Handles the GET request and provides context data to the investment template."""
        try:
            investor = Investor.objects.get(id=request.user.id)
        except Investor.DoesNotExist:
            messages.error(self.request, "Access restricted, investment page is for investor only.")
            return redirect("b2d:home")

        try:
            fundraise = FundRaising.objects.get(id=self.kwargs['fundraise_id'])
        except FundRaising.DoesNotExist:
            return render(request, "b2d/404.html", status=404)

        form = self.get_form(self.form_class)
        context = {
            'fundraise': fundraise,
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Handles the POST request when the form is submitted."""
        investor = get_object_or_404(Investor, id=self.request.user.id)
        fundraise = get_object_or_404(FundRaising, id=self.kwargs['fundraise_id'])
        form = self.get_form(self.form_class)
        context = {
            'fundraise': fundraise,
            'form': form
        }

        if form.is_valid():
            investment = form.save(investor=investor, fundraise=fundraise)
            db_logger.info(f"Investor {investor.id} invest in fundraising {fundraise.id} for {investment.amount}$.")
            messages.success(self.request, "Your investment has been submitted and is pending admin approval.")
            return redirect(reverse('b2d:business_detail', kwargs={'pk': fundraise.business_id}))

        messages.error(self.request, "There was an error processing your investment.")
        return render(self.request, self.template_name, context)
