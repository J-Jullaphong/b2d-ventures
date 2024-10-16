from decimal import Decimal

from django.db import models
from django.db.models import Sum

from .business import Business
from .investment import Investment

STATUS_CHOICES = [
    ('approve', 'Approve'),
    ('reject', 'Reject'),
    ('wait', 'Wait'),
]


class FundRaising(models.Model):
    """FundRaising Model represents a fundraising of a business, containing details information."""
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    publish_date = models.DateField()
    deadline_date = models.DateField()
    minimum_investment = models.DecimalField(max_digits=10, decimal_places=2)
    shares_percentage = models.DecimalField(max_digits=4, decimal_places=2)
    fundraising_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='wait',
    )

    class Meta:
        verbose_name = "Fundraising"
        verbose_name_plural = "Fundraisings"

    def get_current_investors(self):
        """Returns the number of investors who have approved investments."""
        investor_count = Investment.objects.filter(fundraise=self,
                                                   investment_status='approve').values(
            'investor').distinct().count()
        return investor_count

    def get_current_investment(self):
        """Calculate the total amount of investments received for this fundraise."""
        investment_total = Investment.objects.filter(fundraise=self,
                                                     investment_status='approve').aggregate(
            total=Sum('amount'))['total']
        return investment_total if investment_total is not None else Decimal(
            '0.00')

    def get_percentage_investment(self):
        """Calculate the percentage of the investment goal that has been reached."""
        current_investment = self.get_current_investment()
        if self.goal_amount > Decimal('0.00') and current_investment > Decimal(
                '0.00'):
            return (current_investment / self.goal_amount) * Decimal('100.00')
        return Decimal('0.00')

    def __str__(self):
        """Create a string representation of the FundRaising instance."""
        return (f"{self.business.name} - "
                f"{self.get_current_investment()}/{self.goal_amount}")
