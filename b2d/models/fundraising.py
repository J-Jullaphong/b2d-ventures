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

    def get_current_investment(self):
        """Calculate the total amount of investments received for this fundraise."""
        investment_total = Investment.objects.filter(fundraise=self).aggregate(total=Sum('amount'))['total']
        return investment_total if investment_total is not None else 0

    def get_percentage_investment(self):
        """Calculate the percentage of the investment goal that has been reached."""
        current_investment = self.get_current_investment()
        if self.goal_amount > 0 and current_investment > 0:
            return (current_investment / self.goal_amount) * 100
        return 0

    def __str__(self):
        """Create a string representation of the FundRaising instance."""
        return (f"{self.business.first_name} - "
                f"{self.get_current_investment()}/{self.goal_amount}")
