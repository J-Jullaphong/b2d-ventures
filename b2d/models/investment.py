from django.db import models

from .investor import Investor

STATUS_CHOICES = [
    ('approve', 'Approve'),
    ('reject', 'Reject'),
    ('wait', 'Wait'),
]


class Investment(models.Model):
    """Investment Model represents an investment of an investor, containing details information."""
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    fundraise = models.ForeignKey("b2d.FundRaising", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    shares_percentage = models.DecimalField(max_digits=4, decimal_places=2)
    investment_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='wait',
    )

    class Meta:
        verbose_name = "Investment"
        verbose_name_plural = "Investments"

    def __str__(self):
        return (f"{self.investor}: Investment of {self.amount} in "
                f"{self.fundraise.business.first_name}")
