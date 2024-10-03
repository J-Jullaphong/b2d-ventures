from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.utils import timezone
from ..models import FundRaising, Investment, Business
from ..forms import FundRaisingForm


class FundRaisingDashboardView(View):
    template_name = 'b2d/fundraising_dashboard.html'

    def get(self, request, *args, **kwargs):
        try:
            business = Business.objects.get(id=request.user.id)
        except Business.DoesNotExist:
            return redirect("b2d:home")

        active_fundraising = FundRaising.objects.filter(
            business=business,
            fundraising_status='approve'
        ).first()

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

            chart_labels = [inv.investment_datetime.strftime('%Y-%m-%d') for inv in investments]
            investment_amounts = [float(inv.amount) for inv in investments]

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
            'investments': investments if show_chart else None
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        business = request.user.business
        form = FundRaisingForm(request.POST)

        if form.is_valid():
            new_fundraising = form.save(commit=False, business=business)
            new_fundraising.business = business
            new_fundraising.save()
            messages.success(request,
                             'Your fundraising event has been created and is awaiting approval.')
            return redirect('b2d:fundraising')

        return render(request, self.template_name,
                      {'form': form, 'show_form': True})
