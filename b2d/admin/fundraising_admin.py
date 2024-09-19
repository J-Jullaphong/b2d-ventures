from django.contrib import admin

from ..models import FundRaising


@admin.register(FundRaising)
class FundraisingAdmin(admin.ModelAdmin):
    list_display = (
    'business', 'goal_amount', 'publish_date', 'fundraising_status')
    actions = ['approve_fundraising']
    fieldsets = (
        (None, {'fields': (
        'business', 'goal_amount', 'publish_date', 'deadline_date',
        'minimum_investment', 'shares_percentage', 'fundraising_status')}),
    )

    def approve_fundraising(self, request, queryset):
        for fundraising in queryset:
            if fundraising.fundraising_status != 'approve':
                fundraising.fundraising_status = 'approve'
                fundraising.save()

                self.message_user(request,
                                  f"Fundraising by {fundraising.business} approved successfully.")

    approve_fundraising.short_description = "Approve selected fundraising events"
