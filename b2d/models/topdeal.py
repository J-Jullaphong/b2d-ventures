from django.db import models

from .fundraising import FundRaising


class TopDeal(models.Model):
    """TopDeal Model to represent a top deal linked to a fundraising campaign."""
    fundraising = models.ForeignKey(FundRaising, on_delete=models.CASCADE)
    display_order = models.PositiveIntegerField()

    def __str__(self):
        """Create a string representation of the top deal."""
        return f"Top Deal: {self.fundraising.business.name} (Order: {self.display_order})"
