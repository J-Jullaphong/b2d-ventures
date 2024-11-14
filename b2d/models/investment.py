import uuid

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
    """Investment Model represents an investment of an investor, containing detailed information."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    fundraise = models.ForeignKey("b2d.FundRaising", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_slip = models.FileField(upload_to=transaction_slip_upload_path, null=True, max_length=1024)
    investment_datetime = models.DateTimeField(default=timezone.now)
    investment_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='wait',
    )

    class Meta:
        verbose_name = "Investment Request"
        verbose_name_plural = "Investment Requests"

    def __str__(self):
        return (f"{self.investor}: Investment of {self.amount} in "
                f"{self.fundraise.business.name} ({self.get_shares()} shares)")

    def get_shares(self):
        """Calculate the number of shares based on the investment amount and the price per share."""
        price_per_share = self.fundraise.get_price_per_share()
        if price_per_share > 0:
            return int(self.amount / price_per_share)
        return 0
