import logging

from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.utils import timezone

from ..models import FundRaising, Investment, Business
from ..forms import FundRaisingForm

db_logger = logging.getLogger('db')


class FundRaisingDashboardView(View):
    """
    View for handling the fundraising dashboard, allowing businesses to manage their fundraising events.
    """
    template_name = 'b2d/fundraising_dashboard.html'

    def get(self, request, *args, **kwargs):
        """Handles GET requests for the fundraising dashboard."""
        try:
            business = Business.objects.get(id=request.user.id)
        except Business.DoesNotExist:
            messages.error(self.request, "Access restricted, fund raising dashboard page is for business owner only.")
            return redirect("b2d:home")

        active_fundraising = FundRaising.objects.filter(
            business=business,
            fundraising_status='approve'
        ).order_by('-publish_date').first()

        pending_fundraising = FundRaising.objects.filter(
            business=business,
            fundraising_status='wait'
        ).first()

        finished_fundraising = FundRaising.objects.filter(
            business=business,
            deadline_date__lt=timezone.now()
        ).order_by('-deadline_date')

        show_chart = False
        chart_labels = []
        chart_data = []
        investments = None

        if active_fundraising:
            show_chart = True
            investments = Investment.objects.filter(fundraise=active_fundraising)
            approved_investments = investments.filter(investment_status='approve')

            chart_labels = [inv.investment_datetime.strftime('%Y-%m-%d') for inv in approved_investments]
            investment_amounts = [float(inv.amount) for inv in approved_investments]

            cumulative_sum = 0
            for amount in investment_amounts:
                cumulative_sum += amount
                chart_data.append(cumulative_sum)

        if active_fundraising and (
                active_fundraising.deadline_date < timezone.now().date() or
                active_fundraising.get_current_investment() >= active_fundraising.goal_amount):
            active_fundraising = None

        form = FundRaisingForm()

        context = {
            'active_fundraising': active_fundraising,
            'pending_fundraising': pending_fundraising,
            'finished_fundraising': finished_fundraising,
            'show_chart': show_chart,
            'chart_labels': chart_labels,
            'chart_data': chart_data,
            'form': form,
            'investments': investments if show_chart else None,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Handles POST requests for creating a new fundraising event."""
        business = request.user.business

        investment_id = request.POST.get('investment_id')
        new_status = request.POST.get('investment_status')

        if investment_id and new_status:
            try:
                investment = Investment.objects.get(id=investment_id,
                                                    fundraise__business=business)
            except Investment.DoesNotExist:
                messages.error(request, "Invalid investment record.")
                return redirect('b2d:fundraising')

            investment.investment_status = new_status
            investment.save()
            db_logger.info(
                f"Business {business.id} updated investment status for {investment.id} to '{new_status}'")
            messages.success(request,
                             "Investment status has been successfully updated.")
            return redirect('b2d:fundraising')

        form = FundRaisingForm(request.POST)

        if form.is_valid():
            new_fundraising = form.save(commit=False, business=business)
            new_fundraising.business = business
            new_fundraising.save()
            db_logger.info(f"Business {business.id} successful create new fundraising {new_fundraising.id}")
            messages.success(request,
                             'Your fundraising campaign has been created and is awaiting approval.')
            return redirect('b2d:fundraising')

        return render(request, self.template_name,
                      {'form': form, 'show_form': True})
