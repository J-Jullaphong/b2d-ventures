from django.contrib import admin

from ..models import Investor


@admin.register(Investor)
class InvestorRegistrationAdmin(admin.ModelAdmin):
    """
        Customizes the admin interface for the Investor model, enabling the
        management and approval of investor registrations.
    """
    list_display = ('first_name', 'last_name', 'email', 'financial_statements',
                    'is_active')
    actions = ['approve_registration']
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'phone_number',
                           'financial_statements', 'is_active')}),
    )

    def approve_registration(self, request, queryset):
        """Custom action to approve selected investor registrations."""
        for registration in queryset:
            if not registration.is_active:
                registration.is_active = True
                registration.save()

                self.message_user(request,
                                  f"{registration.email} approved successfully.")

    approve_registration.short_description = "Approve selected registrations"
