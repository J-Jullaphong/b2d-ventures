import json
from django.views.generic import TemplateView
from django.db.models import Sum, F
from ..models import Investment


class PortfolioView(TemplateView):
    template_name = 'b2d/portfolio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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

        total_investment = sum(investment['total_invested'] for investment in investments)

        labels = [investment['business_name'] for investment in investments]
        data = [
            (float(investment['total_invested']) / float(total_investment)) * 100
            for investment in investments
        ]

        print(investments)

        context['investments'] = investments
        context['total_investment'] = total_investment
        context['investment_data'] = json.dumps({
            'labels': labels,
            'data': data,
        })

        return context
