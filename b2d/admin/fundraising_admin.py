from django.contrib import admin

from ..models import FundRaising


@admin.register(FundRaising)
class FundraisingAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the FundRaising model, allowing for
    management and approval of fundraising events.
    """
    readonly_fields = [
        'business', '_goal_amount', 'publish_date', 'deadline_date',
        '_minimum_investment', 'shares', 'share_type', 'price_per_share'
    ]
    list_display = (
        'business', '_goal_amount', 'publish_date', 'deadline_date',
        'fundraising_status', 'share_type', 'shares'
    )
    actions = ['approve_fundraising']
    fieldsets = (
        ('Information', {
            'fields': (
                'business', '_goal_amount', 'publish_date', 'deadline_date',
                '_minimum_investment', 'shares', 'share_type',
                'price_per_share', 'fundraising_status'
            )
        }),
    )
    list_filter = (
    'fundraising_status', 'publish_date', 'deadline_date', 'share_type')

    def has_add_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'Fundraising Campaigns'
        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = f"Fundraising Campaign: {object_id}"
        extra_context['subtitle'] = None
        return super().change_view(request, object_id, form_url,
                                   extra_context=extra_context)

    def render_change_form(self, request, context, add=False, change=False,
                           form_url='', obj=None):
        context.update({
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change,
                                          form_url, obj)

    @admin.display(description='Goal Amount')
    def _goal_amount(self, obj):
        return f"${obj.goal_amount}"

    @admin.display(description='Minimum Investment')
    def _minimum_investment(self, obj):
        return f"${obj.minimum_investment}"

    @admin.display(description='Price Per Share')
    def price_per_share(self, obj):
        return f"${obj.get_price_per_share()}"

    def approve_fundraising(self, request, queryset):
        """Custom action to approve selected fundraising events."""
        for fundraising in queryset:
            if fundraising.fundraising_status != 'approve':
                fundraising.fundraising_status = 'approve'
                fundraising.save()
                self.message_user(
                    request,
                    f"Fundraising by {fundraising.business} approved successfully."
                )

    approve_fundraising.short_description = "Approve selected fundraising events"
