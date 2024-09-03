from django.db import models

from .business import Business
from .investment import Investment


class FundRaising(models.Model):
    """FundRaising Model represents a fundraising of a business, containing details information."""
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    publish_date = models.DateField(auto_now_add=True)
    deadline_date = models.DateField()
    minimum_investment = models.DecimalField(max_digits=10, decimal_places=2)
    shares_percentage = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return (f"{self.business.first_name} - "
                f"{self.get_current_investment()}/{self.goal_amount}")

    def get_current_investment(self):
        return Investment.objects.filter(fundraise__pk=self.pk).sum("amount")
