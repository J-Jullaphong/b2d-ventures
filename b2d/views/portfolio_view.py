import json

from django.db.models import Sum, F
from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import render, redirect

from ..models import Investment, Investor


class PortfolioView(TemplateView):
    """View for displaying the user's investment portfolio."""
    template_name = 'b2d/portfolio.html'

    def get(self, request):
        """
        Provides context data to the portfolio template including total investment,
        business names, and percentages for each business in the portfolio.
        """
        try:
            investor = Investor.objects.get(id=request.user.id)
        except Investor.DoesNotExist:
            messages.error(self.request, "Access restricted, portfolio page is for investor only.")
            return redirect("b2d:home")

        # Aggregate investments by business and calculate total invested and shares percentage
        investments = (
            Investment.objects
            .filter(investor=self.request.user)
            .values('fundraise__business', 'fundraise__share_type')
            .annotate(
                business_name=F('fundraise__business__name'),
                share_type=F('fundraise__share_type'),
                total_invested=Sum('amount'),
                total_shares=Sum('shares')
            )
            .order_by('fundraise__business')
        )

        # Calculate the total investment made by the user
        total_investment = sum(investment['total_invested'] for investment in investments)

        # Prepare labels and data for the investment chart
        labels = [investment['business_name'] for investment in investments]
        data = [
            (float(investment['total_invested']) / float(total_investment)) * 100
            for investment in investments
        ]

        context = {
            'investments': investments,
            'total_investment': total_investment,
            'investment_data': json.dumps({
                'labels': labels,
                'data': data,
            })
        }

        return render(request, self.template_name, context)
