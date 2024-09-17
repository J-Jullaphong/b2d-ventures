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
    publish_date = models.DateField(auto_now_add=True)
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

    def __str__(self):
        return (f"{self.business.first_name} - "
                f"{self.get_current_investment()}/{self.goal_amount}")

    def get_current_investment(self):
        return Investment.objects.filter(fundraise=self).aggregate(
            total=Sum('amount'))['total'] or 0

    def get_percentage_investment(self):
        return (Investment.objects.filter(fundraise=self).aggregate(
            total=Sum('amount'))['total'] / self.goal_amount) * 100
