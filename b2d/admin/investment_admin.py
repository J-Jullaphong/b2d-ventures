from django.contrib import admin
from django.utils.timezone import localtime

from ..models import Investment


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the Investment model, enabling the
    management and approval of investments made by investors in fundraising events.
    """
    readonly_fields = ['investor', 'investor_email', 'investor_phone_number',
                       'fundraise', '_amount', 'shares',
                       'transaction_slip', 'investment_datetime_with_timezone']
    list_display = (
        'investor', 'fundraise', '_amount', 'shares',
        'investment_status', 'investment_datetime_with_timezone'
    )
    actions = ['approve_investments']
    fieldsets = (
        ('Investor', {
            'fields': ('investor', 'investor_email', 'investor_phone_number')
        }),
        ('Investment Information', {
            'fields': ('fundraise', '_amount', 'shares',
                       'transaction_slip', 'investment_status',
                       'investment_datetime_with_timezone')
        }),
    )
    list_filter = ('investment_status', 'investment_datetime')
    date_hierarchy = 'investment_datetime'
    ordering = ('-investment_datetime',)

    def has_add_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'Investment Requests'
        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = f"Investment Request: {object_id}"
        extra_context['subtitle'] = None
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False,
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def approve_investments(self, request, queryset):
        """Custom action to approve selected investments."""
        approved_count = 0
        for investment in queryset:
            if investment.investment_status != 'approve':
                investment.investment_status = 'approve'
                investment.save()
                approved_count += 1

        self.message_user(request, f"{approved_count} investment(s) approved successfully.")

    approve_investments.short_description = "Approve selected investments"

    @admin.display(description='Email')
    def investor_email(self, obj):
        return obj.investor.email if obj.investor else None

    @admin.display(description='Phone Number')
    def investor_phone_number(self, obj):
        return obj.investor.phone_number if hasattr(obj.investor, 'phone_number') else None

    @admin.display(description='Amount')
    def _amount(self, obj):
        return f"${obj.amount}"

    @admin.display(description='Shares')
    def shares(self, obj):
        return obj.get_shares()

    @admin.display(description='Investment Date/Time')
    def investment_datetime_with_timezone(self, obj):
        if obj.investment_datetime:
            localized_time = localtime(obj.investment_datetime)
            return localized_time.strftime('%d/%m/%Y %H:%M:%S %Z')
        return None
