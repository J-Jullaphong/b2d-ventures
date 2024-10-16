from django.contrib import admin

from ..models import Investment


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    """
        Customizes the admin interface for the Investment model, enabling the
        management and approval of investments made by investors in fundraising events.
    """
    list_display = ('investor', 'fundraise', 'amount', 'shares_percentage',
                    'investment_status', 'investment_datetime')
    actions = ['approve_investments']
    fieldsets = (
        (None, {
            'fields': ('investor', 'fundraise', 'amount', 'shares_percentage',
                       'transaction_slip', 'investment_status',
                       'investment_datetime')
        }),
    )

    def approve_investments(self, request, queryset):
        """Custom action to approve selected investments."""
        for investment in queryset:
            if investment.investment_status != 'approve':
                investment.investment_status = 'approve'
                investment.save()

                self.message_user(request,
                                  f"Investment by {investment.investor} approved successfully.")

    approve_investments.short_description = "Approve selected investments"
