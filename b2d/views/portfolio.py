import json

from django.db.models import Sum, F
from django.views.generic import TemplateView

from ..models import Investment


class PortfolioView(TemplateView):
    """View for displaying the user's investment portfolio."""
    template_name = 'b2d/portfolio.html'

    def get_context_data(self, **kwargs):
        """
        Provides context data to the portfolio template including total investment,
        business names, and percentages for each business in the portfolio.
        """
        context = super().get_context_data(**kwargs)

        # Aggregate investments by business and calculate total invested and shares percentage
        investments = (
            Investment.objects
            .filter(investor=self.request.user)
            .values('fundraise__business')
            .annotate(
                business_name=F('fundraise__business__name'),
                total_invested=Sum('amount'),
                total_shares=Sum('shares_percentage')
            )
        )

        # Calculate the total investment made by the user
        total_investment = sum(investment['total_invested'] for investment in investments)

        # Prepare labels and data for the investment chart
        labels = [investment['business_name'] for investment in investments]
        data = [
            (float(investment['total_invested']) / float(total_investment)) * 100
            for investment in investments
        ]

        context['investments'] = investments
        context['total_investment'] = total_investment
        context['investment_data'] = json.dumps({
            'labels': labels,
            'data': data,
        })

        return context
