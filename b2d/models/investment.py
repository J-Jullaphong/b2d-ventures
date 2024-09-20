from django.db import models
from django.utils import timezone

from .investor import Investor

STATUS_CHOICES = [
    ('approve', 'Approve'),
    ('reject', 'Reject'),
    ('wait', 'Wait'),
]


def transaction_slip_upload_path(instance, filename):
    """Generate file path for new transaction slip."""
    return f"investment_slips/{instance.fundraise.id}/{instance.investor.id}/{filename}"


class Investment(models.Model):
    """Investment Model represents an investment of an investor, containing details information."""
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    fundraise = models.ForeignKey("b2d.FundRaising", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    shares_percentage = models.DecimalField(max_digits=4, decimal_places=2)
    transaction_slip = models.FileField(upload_to=transaction_slip_upload_path, null=True)
    investment_datetime = models.DateTimeField(default=timezone.now)
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
